'''
:TODO: endpoint /ads?
:TODO:
:TODO:
:TODO:
:TODO:
:TODO:
:TODO:
:TODO:
:TODO:
:TODO:
:TODO:
:TODO:
:TODO:
'''

from flask import Blueprint, request
from models.tablecreator import TableAds
from models.settup_filter_page import Jeson_results
from flask_restful import reqparse

ads_routes = Blueprint('ads_routes', __name__, url_prefix='/api')

@ads_routes.route('/ads', methods=['GET'])
def ads():
    '''
    ?search=
    ?name=
    ?price>
    ?price<
    ?expire<
    :param search:
    :return:
    '''
    ads_list = Jeson_results().pack_json(TableAds().retrieve_all_by_search(request.args.get("search")))
    return {"Ads" : ads_list}


@ads_routes.route('ads/count', method=['GET'])
def count_ads():
    pass


@ads_routes.route('/ads/<int:id>')
def ads_id(id):
    return {"message":id}

@ads_routes.route('/ads?<path:query>')
def ads_query(query):
    #by_name
    #by_search
    #by_price_min_max
    return {"Message":query}

@ads_routes.route('/ads/<int:id>', methods=['PUT'])
def update_ads(id):
    #update
    pass