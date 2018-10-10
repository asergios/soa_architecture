'''
António Sérgio Silva
asergiosilv@gmail.com https://asergio.pw
Engenharia de Servicos 2018/19 MEC:76678 asergio@ua.pt
'''

from flask import Flask, request, jsonify, render_template
from util import *
from apispec import APISpec
from apispec.ext.flask import FlaskPlugin
import database as db
import secrets, json

app = Flask(__name__)
app.config.from_pyfile('config.py')

# Create an APISpec
spec = APISpec(
    title='StrongPay',
    base_path='http://127.0.0.1:5000/',
    version='1.0.0',
    openapi_version='3.0.0',
    plugins=[
        FlaskPlugin()
    ]
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/docs')
def docs():
    return render_template('doc.html')

@app.route('/CreateCheckout', methods=['POST'])
def create_checkout():
    ''' CreateCheckout
    ---
    post:
        description: Creates a checkout
        tags:
            - Generating a payment
        requestBody:
            required: true
            content:
              application/x-www-form-urlencoded:
                schema:
                  type: object
                  properties:
                    AMOUNT:
                      type: double
                    MERCHANT:
                      type: string
                    RETURN_URL:
                      type: string
                    CANCEL_URL:
                      type: string
                  required:
                    - AMOUNT
                    - MERCHANT
                    - RETURN_URL
                    - CANCEL_URL
        responses:
            201:
                description: A JSON containing a TOKEN that indentifies the Checkout
                content:
                    application/json:
                      schema:
                        properties:
                          TOKEN:
                            type: string
            400:
                description: A JSON containing a ERROR that indentifies the problem
                content:
                    application/json:
                      schema:
                        properties:
                          ERROR:
                            type: string
    '''
    # request.form looks ugly and takes too much space...
    param = request.form
    keys = [k for k in param.keys()]

    # Checking for required parameters
    if not param or not check_parameters(keys, param):
        return jsonify({'ERROR': 'Invalid format or parameters missing.'}), 400

    # Cheking if URI are valid
    if not uri_validator(param['RETURN_URL']) or not uri_validator(param['CANCEL_URL']):
        return jsonify({'ERROR': 'RETURN or CANCEL URI with invalid format.'}), 400

    # Checking if amount is a valid number
    if not is_number(param['AMOUNT']):
        return jsonify({'ERROR': 'AMOUNT not valid.'}), 400

    # Checking if merchant exists
    if not db.exists('MERCHANT', 'id', param['MERCHANT']):
        return jsonify({'ERROR': 'MERCHANT doesn\'t exist.'}), 400

    # Generating token and checking if it doesn't exist already
    while True:
        token = secrets.token_urlsafe(16)
        if not db.exists('CHECKOUT', 'id', token):
            break

    # Inserting new checkout to database
    try:
        validation = db.insert('CHECKOUT', \
            ('id', 'amount', 'return_url', 'cancel_url', 'merchant'), \
            tuple( [token] + [param[k] for k in keys] ) )
    except Exception as e:
        return jsonify({'ERROR': 'An error ocurred on the Database.'}), 500

    # Everything went well, returning token for new checkout
    return jsonify({'CHECKOUT_TOKEN': token}), 201

with app.test_request_context():
    spec.add_path(view=create_checkout)

with open('static/swagger.json', 'w') as f:
    json.dump(spec.to_dict(), f)

if __name__ == '__main__':
    app.run(debug=True, port=5000) #run app in debug mode on port 5000
