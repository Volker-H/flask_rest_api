# section 6
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="Feld kann nicht leer sein"
                        )
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="jedes Item braucht eine StoreID"
                        )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': "item does not exist"}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "sorry pal '{}' gibt es schon".format(name)}, 400
        request_data = Item.parser.parse_args()
        item = ItemModel(name, request_data['price'],request_data['store_id'])
        try:
            item.save_to_db()
        except:
            return {'message': "An error occurred by inserting"}, 500  # internal Server error
        return item.json(), 201  # 201 für created

    def put(self, name):
        request_data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name, request_data['price'],request_data['store_id'])
        else:
            item.price = request_data['price']
        item.save_to_db()
        return item.json()

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            ItemModel.delete(item)
        return {'message': "item deleted"}


class Items(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
