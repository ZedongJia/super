import os

from bin.complier import Complier
from bin.urls import Url
from bin.utls import replaceSlot, o_tag, c_tag
from bin.vdom import Node
import settings

class Path:
    def __init__(self, url: str):
        r'''
        @param url --the path url of the file
        '''
        self._path = url
        self._modificationTime = self._getModificationTime()
        
    def getPath(self) -> str:
        return self._path
    
    def _getModificationTime(self) -> float:
        return os.stat(self._path).st_mtime
    
    def isModified(self) -> bool:
        new_time = os.stat(self._path).st_mtime
        if self._modificationTime != new_time:
            self._modificationTime = new_time
            return True
        return False
            

class File:
    def __init__(self, path: Path, FILES: list):
        r'''
        @param path --path Object
        @param encoding --charset uesd to encode
        '''

        self._path = path
        self.FILES = FILES
        
        # concrate dependency
        self._register: dict[str,str] = {}
        self._import: dict[str,str] = {}
        
        # basic
        self._script = {}
        self._dependency = {}
        self._components = []
        self.subFiles = []
        
        self._construct()
    
    def _construct(self):
        self._load()
        self._decodeDependency()
    
    def _load(self):
        with open(self._path.getPath(), 'r', encoding=settings.ENCODING) as reader:
            file_content = reader.read()
        self._script, self._dependency, self._components = Complier.complier(file_content)

    def _decodeDependency(self):
        r'''
        decode dependency,
        
        Necessary:  name
        '''
        self._register = self._dependency.get('register', {})
        self._import = self._dependency.get('import', {})
        
    def getComponentName(self) -> str:
        return self._register['name']
    
    def toHTML(self, slots: dict = None, isPage: bool = False, paramsSlots: dict[str, str] = {}) -> str:

        html = ''

        for _c in self._components:
            html += _c._toHTML(self)
        
        # replace slots
        if slots != None:
            html = replaceSlot(slots,'{{', '}}', html)
        
        # add script
        if isPage:
            index = html.rfind('</html>') - 6
            e_tag = ''
            if index != -1:
                html.removesuffix('</html>')
                ending = '</html>'
            html += self._toScript(paramsSlots) + e_tag
        return html
    


    def _toScript(self, paramsSlots: dict[str, str] = {}) -> str:
        script = self._reconstructScript()
        # check onload
        if script['onload'] != '':
            script['onload'] = 'window.onload = () => {\n' + script['onload'] + '}\n'
        
        # replace slots condition
        for _k, _v in paramsSlots.items():
            script['import'] = script['import'].replace(_k, _k + '=' + _v)
        
        # concat
        temp = ''
        for _v in script.values():
            temp += _v
        
        script = temp
        
        if script != '':
            # transform to script
            script = o_tag('script') + '\n' + script + c_tag('script') + '\n'
        
        return script
    
    def _reconstructScript(self) -> dict[str, str]:
        # preparing
        script = {
            'onload': '',
            'import': '',
            'default': ''
        }
        # badly O(n^2)
        for _k in script.keys():
            _l = self._script[_k]
            for _s in _l:
                if _s != '':
                    script[_k] += _s
        
        for name in self.subFiles:
            sub_script = self.FILES[name]._reconstructScript()
            for _k in script.keys():
                script[_k] += sub_script[_k]

        return script
        
    def _belongTo(self, file):
        file.subFiles.append(self.getComponentName())
    
class FileHash:
    r'''
    use HashMap to store files
    
    '''

    def __init__(self, pathList: list[Path]):
        self.FILES: dict[str, File] = {}
        self.pathList = pathList
        self._buildHash()
    
    def _buildHash(self):
        for path in self.pathList:
            file = File(path, self.FILES)
            self.FILES[file.getComponentName()] = file

class Stream:
    
    # scan group
    @staticmethod
    def scanFiles() -> dict[str,list[Path]]:
        r'''
        @return a dict about {
            '.html': [],
            '.png': [],
            '.jpg': [],
            '.webp': [],
            ...
        }
        '''
        pathList = {k:[] for k in settings.FILE_TYPES}
        for base in settings.SCAN_DIRS:
            Stream._scan(base, pathList)

        return pathList
    
    @staticmethod
    def _scan(root: str, pathList: dict):
        for (dirpath, dirnames, filenames) in os.walk(root):
            for name in filenames:
                suffix = name[name.find('.'):len(name)]
                if suffix not in settings.FILE_TYPES:
                    continue
                path = dirpath.replace('\\', '/') + '/' + name
                pathList[suffix].append(Path(path))
    
    @staticmethod
    def loadFiles(FILES: dict, randomSlots: dict[str, str] = {}, paramsSlots: dict[str, str] = {}):
        r'''
        load files to urls
        '''
        for url in settings.ROUTER:
            Stream._loadHTML(FILES, url, randomSlots, paramsSlots)
    
    # write group
    @staticmethod
    def writeFiles():
        for url in settings.ROUTER:
            Stream._writeHTML(url)
    
    @staticmethod
    def _loadHTML(FILES: dict[str,File], url: Url, randomSlots: dict[str, str] = {}, paramsSlots: dict[str, str] = {}):
        html = FILES[url.name].toHTML(isPage=True, paramsSlots=paramsSlots)
        # static slots
        html = replaceSlot(settings.STATIC_REGISTER, '{{', '}}', html, url.getPathPrefix() + settings.STATIC_RESOURCE_DIR)
        # random slots
        html = replaceSlot(randomSlots, '{{', '}}', html)
        
        url.setHTML(html)
        
        for _u in url.include:
            Stream._loadHTML(FILES, _u)   
    
    @staticmethod
    def _writeHTML(url: Url):
        dir_path = settings.BASE_DIR + url.dir_path
        path = settings.BASE_DIR + url.getPath()
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        with open(path, 'w', encoding=settings.ENCODING) as writer:
            writer.write(url.html)
        
        for _u in url.include:
            Stream._writeHTML(_u)