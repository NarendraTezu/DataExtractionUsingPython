# DataExtractionUsingPython
Filtering the data from files and find useful data. 

Redquried Software : Python 3.8.5
For Running The file : python3 question1_9.py
Output will be : on terminal and in current directory two json file 
	1. normalized_mrp_today.json  
	2 .normalized_mrp_yesterday.json



Given two JSON files (yesterday.json, today.json), write a small analytics program to perform the following:

1. Number of URLH which are overlapping (Common) in two files.

2. For all the URLH which are overlapping, calculate the price difference (wrt available_price) if there is any between yesterday's and today's crawls (scraped data). There might be duplicate URLHs in which case you can choose the first valid (with http_status 200) record.

3. Number of Unique categories in both files.

4. Display List of categories which is not overlapping (Common) from two given files.

5. Generate the stats with count of urlh for all taxonomies (taxonomy is concatenation of category and subcategory separated by " > ") for today's file.
Eg:
Cat1 > Subcat1: 3500
Cat1 > Subcat2: 2000
Cat2 > Subcat3: 8900

6. Generate a new file where mrp is normalized. If there is a 0 or a non-float value or the key doesn't exist, make it "NA".

7. Display the title and price of 10 items having least price.
Eg:
Title1 --> its price
Title2 --> its price
upto 10

8. Display the top 5 subcategories having the highest items.

9. Display stats of how many items have failed status (http_status other than 200 is to be considered as failure).
Eg.
http_status     count
500             23
404             12
