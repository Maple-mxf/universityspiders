from jsonpath_ng import parse
import json


def _parse_api_resp(resp_text) -> tuple:
    json_data = json.loads(resp_text)
    code = parse('$.code').find(json_data)[0].value
    message = parse('$.message').find(json_data)[0].value
    if code != '0000':
        return False, {'code': code, 'message': message}
    data = parse('$.data').find(json_data)[0].value
    return True, data


def _mapped_to_textlist(nodelist, css_elist):
    if nodelist is None: return []
    ret = []
    for node in nodelist:
        texts = [node.css(css).extract_first() for css in css_elist]
        ret.append(' '.join([text for text in texts if text is not None]))
    return ret
