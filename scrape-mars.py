# imports
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import datetime as dt

# scrape all function 
def scrape_all():
    # Set up splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    news_title, news_body = scrape_news(browser)

    # build a dictionary with the information from the scrapes
    marsData = {
        "newsTitle": news_title,
        "newsParagraph": news_body,
        "featuredImage": scrape_image(browser),
        "facts": scrape_facts(browser),
        "hemispheres": scrape_hemispheres(browser),
        "lastUpdated": dt.datetime.now()
    }

    # stop web driver
    browser.quit()

    # display output
    return marsData

# scrape mars news
def scrape_news(browser):
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # convert to soup object
    html = browser.html
    news_soup = soup(html, 'html.parser')

    slide_elem = news_soup.select_one('div.list_text')

    # Grab the title and body paragraph
    news_title = slide_elem.find('div', class_='content_title').get_text()
    news_body = slide_elem.find('div', class_='article_teaser_body').get_text()

    # return the news title and paragraph
    return news_title, news_body

# scrape featured image page
def scrape_image(browser):
    #visit url
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # find and click the featured img button
    full_image_link = browser.find_by_tag('button')[1]
    full_image_link.click()

    # parse the html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # find relative image url
    img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    # get the absolute URL
    img_url_abs = f'https://spaceimages-mars.com/{img_url_rel}'

    # return the image url
    return img_url_abs

# scrape through facts page
def scrape_facts(browser):
    #visit url
    url = 'https://galaxyfacts-mars.com/'
    browser.visit(url)

    #parse the html with soup
    html = browser.html
    fact_soup = soup(html, 'html.parser')

    # find the facts location
    factsLocation = fact_soup.find('div', class_='diagram mt-4')
    
    # grab the html for the fact table
    factTable = factsLocation.find('table')

    # create empty string
    facts = ""

    # add the facts to the empty string
    facts += str(factTable)

    return facts

# scrape through hemispheres page
def scrape_hemispheres(browser):
    # visit url
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # Create a list to hold the images and titles
    hemisphere_img_urls = []

    # loop through the links, click each, find the sample anchor, return the href
    for i in range(4):
        hemisphereInfo = {}
    
        # find the elements on each loop
        browser.find_by_css('a.product-item img')[i].click()
    
        # Find the sample image anchor tag and extract the href
        sample = browser.links.find_by_text('Sample').first
        hemisphereInfo['img_url'] = sample['href']
    
        # Get the hemisphere title
        hemisphereInfo['title'] = browser.find_by_css('h2.title').text
    
        # Append the hemisphere title to list
        hemisphere_img_urls.append(hemisphereInfo)
    
        # Navigate back
        browser.back()

    return hemisphere_img_urls


# set up as a flask app
if __name__ == "__main__":
    print(scrape_all())