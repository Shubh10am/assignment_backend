from flask_jwt_extended import create_access_token, jwt_required
from flask_restx import Resource, Namespace

from web.api.resources.ottermap_task.model import Shop
from web.api.resources.ottermap_task.parser import search_parser, shop_parser
from web.api.resources.ottermap_task.serializer import shop_model
from web.api.resources.ottermap_task.utils import haversine
from web.api.resources.ottermap_task.utils import data_envelope, format_response

ns = Namespace("Shop API", description="API to interact with Shop App", path="/shops")


@ns.route('/create-token')
class Login(Resource):
    @staticmethod
    def post():
        """API To Create Access Token in Order To Access All APIs"""
        username = "shubh"
        password = "shubh@12"

        if username == "shubh" and password == "shubh@12":
            access_token = create_access_token(identity=username)
            return format_response(None, 200, "Token Generated successful", custom_ob=access_token)

        return format_response(None, 401, "Invalid credentials")


@ns.route('/register')
class RegisterShop(Resource):
    @jwt_required()
    @ns.expect(shop_parser, validate=True)
    @ns.marshal_with(data_envelope(shop_model))
    def post(self):
        """API To Add A Shop's Details"""
        args = shop_parser.parse_args()
        name = args.get('name')
        latitude = args.get('latitude')
        longitude = args.get('longitude')

        # Validate latitude and longitude
        if not (-90 <= latitude <= 90):
            return format_response(None, 400, "Invalid Latitude")
        if not (-180 <= longitude <= 180):
            return format_response(None, 400, "Invalid Longitude")

        shop = Shop()
        shop.shop_id = shop.generate_id()
        shop.name = name
        shop.latitude = latitude
        shop.longitude = longitude

        return format_response(shop, 200, "Shops Details Saved Successfully")


@ns.route('/search')
class SearchShops(Resource):
    @ns.expect(search_parser, validate=True)
    def get(self):
        """API To Search Shops"""
        args = search_parser.parse_args()
        user_lat = args['latitude']
        user_lon = args['longitude']

        shops = Shop.objects()
        shop_distances = []

        for shop in shops:
            distance = haversine(user_lat, user_lon, shop.latitude, shop.longitude)
            shop_distances.append({'name': shop.name, 'distance': distance})

        shop_distances.sort(key=lambda x: x['distance'])

        return format_response(None, 200, "Shops fetched successfully", custom_ob=shop_distances)
