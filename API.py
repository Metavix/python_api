import json
import requests
import dbm
import pymongo
from flask import Flask, jsonify, request


class API:
    def __init__(self):
        """
        Constructor of the class
        """
        self._client_database = pymongo.MongoClient("mongodb://localhost:27017")
        self._my_db = self._client_database["loanDB"]
        self._user_table = self._my_db["user_table"]
        self._loan_table = self._my_db["loan_table"]

    def new_user(self, username, password, email, business_name, business_id):
        """
        :param username: <str> the user name to log in
        :param password: <str> the password to log in
        :param email: <str> the email of the user
        :param business_name: <str> the name of the business
        :param business_id: <str> the id of the company in the country
        :return: <bool> True or False
        """
        my_query = {'username': username}
        item_count = self._user_table.count_documents(my_query)
        if item_count == 0:
            data_to_insert = {
                "username": username,
                "password": password,
                "email": email,
                "business_name": business_name,
                "business_id": business_id
            }
            _id = self._user_table.insert_one(data_to_insert)
            return _id
        return 0

    def ask_loan(self, amount, user_id):
        """
        :param amount: <int> the amount of the loan
        :param user_id: <int> the user id
        :return: <str> state of the loan
        """
        print(amount)
        if amount == 50000:
            info_to_insert = {
                "user_id": user_id,
                "amount": amount,
                "application_status": "Undecided",
                "loan_status": "closed"
            }
        else:
            info_to_insert = {
                "user_id": user_id,
                "amount": amount,
                "application_status": "Approved",
                "loan_status": "Active"
            }
        if amount > 50000:
            info_to_insert = {
                "user_id": user_id,
                "amount": amount,
                "application_status": "Declined",
                "loan_status": "closed"
            }

        print(info_to_insert)
        x = self._loan_table.insert_one(info_to_insert)
        info_to_insert.pop('_id')
        return info_to_insert

    def return_user_id(self, username, password):
        """
        :return: The directory of the user
        """
        my_query = {'username': username, 'password': password}
        ans = self._user_table.find_one(my_query)
        print(ans["business_id"])
        return ans["business_id"]

    def check_user(self, username, password):
        """
        :param username: <str> The username to ask to database
        :param password: <str> The password of the user
        :return: <bool> true or false
        """
        my_query = {'username': username, 'password': password}
        item_count = self._user_table.count_documents(my_query)
        print(item_count)
        if item_count == 0:
            return False
        else:
            return True


# Instantiate methods
app = Flask(__name__)

# Instantiate the API
api = API()


@app.route('/newUser', methods=['POST'])
def new_user():
    bdy_parameters = request.get_json()
    # Check that the body is complete
    required = ['username', 'password', 'email', 'business_name', 'business_id']
    if not all(k in bdy_parameters for k in required):
        return 'Missing parameter', 400
    res = api.new_user(bdy_parameters['username'], bdy_parameters['password'], bdy_parameters['email'],
                       bdy_parameters['business_name'], bdy_parameters['business_id'])
    if res == 0:
        return 'User already exist', 400
    else:
        return 'User has been created the id is: ', 200


@app.route('/askLoan', methods=['POST'])
def ask_loan():
    bdy_parameters = request.get_json()
    # Check that the body is complete
    print(bdy_parameters)
    required = ['id', 'amount']
    if not all(k in bdy_parameters for k in required):
        return 'Missing parameter', 400
    ans = api.ask_loan(bdy_parameters['amount'], bdy_parameters['id'])
    return ans, 200


@app.route('/sigIn', methods=['POST'])
def sign_in():
    bdy_parameters = request.get_json()
    print(bdy_parameters)
    # Check that the body is complete
    required = ['username', 'password']
    if not all(k in bdy_parameters for k in required):
        return 'Missing parameter', 400
    # TODO: go for a function to ask for existing user
    ans = api.check_user(bdy_parameters['username'], bdy_parameters['password'])

    if ans:
        response = {
            'username': bdy_parameters['username'],
            'user_id': api.return_user_id(bdy_parameters['username'], bdy_parameters['password'])
        }
        return jsonify(response), 200
    else:
        return 'User does not exist', 200


# Uncomment this line if you want to specify the port number in the code
app.run(debug=True, host='0.0.0.0', port=5000)
