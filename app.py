# app.py

from flask import Flask, render_template, url_for
from datetime import datetime
from flask_login import UserMixin
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_cors import CORS
from supabase import create_client, Client
import supabase

url: str = 'https://kaqvgzyugazqgjztgdac.supabase.co'
key: str = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImthcXZnenl1Z2F6cWdqenRnZGFjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDI1NzMxMjgsImV4cCI6MjAxODE0OTEyOH0.ArTPJlFmrARrMPMajee4oYXx7Evng1OGXVP3gKiS4rE'
supabase: Client = create_client(url, key)

app = Flask(__name__)
CORS(app)
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'specsysix'
db.init_app(app)
app.app_context().push()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    # username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    mobile = db.Column(db.String(15), nullable=False)  # Change to String for compatibility
    aadhaar = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    disable = db.Column(db.String(5), nullable=False)
    dob = db.Column(db.String(20), nullable=False)
    education = db.Column(db.String(20), nullable=False)
    pj_location = db.Column(db.String(20), nullable=False)
    skills = db.Column(db.String(255), nullable=True)  # Assuming skills can be stored as a comma-separated string
    state = db.Column(db.String(20), nullable=False)


@app.route('/get_user', methods=['GET'])
def return_user():
    try:
        users = User.query.all()
        # user_list = [{'id': user.id, 'name': user.name, 'email': user.email, 'mobile': user.mobile, } for user in users]
        
        user_list = [
    {
        'id': user.id,
        'name': user.name,
        'password': user.password,
        'email': user.email,
        'mobile': user.mobile,
        'aadhaar': user.aadhaar,
        'address': user.address,
        'disable': user.disable,
        'dob': user.dob,
        'education': user.education,
        'pj_location': user.pj_location,
        'skills': user.skills.split(',') if user.skills else [],
        'state': user.state
    }
    for user in users
]

        return jsonify({'users': user_list, 'message': 'success'})
    except Exception as e:
        return jsonify({'error': 'Internal Server Error'}), 500


@app.route('/add_user', methods=['POST'])
def add_user():
    if request.method == 'POST':
        data = request.get_json()

        # Validate required fields

        required_fields = ['fullName', 'password', 'email', 'mobile', 'aadhaar', 'address', 'disable', 'dob', 'education', 'pj_location', 'state', 'skills'] 
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        # Ensure mobile is a number
        try:
            mobile_number = int(data['mobile'])
        except ValueError:
            return jsonify({'error': 'Mobile must be a valid number'}), 400

        new_user = User(
           name=data['fullName'],
            # username=data['username'],
            password=data['password'],
            email=data['email'],
            mobile=str(mobile_number),
            aadhaar=data['aadhaar'],
            address=data['address'],
            disable=data['disable'],
            dob=data['dob'],
            education=data['education'],
            pj_location=data['pj_location'],
            skills=','.join(data['skills']) if 'skills' in data else None,
            state=data['state']  
        )

        try:
            db.session.add(new_user)
            db.session.commit()
            count = supabase.table('specsy6').insert({ "name": new_user.name , "password": new_user.password , "email" : new_user.email , "mobile" : new_user.mobile , "aadhaar" : new_user.aadhaar , "address" : new_user.address , "disable" : new_user.disable , "dob" : new_user.dob , "education" : new_user.education , "pj_location" : new_user.pj_location , "skills" : new_user.skills , "state" : new_user.state}).execute()
            return jsonify({'message': 'User added successfully'}), 201
        except IntegrityError as e:
            db.session.rollback()
            return jsonify({'error': 'Username or email already exists'}), 409
        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify({'error': 'Internal Server Error'}), 500






@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()

        # Validate required fields
        required_fields = ['email', 'password']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        email = data['email']
        password = data['password']
        

        # Check if the user exists and the password is correct
        user = User.query.filter_by(email=email, password=password).first()
        id = user.id

        if user:
            return jsonify({'message': 'Login successful', 'id': id}), 200
        else:
            return jsonify({'error': 'Invalid email or password'}), 401




@app.route('/api/resource/<custom_id>', methods=['GET'])
def get_resource(custom_id):
    # Perform logic to retrieve resource based on the custom ID
    # For example, you can query a database
    user = User.query.get(custom_id)
    resource_data = {'id': custom_id, 'email': user.email, 'mobile': user.mobile, 'name': user.name, 'password': user.password, 'aadhaar': user.aadhaar, 'address': user.address, 'disable': user.disable, 'dob': user.dob, 'education': user.education, 'pj_location': user.pj_location, 'skills': user.skills, 'state': user.state}
    
    # Return the resource data as JSON
    return jsonify(resource_data)





if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

















# from flask import Flask, render_template, url_for


# from flask_sqlalchemy import SQLAlchemy
# from flask_login import UserMixin
# from flask import Flask, request, jsonify
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.exc import IntegrityError

# app = Flask(__name__)
# db = SQLAlchemy()
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# app.config['SECRET_KEY'] = 'specsysix'
# db.init_app(app)
# app.app_context().push()


# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(20), nullable=False)
#     username = db.Column(db.String(20), nullable=False, unique=True)
#     emailid = db.Column(db.String(20), nullable=False)
#     password = db.Column(db.String(80), nullable=False)
#     mobileno = db.Column(db.String(20), nullable=False)
#     # dob = db.Column(db.String(20), nullable=False)
#     # gender = db.Column(db.String(20), nullable=False)
#     # caddress = db.Column(db.String(100), nullable=False)
#     # paddress = db.Column(db.String(100), nullable=False)
#     # disable = db.Column(db.String(20), nullable=True)
#     # aadhaar_no = db.Column(db.String(20), nullable=False)


# @app.route('/register', methods=['POST'])
# def getvalue():
#     data = request.get_json()

#     # Validate required fields
#     required_fields = ['name', 'username', 'password', 'emailid', 'mobileno']
#     for field in required_fields:
#         if field not in data:
#             return jsonify({'error': f'Missing required field: {field}'}), 400


#     try:
#         mobile_number = int(data['mobileno'])
#     except ValueError:
#         return jsonify({'error': 'Mobile must be a valid number'}), 400

#     new_user = User(
#         name=data['name'],
#         username=data['username'],
#         password=data['password'],
#         emailid=data['emailid'],
#         mobileno=str(mobile_number)  # Store as string in the database
#     )

#     try:
#         db.session.add(new_user)
#         db.session.commit()
#         return jsonify({'message': 'User added successfully'}), 201
#     except IntegrityError as e:
#         db.session.rollback()
#         return jsonify({'error': 'Username or email already exists'}), 409
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'error': 'Internal Server Error'}), 500


# if __name__ == '__main__':
#     app.run(debug=True)
