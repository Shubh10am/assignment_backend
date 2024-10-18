from flask_restx import Api, fields

api = Api(version="1.0",
          title="Webtoons API",
          description="API to manage your Shops Data", ui=False)

shop_model = api.model('Shop', {
    'shop_id': fields.String(required=True, description='Shop ID'),
    'name': fields.String(required=True, description='Name of the shop'),
    'latitude': fields.Float(required=True, description='Latitude of the shop'),
    'longitude': fields.Float(required=True, description='Longitude of the shop')
})

shop_model_data = api.model('Shop', {
    'name': fields.String(required=True, description='Name of the shop'),
    'distance': fields.Float(required=True, description='Distance from user')
})
