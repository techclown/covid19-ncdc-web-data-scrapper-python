from bs4 import BeautifulSoup # we will be using this to scrap a website
from datetime import datetime  # We will be using this to generate csv name from timestamp
import requests  # we will be using this to download a website data
import csv  # we will be using this to generate a csv file

# Set headers
headers = requests.utils.default_headers()
headers.update({'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'})

# Define and Access URL
url = "https://covid19.ncdc.gov.ng"  # this is the url of the website to be scrapped
req = requests.get(url, headers)  # the request library is used to get the website contents

site = BeautifulSoup(req.content, 'html.parser')  # now beautiful soup can read the request content and parse as html

table = site.find("table", id="custom3")  # now get the table element with id 'custom3'

# GET THE TABLE HEADERS AS AN ARRAY
head = table.find_all("th")  # inside the table extracted, find the 'th' which is the table header
heads = []
for v in head:
    heads.append(v.get_text(strip=True))

head_length = len(head)  # I want to know the length of the table header

# GET THE TABLE DATA
data = table.find_all("td")  # inside the table, find the 'th' which are the table data

data_length = len(data) - head_length  # I want to know the length of the table data excluding the footer

no_states = data_length / head_length  # The is the number of states reported

nigeria_data = []  # I will store the states as a dictionary here

# EXTRACT EACH STATE AS TUPLE AND STORE INSIDE A DICTIONARY
for i in range(1, data_length, head_length): # This loop splits the data into states segment base on header length
    state_name = data[i - 1].find('p').get_text(strip=True)
    state_cases = data[i].find('p').get_text(strip=True)
    state_active = data[i + 1].find('p').get_text(strip=True)
    state_discharged = data[i + 2].find('p').get_text(strip=True)
    state_death = data[i + 3].find('p').get_text(strip=True)
    state = {heads[0]: state_name, heads[1]: state_cases, heads[2]: state_active, heads[3]: state_discharged,
             heads[4]: state_death}

    nigeria_data.append(state)


# LET'S WRITE OUR DATA TO CSV

file_name = "{}{}{}{}{}{}{}{}{}".format('Aitechma_Nigeria_Covid_Report_Bot_', datetime.now().year, datetime.now().month,
             datetime.now().day, datetime.now().hour, datetime.now().minute, datetime.now().second,
             datetime.now().microsecond, '.csv')  # We will define how to name the file. Decided to use timestamp

with open(file_name, 'w') as file_data:  # We will open the file_name and write 'w' data
    converter = csv.DictWriter(file_data, fieldnames=heads)  # We will define the header;;; remember variable heads
    converter.writeheader()  # So write the header now

    for data in nigeria_data:  # loop through all the tuple in the dictionary we created
        converter.writerow(data)  # write their data inside the file create in line 50

    print('Your Nigeria covid report has been generated inside {}'.format(file_name))
    # Print something for your user to see.


