from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests
from urllib.parse import urlparse
import time

def scrape():
    dict_mars = {}
    #Chromedriver
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    #NASA Mars News
    url_mars = 'https://mars.nasa.gov/news/'
    browser.visit(url_mars)
    #BeautifulSoup Parse News title
    html = browser.html
    soup_news = BeautifulSoup(html, 'html.parser')

    news_title = soup_news.find('div', class_='content_title').text
    news_p = soup_news.find('div', class_='article_teaser_body').text
    if len(news_p) != 0:
        news_p = soup_news.find('div', class_='article_teaser_body').text
    else:
        news_p = "empty news_p"

    dict_mars["news_title"] = news_title
    dict_mars["news_p"] = news_p

    #JPL Mars Space Images - Featured Image
    orig_url_jpl = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    parsed_uri = urlparse('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars' )
    url_jpl = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
    browser.visit(orig_url_jpl)

    time.sleep(3)
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(3)
    browser.find_by_css('a.fancybox-expand')
    time.sleep(3)

    html = browser.html
    soup_jpl = BeautifulSoup(html, 'html.parser')
    img = soup_jpl.find('img', class_='fancybox-image')['src']
    featured_image_url = url_jpl + img

    dict_mars["featured_image_url"] = featured_image_url

    #Mars Weather
    url_twitter = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_twitter)
    html = browser.html
    soup_twitter = BeautifulSoup(html, 'html.parser')

    tweeter = soup_twitter.find('ol', class_='stream-items')
    mars_weather = tweeter.find('p', class_="tweet-text").text
    dict_mars["mars_weather"] = mars_weather

    #Mars Facts
    url_mars_facts = "https://space-facts.com/mars/"
    browser.visit(url_mars_facts)
    html = browser.html
    soup_mars_facts = BeautifulSoup(html, 'html.parser')

    table_mars_facts = soup_mars_facts.find('table', class_='tablepress tablepress-id-mars')
    col1 = table_mars_facts.find_all('td', class_='column-1')
    col2 = table_mars_facts.find_all('td', class_='column-2')

    keys = []
    values = []

    for row in col1:
        keym = row.text.strip()
        keys.append(keym)
    
    for row in col2:
        value = row.text.strip()
        values.append(str(value))
    
    mars_facts = pd.DataFrame({
        "keym":keys,
        "Value":values
        })

    html_mars_facts = mars_facts.to_html(header=False, index=False)
    dict_mars["mars_facts"] = html_mars_facts

    #Mars Hemispheres
    url_hemispheres = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    parsed_uri_hemispheres = urlparse(url_hemispheres)
    url_hemispheres_p = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri_hemispheres)
    browser.visit(url_hemispheres)
    html = browser.html
    soup_hemispheres = BeautifulSoup(html, 'html.parser')

    #adding title and image in to dictinary and dictanary in to list
    hemisphere_image_urls = []
    all_itmes = soup_hemispheres.find_all("div", class_="item")

    for item in all_itmes:
        dict_img = {}
        title = item.find("h3").text
        link = item.find("div", class_="description").a["href"]
        full_link = url_hemispheres_p + link
        browser.visit(full_link)
        html = browser.html
        soup_img_hemispheres = BeautifulSoup(html, 'html.parser')
        url = soup_img_hemispheres.find("img", class_="wide-image")["src"]
        full_img_url = url_hemispheres_p+url
        
        dict_img["title"] = title
        dict_img["img_url"] = full_img_url
        
        hemisphere_image_urls.append(dict_img)
    dict_mars["hemisphere_image_urls"] = hemisphere_image_urls
    browser.quit()
    return dict_mars
