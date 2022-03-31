from flask import jsonify, flash, render_template
from ServerlessApp.Code.dbmongo import DbMongo
from ServerlessApp.Code.config import DB_HOST, DB_PORT, DB_NAME


class Transactions:
    """
    This module handles tha transactions section of the application
    """

    def __init__(self):
        """
        This method creates the database authentication object
        :param config: configuration to be connected to the database
        :return: database object
        """
        self.db_config = {"host": DB_HOST, "port": DB_PORT, "db_name": DB_NAME}
        self.db_obj = DbMongo()
        self.db_obj.db_connect(self.db_config)

    def login(self, request):
        """
        This function is responsible for authorizing the user
        """
        try:
            email = request.form.get('email')
            password = request.form.get('password1')
            user_accounts = self.db_obj.get_one("accounts", {"email": email})
            if user_accounts["email"] == email:
                if user_accounts["password"] == password:
                    return render_template("dashboard.html")
            else:
                return {"Status": "Cannot access the account"}
        except Exception as error:
            return {"Status": "Error in authorizing the user {}".format(error)}

    def sign_up(self, request):
        """
        This function is responsible for creating a user account the amount to the account
        :return:
        """
        try:
            email = request.form.get('email')
            firstname = request.form.get('firstname')
            lastname = request.form.get('lastname')
            phone_number = request.form.get('phonenumber')
            birth_date = request.form.get('DOB')
            password = request.form.get('password1')
            confirm_password = request.form.get('password2')
            address = request.form.get('address')
            city = request.form.get('city')
            Province = request.form.get('Province')
            ZipCode = request.form.get('ZipCode')
            phonenumber = request.form.get('phonenumber')
            AccountNumber = int(request.form.get('AccountNumber'))
            accountType = request.form.get('accountType')

            if len(email) < 4:
                flash('Email must be greater than 3 characters.', category='error')
            elif len(firstname) < 2:
                flash('First name must be greater than 1 character.', category='error')
            elif len(lastname) < 2:
                flash('First name must be greater than 1 character.', category='error')
            elif len(phone_number) < 2:
                flash('First name must be greater than 1 character.', category='error')
            elif len(birth_date) < 2:
                flash('First name must be greater than 1 character.', category='error')
            elif password != confirm_password:
                flash('Passwords dont match.', category='error')
            elif len(password) < 7:
                flash('Password must be at least 7 characters.', category='error')
            else:
                flash('Account created!', category='success')

            data = {'firstname': firstname, 'lastname': lastname, 'email': email, 'city': city,
                    'phone_number': phone_number, 'DOB': birth_date, 'password': password,
                    'address': address, 'province': Province, 'ZipCode': ZipCode,
                    'phone': phonenumber, "AccountNumber": AccountNumber, "Acc_Type": accountType,
                    "Amount": 0}

            self.db_obj.create('accounts', data)
            # return render_template("l.html")
            return {"Status": "Account created successful"}
        except Exception as error:
            return {"Status": "Error in creating account \n {}".format(error)}

    def credit(self, request):
        """
        This function is responsible for crediting the amount to the account
        :return:
        """
        try:
            account_number = request.get("AccountNumber")
            amount_to_credit = request.get("Amount")
            depositor_name = request.get("DepositorName")
            print("AccountNumber",  account_number)
            account = self.db_obj.get_one("accounts", {"AccountNumber": account_number})
            print(account)
            if account is not None:
                print(1)
                self.db_obj.set_one("accounts", {"AccountNumber": account_number},
                                    {"Amount": int(account["Amount"]) + amount_to_credit})
                print(2)
                self.db_obj.create("Transactions", {"AccountNumber": account_number,
                                                    "amount": amount_to_credit, "transaction": "credit",
                                                    "Depositor": depositor_name})
                print(3)
                account.pop("_id", None)
                account["Amount"] = (int(account["Amount"]) + amount_to_credit)
                return account
            else:
                return jsonify({"error": "No such record found"})
        except KeyError as error:
            print("Exception occurred while crediting the money ", error)
            return {"Status": "Check it properly"}

    def debit(self, request):
        """
        This function is responsible for debit the amount from the account
        :return:
        """
        try:
            account_number = request.get("AccountNumber")
            amount_to_debit = request.get("Amount")
            payee = request.get("DepositorName")
            account = self.db_obj.get_one("accounts", {"AccountNumber": account_number})
            avail_amount = account["Amount"]
            if account is not None:
                if avail_amount >= amount_to_debit:
                    self.db_obj.set_one("accounts", {"AccountNumber": account_number},
                                        {"Amount": int(avail_amount) - amount_to_debit})
                    self.db_obj.create("Transactions", {"AccountNumber": account_number,
                                                        "amount": amount_to_debit, "transaction": "debit",
                                                        "payee": payee})
                    account.pop("_id", None)
                    account["Amount"] = (int(avail_amount) - amount_to_debit)
                    return account
                else:
                    return {"error": "Insufficient balance"}
            else:
                return jsonify({"error": "No such record found"})
        except KeyError as error:
            print("Exception occurred while debiting the money")
            return "Check it properly "

    def transfer(self, request):
        """
        This function is responsible for transferring money to another accounts
        :return:
        """
        try:
            sender_acc_number = 1234567898
            receiver_account_number = request.get("AccountNumber")
            amount_to_transfer = request.get("Amount")
            payee = request.get("DepositorName")
            # get sender account details
            sender_account = self.db_obj.get_one("accounts", {"AccountNumber": sender_acc_number})
            avail_amount = sender_account["Amount"]
            # get receiver account details
            receiver_account = self.db_obj.get_one("accounts", {"AccountNumber": receiver_account_number})
            receiver_amount = receiver_account["Amount"]
            if sender_account and receiver_account is not None:
                if avail_amount >= amount_to_transfer:
                    self.db_obj.set_one("accounts", {"AccountNumber": sender_acc_number},
                                        {"Amount": int(avail_amount) - amount_to_transfer})
                    self.db_obj.create("Transactions", {"AccountNumber": sender_acc_number,
                                                        "amount": amount_to_transfer, "transaction": "debit",
                                                        "payee": payee})
                    sender_account.pop("_id", None)
                    sender_account["Amount"] = (int(avail_amount) - amount_to_transfer)

                    self.db_obj.set_one("accounts", {"AccountNumber": receiver_account_number},
                                        {"Amount": int(receiver_amount) + amount_to_transfer})
                    self.db_obj.create("Transactions", {"AccountNumber": sender_acc_number,
                                                        "amount": amount_to_transfer, "transaction": "credit",
                                                        "payee": payee})
                    receiver_account["Amount"] = int(receiver_amount) + amount_to_transfer
                    sender_account.pop("_id", None)
                    receiver_account.pop("_id", None)
                    return receiver_account
                else:
                    return {"error": "Insufficient balance"}
            else:
                return jsonify({"error": "No such record found"})
        except KeyError as error:
            print("Exception occurred while debiting the money")
            return "Check it properly Yoo"

    def pay_bills(self, request):
        """
        This module helps in handling the bills payments of the user
        :return:
        """
        try:
            vendor_name = request.get("vendor")
            amount = request.get("Amount")
            account_number = 1234567898
            sender_account = self.db_obj.get_one("accounts", {"AccountNumber": account_number})
            available_amount = sender_account.get("Amount")
            if available_amount >= amount:
                self.db_obj.set_one("accounts", {"AccountNumber": account_number},
                                    {"Amount": available_amount - amount})
                self.db_obj.create("Transactions", {"AccountNumber": account_number,
                                                    "amount": amount, "transaction": "debit",
                                                    "payee": vendor_name})
                return {"Status": "Your payment of {} to {} is successful".format(amount, vendor_name)}
            else:
                return {"Status": "Insufficient balance"}
        except Exception as error:
            return {"Status": "Error occurred " + str(error)}

    def modify_details(self, request):
        """
        This module helps in modifying the user account details
        :return:
        """
        try:
            details_to_modify = list(request.keys())
            updated_data = {}
            for key in details_to_modify:
                updated_data[key] = request.get(key)
            self.db_obj.set_one("accounts", {"AccountNumber": 1234567898}, updated_data)
            data = self.db_obj.get_one("accounts", {"AccountNumber": 1234567898})
            data.pop("_id", None)
            return {"Status": data}

        except Exception as error:
            return {"Status": "Error occurred while updating the details"}

    def interac(self, request):
        """
        This module helps in sending money through interac to other accounts
        :return:
        """
        try:
            email_id = request.get("email")
            amount = request.get("Amount")
            account_number = 1234567898
            sender_account = self.db_obj.get_one("accounts", {"AccountNumber": account_number})
            available_amount = sender_account.get("Amount")
            if available_amount >= amount:
                self.db_obj.set_one("accounts", {"AccountNumber": account_number},
                                    {"Amount": available_amount - amount})
                self.db_obj.create("Transactions", {"AccountNumber": account_number,
                                                    "amount": amount, "transaction": "debit",
                                                    "payee": email_id})
                return {"Status": "Your payment of {} to {} is successful".format(amount, email_id)}
            else:
                return {"Status": "Insufficient balance"}
        except Exception as error:
            return {"Status": "Error occurred " + str(error)}
