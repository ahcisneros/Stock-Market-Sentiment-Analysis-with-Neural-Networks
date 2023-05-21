import GetOldTweets3 as got
import datetime as dt
import pandas as pd
import os
from datetime import date
from calendar import monthrange
import numpy as np
from datetime import datetime
import time


def main():
    """pip install GetOldTweets3"""
    list_years = [2020, 2019, 2018, 2017, 2016] """change the number of years it will trace back"""
    companies = ["amazon", "apple", "netflix", "facebook", "microsoft", "google", "alphabet", "boeing"] """input within the list the terms to be analyzed"""
    initiate(list_years, companies)


def initiate(list_years, companies):
    """iterates per 1 day of each month of each year and calls the twitter scraping function"""
    base_df = pd.DataFrame()
    for term in companies:
        print(f"Analyzing term: {term} \n")
        for year in list_years:
            if year == 2020:
                current_month = int(str(date.today()).split("-")[1].strip("0"))
                numerical_months = list(range(current_month + 1))
                del numerical_months[0]
            else:
                numerical_months = list(range(13))
                del numerical_months[0]
            for month in numerical_months:
                if year == 2020:
                    if int(month) == int(str(date.today()).split("-")[1].strip("0")):
                        num_days = int(str(datetime.date(datetime.now())).split("-")[2])
                        print(num_days)
                    else:
                        num_days = int(str(monthrange(year, month)).split(", ")[1].replace(")", ""))
                else:
                    num_days = int(str(monthrange(year, month)).split(", ")[1].replace(")", ""))
                print(f"Current Year: {year} / Month: {month}")
                lst = list(range(num_days + 1))
                del lst[0]
                lst.append(num_days - 1)
                lst = list(set(np.sort(lst)))
                for day in lst:
                    if int(day) == num_days:
                        if int(month) + 1 == 13:
                            df = twitter_scraping_v3(int(day), int(1), int(month), int(1), int(year),
                                                     int(year + 1), str(term))
                            base_df = pd.concat([df, base_df], ignore_index=True)
                        elif int(year) == 2020 and int(month) == int(str(date.today()).split("-")[1].strip("0")):
                            df = twitter_scraping(int(day), int(day + 1), int(year), int(month), str(term))
                            base_df = pd.concat([df, base_df], ignore_index=True)
                        else:
                            df = twitter_scraping_v2(int(day), int(1), int(year), int(month),
                                                     int(month + 1), str(term))
                            base_df = pd.concat([df, base_df], ignore_index=True)
                    else:
                        df = twitter_scraping(int(day), int(day + 1), int(year), int(month), str(term))
                        base_df = pd.concat([df, base_df], ignore_index=True)

                save_df(base_df, term)
                print(f"Saving complete for month {month}\n")


def twitter_scraping_v3(first_day, second_day, first_month, second_month,
                        first_year, second_year, term):
    """gets called per 2 sets of days for the start and end parameter of the
    twitter scraper function"""

    start = dt.date(first_year, first_month, first_day)
    end = dt.date(second_year, second_month, second_day)

    return framework_scrapper(start, end, term)


def twitter_scraping_v2(first_day, second_day, year, first_month, second_month, term):
    """gets called per 2 sets of days for the start and end parameter of the
    twitter scraper function"""

    start = dt.date(year, first_month, first_day)
    end = dt.date(year, second_month, second_day)

    return framework_scrapper(start, end, term)


def twitter_scraping(first_day, second_day, year, month, term):
    """gets called per 2 sets of days for the start and end parameter of the
    twitter scraper function"""
    start = dt.date(year, month, first_day)
    end = dt.date(year, month, second_day)

    return framework_scrapper(start, end, term)


def framework_scrapper(start, end, term):
    print(f"Start: {start} / End: {end} / Term: {term}")
    count = 1000

    try:
        df = core_scrapper(start, end, term, count)
    except:
        try:
            print("Waiting 10 min....")
            time.sleep(600)
            df = core_scrapper(start, end, term, count)

        except:
            try:
                print("Waiting 3 min more....")
                time.sleep(180)
                df = core_scrapper(start, end, term, count)
            except:
                try:
                    print("Waiting 10 min more....")
                    time.sleep(600)
                    df = core_scrapper(start, end, term, count)
                except:
                    pass

    print("Data extraction completed.")
    print(f"Total Tweets Collected: {len(df)} \n")

    return df


def core_scrapper(start, end, term, count):
    tweet_criteria = got.manager.TweetCriteria().setQuerySearch(term).setSince(str(start)).setUntil(str(end))
    tweet_criteria = tweet_criteria.setMaxTweets(count)
    tweets = got.manager.TweetManager.getTweets(tweet_criteria)
    df = pd.DataFrame(t.__dict__ for t in tweets)

    return df


def save_df(dataframe, term):
    """checks to see if an existing csv file exists if it does it'll update it with the new
        articles and if it does not it will create a new csv file for the company"""
    if os.path.exists(f"E:\\Tweet Data\\tweets {term}.csv"):
        existing_df = pd.read_csv(f"E:\\Tweet Data\\tweets {term}.csv")
        updated_df = existing_df.append(dataframe, ignore_index=True)
        no_duplicated_df = updated_df.drop_duplicates('text', keep='last')
        no_duplicated_df.to_csv(f"E:\\Tweet Data\\tweets {term}.csv", mode='w', index=False)
    else:
        dataframe = dataframe.reset_index()
        no_duplicated_df = dataframe.drop_duplicates('text', keep='last')
        no_duplicated_df.to_csv(f"E:\\Tweet Data\\tweets {term}.csv", index=False)


main()
