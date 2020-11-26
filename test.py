from models.tablecreator import TableAds

t = TableAds().retrieve_all_ads("neispravno")


def my_itterator(glasanje):
    for item in glasanje:
        yield item.name, item.price, item.link


sve = my_itterator(t)

print(next(sve))
print(next(sve))
print(next(sve))
print(next(sve))
print(next(sve))
print(next(sve))
print(next(sve))
