############################################################################
# Name: Kevin Hou
# Date: May 4, 2017
#
# Project Name: GetAlbumPhotos.py
#
# Description:
#   Grabs Flickr images using url of the first photo in the album
#
# Usage:
#   python GetAlbumPhotos.py
############################################################################

################   User Options   ################
OUTPUT_FILE = "[album]-[date].js"
FIRST_IMG_URL = "https://www.flickr.com/photos/161442428@N03/27988049148/in/album-72157694629581711/"
# FIRST_IMG_URL = "https://www.flickr.com/photos/161442428@N03/41856635411/in/album-72157694629581711/" # Last image
# FIRST_IMG_URL = "https://www.flickr.com/photos/161442428@N03/41856634091/in/album-72157694629581711/" # Second to last image
MAX_WAIT = 5 # Maximum waiting time for an image to load

################   Imports   ################
# Selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC # Waiting for things to load

# Date parsing
from datetime import datetime
from dateutil.parser import parse
import calendar
import time

import glob # Grabbing files with extensions
import io

################   Setup Driver   ################
# Incognito Chrome
option = webdriver.ChromeOptions()
option.add_argument("--incognito")

# Use the Chrome driver
driver = webdriver.Chrome(chrome_options=option)

# Initial URL (first image)
driver.get(FIRST_IMG_URL) # Latest image

################   Main   ################
# States
hasNextImage = True

# Master data
data = []

albumTitle = driver.title.split(' | ')[0] # Get the album title
print("Album title: %s" % albumTitle)

class element_by_class_has_href(object):
    """An expectation for checking that an element has a href link

    className - used to find the element
    returns the WebElement once it has a working link
    """
    def __init__(self, className):
        self.className = className

    def __call__(self, driver):
        element = driver.find_element_by_class_name("navigate-next") # Finding the referenced element
        href = element.get_attribute("href")
        if not href.endswith("#"): # Wait until it's the URL for the next element
            return element
        else:
            return False

################   Webscrape Flickr   ################
print("// Last updated: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "") # Timestamp
print("const albumData = [") # Open array

while (hasNextImage):
    # Get the image ID from the URL
    currentURL = driver.current_url # Gets the ID of the image
    # print("Image URL: %s" % currentURL)

    # Get the image URL source
    time.sleep(1)
    image = driver.find_element_by_class_name("main-photo").get_attribute("src")
    time.sleep(1)
    # print("Image source: %s" % image)

    # Get meta data container
    metaContainer = driver.find_element_by_class_name("sub-photo-right-view")

    # Get date and time and parse
    parsedTime = metaContainer.find_element_by_class_name("date-taken-label").text # Example: Taken on July 3, 2015
    parsedTime = str(parsedTime.split("Taken on ")[1])
    parsedDate = datetime.strptime(parsedTime, '%B %d, %Y') # Example: July 03, 2015
    isoDate = parsedDate.isoformat()

    # Log to master data set
    data.append({ "url": currentURL, "image": image, "date": isoDate })

    print("  {")
    print("    \"image\": \"" + image + "\",")
    print("    \"id\": \"" + currentURL + "\",")
    print("    \"date\": \"" + isoDate + "\"")
    print("  },")

    # time.sleep(2) # To allow page loads
    try:
        nextImageButton = WebDriverWait(driver, MAX_WAIT).until(
            element_by_class_has_href('navigate-next')
        )
        nextURL = nextImageButton.get_attribute('href')
    except TimeoutException:
        # print("[Failure] Caught timeout")
        print("No more images in this album")
        hasNextImage = False # No more images in album
    # finally:
    #     print("Finally done..?")

    if hasNextImage:
        # print("Next URL: %s" % nextURL)
        driver.get(nextURL)

driver.close()
print("];\n") # Close array

print("%d image(s) found" % len(data))

################   Output to JS File   ################
OUTPUT_FILE = OUTPUT_FILE.replace("[date]", str(calendar.timegm(time.gmtime()))) # Add epoche timestamp
OUTPUT_FILE = OUTPUT_FILE.replace("[album]", albumTitle.replace(' ',  '-'))
print("Writing to file %s" % OUTPUT_FILE)
try:
    with io.FileIO(OUTPUT_FILE, 'w') as outputFile: # Writing file and creating file if it doesn't exist
        outputFile.write("// Last updated: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n") # Timestamp
        outputFile.write("const albumData = [\n") # Open array

        # Cycle through data
        for image in data:
            outputFile.write("  {\n")
            outputFile.write("    \"image\": \"" + image["image"] + "\",\n")
            outputFile.write("    \"id\": \"" + image["url"] + "\",\n")
            outputFile.write("    \"date\": \"" + image["date"] + "\"\n")
            outputFile.write("  },\n")

        outputFile.write("];\n") # Close array

        outputFile.close()
except IOError as err:
    print("I/O error: %s" % err)
