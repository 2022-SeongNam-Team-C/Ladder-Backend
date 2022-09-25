from flask import current_app, request, Blueprint, jsonify
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
from flask_restx import Resource, Namespace

Email = Namespace('api/v1')
bp = Blueprint("Emailsend", __name__, url_prefix="/api/v1")

@Email.route('/images/transmission')
@Email.doc(params={'Authorization': {'type': 'string', 'in': 'header'}})
class Emailsend(Resource):
    def post(self):
        mail = Mail(current_app)
        current_app.config['MAIL_SERVER']='smtp.gmail.com'
        current_app.config['MAIL_PORT']=465
        current_app.config['MAIL_USERNAME']='hee98.09.14@gmail.com'
        current_app.config['MAIL_PASSWORD']=''
        current_app.config['MAIL_USE_TLS']=False
        current_app.config['MAIL_USE_SSL']=True
        mail = Mail(current_app)

        file = request.files['file']
        file.save(secure_filename(file.filename))
        msg = Message('파일 전송 테스트', sender='hee98.09.14@gmail.com', recipients=['hee98.09.14@gmail.com'])
        msg.body = '메일이 잘 전송되었나요?'
        with current_app.open_resource(secure_filename(file.filename)) as fp:
            msg.attach(secure_filename(file.filename), 'image/png', fp.read())
        
        mail.send(msg)