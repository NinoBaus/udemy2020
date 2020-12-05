
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
