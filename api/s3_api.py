from flask import request, Blueprint
from werkzeug.utils import secure_filename

from entity import database
from entity.model import Image

from crypt import methods
from datetime import datetime as dt

from s3bucket.s3_connect import s3
from s3bucket.s3_upload import s3_put_result_image, s3_put_origin_image
from flask_restx import Resource, Namespace

bp = Blueprint('s3', __name__, url_prefix='/api/v1')

s3 = Namespace('api/v1')

# s3버킷에 이미지 업로드하며, DB에 image_url과 현재 로그인된 사용자 id저장
# (미완) 현재 로그인된 사용자 정보 

@s3.route('/s3/result/upload-image-url')
@s3.doc(params={'image_name': {'description': '', 'type': 'string', 'in': 'header'}})
class upload_result_image(Resource):
    def post(self):
        # html에서 가져온 이미지 
        file = request.files['file']

        # 파일 이름 지정
        filename = file.filename.split('.')[0]
        image_type = file.filename.split('.')[-1]
        image_created = dt.now().strftime('%Y-%m-%d-%H-%M-%S')
        image_name = f"{image_created}--{filename}.{image_type}"

        # s3버킷에 업로드
        s3_put_result_image(s3, 'ladder-s3-bucket', file, image_name)

        # 현재 로그인 사용자 정보 (토큰 연결시 수정 예정)
        user_id = 1
        #writer = get_user()

        # postgres image table에 업로드
        result_url = "https://ladder-s3-bucket.s3.ap-northeast-2.amazonaws.com/result/"+image_name
        result_url = result_url.replace(" ","/")
        database.add_instance(Image, user_id = user_id, result_url = result_url, is_deleted = False)

        return "성공적으로 사진이 S3에 저장되었습니다."


# origin 이미지 S3업로드
@s3.route('/s3/origin/upload-image-url')
@s3.doc(params={'image_name': {'description': '', 'type': 'string', 'in': 'header'}})

class upload_origin_image(Resource):
    def post(self):
        file = request.files['file']

        filename = file.filename.split('.')[0]
        image_type = file.filename.split('.')[-1]
        image_created = dt.now().strftime('%Y-%m-%d-%H-%M-%S')
        image_name = f"{image_created}--{filename}.{image_type}"

        s3_put_origin_image(s3, 'ladder-s3-bucket', file, image_name)

        # 현재 로그인 사용자 정보 (토큰 연결시 수정 예정)
        user_id = 1
        #writer = get_user()

        origin_url = "https://ladder-s3-bucket.s3.ap-northeast-2.amazonaws.com/origin/"+image_name
        origin_url = origin_url.replace(" ","/")
        database.add_instance(Image, user_id = user_id, origin_url = origin_url, is_deleted = False)

        return "성공적으로 사진이 S3에 저장되었습니다."

# (result)변환 이미지 URL불러오기
@s3.route('/s3/result/get-image-url/')
@s3.doc(params={'image_name': {'description': '', 'type': 'string', 'in': 'header'}})
class get_result_image(Resource):
    def post(self):
        image_name = image_name
        result_image_url = f"https://ladder-s3-bucket.s3.ap-northeast-2.amazonaws.com/result/{image_name}"
        return result_image_url, 200

# (origin)원본 이미지 URL불러오기
@s3.route('/s3/origin/get-image-url/')
@s3.doc(params={'image_name': {'description': '', 'type': 'string', 'in': 'header'}})
class get_origin_image(Resource):
    def post(self):
        image_name = image_name
        origin_image_url = f"https://ladder-s3-bucket.s3.ap-northeast-2.amazonaws.com/origin/{image_name}"

        return origin_image_url, 200