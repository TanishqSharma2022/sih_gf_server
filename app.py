# app.py

from flask import Flask, render_template, url_for
from datetime import datetime, date
from flask_login import UserMixin
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_cors import CORS
from supabase import create_client, Client
import supabase
from sqlalchemy.sql import text
import seaborn as sns
from collections import defaultdict, Counter

url: str = 'https://kaqvgzyugazqgjztgdac.supabase.co'
key: str = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImthcXZnenl1Z2F6cWdqenRnZGFjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDI1NzMxMjgsImV4cCI6MjAxODE0OTEyOH0.ArTPJlFmrARrMPMajee4oYXx7Evng1OGXVP3gKiS4rE'
supabase: Client = create_client(url, key)

app = Flask(__name__)
CORS(app)
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:LENMwwPkbxc4U9rD@db.mabfnfptjihwtnyenelo.supabase.co:5432/postgres'
app.config['SECRET_KEY'] = 'specsysix'
db.init_app(app)
app.app_context().push()

class User(db.Model):
    __tablename__ = 'sih'
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
    gender = db.Column(db.String(20), nullable=False)
    education = db.Column(db.String(20), nullable=False)
    pj_location = db.Column(db.String(20), nullable=False)
    skills = db.Column(db.String(255), nullable=True)  # Assuming skills can be stored as a comma-separated string
    state = db.Column(db.String(20), nullable=False)

@app.route('/')
def welcome():
    return "Hello"

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


@app.route('/auth/callback' , methods=['POST'])
def callback(data):
    print(data)
    return data


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


@app.route('/analytics/gender')
def gender_analytics_donut():
    # need to get data, 
    
    # query database for tuple stats <stop,route,onboarding/eliding/count>
    #prepare onboarding/eliding array and prepare toggle on frontend
    
    dic_gender_count = {}
    
    text1= text("Select gender,count(*) as count from sih group by gender")
    
    
    result  = db.session.execute(text1)
    #print(result)
    
    dic_gender_analytics_count = {}
    labels_arr = []
    counts_arr =  []
    
    for row in result:
        labels_arr += [row.gender]
        counts_arr += [row.count]
    

    pallete = sns.color_palette(None,len(labels_arr))

    # #print(data)
    return jsonify(counts_arr)


@app.route('/analytics/age')
def age_analytics():
    # need to get data, 
    
    # query database for tuple stats <stop,route,onboarding/eliding/count>
    #prepare onboarding/eliding array and prepare toggle on frontend
        
    text1= text( "Select  DATE_PART('year', now()::date)-DATE_PART('year', dob) as age,count(*) from sih  group by age;")
    
    
    result  = db.session.execute(text1)
    

    arr = [list(i) for i in result]
    
    age_data = {
        '18-25': 0,
        '25-30': 0,
        '30-35': 0,
        '35-40': 0,
        '40-45': 0,
        '45-50': 0,
        '50+': 0,
         
            
    }
    for i in arr:
        a,b = i
        if a > 18 and a<=25:
            age_data['18-25']+=b
        elif a > 25 and a<=30:
            age_data['25-30']+=b
        elif a > 30 and a<=35:
            age_data['30-35']+=b
        elif a > 35 and a<=40:
            age_data['35-40']+=b
        elif a > 40 and a<=45:
            age_data['40-45']+=b
        elif a > 45 and a<=50:
            age_data['45-50']+=b
        elif a > 50:
            age_data['50+']+=b
    return jsonify(age_data)
    #print(result)
    # age_arr = []
    # rows = result.fetchall()
    # for row in rows:
    #     dob = row[0]
    #     birth_date = datetime.strptime(str(dob), '%Y-%m-%d').date()
    #     today = date.today()
    #     age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    #     print("Age:", age)
    #     age_arr.append(age)
    
    # age_arr.sort()
    
    # def group_ages(age_array):
    #     age_ranges = [(18, 25), (25, 30), (30, 35), (35, 40), (40, 45), (45, 50), (50, float('inf'))]
    #     age_counter = Counter()
    #     for age in age_array:
    #         for lower, upper in age_ranges:
    #             if lower <= age < upper:
    #                 age_counter[(lower, upper)] += 1
    #                 break

    #     return age_counter

    # result = group_ages(age_arr)

    # for age_range, count in result.items():
    #     lower, upper = age_range
    #     if upper == float('inf'):
    #         print(f"Ages {lower} and above: {count}")
    #     else:
    #         print(f"Ages {lower}-{upper - 1}: {count}")

    # result_dict = {}
    # age_counter=Counter()
    # for age_range, count in age_counter.items():
    #     lower, upper = age_range
    #     if upper == float('inf'):
    #         result_dict[f"Ages {lower} and above"] = count
    #     else:
    #         result_dict[f"Ages {lower}-{upper - 1}"] = count

    # return json.dumps(result_dict, indent=2)
    # # 18-25,25-30,30-35,35-40,40-45,45-50,50+
    # #series=interval vals label= count
    # # #print(data)


@app.route('/analytics/usersdata')
def userdata_analytics():
    from sqlalchemy.orm import sessionmaker
    Session = sessionmaker(bind = db.engine)
    session = Session()
    result = session.query(User).count()
    print(result)
    return result

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
