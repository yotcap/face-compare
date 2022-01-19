import json
import re
import base64
from flask import Response
from functools import wraps
from io import BytesIO

import constants as CONST


'''
    将base64字符串转换为文件流
'''
def read_file_from_base64(base64img):
    base64_data = re.sub('^data:image/.+;base64,', '', base64img)
    byte_data = base64.b64decode(base64_data)
    image_data = BytesIO(byte_data)
    return image_data


# '''
#     检查用户人脸注册、验证请求参数
#     True - 校验通过
#     False - 校验失败
# '''
# def check_user_face_params_from_req(req_data):
#     if ('userid' not in req_data.keys() or
#         'imgData' not in req_data.keys() or
#         req_data['userid'] == 'null' or
#         req_data['imgData'] == 'null'):
#         return False
        
#     else:
#         return True


# '''
#     获取用户唯一 id
# '''
# def getUserUnique(userid):
#     return userid


'''
    response
'''
def api_result(code, msg, params={}):
    if (code == CONST.code['success']) and (msg == ''):
        msg = '操作成功'
    if (code == CONST.code['fail']) and (msg == ''):
        msg = '操作失败'

    _res = {
        'code': code,
        'msg': msg
    }
    _res = dict(_res, **params)

    return jsonres(_res)


'''
    Response Header
'''
def returns_json_utf8(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        r = f(*args, **kwargs)
        return Response(r, content_type='application/json; charset="utf-8')
    return decorated_function

'''
    response unicode to utf8
'''
def jsonres(params):
    return json.dumps(params, ensure_ascii=False).encode('utf8')
