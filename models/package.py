import requests as req
from bs4 import BeautifulSoup as Soup
from models.tablecreator import TableAds
from threading import Thread
import time
import re

class Pack:
    def __init__(self, user_id, search=""):
        self.user_id = user_id
        self.search = search.replace("_", " ")
        self.table_name = search
        self.url_auction = f"https://www.limundo.com/pretragaLimundo.php?bSearchBox=1&txtPretraga={self.search}&Submit=&sSort=vreme&sSmer=ASC&tipCena=2&iStr="
        #check if search already exists
        self.get_search = TableAds().retrieve_search(self.search)

    def store_ads(self):
        # check if search is valid
        if self.check_if_search_is_valid():
            # store pages number in pagination variable
            pagination = self.pagination(self.url_auction)
            # if there is only 1 page, run code only for that page
            if pagination == 0:
                self.return_ads(self.user_id, self.url_auction)
                return 201
            else:
                self.return_ads(self.user_id, self.url_auction)
                pages = self.pagination(self.url_auction)
                pagination_thread = Thread(target=self.iterate_pages, args=(pages,))
                pagination_thread.start()
                return 201
        # If search isn't valid return None
        else:
            return None

    def iterate_pages(self, page_number):
        # iterate through pages
        # import time
        # time.sleep(5)
        for i in range(page_number):
            if i == 0 or i == 1:
                pass
            else:
                url = self.url_auction + str(i)
                self.return_ads(self.user_id, url)

    def return_ads(self, user_id, url):
        '''
        Storring data in db.
        :param user_id and page url:
        :return: Currently nothing.
        :TODO: Make this callable so it is more readable and it would be used only to get ads from the page
        '''
        response = req.get(url)
        soup_prepare = Soup(response.text , "html.parser")
        i = 0
        for ads in soup_prepare.find_all(class_="auction_list_item auction_item"):
            i +=1

            #AD_NAME
            ad_name_finder = ads.find_all("a")
            ad_name_list = ad_name_finder[1].text.strip("\n").split("  ")
            ad_name_prepare = []
            for list in ad_name_list:
                if list == "":
                    pass
                else:
                    ad_name_prepare.append(list)
            ad_name = "".join(ad_name_prepare)

            #AD_PRICE
            '''TO DO (RESOLVE ISSUE WITH DOT IN THE PRICE)'''
            ad_price_finder = ads.find(class_="list_item_cena")
            ad_price_clear = ad_price_finder.text.strip("\n").split("  ")
            ad_price_list = []
            for item in ad_price_clear:
                item_list = []
                try:
                    if "." in item:
                        for n in item:
                            if n == ".":
                                pass
                            else:
                                item_list.append(n)

                        item_with_dot = "".join(item_list)
                        item_with_dot = int(item_with_dot)
                        ad_price_list.append(item_with_dot)
                    item = int(item)
                    ad_price_list.append(item)
                except:
                    pass
            ad_price = ad_price_list[0]

            #AD_PICTURE
            ad_picture_finder = ads.find("img")
            ad_picture_clear = str(ad_picture_finder).split('src="//static.limundoslike.com/')
            ad_picture = "https://www.limundo.com/" + ad_picture_clear[1].strip("\"/>")

            #AD_EPIRE_TIME
            ad_expire_finder = ads.find(class_="lista_time")
            ad_expire = ad_expire_finder.text.strip("\n")

            #AD_EXPIRE_UNIX_TIME
            current_unix_date = int(time.time())
            if "sek" in ad_expire:
                ad_expire_unix = int(re.sub("[^0-9]", "", ad_expire))
            elif "min" in ad_expire:
                minut = int(re.sub("[^0-9]", "", ad_expire))
                ad_expire_unix = minut * 60
            elif "sat" in ad_expire:
                sat = int(re.sub("[^0-9]", "", ad_expire))
                ad_expire_unix = sat * 3600
            elif "dan" in ad_expire:
                dan = int(re.sub("[^0-9]", "", ad_expire))
                ad_expire_unix = dan * 86400

            ad_expire_unix_time = ad_expire_unix + current_unix_date

            #AD_LINK
            ad_link_finder = ads.find("a", href=True)
            ad_link = ad_link_finder["href"]
            #CHECK IF LINK EXISTS FOR USER_ID
            if self.get_search:
                if not TableAds().retrive_if_link_exists_and_user_id(link=ad_link, user_id=self.user_id, expire=ad_expire, price=ad_price):
                    TableAds().create_all_ads(name=ad_name, price=ad_price, picture=ad_picture, expire=ad_expire, link=ad_link, search=self.search, user_id=user_id, expire_unix=ad_expire_unix_time)
            else:
                TableAds().create_all_ads(name=ad_name, price=ad_price, picture=ad_picture, expire=ad_expire, expire_unix=ad_expire_unix_time,
                                          link=ad_link, search=self.search, user_id=user_id)

            response.close()

    def pagination(self, url):
        response_pagination = req.get(url)
        soup_prepare = Soup(response_pagination.text, "html.parser")
        pagination_check = soup_prepare.find(class_="pagination_nav")
        pages_number = []
        if "style" in str(pagination_check):
            return 0
        else:
            for pages in pagination_check.text.split(" "):
                try:
                    pages = int(pages)
                    pages_number.append(pages)
                except:
                    pass

            return pages_number[-1]

    def check_if_search_is_valid(self):
        response = req.get(self.url_auction)
        soup_prepare = Soup(response.text, "html.parser")
        if not "Trenutno nema aukcije" in soup_prepare.text:
            return True