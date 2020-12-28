import sqlite3
from db import session
from models.all_ads import All_ads
from models.user import User
from sqlalchemy import and_


class TableAds:
    def create_all_ads(self, name, price, picture, expire, link, search, user_id):
        query = All_ads(name=name, price=price, picture=picture, expire=expire, link=link, search=search, user_id=user_id)
        session.add(query)
        session.commit()

    def retrieve_all_ads(self, search):
        query = session.query(All_ads).filter_by(search=search).all()
        return query

    def update_ad_by_id(self, search, id):
        query = All_ads().query.filter_by(search=search, id=id).first()
        query.show = False
        session.commit()

    def retrieve_ads_by_search_and_id(self, search, user_id):
        query = session.query(All_ads).filter(
            and_(
                All_ads.search == search,
                All_ads.user_id == user_id,
                All_ads.show == 1
            )
        ).order_by(All_ads.id)
        return query

    def retrieve_search(self, search):
        query = session.query(All_ads).filter(All_ads.search == search).first()
        return query

    def retrieve_all_by_search(self, search):
        query = session.query(All_ads).filter(All_ads.search == search).all()
        return query

    def retrive_if_link_exists_and_user_id(self, link, user_id, expire, price):
        try:
            query = session.query(All_ads).filter(
                and_(
                    All_ads.user_id == user_id,
                    All_ads.link == link
                )
            ).first()
            query.expire = expire
            query.price = price
            session.commit()
            return query
        except:
            return None

    def set_new_expire(self, link, id, expire):
        query = self.retrive_if_link_exists_and_user_id(link, id)
        query.expire = expire
        session.commit()

    def delete_ads_for_search(self, search, user_id):
        query = session.query(All_ads).filter(
            and_(
                All_ads.search == search,
                All_ads.user_id == user_id,
                All_ads.show == 1
            )
        )
        query.all()
        for ad in query:
            session.delete(ad)
            session.commit()

    def update_ad_save_remove(self, id, store):
        '''
        This should set the add to preview or not preview to the customer by updating show field to 0 for don't show and 2 for show ad
        :param id: Ad ID
        :param store: 0 > Not interested | 2 > Interested in ad
        :return: None
        '''
        query = session.query(All_ads).filter(All_ads.id == id).first()
        query.show = store
        session.commit()

    def return_saved_passed(self, search, user_id, show):
        query = session.query(All_ads).filter(
            and_(
                All_ads.search == search,
                All_ads.user_id == user_id,
                All_ads.show == show
            )
        )
        data = query.all()
        return data

    def first_add_that_should_be_seen(self, search, user_id):
        query = session.query(All_ads).filter(
            and_(
                All_ads.search == search,
                All_ads.user_id == user_id,
                All_ads.show == 1
            )
        ).order_by(All_ads.updated_at.desc()).first()
        return query

class User_query:
    def return_user_id_by_username(self, username):
        query = session.query(User).filter(User.username == username).first()
        return query.id
