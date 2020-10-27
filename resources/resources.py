from models.package import Pack
from models.tablecreator import TableCreator
from flask_restful import Resource, reqparse

class Search(Resource):
    def post(self, search_items):
        search = str(search_items).replace(" ", "_")
        packer = Pack(search).store_ads()
        if packer:
            return {"message": "Search is valid and we are storring data."}
        return {"message":"No ad for that item."}

    def get(self, search_items):
        getter = TableCreator(search_items).retrieve_items()
        items = []
        if getter:
            for item in getter:
                items.append({"id":item[0], "name": item[1], "price": item[2], "picture": item[3], "expire": item[4], "link": item[5], "show": item[6]})
            return {"items": items}
        return {"message": "No such table"}

    def put(self, search_items):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, help='Item id, intiger')
        parser.add_argument('show', type=int, help='Show = true/false')
        args = parser.parse_args()
        id = args["id"]
        show = args["show"]
        getter = TableCreator(search_items).return_item(args)
        for fields in getter:
            updated_item = {"id":fields[0], "name": fields[1], "price": fields[2], "picture": fields[3], "expire": fields[4], "link": fields[5], "show": fields[6]}
        return updated_item