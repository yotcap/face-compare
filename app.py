import logging
import os
from pymongo import MongoClient
from flask import Flask, request
from flask_cors import CORS
import face_recognition
import time

import config as CONFIG
import constants as CONST
from utils import (read_file_from_base64,
                    api_result)

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m-%d-%Y %H:%M:%S %p"
logging.basicConfig(level=logging.DEBUG, filename=CONFIG.LOG_FILENAME,
                    datefmt=DATE_FORMAT, format=LOG_FORMAT)  # 从debug输出

# You can change this to any folder on your system
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'JPG'}

# mongodb连接
conn = MongoClient(CONFIG.db['host'], CONFIG.db['port'])
db = conn.admin
db.authenticate(CONFIG.db['user'], CONFIG.db['pwd'])
db = conn.detection_face_compare  # 连接detection_single_db数据库，没有则自动创建
log_compare = db.log_compare    # 人像比对日志

app = Flask(__name__, static_url_path='', static_folder='dist')
CORS(app, supports_credentials=True)


'''
    人像比对
'''
@app.route('/user/face/compare', methods=['post'])
def user_face_compare():
    req_data = request.json

    if ('imgData1' not in req_data.keys() or
        'imgData2' not in req_data.keys() or
        req_data['imgData1'] == 'null' or
        req_data['imgData2'] == 'null'):
        return api_result(CONST.code['error_params'], '参数错误')
    
    base64_img_face1 = req_data['imgData1']
    base64_img_face2 = req_data['imgData2']

    imgFile1 = read_file_from_base64(base64_img_face1)
    imgFile2 = read_file_from_base64(base64_img_face2)

    img1 = face_recognition.load_image_file(imgFile1)
    img2 = face_recognition.load_image_file(imgFile2)

    # 获取人脸编码
    code1 = face_recognition.face_encodings(img1)
    code2 = face_recognition.face_encodings(img2)

    # 未识别到人像
    if len(code1) == 0:
        return api_result(CONST.code['error_face1_encoding'], '未识别图像1中的人像')
    if len(code2) == 0:
        return api_result(CONST.code['error_face2_encoding'], '未识别图像2中的人像')

    # 人像过多
    if len(code1) > 1:
        return api_result(CONST.code['error_img1_face_too_many'], '图像1中的人像过多')
    if len(code2) > 1:
        return api_result(CONST.code['error_img2_face_too_many'], '图像2中的人像过多')

    match_results = face_recognition.compare_faces([code1[0]], code2[0], CONFIG.SIMILARITY_TOLERANCE)
    recognition_result = 1 if match_results[0] else 0

    # 人像比对的差值（不相似度）
    # 欧氏距离
    face_distances = face_recognition.face_distance([code1[0]], code2[0])
    face_distance = round(face_distances[0], 2)

    if (recognition_result == 1):
        _code = CONST.code['success']
        _msg = '比对成功'
    else:
        _code = CONST.code['error_compare']
        _msg = '比对失败，tolerance 为' + str(CONFIG.SIMILARITY_TOLERANCE)


    # 比对日志
    log_data = {
        'origin': req_data['origin'],
        # 'userid': req_data['userid'],
        'recognitionResult': recognition_result,
        'faceDistance': face_distance,
        'tolerance': CONFIG.SIMILARITY_TOLERANCE,
        'createTime': time.time()
    }
    log_compare.insert_one(log_data)
    
    return api_result(_code, _msg, {
        'recognition_result': recognition_result,
        'face_distance': face_distance
    })


@app.before_request
def process_request(*args, **kwargs):
    print(request.path)

    # if request.path in ['/user/faceAuth']:
    #     return None
    

if __name__ == "__main__":
    app.config['JSON_AS_ASCII'] = False
    app.config['JSONIFY_MIMETYPE'] = "application/json;charset=utf-8"
    app.run(host=CONFIG.app['host'], port=CONFIG.app['port'], debug=CONFIG.app['debug'])
