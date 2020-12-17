'''
file = open("text" , "r")
linije = file.readlines()
for test in linije:
    test = test.strip("\n")
    test = test.replace("<br>string<br>", " string ")
    test = test.replace("<br>datetime<br>", " datetime ")
    test = test.replace("<br>integer<br>", " integer ")
    test = test.replace("<br>list of objects<br>", " list of objects ")
    test = test.replace("required", "_required_ ")
    test = test.replace("optional", "_optional_ ")
    test = test.replace("|", "<br>")
    test = test + "|"
    # print(test)

file = open("text1" , "r")
linije = file.readlines()
for test in linije:
    test = test.strip("\n")
    test = test.replace("|", "<br>")
    test = test + "|"
    print(test)
# print(test)
'''

import json

with open("text", 'r') as file:
    t = json.loads(file.read())
    list1 = []
    for l_i in t['charge']['line_items']:
        # print(l_i['subscription_id'])
        list1.append(l_i['title'])


with open("text1", 'r') as file:
    t = json.loads(file.read())
    list2 = []
    for l_i in t['charge']['line_items']:
        # print(l_i['subscription_id'])
        list2.append(str(l_i['title']))


if list1 == list2:
    print(True)

print(list1)
print(list2)
list3 = list2 + list1
print(len(set(list3)))



#
# print(len(list1))
# print(len(set(list1)))
# print(len(list2))
# print(len(set(list2)))
# list3 = list1 + list2
# print(len(list3))
#
# tr = set(list3)
# print(len(tr))