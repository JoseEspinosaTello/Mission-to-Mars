#!/usr/bin/env python
# coding: utf-8


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager


def scrape_all():

    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    
    browser = Browser('chrome', **executable_path, headless=True)

    news_paragraph, news_title = mars_news(browser)

    print(news_title)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemisphere_image_urls": mars_hemi(browser)
    }

    # Stop webdriver and return data
    browser.quit()

    return data


def mars_news(browser):
    #assgin url and instruct browser to visit it
    # Visit the mars nasa news site
    #url = 'https://redplanetscience.com'
    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    #we're searching for elements with a specific combination of tag (div) and attribute (list_text).
    #As an example, ul.item_list would be found in HTML as <ul class="item_list">.




    #set up html parser

    html = browser.html
    news_soup = soup(html, 'html.parser')
    
    
    
    # Add try/except for error handling

    try:
        
        #assign the title and summary text to variables we'll reference later
        slide_elem = news_soup.select_one('div.list_text')
        
        #slide_elem.find('div', class_= 'content_title')



        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
        


        #Use the parent element to find the paragraph text
        news_paragraph = slide_elem.find('div', class_='article_teaser_body').get_text()
        
        # print(f'this is the paragraph: {news_paragraph}')
        # print(f'TITLE: {news_title}')
    except AttributeError:

        return None, None
    
    return news_paragraph, news_title



# ### Featured Images

def featured_image(browser):

    # Visit URL
    #url = 'https://spaceimages-mars.com'
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)



    # Find and click the full image button

    full_image_elem =browser.find_by_tag('button')[1]

    full_image_elem.click()



    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')


    try:

        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        
    except AttributeError:
        
        return None
       
    #img_url_rel




    # Use the base URL to create an absolute UR

    #img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
    print(f'this is the image {img_url}')
    return img_url




def mars_facts():

    # Add try/except for error handling
    try:    
        #By specifying an index of 0, we're telling Pandas to pull only the first table it encounters,
        #or the first item in the list. Then, it turns the table into a DataFrame.
        #df = pd.read_html('https://galaxyfacts-mars.com')[0]
        df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]


    except BaseException:
      return None

    #assign columns to the new DataFrame for additional clarity.
    df.columns=['description', 'Mars', 'Earth']

    #set the description as the index, inplace=true makes the change to current df
    df.set_index('description', inplace=True)



    # Convert dataframe into HTML format, add bootstrap
    #return df.to_html()
    return df.to_html(classes="table table-striped")

def mars_hemi(browser):

    
    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'

    browser.visit(url)




    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    #this needs to exist outside the loop because click action will search through this soup page
    html = browser.html
    hemi_soup = soup(html, 'html.parser')
    #print(hemi_soup)
   
    for link in range(4):

        try:

     
            browser.links.find_by_partial_text('Enhanced')[link].click()
            
            
            html = browser.html
            enh_soup = soup(html, 'html.parser')
            
            title = enh_soup.find('h2').text
            print(title)
            
            
            
            #Will return large picture Class = "wide-image"
            img_url_rel = enh_soup.find('img', class_="wide-image").get('src')
            print(img_url_rel)
            img_url = f'https://marshemispheres.com/{img_url_rel}'
            print(img_url)
            
            #Create dictionary and add values
            enhanced_title_img = {
                'img_url': img_url,
                'title': title
            }
            
            #append dict to list
            hemisphere_image_urls.append(enhanced_title_img)
            
            browser.back()

        except AttributeError:
        
            return None


    return hemisphere_image_urls




if __name__ == "__main__":
    
    # If running as script, print scraped data
    print(scrape_all())






