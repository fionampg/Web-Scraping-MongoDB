# ## MongoDB  and Flask Application
# Use MongoDB with Flask templating to create a new HTML page that display all the of the information that was scraped 
# from URLs in the Jupyter notebook
# * Start by converting your Jupyter notebook into a Python script called scrape_mars.py with a function called scrape that will 
# execute all of your scraping code from above and return one Python dictionary containing all of the scraped data.

# * Next, create a route called /scrape that will import your scrape_mars.py script and call your scrape function.

# * Store the return value in Mongo as a Python dictionary.

# * Create a root route / that will query your Mongo database and pass the mars data into an HTML template to display the data.
# * Create a template HTML file called index.html that will take the mars data dictionary and display all of the data in 
# the appropriate HTML elements. Use the following as a guide for what the final product should look like, 
# but feel free to create your own design


# Import modules
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd 
import requests

# Inititialize browser

def init_browser():
    # Mac users 
    # -- don't forget to change the path of the chromedriver.exe
    # executable_path = {'executable_path': '/usr/local/bin/chromedriver.exe'}
    # return Browser('chrome', **executable_path, headless = False)

    # windows Users
    # -- don't foget to change the path of the chromedrive.exe
    #Choose the executable path to driver
    executable_path = {'executable_path':'chromedriver.exe'}
    return Browser('chrome',**executable_path, headless = True)

# Create dictionary for gathered data to import into MongoDB
dict_mars_info = {}

# Scrape NASA Mars News
def scrape_mars_news():
    try:
        # Initialize browser
        browser = init_browser()

        # Access NASA Mars News site's URL through splinter
        url = 'https://mars.nasa.gov/news/'
        browser.visit(url)

        # HTML object
        html = browser.html

        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        # Retrieve the latest element that contains news title and news paragraph
        newstitle = soup.find('div', class_='content_title').find('a').text
        newsparag = soup.find('div', class_='article_teaser_body').text

        # Insert results to dictionary
        dict_mars_info['news_title'] = newstitle
        dict_mars_info['news_parag'] = newsparag

        return dict_mars_info

    finally: 
        browser.quit()

# Scrape Featured Image
def scrape_mars_feat_image():
    try:
        # Initialize browser
        browser = init_browser()

        # Access NASA Mars Space images' URL through splinter
        url_featd_image = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(url_featd_image)

        # HTML object
        html_img = browser.html

        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(html_img, 'html.parser')

        # Retrieve the url background image from style tag
        feat_image_url = soup.find('article')['style'].replace('background-image: url(','').replace(');','')[1:-1]

        # Website url
        mainurl = 'https://www.jpl.nasa.gov'

        # Add url of scrapped route to website url
        featured_image_url = mainurl + feat_image_url

        # Display the complete link to featured image
        featured_image_url    

        # Add link to dictionary
        dict_mars_info['url_featured_img'] = featured_image_url

        return dict_mars_info
    
    finally:
        browser.quit()

# Scrape Mars Weather
def scrape_mars_weather():

    try:
        # Initialize browser
        browser = init_browser()

        # Access Mars Weather twitter account's URL through splinter
        weather_url = 'https://twitter.com/marswxreport?lang=en'
        browser.visit(weather_url)

        # HTML object
        html_weather = browser.html

        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(html_weather,'html.parser')

        # Find the elements that contain tweets
        tweets = soup.find_all('div', class_='js-tweet-text-container')

        # Get elements that contain news title 
        # Search entries that shows weather related posts to exclude non-weather tweets
        for tweet in tweets:
            mars_weather = tweet.find('p').text
            if 'Sol' and 'pressure' in mars_weather:
                print(mars_weather)
                break
            else:
                pass

        # Add twitter content into dictionary
        dict_mars_info['mars_weather'] = mars_weather

        return dict_mars_info

    finally:
        browser.quit()

# Scrape Mars Facts
def scrape_mars_facts():
    # Visit the Mars Facts URL
    facts_url = 'https://space-facts.com/mars/'

    # Use Pandas' "read_html" to parse the URL
    facts_mars = pd.read_html(facts_url)

    # Find the Mars Facts dataframe in the list of dataframes and assign variable mars_df
    mars_df = facts_mars[0]

    # Set columns: 'description' and 'value'
    mars_df.columns = ['Description', 'Value']

    # Set index to 'Description' column, with no row indexing
    mars_df.set_index('Description', inplace = True)

    # Save HTML code to folder 
    marsdata = mars_df.to_html()

    # Add HTML code for dataframe to dictionary
    dict_mars_info['marsdata'] = marsdata

    return dict_mars_info

# Scrape Mars Hemispheres
def scrape_mars_hemisphere():

    try: 
        # Initialize browser
        browser = init_browser()

        # Access Mars Weather twitter account's URL through splinter
        hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(hemisphere_url)

        # HTML object
        html_hemispheres = browser.html

        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(html_hemispheres, 'html.parser')

        # Retrieve all items with Mars hemisphere info
        items = soup.find_all('div',class_='item')

        # Create empty list for hemisphere URLs
        list_hemisphere_img_url = []

        # Store main URL
        hemisphere_mainurl = 'https://astrogeology.usgs.gov/'

        # For loop for items found and stored through BeautifulSoup
        for x in items:
            # get title
            title = x.find('h3').text
            
            # get link to full image website
            partial_imgurl = x.find('a',class_='itemLink product-item')['href']
            
            # Navigate to link that contains the full image website
            browser.visit(hemisphere_mainurl + partial_imgurl)
            
            # HTML object of individual hemisphere info website
            partial_imghtml = browser.html
            
            # Parse HTML with BeautifulSoup for each hemisphere info website
            soup = BeautifulSoup(partial_imghtml, 'html.parser')
            
            # Retrieve source of full image 
            imgurl = hemisphere_mainurl + soup.find('img',class_='wide-image')['src']
            
            # Append the retrieved data to a list of dictrionary
            list_hemisphere_img_url.append({"title":title,"img_url":imgurl})
            
        # Add list of urls of the images of the hemisphere to dictionary
        dict_mars_info['hemisphere_img_url'] = list_hemisphere_img_url

        return dict_mars_info
    
    finally: 
        browser.quit()