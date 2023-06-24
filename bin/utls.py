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