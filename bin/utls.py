def decodeParams(params: str) -> list[str]:
    r'''
    decode like "['param1', 'param2']"
    '''
    if params == '':
        return []
    params.removeprefix('[').removesuffix(']').split(',')
    params = [param.removeprefix('\'').removeprefix('\"').removesuffix('\'').removesuffix('\"') for param in params]
    return params

def o_tag(tag: str, attr: dict = {}) -> str:
    _attr = ''
    for _k, _v in attr.items():
        _attr += ' ' + _k + '=' + "\"" + _v + "\""
    return '<' + tag + _attr + '>'
    
def c_tag(tag: str) -> str:
    return '</' + tag + '>'


def findSlot(file: str, start_pos: int, start_delimiter: str, end_delimiter: str) -> tuple[int, str, int]:
    r'''
    @return (start, inner_content, end),
    
    if not find, return (-1, '', -1)
    '''
    not_find = (-1, '', -1)
    
    s_d_len = len(start_delimiter)
    e_d_len = len(end_delimiter)
    
    start = file.find(start_delimiter, start_pos)
    if start == -1:
        return not_find
    end = file.find(end_delimiter, start)
    if end == -1:
        return not_find
    content = file[start + s_d_len:end].replace(' ', '')
    
    end = end + e_d_len

    return start, content, end

def replaceSlot(slots: dict[str, str], start_delimiter: str, end_delimiter: str, html: str, prefix: str = '', suffix: str = '') -> str:

    start, name, end = findSlot(html, 0, start_delimiter, end_delimiter)
    while start != -1:
        slot = slots.get(name, None)
        if slot != None:
            html = html.replace(html[start:end], prefix + slot + suffix)
        start, name, end = findSlot(html, start + 1, start_delimiter, end_delimiter)
    return html