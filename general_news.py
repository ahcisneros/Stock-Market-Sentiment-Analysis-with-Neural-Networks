import os
from calendar import monthrange
from datetime import date
import pandas as pd
from newsapi import NewsApiClient


def main():
    """begin iterating at any day through a months worth of data"""
    company = ["amazon", "boeing", "apple", "netflix", "tesla", "facebook", "microsoft", "google", "alphabet"]
    current_month = int(str(date.today()).split("-")[1].strip(""))
    current_date = int(str(date.today()).split("-")[2].strip(""))
    list_months = [current_month, current_month - 1]
    for term in company:
        print(f"analyzing {term}")
        for month in list_months:
            left_over_dates = int(str(monthrange(2020, month)).split(", ")[1].replace(")", "")) - current_date
            if month == current_month:
                first_month_dates_list = dates_filter(list(range(current_date)))
                if len(str(month)) == 1:
                    month = "0" + str(month)
                for day in first_month_dates_list:
                    headline_extraction(day, month, term)
            elif left_over_dates != 0:
                num_dates = int(str(monthrange(2020, month)).split(", ")[1].replace(")", ""))
                second_month_date_list = dates_filter(list(range(num_dates))[::-1][:left_over_dates])
                if len(str(month)) == 1:
                    month = "0" + str(month)
                for day in second_month_date_list:
                    headline_extraction(day, month, term)



def headline_extraction(day, month, term):
    """iterates through an entire months worth of dates and extracts the articles containing
     specified keywords for each given day"""
    """6876de1e74b64e4e862fc0b7943133be"""
    """1f66071454d94bf49a229003cc0a66d0"""
    """b87aacedc4db4880b592647e573fffd3"""
    num_articles = 100

    start = f"2020-{month}-{day}"
    end = f"2020-{month}-{day}"
    try:
        news = NewsApiClient(api_key="b87aacedc4db4880b592647e573fffd3")
        data = news.get_everything(q=term, sources=news_sites(), from_param=start,
                                   to=end, language="en", page_size=num_articles, sort_by='relevancy')

        print(f"Analyzing month {month} / day {day}: Found " + str(data["totalResults"]))
        news_df = df_setup(data)
        save_df(news_df, term)
    except:
        try:
            news = NewsApiClient(api_key="1f66071454d94bf49a229003cc0a66d0")
            data = news.get_everything(q=term, sources=news_sites(), from_param=start,
                                       to=end, language="en", page_size=num_articles, sort_by='relevancy')

            print(f"Analyzing month {month} / day {day}: Found " + str(data["totalResults"]))
            news_df = df_setup(data)
            save_df(news_df, term)
        except:
            try:
                news = NewsApiClient(api_key="6876de1e74b64e4e862fc0b7943133be")
                data = news.get_everything(q=term, sources=news_sites(), from_param=start,
                                           to=end, language="en", page_size=num_articles, sort_by='relevancy')

                print(f"Analyzing month {month} / day {day}: Found " + str(data["totalResults"]))
                news_df = df_setup(data)
                save_df(news_df, term)
            except:
                print(f"skipped {start}/{end}")


def news_sites():
    """list of news sites that are being data-scraped"""
    news_site = "bloomberg,business-insider,financial-post," \
                "fortune,the-washington-post,time," \
                "the-washington-times,the-wall-street-journal," \
                "the-huffington-post,reuters,google-news,bbc-news," \
                "nbc-news,associated-press,axios,cbs-news,cnn" \
                "crypto-coins-news,msnbc,nbc-news,usa-today"

    return news_site


def df_setup(data):
    """sets up the json file derived from the news_api into a df that will
    be used for sentiment analysis"""
    articles = data["articles"]
    df = pd.DataFrame(articles)
    news_headline_df = pd.concat([pd.DataFrame({"media_source": get_sources(articles),
                                                "date": get_dates(df)}), df], axis=1)
    news_headline_df.drop(["author", "urlToImage", "content", "source", "publishedAt", "description"],
                          axis=1, inplace=True)

    return news_headline_df


def get_dates(df):
    """"get the core data from the json file"""
    list_dates = []
    for row in df["publishedAt"]:
        timestamp = row.split("T")[0]
        list_dates.append(timestamp)
    return list_dates


def get_sources(article):
    """gets the core source name from the json file """
    list_source = []
    for x, y in enumerate(article):
        source = list(y["source"].values())[1]
        list_source.append(source)
    return list_source


def dates_filter(list_of_dates):
    """"dates are added a zero if number of elements in the string is one"""
    for index, day in enumerate(list_of_dates):
        day += 1
        if len(str(day)) == 1:
            day = "0" + str(day)
        else:
            day = str(day)
        list_of_dates[index] = day

    return list_of_dates


def save_df(news_df, company_name):
    """checks to see if an existing csv file exists if it does it'll update it with the new
    articles and if it does not it will create a new csv file for the company"""
    if os.path.exists(r'E:\News Data\headlines {}.csv'.format(company_name)):
        existing_df = pd.read_csv(r'E:\News Data\headlines {}.csv'.format(company_name))
        updated_df = existing_df.append(news_df, ignore_index=True)
        no_duplicated_df = updated_df.drop_duplicates('title', keep='last')
        no_duplicated_df.to_csv(r'E:\News Data\headlines {}.csv'.format(company_name), mode='w', index=False)
    else:
        news_df.to_csv(r'E:\News Data\headlines {}.csv'.format(company_name), index=False)


main()
