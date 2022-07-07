#!/usr/bin/env python
# coding: utf-8



# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd




executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)




#assgin url and instruct browser to visit it
# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)
#we're searching for elements with a specific combination of tag (div) and attribute (list_text).
#As an example, ul.item_list would be found in HTML as <ul class="item_list">.




#set up html parser

html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')




#assign the title and summary text to variables we'll reference later
slide_elem.find('div', class_= 'content_title')



# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title




#Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ## JPL Space Images Featured Image
# ### Featured Images



# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)



# Find and click the full image button

full_image_elem =browser.find_by_tag('button')[1]

full_image_elem.click()




# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup




# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel




# Use the base URL to create an absolute URL

img_url =f'https://spaceimages-mars.com/{img_url_rel}'

img_url


# ### Mars Facts



#By specifying an index of 0, we're telling Pandas to pull only the first table it encounters,
#or the first item in the list. Then, it turns the table into a DataFrame.
df = pd.read_html('https://galaxyfacts-mars.com')[0]

df.head()



#assign columns to the new DataFrame for additional clarity.
df.columns=['description', 'Mars', 'Earth']

#set the description as the index, inplace=true makes the change to current df
df.set_index('description', inplace=True)
df



df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles


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

    #find title
    #This wont work because it will only pull first title from front page
    #title_url_rel = hemi_soup.find('h3').text
   
    #thumbpic is too small
    #img_url_rel = hemi_soup.find('img', class_='thumb').get('src')
        
    #need to click the link to retreive large picture
    #will search for partial text "Enhanced since all links end with Enhanced"
    browser.links.find_by_partial_text('Enhanced')[link].click()
    
    #new code to retrieve info for new page after click
    #soup.find will now search through this page
    html = browser.html
    enh_soup = soup(html, 'html.parser')
    #print(hemi_soup)

    #find title
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




# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls



# 5. Quit the browser
browser.quit()




