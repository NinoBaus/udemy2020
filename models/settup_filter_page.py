from models.tablecreator import TableAds
from models.package import Pack

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
            print(self.current_id)
            print(ad.id)
            yield ad.name, ad.price, ad.link, ad.expire, ad.picture, ad.search, ad.id