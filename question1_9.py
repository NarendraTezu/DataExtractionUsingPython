import json
import operator
import re
from collections import Counter


def getJSON(file, day):
    with open(file, 'r+') as fp:
        for line in fp:
            day.append(json.loads(line))
    return day

today = [] 
yesterday = []
urlh_today = [] 
urlh_yesterday = []
categories_today = []
categories_yesterday = []
subcat_today = []
subcat_yesterday = []
subcategory = []
title = []
price = []
status_code = []
price_normalized_list_t = []
price_normalized_list_y = []

list_today = getJSON('./today.json', today)
list_yesterday = getJSON('./yesterday.json', yesterday)


for item_t in list_today:
    urlh_today.append(item_t['urlh'])
    categories_today.append(item_t['category'])
    subcat_today.append(item_t['subcategory'])
    subcategory.append(item_t['subcategory'])
    title.append(item_t['title'])
    if item_t['available_price'] != None:
        price.append(float(item_t['available_price']))
    status_code.append(item_t['http_status'])
    
for item_y in list_yesterday:
    urlh_yesterday.append(item_y['urlh'])
    categories_yesterday.append(item_y['category'])
    subcat_yesterday.append(item_y['subcategory'])
    subcategory.append(item_y['subcategory'])
    title.append(item_y['title'])
    if item_y['available_price'] != None:
        price.append(float(item_y['available_price']))
    status_code.append(item_y['http_status'])
    
        
        
# 1. Number of URLH which are overlapping (Common) in two files.
# In this question i am fatching the urlh from both file and olny printing the common urlh count
overlapped_urlh = list(set(urlh_today).intersection(urlh_yesterday))
print("1. Number of overlapped urlh: ", len(overlapped_urlh),"\n\n")





# 2. For all the URLH which are overlapping, calculate the price difference (wrt available_price) 
# if there is any between yesterday's and today's crawls (scraped data). 
#There might be duplicate URLHs in which case you can choose the first valid (with http_status 200) record.
# In this Question i am find all common urlh which is not faild in both file and calculating the price difference 


set_overlapped_urlh = set(overlapped_urlh)

print("2.For all the URLH which are overlapping,the price difference is :")

for item_t in list_today[0:10000]:
    if item_t['http_status'] == "200":
        for item_y in list_yesterday[0:10000]:
            if item_y['http_status'] == "200":
                if item_t['urlh'] == item_y['urlh'] and item_t['urlh'] in set_overlapped_urlh:
                    temp1 = item_t['available_price']
                    temp2 = item_y['available_price']
                    if temp1 != None and temp2 != None:
                        temp1 = float(temp1)  
                        temp2 = float(temp2)
                        if (type(temp1) == 'int' or type(temp1 == 'float')) and (type(temp2) == 'int' or type(temp2 == 'float')):
                            if temp1 != temp2:
                                print("     %.2f" %abs(temp1-temp2))                        
                                set_overlapped_urlh.remove(item_t['urlh'])
                    break


print("\n\n")

# 3. Number of Unique categories in both files.
# I was bit confuse in this question if unique means all category in combined file only once, below will ans

categories_unique = set(categories_today).union(set(categories_yesterday))
print("3. Number of unique categories in both files: ", len(categories_unique), "\n\n")



# 4.Display List of categories which is not overlapping (Common) from two given files.
# In this question i am find only those category which are not common in both file using set symmetric difference
print("4. List of categories which is not overlapping: ", list(set(categories_today).symmetric_difference(set(categories_yesterday))),"\n\n")




# 5. Generate the stats with count of urlh for all taxonomies (taxonomy is concatenation of category and subcategory separated by " > ") for today's file.
subcat_set = set(subcat_today).intersection(subcat_yesterday)
list_total = list_today + list_yesterday
subcat_total = subcat_today + subcat_yesterday
subcat_dict = Counter(subcat_total)
print("5. Generate the stats with count of urlh for all taxonomies.")
for item in list_total:
    if item['category'] in categories_unique and item['subcategory'] in subcat_set:
        print("     ",item['category'] + " > " + item['subcategory'] + ": " + str(subcat_dict[item['subcategory']]))
        subcat_set.remove(item['subcategory'])
print("\n\n")





# 6. Generate a new file where mrp is normalized. If there is a 0 or a non-float value or the key doesn't exist, make it "NA"
# In this Question i am finding the dictnory using regex i am finding where mrp is 0 or None then making NA
# And creating a new file and storng these new dict

print("6. Generate a new file where mrp is normalized.")
for item_t in list_today:
        try:
                if (item_t["mrp"] == "0") or (re.match("^\d+?\.\d+?$", item_t["mrp"]) is None) or (item_t["mrp"] == None):
                    item_t["mrp"] = "NA"
        except TypeError:
                item_t["mrp"] = "NA"
        price_normalized_list_t.append(item_t)

for item_y in list_yesterday:
        try:
                if (item_y["mrp"] == "0") or (re.match("^\d+?\.\d+?$", item_y["mrp"]) is None) or (item_y["mrp"] == None):
                        item_y["mrp"] = "NA"
        except TypeError:
                item_y["mrp"] = "NA"
        price_normalized_list_y.append(item_y)


with open("normalized_mrp_today.json", "w") as f:
    json.dump(price_normalized_list_t, f)
    

with open("normalized_mrp_yesterday.json", "w") as f:
    json.dump(price_normalized_list_y, f)
print("      Normilized file normalized_mrp_today.json and normalized_mrp_yesterday.json is genreted please find in current folder \n\n")




# 7. Display the title and price of 10 items having least price.
# In this question i am fatching title and price
# Making dictnory title as key and price as value
# Sorting the dictnory besed on ACSC order and printing first 10 value

dictionary = dict(zip(title, price))
result = dict(sorted(dictionary.items(), key=operator.itemgetter(1), reverse= False))
print("7. Display the title and price of 10 items having least price..")
for i, (k, v) in enumerate(result.items()):
    if i < 10:
        print("     ",k,"-->", v)
print("\n\n")



#8. Display the top 5 subcategories having the highest items.
# In this question i am fatching title and their subcatogry
# Making dictnory title as key because key could not be duplicate 
# uning collections Counter class counting the subcategory related to each title
# Sorting the counter obj besed on DESC order and printing top 5 value

dictionary = dict(zip(title, subcategory))
result = Counter(dictionary.values())
sort_dict = dict(sorted(result.items(), key=operator.itemgetter(1), reverse= True))
print("8. Display the top 5 subcategories having the highest items.")           
for i, (k, v) in enumerate(sort_dict.items()):
    if i < 5:
        print("     ",k,"-->", v)
print("\n\n")     




#9. Display stats of how many items have failed status (http_status other than 200 is to be considered as failure).
# In this question i am fatching the failed status code 
# And printing the status code and their count

print("9. Display stats of how many items have failed status")
fail_satus_code = []
for i in status_code:
    if i != "200":
        fail_satus_code.append(i)
temp = []
print("      http_status     count")
for i in fail_satus_code:
    if i not in temp:
        print("     ",i,"           ",fail_satus_code.count(i))
        temp.append(i)
