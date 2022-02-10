This repository contains the code for a web scraping engine that scrapes customer review data from Yelp. For a google colaboratory or local implementation the scraped data is stored in a csv file. For AWS cloud implementation the scraped data is stored in a dynamodb table.

Below is a guide to implement the scraping engine on google colaboratory, local computer or on the cloud using AWS.

# Google colaboratory implementation of Yelp scraper:

For a simple implementation of Yelp scraper visit the following
google colaboratory link:

https://colab.research.google.com/drive/1tg5S5zII2eMw9JRCbM1sZvTsalHciwCJ?usp=sharing


# Local desktop implementation of Yelp scraper:

The libraries needed to run the code are listed in the requirements.txt
file.

The following is a guide to install the necessary libraries and run the code in a virtual environemnt:

- Open a terminal application and clone this repository in your current directory using the following command:

$ git clone https://github.com/Erfangithub/Customer-Review-Scraper.git

Change directory into the downloaded (or cloned) folder Customer-Review-Scraper.

Alternatively you can download the zipfile of the repository, open the zipfile and change directory into the main folder: Customer-Review-Scraper-main

- create a virtual environement using the command:

$ virtualenv v-env

- activate the virtual environment:

$ source v-env/bin/activate

- upgrade pip to latest version:

$ pip install --upgrade pip

- install the packages using the command:

$ pip3 install -r requirements.txt

- set the scraping parameters in lambda_function.py and run the code:

$ python3 lambda_function.py


# AWS cloud implementation



