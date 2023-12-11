from flask import Flask,request,jsonify
from flask_cors import CORS
import pytesseract
from PIL import Image
import re
import numpy as np
import cv2
import matplotlib.pyplot as plt


app = Flask(__name__)
CORS(app)

class Vali:
    @staticmethod
    def val_addhar(image_path,user):
        key = False
        image_file = image_path
        img = Image.open(image_path)
        ocr_result = pytesseract.image_to_string(img,lang='mar+eng')
        list = ocr_result.split('\n')
        user_name = re.compile(re.escape(user),re.IGNORECASE)
        reg_ex = r".*\b(\d{4}\s?\d{4}\s?\d{4})\b.*"
        vid_reg_ex = r'VID\s*:\s*(\d{4}\s?\d{4}\s?\d{4}\s?\d{4})'
        name_flag = 0
        ad_no_flag = 0
        vid_no_flag = 0
        gender_flag = 0
        for i in list:
            if user_name.search(i.lower()):
                name_flag = 1
            if re.search(reg_ex,i):
                ad_no_flag = 1
            if 'male' in i.lower() or 'पुरुष' in i or 'स्त्री' in i or 'female' in i.lower():
                gender_flag = 1
            if re.search(vid_reg_ex,i):
                vid_no_flag = 1
        if name_flag and ad_no_flag and gender_flag == 1:
            if vid_no_flag == 1:
                key = True
            key = True
        return key

def save_uploaded_file(file):
    file_path = f"uploads/{file.filename}"
    file.save(file_path)
    return file_path

@app.route("/validate", methods=['POST'])
def validate():
    try:
        image = request.files.get('image_path')
        user = request.form.get('user')
        key = Vali.val_addhar(image, user)
        return {'key': key}
    except Exception as e:
        error_msg = str(e)
        return {'error': error_msg}, 500

if __name__ == '__main__':
    app.run(debug=True)























