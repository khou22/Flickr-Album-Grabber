from bs4 import BeautifulSoup # Module to sort through the html
import lxml # Module to parse through the html for BeautifulSoup
import urllib2 # Gets html
# import webbrowser # This module can control the browser
#
# url = "https://www.flickr.com/photos/khou22/albums"
#
# try: # Make sure link exists
#     urllib2.urlopen(url)
# except urllib2.HTTPError, e:
#     print(e.code) # Return any errors
# except urllib2.URLError, e:
#     print(e.args)
#
# response = urllib2.urlopen(url) #Get markdown
#
# html = response.read() #Markdown

data = ""
with open('page.html', 'r') as file:
    data = file.read()

soup = BeautifulSoup(data, "lxml") # Using lxml parser
print(soup.title)
print(soup.findAll("div", { "class": "view photo-list-album-view requiredToShowOnServer" }))

