from audioop import add
from .__init__ import create_app
from flask_pymongo import PyMongo
from flask import Flask, app, jsonify, request, flash


def postData(firstname, lastname, phonenumber, DOB, email, password1):
    """
    :param firstname:
    :param lastname:
    :param phonenumber:
    :param DOB:
    :param email:
    :param password1:
    :return:
    """
    flask_obj = create_app()
    Mongo = PyMongo(flask_obj)
    currentcollection = Mongo.db.Banking

    # email validation
    if currentcollection.find_one({"email": email}):
        return jsonify({'error': "email already in use"}), 400
    else:
        currentcollection.insert({'firstname': firstname, 'lastname': lastname,
                                  'phonenumber': phonenumber,
                                  'DOB': DOB,
                                  'email': email,
                                  'password1': password1
                                  })
    return jsonify({'firstname': firstname, 'lastname': lastname,
                    'phonenumber': phonenumber,
                    'DOB': DOB,
                    'email': email,
                    'password1': password1
                    })


# def validatelogin(email, password1):
#     flask_obj = create_app()
#     Mongo = PyMongo(flask_obj)
#     currentcollection = Mongo.db.Banking

#     a = currentcollection.find_one({'email': email})
#     if a:
#         if a({'password1': password1} == password1):
#             flash("logged in sucessfully", category= 'sucess')
#         else:
#             flash('incorrect password', category='error')
#     else:
#         flash('email not found', category='error')

def pData(firstname, lastname, email, password1, DOB, address, city, Province, ZipCode, phonenumber, AccountNumber,
          accountType):
    flask_obj = create_app()
    Mongo = PyMongo(flask_obj)
    currentcollection = Mongo.db.Information
    # email validation
    if currentcollection.find_one({"email": email}):
        return jsonify({'error': "email already in use"}), 400
    else:
        currentcollection.insert({'firstname': firstname, 'lastname': lastname, 'email': email,
                                  'password1': password1,
                                  'DOB': DOB,
                                  'address': address,
                                  'city': city,
                                  'Province': Province,
                                  'ZipCode': ZipCode,
                                  'phonenumber': phonenumber,
                                  'AccountNumber': AccountNumber,
                                  'accountType': accountType
                                  })
    return jsonify({'firstname': firstname, 'lastname': lastname, 'email': email,
                    'password1': password1,
                    'DOB': DOB,
                    'address': address,
                    'city': city,
                    'Province': Province,
                    'ZipCode': ZipCode,
                    'phonenumber': phonenumber,
                    'AccountNumber': AccountNumber,
                    'accountType': accountType
                    })
