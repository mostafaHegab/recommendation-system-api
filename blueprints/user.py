from flask import Blueprint , jsonify, request , make_response , redirect 
import models.users_model as um
import os
from werkzeug.utils import secure_filename

user = Blueprint('user', __name__)

print(os.path.dirname(os.path.abspath(__file__)))

@user.route('', methods=['GET','PUT'])
def user_info():
    id = request.json['id']
    firstname = request.json['firstname']
    lastname = request.json['lastname']

    if request.method == 'GET':
        info = um.user_info(id)
        return make_response(jsonify(info), 200) 
    elif request.method == 'PUT':
        # change user info
        change_info =um.change_user_info(id,firstname,lastname)
        return make_response(jsonify({'message': 'Info Changed'}), 200)


uploaded_Images ="C:\\Users\DESKTOP\Desktop\grad-proj-api/uploads"
allowed_image_extentions =["JPEG", "JPG", "PNG"]

@user.route('change_image/<int:id>',methods=['POST'])

def change_image(id):
    
        if request.files:
            image = request.files["image"]
            if image.filename == "":
                    print("No filename")

            if not "." in image.filename:
                 return False
                 ext = filename.rsplit(".", 1)[1]
                 if ext.upper() in allowed_image_extentions:
                     return True
                 else:
                     return False
            filename = secure_filename(image.filename)
            newfilename = str(id)+"."+ (filename.rsplit(".", 1)[1])
            image.save(os.path.join(uploaded_Images, newfilename))
            profileimage =um.change_profile_image(2,image)
            return make_response(jsonify({'message': 'Profile Picture Changed'}), 200) 

        else:
            print("That file extension is not allowed")


                   

        
@user.route('change_password',methods=['PUT'])
def change_user_password():
    id = request.json['id']
    newpassword = request.json['newpassword']
    oldpassword = request.json['oldpassword']
    user_pass = um.get_user_password(id)
    if user_pass != oldpassword:
        return make_response(jsonify({'message': 'Wrong Password'}), 406)
    
    elif user_pass == oldpassword:
        # change password
        user_password = um.change_password(id, newpassword)
        return make_response(jsonify({'message': 'Password Changed'}), 200)

    

    
      
