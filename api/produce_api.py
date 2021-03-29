from flask import Flask
from flask_restful import Resource, Api, reqparse
from string import ascii_uppercase, digits
from random import choices
import json

app = Flask (__name__)
api = Api(app)
parser = reqparse.RequestParser()

"""
Info about Data Struct for storing produce --

PRODUCE - TYPE: dict
    Key: 
        produce code: 16 char string consisting of 4 'dash-seperated' 4 character strings (19 chars total). Alphanumeric and case insensitive
    Value:
        stuct:
            produce code: 16 char string consisting of 4 dash seperated 4 character strings (19 chars total). Alphanumeric and case insensitive
                use generateProduceCode() to generate a unique code when POSTing new produce
                not passed in via api-call
            name: Case insensitive alphanumeric string
            price: number with exactly 2 decimal places

initial json:
    PRODUCE = {
        'A12T-4GH7-QPL9-3N4M': {'produce code': 'A12T-4GH7-QPL9-3N4M', 'name': 'Lettuce', 'price': 3.46},
        'E5T6-9UI3-TH15-QR88': {'produce code': 'E5T6-9UI3-TH15-QR88', 'name': 'Peach', 'price': 2.99},
        'YRT6-72AS-K736-L4AR': {'produce code': 'YRT6-72AS-K736-L4AR', 'name': 'Green Pepper', 'price': 0.79},
        'TQ4C-VV6T-75ZX-1RMR': {'produce code': 'TQ4C-VV6T-75ZX-1RMR', 'name': 'Gala  Apple', 'price': 3.59}
    }
"""

with open('../data/db.json') as f:
    PRODUCE = json.load(f)

"""
ensureUniqueItem ensures incoming item is not already in database
    checks if name is already associated with an item
"""
def ensureUniqueItem(name):
    for produce_id, produce in PRODUCE.items():
        if produce['name'].capitalize() == name.capitalize():
            return False
    return True

"""
validateName checks to ensure incoming name is valid
A valid name consists of:
    Alphanumeric chars ONLY
    is NOT an empty string (this disqualifies as alphanumeric)
"""
def validateName(name):
   isValidName = name.isalnum()
   return isValidName

"""
validatePrice ensures incoming price is a number
    ensures price is a number
"""
def validatePrice(price):
    try:
        numPrice = float(price)
        return True
    except:
        return False

"""
performValidation executes validation functions all at once
    see individual functions for details
"""
def performValidation(name, price):

    if not ensureUniqueItem(name):
        return False

    if not validateName(name):
        return False

    if not validatePrice(price):
        return False

    return True

"""
generateProduceCode will generate a unique code for each produce in our dict
    produce code: 16 char string consisting of 4 'dash-seperated' 4 character string segments (19 chars total). Alphanumeric and case insensitive
    example: A12T-4GH7-QPL9-3N4M
"""
def generateProduceCode():
    codeSegment1 = ''.join(choices(ascii_uppercase+digits, k=4));
    codeSegment2 = ''.join(choices(ascii_uppercase+digits, k=4));
    codeSegment3 = ''.join(choices(ascii_uppercase+digits, k=4));
    codeSegment4 = ''.join(choices(ascii_uppercase+digits, k=4));
    produceCode = codeSegment1 + '-' + codeSegment2 + '-' + codeSegment3 + '-' + codeSegment4
    return produceCode

"""
formatPrice ensures that price is in the proper format #.##
    will add 0's if not enough numbers after decimal
    will round if too many number after decimal
"""
def formatPrice(price):
    return "{:.2f}".format(float(price))

class ProduceList(Resource):
    def get(self):
        return PRODUCE

    def post(self):
        parser.add_argument("name")
        parser.add_argument("price")
        args = parser.parse_args()

        if not performValidation(args['name'], args['price']):
            return "Invalid Request", 400

        formattedPrice = formatPrice(args['price'])
        produce_id = generateProduceCode()

        PRODUCE[produce_id] = {
            "produce code": produce_id,
            "name": args["name"],
            "price": formattedPrice
        }

        return PRODUCE[produce_id], 201

class Produce(Resource):
    def get(self, produce_id):
        if produce_id not in PRODUCE:
            return 'Not found', 404
        else:
            return PRODUCE[produce_id]

    def delete(self, produce_id):
        if produce_id not in PRODUCE:
            return 'Not found', 404
        else:
            del PRODUCE[produce_id]
            return '', 204

api.add_resource(ProduceList, '/produce/')
api.add_resource(Produce, '/produce/<produce_id>')


if __name__ == '__main__':
    app.run(debug=True)