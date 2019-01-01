import sqlite3
from flask_jwt import jwt, jwt_required
from flask_restful import Resource, reqparse
from models.item import ItemModel

class Item(Resource):

    parser = reqparse.RequestParser();
    parser.add_argument('price', type=float, required=True, help='This cannot be blank!')
    parser.add_argument('store_id', type = int, required=True, help='Each item need to belong to a store')

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json(), 201
        return {'message' : 'Item not found'}, 401
        
    # Create a new item
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message' : "An item with name '{}' already exist".format(name)}, 400

        data = self.parser.parse_args()
        item = ItemModel(name, data['price'], data['store_id'])

        try:
            item.save_to_db()
            return item.json(), 201
        except:
            return {'message' : 'An error occurred when inserting the item'}, 500

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message' : 'Item deleted'}
        return {'message' : 'Item not found'}

    def put(self, name):
        data = self.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if not item:
            item = ItemModel(name, data['price'], data['store_id'])
        else:
            item.price = data['price']
        try:
            item.save_to_db()
            return item.json()
        except:
            return {'message' : 'An error occurred when updating the item'}, 500    


class ItemList(Resource):
    def get(self):
        return {'items' : [item.json() for item in ItemModel.query.all()]}
