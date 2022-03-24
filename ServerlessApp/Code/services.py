from flask import jsonify

from Code.transactions import Transactions


class Services:
    """
    This file acts as a wrapper between transactions and routes
    """

    @staticmethod
    def credit_amount(request):
        """
        This function is responsible for crediting the amount to the account
        :return:
        """
        trans_obj = Transactions()
        return trans_obj.credit(request)

    @staticmethod
    def debit_amount(request):
        """
        This function is responsible for debit the amount to the account
        :return:
        """
        trans_obj = Transactions()
        return trans_obj.debit(request)

    @staticmethod
    def transfer_amount(request):
        """
        This function is responsible for transfer the amount to another account
        :return:
        """
        trans_obj = Transactions()
        return trans_obj.transfer(request)

    @staticmethod
    def pay_bills(request):
        """
        This function is responsible for paying the bills to the vendor
        :return:
        """
        trans_obj = Transactions()
        return trans_obj.pay_bills(request)

    @staticmethod
    def interac(request):
        """
        This function is responsible for paying the bills to the vendor
        :return:
        """
        trans_obj = Transactions()
        return trans_obj.interac(request)


