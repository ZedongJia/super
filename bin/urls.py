
class Url:
    def __init__(self, name: str, include: list = []) -> None:
        self.name = name
        self.include = include
        self.dir_path = ''
        self.depth = 1
        
        self.html = ''
        
        for url in include:
            url._setDirPath(self.dir_path + self.name + '/')
    
    def getPath(self) -> str:
        r'''
        @return path(like 'xxx/xxx/xxx/file.html')
        '''
        return self.dir_path + self.name + '.html'
    
    def _setDirPath(self, path):
        self.depth += 1
        self.dir_path = path
    
    def setHTML(self, html: str):
        r'''
        load html and replace static resource
        '''
        self.html = html

    def getPathPrefix(self):
        return '../'*self.depth