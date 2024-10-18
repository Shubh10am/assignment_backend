from flask_restx import reqparse

shop_parser = reqparse.RequestParser()
shop_parser.add_argument('name', type=str, required=True, help='Name of the shop')
shop_parser.add_argument('latitude', type=float, required=True, help='Latitude of the shop')
shop_parser.add_argument('longitude', type=float, required=True, help='Longitude of the shop')

search_parser = reqparse.RequestParser()
search_parser.add_argument('latitude', type=float, required=True, help='User latitude')
search_parser.add_argument('longitude', type=float, required=True, help='User longitude')
