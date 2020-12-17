from flask import Blueprint, request
from flask_restful import reqparse

ads_routes = Blueprint('ads', __name__, url_defaults='/api')

@ads_routes.route('/ads', methods=['GET', 'POST'])
def ads():
    if request.method == 'POST':
        #create_ad
        pass

    return {"message" : "All_ads"}

@ads_routes.route('/ads/<int:id>')
def ads_id(id):
    return {"message":"ad_by_id"}

@ads_routes.route('/ads?<path:query>')
def ads_query(query):
    #by_name
    #by_search
    #by_price_min_max
    return {"Message":query}

@ads_routes.route('/ads/<int:id>', methods=['PUT'])
def ads(id):
    #update
    pass