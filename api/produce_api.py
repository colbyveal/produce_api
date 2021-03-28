from flask import Flask
from flask_restful import Resource, Api, reqparse
from string import ascii_uppercase, digits
from random import choices

app = Flask (__name__)
api = Api(app)
parser = reqparse.RequestParser()

"""
PRODUCE - TYPE: dict
    Key: 
        produce code: 16 char string consisting of 4 'dash-seperated' 4 character strings (19 chars total). Alphanumeric and case insensitive
    Value:
        stuct:
            produce code: 16 char string consisting of 4 dash seperated 4 character strings. Alphanumeric and case insensitive
                use generateProduceCode() to generate a unique code when POSTing new produce
                not passed in via api-call
            name: Case insensitive alphanumeric string
            price: number with exactly 2 decimal places
"""
PRODUCE = {
    'A12T-4GH7-QPL9-3N4M': {'produce code': 'A12T-4GH7-QPL9-3N4M', 'name': 'Lettuce', 'price': 3.46},
    'E5T6-9UI3-TH15-QR88': {'produce code': 'E5T6-9UI3-TH15-QR88', 'name': 'Peach', 'price': 2.99},
    'YRT6-72AS-K736-L4AR': {'produce code': 'YRT6-72AS-K736-L4AR', 'name': 'Green Pepper', 'price': 0.79},
    'TQ4C-VV6T-75ZX-1RMR': {'produce code': 'TQ4C-VV6T-75ZX-1RMR', 'name': 'Gala  Apple', 'price': 3.59}
}

"""
generateProduceCode will generate a unique code for each produce in our dict
    produce code: 16 char string consisting of 4 'dash-seperated' 4 character strings (19 chars total). Alphanumeric and case insensitive
    example: A12T-4GH7-QPL9-3N4M
"""
def generateProduceCode():
    codeChunk1 = ''.join(choices(ascii_uppercase+digits, k=4));
    codeChunk2 = ''.join(choices(ascii_uppercase+digits, k=4));
    codeChunk3 = ''.join(choices(ascii_uppercase+digits, k=4));
    codeChunk4 = ''.join(choices(ascii_uppercase+digits, k=4));
    produceCode = codeChunk1 + '-' + codeChunk2 + '-' + codeChunk3 + '-' + codeChunk4
    return produceCode

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
formatPrice ensures incoming price is of format #.##
    ensures price is a number
    will add 0's or round if needed
"""
def formatPrice(price):
    try:
        numPrice = float(price)
        return '{:.2f}'.format(numPrice)
    except:
        return False

class ProducesList(Resource):
    def get(self):
        return PRODUCE

    def post(self):
        parser.add_argument("name")
        parser.add_argument("price")
        args = parser.parse_args()

        formattedPrice = formatPrice(args["price"])

        if not validateName(args["name"]):
            return "Invalid request", 400

        if not formattedPrice:
            return "Invalid request", 400

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
            
    def put(self, produce_id):
        parser.add_argument("produce code")
        parser.add_argument("name")
        parser.add_argument("price")
        args = parser.parse_args()

        if produce_id not in PRODUCE:
            return 'Not found', 404
        else:
            produce = PRODUCE[produce_id]
            produce['produce code'] = args['produce code'] if args ['produce code'] is not None else produce ['produce code']
            produce['name'] = args['name'] if args ["name"] is not None else produce ["name"]
            produce['price'] = args['price'] if args ["price"] is not None else produce ["price"]
            return PRODUCE[produce_id], 200

    def delete(self, produce_id):
        if produce_id not in PRODUCE:
            return 'Not found', 404
        else:
            del PRODUCE[produce_id]
            return '', 204

api.add_resource(ProducesList, '/produce/')
api.add_resource(Produce, '/produce/<produce_id>')

if __name__ == '__main__':
    app.run(debug=True)