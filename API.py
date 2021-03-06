import json
import requests
from urllib.parse import urlparse
from flask import Flask, jsonify, request


class API:
    def __init__(self):
        self.user_id = {}

    def ask_loan(self, amount, user_id):
        """
        :param amount: <int> the amount of the loan
        :param user_id: <int> the user id
        :return: <str> state of the loan
        """
        if amount == 

    def return_user_id(self):
        """
        :return: The directory of the user
        """
        return self.user_id['id']

    @staticmethod
    def check_user(username, password):
        """
        :param username: <str> The username to ask to database
        :param password: <str> The password of the user
        :return: <bool> true or false
        """
        # TODO: ask to database for existing user
        response = True
        if response:
            return True
        else:
            return False


# Instantiate methods
app = Flask(__name__)

# Instantiate the API
api = API()


@app.route('/sigIn', methods=['GET'])
def sign_in():
    bdy_parameters = request.get_json()

    # Check that the body is complete
    required = ['username', 'password']
    if not all(k in bdy_parameters for k in required):
        return 'Missing parameter', 400
    # TODO: go for a function to ask for existing user
    ans = api.check_user(bdy_parameters['username'], bdy_parameters['password'])

    if ans:
        response = {
            'username': bdy_parameters['username'],
            'user_id': api.return_user_id()
        }
        return jsonify(response), 200
    else:
        return 'User does not exist', 200


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port)
