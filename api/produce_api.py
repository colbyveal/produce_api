from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask (__name__)
api = Api(app)

PRODUCE = {
    'A12T-4GH7-QPL9-3N4M': {'name': 'Lettuce', 'price': 3.46},
    'E5T6-9UI3-TH15-QR88': {'name': 'Peach', 'price': 2.99},
    'YRT6-72AS-K736-L4AR': {'name': 'Green Pepper', 'price': 0.79},
    'TQ4C-VV6T-75ZX-1RMR': {'name': 'Gala  Apple', 'price': 3.59}
}

parser = reqparse.RequestParser()

class ProducesList(Resource):
    def get(self):
        return PRODUCE

    def post(self):
        parser.add_argument("name")
        parser.add_argument("price")
        args = parser.parse_args()
        produce_id = int(max(PRODUCE.keys()))  + 1
        produce_id = '%i' % produce_id
        PRODUCE[produce_id] = {
            "name": args["name"],
            "price": args["price"]
        }                
        return PRODUCE[produce_id], 201


class Produce(Resource):
    def get(self, produce_id):
        if produce_id not in PRODUCE:
            return 'Not found', 404
        else:
            return PRODUCE[produce_id]
            
    def put(self, produce_id):
        parser.add_argument("name", type=string, help="Name ")
        parser.add_argument("price")
        args = parser.parse_args()

        if produce_id not in PRODUCE:
            return 'Not found', 404
        else:
            produce = PRODUCE[produce_id]
            produce['name'] = args['name'] if args ["name"] is not None else produce ["name"]
            produce['price'] = args['price'] if args ["price"] is not None else produce ["price"]
            return PRODUCE[produce_id]

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