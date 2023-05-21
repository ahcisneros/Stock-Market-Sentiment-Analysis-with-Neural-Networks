import nltk
from newspaper import Article
from bs4 import BeautifulSoup as soups
import requests
from newspaper import Config
import datetime
import numpy as np
import time
import pandas as pd
import os
import itertools

# research

company_list =  ["amazon", "berkshire hathaway", "alphabet", "exxon mobil", "walt disney", "tesla", "exxon mobil"]
counter_loops = 0

# "facebook", "goldman sachs", "gazprom", "apple", "alibaba", "boeing", "bitcoin",

while counter_loops <= 2:
    for companies in itertools.cycle(company_list):

        time_1 = datetime.datetime.today()

        company = companies
        base_url = "https://www.google.com/search?q={0}&source=lnms&tbm=nws&num=100".format(company)
        print("Analyzing {}".format(company))

        def next_page_url(url): 
            response = requests.get(url)
            soup = soups(response.text, "html.parser")
            url_exists = soup.find("a", {"aria-label": "Next page"})

            random_times = np.random.randint(10, 50, size=10)
            sec = np.random.choice(random_times, size=1, replace=False)
            sec = int(sec)

            if url_exists != None:
                partial_url = url_exists.get("href")
                next_page = "https://www.google.com" + str(partial_url)

                print("Waiting: " + str(sec) + " secs")
                time.sleep(sec)

                return [url] + next_page_url(next_page)
            else:
                print("First Section Complete:")
        
                return [url]

        def get_urls(urls):
            complete_list = []  
            counter = 0

            for data in urls:
                random_times = np.random.randint(10, 50, size=10)
                sec = np.random.choice(random_times, size=1, replace=False)
                sec = int(sec)

                print("Waiting: " + str(sec) + " secs for next page")
                time.sleep(sec)

                response = requests.get(data)
                soup = soups(response.text, "html.parser")  
                articles = soup.findAll("div", {"class": "kCrYT"})  

                for html in articles:  
                    try:
                        article_links = html.a
                        unusable_url = article_links.get("href").strip("/url?q=")
                        usable_url = unusable_url.split("&sa")[0]
                        complete_list.append(usable_url)
                    except:
                        counter += 1

                        continue

            complete_list = list(set(complete_list))
            print("Completed Section 3:" + "\n" + "total gathered urls: " + str(len(complete_list)) + "\n" + "skipped urls: " + str(counter))

            return complete_list

        def articles(urls):
            counter = 0
            list_of_dictionaries = []

            for f in urls:
                try:
                    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
                    config = Config()
                    config.browser_user_agent = user_agent
                    article = Article(f, config=config)
                    article.download()
                    article.parse()
                    nltk.download('punkt')
                    article.nlp

                    data_dict = {
                        "title": "{}".format(article.title),
                        "authors": "{}".format(article.authors),
                        "url": "{}".format(article.url),
                        "date": "{}".format(article.publish_date),
                        "text": "{}".format(article.text)
                    }

                    list_of_dictionaries.append(data_dict)
                except:
                    with open(r"Documents/Data_Scraping/errors.txt", "a") as file:
                        file.write(article.url + ":" + str(datetime.datetime.today()) + "\n")

                    counter += 1

                    continue

            print("Completed Section 3:" + "\n" + "articles skipped: " + str(counter))

            return list_of_dictionaries

        def dataframe(data):
            columns = ["title", "authors", "url", "date", "text"]
            complete_data = pd.DataFrame(data, columns=columns)

            if os.path.exists(r'C:\Users\Alexis\Documents\Data_Scraping\data\{}.csv'.format(company)):
                dataframe_1 = pd.read_csv(r'C:\Users\Alexis\Documents\Data_Scraping\data\{}.csv'.format(company))
                dataframe_1 = dataframe_1.append(complete_data, ignore_index=True)
                data = dataframe_1.drop_duplicates('url', keep='last')
                print(data)
                data.to_csv(r'C:\Users\Alexis\Documents\Data_Scraping\data\{}.csv'.format(company), mode='w', index=False)
            else:
                complete_data.to_csv(r'C:\Users\Alexis\Documents\Data_Scraping\data\{}.csv'.format(company), index=False)
    
        page_urls = next_page_url(base_url)
        list_urls = get_urls(page_urls)
        data_frame_data = articles(list_urls)
        dataframe(data_frame_data)

        time_2 = datetime.datetime.today()
        time_3 = time_2 - time_1
        print("Time to complete: " + str(time_3))
        time.sleep(60)

        counter_loops += 2