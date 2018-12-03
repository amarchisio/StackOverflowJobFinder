# Andrew Marchisio
# Program to extract job listings from Stack Overflow's Jobs RSS Feed
# Displays notifications on desktop to Windows 10 and Linux users

from bs4 import BeautifulSoup
import requests
import re
from geopy.geocoders import Nominatim
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import lxml

def main():
    print("\nThis program allows you to search for jobs using StackOverflow's Job Search RSS Feed.")

    custom_filter = input("Enter a custom filter (not case-sensitive): ")

    print("\nLooking up jobs within 50 miles of Bridgewater, MA...")

    # URL to query
    url = "https://stackoverflow.com/jobs/feed?l=Bridgewater%2C+MA%2C+United+States&u=Miles&d=50"

    # query the url and save the raw text
    raw_rssfeed = query_api(url)

    # format the raw rss feed from stack overflow with beautifulsoup
    formatted_rssfeed = create_soup(raw_rssfeed)

    # pull out jobs
    jobs = parse_soup(formatted_rssfeed)

    # filter the results
    stripped_titles = filter_results(custom_filter, jobs)
    print(stripped_titles)

    # only keep the city names. ex: Boston, MA
    cities = regex_search(stripped_titles)

    # count how many times each city is seen
    counts = count_each_city(cities)

    for key, value in counts.items():
        print(key)
        print(value)

    # find the coordinates of each city
    find_coords(counts)

    draw_map(counts, custom_filter)

    # notify user program is finished
    print("\nProgram complete!")


# send request to rss feed and parse the text
def query_api(url):
    # set rssfeed to raw output of rss feed
    rssfeed = requests.get(url)
    # verify the server gave an OK (200)
    if rssfeed.status_code == 200:
        # only keep the text from the request, ignore headers etc.
        rssfeed = rssfeed.text
        return rssfeed
    else:
        exit("Error contacting Stack Overflow RSS Feed.")


def create_soup(raw_rssfeed):
    # turn the raw text into soup that is ready for processing
    formatted_rssfeed = BeautifulSoup(raw_rssfeed, features="xml")
    # return the formatted soup
    return formatted_rssfeed


# parse the soup for relevant information
def parse_soup(formatted_rssfeed):
    # find all of the 'title text' <title> 'title text' </title>
    jobs = formatted_rssfeed.find_all('title')
    return jobs


def filter_results(custom_filter, jobs):
    job_count = 0

    # just the job title text, no tags
    stripped_titles = ""

    for i in range(2, len(jobs)):

        # get the current title
        current_title = jobs[i].get_text()

        # count jobs, print jobs, and save raw job title to string
        if custom_filter.lower() in current_title.lower():
            # print link and title to console in readable format
            print("\n", current_title, "\n", end='')
            stripped_titles += current_title
            job_count += 1

    print("\n", job_count, "jobs found with your filter!")
    return stripped_titles


def regex_search(stripped_titles):
    cities = (re.findall("\w[A-Za-z ]+, [A-Z]{2}", stripped_titles))
    for i in cities:
        print(i)
    return cities


def count_each_city(cities):
    counts = dict()
    for i in cities:
        counts[i] = counts.get(i, 0) + 1
        print(i)
        # find_coords(i)

    print(counts)
    return counts


def find_coords(city):
    geo_locator = Nominatim()
    location = geo_locator.geocode(city)
    try:
        print(location.latitude, location.longitude)
        lat = location.latitude
        lon = location.longitude
        return lon, lat

    except:
        print("invalid location")
        return 0, 0


def draw_map(counts_dict, custom_filter):
    # work on zoom/area to be rendered

    map = Basemap(resolution='h', llcrnrlon=-73.5, llcrnrlat=41.25, urcrnrlon=-68.5, urcrnrlat=43.25,
                  projection='merc', lon_0=-72)

    map.drawstates()
    map.drawcoastlines()
    map.drawcountries()
    map.fillcontinents(color='#3b5998')
    # map.drawmapboundary(fill_color='aqua')
    plt.title(custom_filter + " Jobs within 50 miles of Bridgewater, MA")

    print(counts_dict)
    for key, value in counts_dict.items():
        lon, lat = find_coords(key)
        x, y = map(lon, lat)
        point = key + ": " + str(value)
        plt.text(x + 3000, y, point, fontsize=10, fontweight='bold', ha='left', va='center', color='black')
        map.plot(x, y, 'ro', markersize=8)

    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())

    plt.show()


# start point
if __name__ == "__main__":
    main()
