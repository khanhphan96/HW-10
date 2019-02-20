import os
from bs4 import BeautifulSoup as bs
import requests
import urllib.request
from splinter import Browser
import time
import pandas as pd
import datetime
url = "https://mars.nasa.gov/news/"
request = requests.get(url, 'lxml')
soup = bs(response.text, 'html.parser')
news_title = soup.find('div', class_="content_title").find("a").text.strip('\t\r\n')
news_p = soup.find('div', class_="rollover_description").text.strip('\t\r\n')

print(news_title)
print(news_p)

url_image = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
request_image = requests.get(url_image)
soup_image = bs(request_image.text, "html.parser")
soup_2_image = soup_image.find_all('div', class_ = 'carousel_items')[0]
find_image = soup_2_image.find('article').attrs['style'].strip()
url = find_image.split("'")[1]
url

url_weather= "https://twitter.com/marswxreport?lang=en"
request_weather = requests.get(url_weather)
soup_weather = bs(response_weather.text, "html.parser")
weather = soup_weather.find_all('div', class_='js-tweet-text-container')
for html in weather:
    html_weather = html.text.strip()
    if html_weather.startswith('Sol'):
        weather = html_weather
        break

print(weather)

url_mars_facts = "http://space-facts.com/mars/"
request_mars_facts = requests.get(url_mars_facts)
soup_mars_facts = bs(response_mars_facts.text, "html.parser")
table = soup_mars_facts.find('table')
rows = table.findAll('tr')

for tr in rows:
    cols = tr.findAll('td')

headings = []
contents = []

for row in table.find_all('tr'):
    column_marker = 0
    columns = row.find_all('td')
    for column in columns:
        if column_marker == 0:
            output = column.get_text().strip()
            headings.append(output)

        else:
            output = column.get_text().strip()
            contents.append(output)

        column_marker += 1

df = pd.DataFrame(contents, headings)

d = {'col1': headings, 'col2': contents}
df = pd.DataFrame(data=contents, index=headings)
df_html_output = df.to_html(header=False)
df

url_hemispheres = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
request_hemisphere = requests.get(url_hemispheres)
soup_hemisphere = bs(request_hemisphere.text, "html.parser")
hemispheres = soup_hemisphere.find_all("img")


for alt in hemispheres:
    if alt['alt'].find('Hemi') != -1:
        print(alt['src'])
        print(alt['alt'])

url_hemispheres_images = []
hemispheres_images = soup_hemisphere.find_all("img")

for alt in hemispheres_images:
    if alt['alt'].find('Hemi') != -1:
        url_hemispheres_images.append({'title':alt['alt'],'img_url':alt['src']})
url_hemispheres_images

from flask import Flask, jsonify, render_template

app = Flask(__name__)



# Flask Routes


@app.route("/scrape")
def scrape():
    now = datetime.datetime.now()
    timestamp = datetime.datetime.strftime(now, '%Y-%m-%d %H:%M%p')


    import pymongo
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)
    db = client.marsDB

    output = {
        "timestamp": timestamp,
        "news_title": news_title,
        "news_p": news_p,
        "mars_weather": weather,
        "featured_image_url": url_hemispheres_images,
        "df_html_output": df_html_output
    }

    db.mars.remove()
    db.mars.insert_one({
        "timestamp": timestamp,
        "news_title": news_title,
        "news_p": news_p,
        "mars_weather": weather,
        "featured_image_url": url_hemispheres_images,
        "df_html_output": df_html_output
    })

    return jsonify(output)


@app.route('/')
def index():
    import pymongo
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)
    db = client.marsDB
    x = db.mars.find()
    news_title = x[0]["news_title"]
    news_p = x[0]["news_p"]
    timestamp = x[0]["timestamp"]
    weather = x[0]["weather"]
    url_hemispheres_images = x[0]["url_hemispheres_images"]
    df_html_output = x[0]["df_html_output"]

    context = {
        'news_title': news_title,
        'news_p': news_p,
        'timestamp': timestamp,
        'mars_weather': weather,
        'featured_image_url': url_hemispheres_images,
        'df_html_output': df_html_output
    }

    front_page = render_template('jinja.html', **context)

    return front_page





if __name__ == "__main__":
    app.run(debug=True)
    raise NotImplementedError()