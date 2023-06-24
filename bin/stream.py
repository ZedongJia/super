import os

from bin.complier import Complier
from bin.urls import Url
from bin.utls import o_tag, c_tag
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
    
    def toHTML(self, slots: dict = None, isPage: bool = False) -> str:

        html = ''

        for _c in self._components:
            html += _c._toHTML(self)
        
        # replace slots
        if slots != None:
            html = self._replaceSlot(slots, html)
        
        # add script
        if isPage:
            index = html.rfind('</html>') - 6
            e_tag = ''
            if index != -1:
                html.removesuffix('</html>')
                ending = '</html>'
            html += self._toScript() + e_tag
        return html
    
    def _replaceSlot(self, slots: dict[str, Node], html: str) -> str:
        offset = 2
        start = html.find('{{')
        while start < len(html) and start != -1:
            end = html.find('}}', start + offset)
            name = html[start + offset:end].replace(' ', '')
            slot = slots.get(name, None)
            if slot != None:
                html = html.replace(html[start:end + 2], slot._toHTML(self))
            start = html.find('{{', start + offset)
        
        return html

    def _toScript(self) -> str:
        onload, default = self._reconstructScript()
        script = 'window.onload = () => {\n' + onload + '}\n' + default
        return o_tag('script') + '\n' + script + c_tag('script') + '\n'
    
    def _reconstructScript(self) -> dict:
        # preparing
        onload = ''
        default = ''
        onload_list = self._script['onload']
        default_list = self._script['default']
        for _s in onload_list:
            if _s != '':
                onload += _s
        for _s in default_list:
            if _s != '':
                default += _s
        
        for name in self.subFiles:
            sub_onload, sub_default = self.FILES[name]._reconstructScript()
            onload += sub_onload
            default += sub_default

        return onload, default
        
    def _belongTo(self, file):
        file.subFiles.append(self.getComponentName())
    
class FileTree:
    r'''
    use HashMap to store files
    
    '''

    def __init__(self, pathList: list[Path]):
        self.FILES: dict[str, File] = {}
        self.pathList = pathList
        self._buildTree()
    
    def _buildTree(self):
        for path in self.pathList:
            file = File(path, self.FILES)
            self.FILES[file.getComponentName()] = file


class Stream:
    
    FILE_TYPES = ['.html']
    
    # scan group
    @staticmethod
    def scanFiles() -> list[Path]:
        pathList = []
        for base in settings.SCAN_DIRS:
            Stream._scan(base, pathList)

        return pathList
    
    @staticmethod
    def _scan(root: str, pathList: list):
        for (dirpath, dirnames, filenames) in os.walk(root):
            for name in filenames:
                if name[name.find('.'):len(name)] not in Stream.FILE_TYPES:
                    continue
                path = dirpath.replace('\\', '/') + '/' + name
                pathList.append(Path(path))
    
    # write group
    @staticmethod
    def writeFiles(FILES: dict):
        for url in settings.ROUTER:
            Stream._writeHTML(FILES, url)
    
    @staticmethod
    def _writeHTML(FILES: dict[str,File], url: Url):
        dir_path = settings.BASE_DIR + url.dir_path
        path = settings.BASE_DIR + url.getPath()
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        with open(path, 'w', encoding=settings.ENCODING) as writer:
            writer.write(FILES[url.name].toHTML(isPage=True))
        
        for _u in url.include:
            Stream._writeHTML(FILES, _u)