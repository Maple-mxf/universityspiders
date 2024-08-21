from jsonpath_ng import parse
import json


def _parse_api_resp(resp_text: str) -> tuple:
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


init_majorscore_req_fn = lambda university_id: {
    'page': 1,
    'size': 20,
    'school_id': university_id,
    'special_group': '',
    'uri': 'apidata/api/gk/score/special'
}

init_admissionsplan_req_fn = lambda university_id, province_id: {
    'local_province_id': province_id,
    'school_id': university_id,
    'size': 20,
    'page': 1,
    'special_group': '',
    'uri': 'apidata/api/gkv3/plan/school'
}

init_universityscore_req_fn = lambda university_id: {
    'page': 1,
    'school_id': university_id,
    'size': 20,
    'uri': 'apidata/api/gk/score/province'
}
