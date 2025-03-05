from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart
app = Flask(__name__)
api = Api(app)


class mail(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        if ("to" in json_data and "subject" in json_data
           and "body" in json_data):
            subject = json_data['subject']
            body = json_data['body']
            print("Preparing to send mail")
            smtp_address = json_data['smtp_ip']
            smtp_port = json_data['smpt_port']
            sender_name = json_data['from_name']
            FROM_address = json_data['from_email']
            receiver = json_data['to'][0]
            receiver = receiver.split(',')
            print(receiver)
            body = body + "<center><br><br><b>*** This is an \
            automatically generated email. ***</b></center>"
            print(body)
            msg = MIMEMultipart()
            msg.attach(MIMEText(body, 'html'))
            msg['To'] = ", ".join(receiver)
            msg['From'] = formataddr((sender_name, FROM_address))
            msg['Subject'] = subject
            # Send the mail
            server = smtplib.SMTP(smtp_address, smtp_port)
            server.sendmail(FROM_address, receiver, msg.as_string())
            server.quit()
            print("Email Sent")
            return jsonify({'Success Message': "Mail Sent successfully"})
        else:
            Error_Message="Missing parameters.. Please check whether values for all 3 parameters are provide 'to','subject','body'"
            return jsonify({'Error Message': Error_Message})


api.add_resource(mail, '/')
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5051, debug=True)
