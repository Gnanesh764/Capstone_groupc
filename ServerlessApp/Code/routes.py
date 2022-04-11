from flask import Blueprint, render_template, request, jsonify, Response, url_for, flash
from werkzeug.utils import redirect

from ServerlessApp.Code.services import Services

auth = Blueprint('auth', __name__)


@auth.route('/', methods=['GET', 'POST'])
def index():
    return render_template("logout.html")


@auth.route('/login', methods=['GET', 'POST'])
def login():
    Response.content_type = 'application/json'
    user_request = request
    if request.method == 'POST':
        login_response = Services.login(user_request)
        print(login_response)
        flash('You are logged in successful', 'success')
        return Services.login(user_request)
    return render_template("l.html")


@auth.route('/logout')
def logout():
    return render_template("landing.html")


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    Response.content_type = 'application/json'
    user_request = request
    if request.method == 'POST':
        # return Services.signup(user_request)
        response_signup = Services.signup(user_request)
        print(response_signup)
        flash('You are now registered and can log in', 'success')
        return response_signup
    return render_template("sign.html")


@auth.route('/credit', methods=['GET', 'POST'])
def credit():
    """
    This function is responsible for crediting the amount to the account
    :return:
    """
    Response.content_type = 'application/json'
    user_request = request
    if request.method == 'POST':
        return jsonify(Services.credit_amount(user_request))
    return render_template("trans.html")


@auth.route('/debit', methods=['GET', 'POST'])
def debit():
    """
    This function is responsible for debit the amount from the account
    :return:
    """
    Response.content_type = 'application/json'
    user_request = request
    if request.method == "POST":
        return jsonify(Services.debit_amount(user_request))
    return render_template("withdraw.html")


@auth.route('/transfer', methods=["GET", "POST"])
def transfer():
    """
    This function is responsible for transferring money to another accounts
    :return:
    """
    Response.content_type = 'application/json'
    user_request = request
    if request.method == "POST":
        return jsonify(Services.transfer_amount(user_request))
    return render_template("transfer.html")


@auth.route('/pay_bills', methods=["GET", "POST"])
def pay_bills():
    """
    This module helps in handling the bills payments of the user
    :return:
    """
    Response.content_type = 'application/json'
    user_request = request
    if request.method == "POST":
        return jsonify(Services.pay_bills(user_request))
    return render_template("paybills.html")


@auth.route('/interac', methods=["GET", "POST"])
def interac():
    """
    This module helps in sending money thorugh interac email id
    :return:
    """
    Response.content_type = 'application/json'
    user_request = request
    if request.method == "POST":
        return jsonify(Services.interac(user_request))
    return render_template("interac.html")


@auth.route('/modify_details', methods=["GET", "POST"])
def modify_details():
    """
    This module helps in modifying the user details
    :return:
    """
    Response.content_type = 'application/json'
    user_request = request.json
    return jsonify(Services.modify_details(user_request))

@auth.route('/dashboard', methods=["GET", "POST"])
def dashboard():
    return render_template("dashboard.html")