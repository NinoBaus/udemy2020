from models.tablecreator import TableAds
from models.package import Pack
import time
from datetime import datetime
import re

class First_run:
    def __init__(self, search, user_id):
        self.search = search
        self.user_id = user_id
        self.current_id = user_id

    def valid_search(self):
        TableAds().delete_ads_for_search(search=self.search, user_id=self.user_id)
        self.storing_data = Pack(search=self.search, user_id=self.user_id).store_ads()
        if self.storing_data:
            return 201

    def iterate_ads(self):
        unshown_ads = TableAds().retrieve_ads_by_search_and_id(search=self.search, user_id=self.user_id)
        for ad in unshown_ads:
            self.current_id = ad.id
            yield ad.name, ad.price, ad.link, ad.expire, ad.picture, ad.search, ad.id


class Jeson_results:
    def __init__(self):
        pass

    def pack_json(self, db_results):
        table = []
        for row in db_results:
            if not row.expire_unix < int(time.time()):
                ads_dict = {}
                ads_dict["id"] = row.id
                ads_dict["name"] = row.name
                ads_dict["picture"] = row.picture
                ads_dict["price"] = row.price
                expire = str(datetime.fromtimestamp(row.expire_unix) - datetime.now())
                expire = expire.split(".")[0]
                if "day" in expire:
                    expire = int(re.sub("[^0-9]", "", expire.split(",")[0]))
                    expire = str(expire + 1) + " dana"
                ads_dict["expire"] = expire
                ads_dict["link"] = row.link
                ads_dict["search"] = row.search
                ads_dict["show"] = row.show
                ads_dict["created_at"] = row.created_at
                ads_dict["updated_at"] = row.updated_at
                ads_dict["user_id"] = row.user_id
                table.append(ads_dict)
            else:
                TableAds().update_ad_save_remove(row.id, 1)

        return table