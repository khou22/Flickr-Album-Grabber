from bs4 import BeautifulSoup # Module to sort through the html
import lxml # Module to parse through the html for BeautifulSoup
# import urllib2 # Gets html
import os # Searching through computer directory
import io
from datetime import datetime # For timestamps

outputFileName = "flickrData.js"
blacklist = ["Design", "Roaracle 2015-2016 T-Shirt Contest"]

################   Get image urls from source   ################
data = ""
with open('page.html', 'r') as file:
    data = file.read()

soup = BeautifulSoup(data, "lxml") # Using lxml parser
albums = soup.select('div[class*="view photo-list-album-view "]') # Using CSS selector

data = []

for album in albums:
    style = album.get("style") # Get the style attribute
    # print(style)

    # Extract image URL
    startKey = "background-image: url(\"//"
    startURL = style.find(startKey) + len(startKey) # Just before background-image URL
    endURL = style.find(".jpg\")", startURL) + len(".jpg")  # Get end of URL
    imageURL = style[startURL:endURL]

    # Get title and link of the album
    linkTag = album.findAll("a")[0]
    linkPrepend = "https://www.flickr.com"
    link = linkPrepend + linkTag.get("href")
    title = linkTag.get("title")

    if title not in blacklist:
        data.append({ "title": title, "link": link, "image": imageURL })


################   Output to JS File   ################
print "{0} albums found".format(len(data))
try:
    with io.FileIO(outputFileName, 'w') as outputFile: # Writing file and creating file if it doesn't exist
        # print "// Last updated: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # print "const flickrData = ["
        outputFile.write("// Last updated: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n") # Timestamp
        outputFile.write("const flickrData = [\n") # Open array

        # Cycle through data
        for album in data:
            outputFile.write("  {\n")
            outputFile.write("    \"title\": \"" + album["title"] + "\",\n")
            outputFile.write("    \"link\": \"" + album["link"] + "\",\n")
            outputFile.write("    \"image\": \"" + album["image"] + "\"\n")
            outputFile.write("  },\n")

        outputFile.write("];\n") # Close array
        # print "];"
        outputFile.close()
except IOError as (errno, strerror):
    print "I/O error({0}): {1}".format(errno, strerror)
