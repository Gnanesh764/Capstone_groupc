from flask import jsonify
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

    def credit(self, request):
        """
        This function is responsible for crediting the amount to the account
        :return:
        """
        try:
            account_number = request.get("AccountNumber")
            amount_to_credit = request.get("Amount")
            depositor_name = request.get("DepositorName")
            account = self.db_obj.get_one("accounts", {"AccountNumber": account_number})
            if account is not None:
                self.db_obj.set_one("accounts", {"AccountNumber": account_number},
                                    {"Amount": int(account["Amount"]) + amount_to_credit})
                self.db_obj.create("Transactions", {"AccountNumber": account_number,
                                                    "amount": amount_to_credit, "transaction": "credit",
                                                    "Depositor": depositor_name})
                account.pop("_id", None)
                account["Amount"] = (int(account["Amount"]) + amount_to_credit)
                return account
            else:
                return jsonify({"error": "No such record found"})
        except KeyError as error:
            print("Exception occurred while crediting the money")
            return "Check it properly"

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
            if available_amount >= amount :
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

    def account_details(self, request):
        """
        This module helps in modifying the user account details
        :return:
        """

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
