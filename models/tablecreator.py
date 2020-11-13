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
        All_ads().query.filter_by(search=search).all()
        return 201

    def update_ad_by_id(self, search, id):
        query = All_ads().query.filter_by(search=search, id=id).first()
        query.show = False
        session.commit()

    def retrieve_first_item(self, search, id):
        query = session.query(All_ads).filter(
            and_(All_ads.search==search,
                 All_ads.id==id)).first()
        return query

    def retrieve_search(self, search):
        query = session.query(All_ads).filter(All_ads.search == search).first()
        return query

    def retrive_if_link_exists_and_user_id(self, link, id):
        query = session.query(All_ads).filter(
            and_(
                All_ads.user_id == id,
                All_ads.link == link
            )
        ).first()
        return query

    def set_new_expire(self, link, id, expire):
        query = self.retrive_if_link_exists_and_user_id(link, id)
        query.expire = expire
        session.commit()

class User_query:
    def return_user_id_by_username(self, username):
        query = session.query(User).filter(User.username == username).first()
        return query.id



class TableCreator:
    def __init__(self, name):
        self.name = name

    def search_values(self, user):
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()

        create_table_if_not_exist = "CREATE TABLE IF NOT EXISTS search_terms (user text, value text)"
        cursor.execute(create_table_if_not_exist)

        store_search_value = "INSERT INTO search_terms VALUES (?,?)"
        cursor.execute(store_search_value, (user, self.name))

        connection.commit()
        connection.close()

    def create_table(self):
        """
        Creating table with customers search value
        DONE
        """
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()

        create_table = f"CREATE TABLE IF NOT EXISTS {self.name} (id INTEGER PRIMARY KEY, name text, price int, picture text, expire text, link text, show true)"

        cursor.execute(create_table)

        connection.close()
    def post_items(self, *args):
        """
        DONE
        Posting items from serach in db
        1. ID           Unique identifier
        2. Name         Ad name String
        3. Price        Price intiger
        4. Picture      Picture link String
        5. Expires      Expires at String
        6. Show         Would customer like to see it or not 1 / 0
        7. Created_at   creating time
        8. Updated_at   updating time
        """
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        self.create_table()

        post_items_in_db = f"INSERT INTO {self.name} VALUES (NULL, ?, ?, ?, ?, ?, true)"
        cursor.execute(post_items_in_db, *args)

        connection.commit()
        connection.close()
    def retrieve_items(self):
        try:
            connection = sqlite3.connect("database.db")
            cursor = connection.cursor()

            get_items = f"SELECT * FROM {self.name}"
            all_items = cursor.execute(get_items).fetchall()
            connection.close()
            return all_items
        except Exception as e:
            if "no such table" in str(e):
                return None
    def return_item(self, *args):
        try:
            connection = sqlite3.connect("database.db")
            cursor = connection.cursor()
            id = args[0]["id"]
            put = f"UPDATE {self.name} SET show=? where id=?"
            item = cursor.execute(put,(args[0]["show"], args[0]["id"])).fetchall()
            connection.commit()
            retrieve_updated_item = f"SELECT * FROM {self.name} where id=?"
            item_updated = cursor.execute(retrieve_updated_item, (id,)).fetchall()
            connection.close()
            return item_updated
        except Exception as e:
            if "no such table" in str(e):
                return None
    def get_first_item(self, id):
        try:
            connection = sqlite3.connect("database.db")
            cursor = connection.cursor()
            get = f"SELECT * FROM {self.name} WHERE ID={id} AND show=True"
            retrieve_first_item = cursor.execute(get).fetchall()
            connection.close()
            return retrieve_first_item
        except Exception as e:
            print(str(e) + " ovde puca")