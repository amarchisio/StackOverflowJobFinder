# Tests for job_finder.py
# Using pytest

import job_finder
import pytest
from bs4 import BeautifulSoup

# test if querying a url returns something
def test_query_api():
    assert job_finder.query_api(
        'https://stackoverflow.com/jobs/feed?l=Boston%2c+MA%2c+United+States&u=Miles&d=50') is not None


# test if soup can be created from dummy data
def test_create_soup():
    raw_rssfeed = "<title>test job</title><link>test url</link>"
    assert job_finder.create_soup(raw_rssfeed) is not None


# test if soup parsing works
def test_parse_soup():
    raw_rssfeed = "<title>test job</title><link>test url</link><title>test job</title><link>test url</link>"
    formatted_rssfeed = BeautifulSoup(raw_rssfeed, features="xml")
    titles = job_finder.parse_soup(formatted_rssfeed)

#test if geopy is working
def test_find_coords():
    test_city = "Boston, MA"
    lon, lat = job_finder.find_coords(test_city)
    assert lat == 42.3604823
    assert lon == -71.0595678

#test regex_search
def test_regex_search():
    test_title = "this is a job title used for testing purposes (Plymouth, MA)"
    assert job_finder.regex_search(test_title) == ['Plymouth, MA']
