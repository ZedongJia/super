
from bin.utls import o_tag, c_tag


class Node:
    r'''
    @intro: this is the basic class of dom element
    '''
    
    '''
    static props
    '''
    COUNT = 0
    
    SELF_CLOSE_TAG = ['input', 'link', 'source', 'meta', '!DOCTYPE']
    
    def __init__(self, tag: str = 'enpty', attr: dict[str, str] = {}, children: list = []) -> None:
        # dom props
        self._tag = tag
        self._attr = attr

        # node props
        self._children = children
        self._id = Node.COUNT
        
        # update static id
        Node.COUNT += 1
    
    def appendChild(self, node):
        r'''
        @param node --child that need appending to this node
        '''
        self._children.append(node)
    
    def appendChildren(self, nodeList: list):
        r'''
        @param nodeList --children that need appending to this node
        '''
        for n in nodeList:
            self._children.append(n)
            
    def removeChild(self, node):
        r'''
        @param node --child that need removing from this node
        '''
        self._children.remove(node)
    
    def setAttribute(self, attr: str, value: str):
        r'''
        @param attr --dom attribute
        @param value --value of attribute
        '''
        self._attr[attr] = value
    
    def _toHTML(self, file) -> str:
        r'''
        @param file --root file of this dom
        '''
        FILES = file.FILES
        # import, need replace and report slots
        if self._tag in FILES.keys():
            slots = self._checkSlots()
            subFile = FILES[self._tag]
            subFile._belongTo(file)
            return subFile.toHTML(slots)
        
        open_tag = o_tag(self._tag, self._attr)
        
        if self._tag in Node.SELF_CLOSE_TAG:
            return open_tag + '\n'
        
        content = ''
        for _c in self._children:
            if type(_c) == str:
                content += _c
            else:
                content += _c._toHTML(file)
        
        return open_tag + '\n' + content + c_tag(self._tag) + '\n'
    
    def _checkSlots(self) -> dict:
        slots = {}
        for _c in self._children:
            if type(_c) == str:
                continue
            slot = _c._attr.get('slot', None)
            if slot != None:
                slots[slot] = _c
        
        return slots