
from bin.utls import o_tag, c_tag
from bin.vdom import Node


class Complier:
    
    SELF_CLOSE_TAG = ['input', 'link', 'source', 'meta', '!DOCTYPE']
    
    IGNORE_SINGLE_CONTENT = ['\n', '\t', ' ', '']
    
    ANNOTATION = {'START': '<!--', 'END': '-->'}
    
    @staticmethod
    def _preprocess(file: str) -> str:
        start_pos = file.find(Complier.ANNOTATION['START'], 0)
        while start_pos != -1:
            end_pos = file.find(Complier.ANNOTATION['END'], start_pos)
            file = file.replace(file[start_pos : end_pos + len(Complier.ANNOTATION['END'])], '')
            start_pos = file.find(Complier.ANNOTATION['START'], 0)
        return file
    
    @staticmethod
    def complier(file: str) -> tuple[dict, dict, list[Node]]:
        r'''
        complier html file to super dependency and Node List
        @param file --html file(str)
        @return (script, dependency, components)
        '''
        file = Complier._preprocess(file)

        script, file = Complier._extractScript(file)
        dependency = Complier._extractDependency(file)

        p = 0
        components = []
        while p < len(file):
            p, _c = Complier._extractElement(file, p)
            Complier._appendContent(components, _c)
        return script, dependency, components

    @staticmethod
    def _extractScript(file: str) -> dict[str,list]:
        r'''
        @type 'onload', 'default'
        '''
        script = {'onload': [], 'default': []}
        # check script
        tag_len = 9
        s_tag = file.find('<script', 0)
        if s_tag != -1:
            s_content, _, attr = Complier._extractLabel(file, s_tag, '<', '>')
        while s_tag < len(file) and s_tag != -1:
            e_content = file.find(c_tag('script'), s_content)
            # get
            content = file[s_content:e_content]
            # remove
            file = file.replace(file[s_tag:e_content + tag_len], '')
            
            if attr.get('onload', None) != None:
                script['onload'].append(content)
            else:
                script['default'].append(content)
            
            # repeat
            s_tag = file.find('<script', s_tag)
            if s_tag != -1:
                s_content, _, attr = Complier._extractLabel(file, s_tag, '<', '>')
        
        return script, file
    
    
    @staticmethod
    def _extractDependency(file: str) -> dict[str,dict]:
        
        dependency = {}
        start = 0
        while Complier._hasLabel(file, start, '{%', '%}'):
            start, tag, attr = Complier._extractLabel(file, start, '{%', '%}', False)
            dependency[tag] = attr
        
        return dependency
    
    
    @staticmethod
    def _extractElement(file: str, start_pos: int) -> tuple[int, Node]:
        r'''
        Extract sub label from start_pos in file
        '''
        if start_pos >= len(file):
            return start_pos
        
        _tag = ''
        _attr = {}
        _content = []

        '''
        skip no use
        '''
        start = Complier._skip(file, start_pos, [' ', '\n', '\t'])
        '''
        get tag and attr
        '''
        if (Complier._hasLabel(file, start, '<', '>')):
            end, _tag, _attr = Complier._extractLabel(file, start, '<', '>')
        else:
            return (len(file), '')
        
        '''
        if in self-close-tag, return
        '''
        if _tag in Complier.SELF_CLOSE_TAG:
            node = Node(_tag, _attr, _content)
            return (end, node)
        
        '''
        get content
        '''
        start = end
        
        while start < len(file):
            while file[start] != '<':
                start += 1
            # append content
            if end != start:
                content = file[end : start].replace('\t', '')
                Complier._appendContent(_content, content)
            
            
            if file[start + 1] == '/':
                # skip to end
                end = start + 1
                while file[end] != '>':
                    end += 1
                end += 1
                break
            start, content = Complier._extractElement(file, start)
            Complier._appendContent(_content, content)
            end = start + 1
        
        node = Node(_tag, _attr, _content)
        
        return (end, node)
    
    @staticmethod
    def _hasLabel(file: str, start_pos: int, start_delimiter: str, end_delimiter: str) -> bool:
        return not (file.find(start_delimiter, start_pos) == -1 or file.find(end_delimiter, start_pos) == -1)
    
    @staticmethod
    def _extractLabel(file: str, start_pos: int, start_delimiter: str, end_delimiter: str, keep_space: bool = True) -> tuple[int ,str, dict[str,str]]:
        r'''
        Extract the label and attributes from struct like
        @input: START_DELIMITER tag name='hello' class='test' END_DELIMITER
        @output: (tag, { name: 'hello', class: 'test'})
        @return: end(int), tag(str), attr(dict)
        '''
        
        ##############
        # prop
        tag = ''
        attr = {}
        end = -1
        ##############
        
        d_len = len(start_delimiter)
        start = file.find(start_delimiter, start_pos) + d_len
        
        # skip space
        while file[start] == ' ':
            start += 1
        
        end = start
        
        # extract tag
        while file[end] != ' ' and not Complier._isDelimiter(file, end, end_delimiter):
            end += 1
        tag = file[start : end]
        # move
        start = end

        # extract attributes
        attr_str = ''
        quote = [False, False] # single, double

        while not Complier._isDelimiter(file, end, end_delimiter):
            end += 1
            
            # check if need to extract
            if (file[end] == ' ' or Complier._isDelimiter(file, end, end_delimiter)) and not Complier._inQuoteCondition(quote):
                # lazy check '=', like class ="dd" -to-> class="dd"
                while file[end] == ' ':
                    end += 1
                if file[end] != '=':
                    if attr_str != '':
                        index = attr_str.find('=')
                        index = index if index != -1 else len(attr_str)
                        key = attr_str[0 : index].replace(' ', '')
                        if index != len(attr_str):
                            value = attr_str[index + 1 : len(attr_str)][1:-1]
                            if not keep_space:
                                value = value.replace(' ', '')
                            attr[key] = value
                        else:
                            attr[key] = key
                    attr_str = ''
                else:
                    # deal condition like '= "dd"' -to-> '="dd"'
                    attr_str += file[end]
                    end += 1
                    while file[end] == ' ':
                        end += 1
            attr_str += file[end]
            
            # check if in quote
            if file[end] == '\'':
                quote[0] = not quote[0]
            if file[end] == '\"':
                quote[1] = not quote[1]
        
        end += d_len

        return end, tag, attr
    
    
    @staticmethod
    def _inQuoteCondition(quote: list[bool]) -> bool:
        r'''
        quote[0] denotes single quote
        
        quote[1] denotes double quote
        ''' 

        return quote[0] or quote[1]
    @staticmethod
    def _isDelimiter(file: str, start_pos: int, delimiter: str) -> bool:
        r'''
        Check --if substr of start_pos, start_pos + len(delimiter) in file is delimiter
        '''
        
        d_len = len(delimiter)
        return file[start_pos : start_pos + d_len] == delimiter
    
    @staticmethod
    def _appendContent(_content: list, content: str):
        r'''
        Check --if the content is legal, append it
        
        else ignore it
        '''
        if content in Complier.IGNORE_SINGLE_CONTENT:
            return
        else:
            _content.append(content)
            
    @staticmethod
    def _skip(file: str, start_pos: int, characters: list) -> int:
        end = start_pos
        while end < len(file) and file[end] in characters:
            end += 1
        return end