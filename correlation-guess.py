#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Correlations guessing game for:
http://guessthecorrelation.com/
James Kahn
"""

################################################################################
### Import libraries
################################################################################
# Selenium let's us interact with a webpage
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# Want to be able to pause running to see what's going on
import time


################################################################################
### Set up ChromeDriver
################################################################################
# Need to specify chromedriver binary location if not in $PATH
chromedriver_location = '/usr/lib/chromium-browser/chromedriver'
# Open the session (opens web browser)
driver = webdriver.Chrome(chromedriver_location)

# Go to the page we want to visit
driver.get("http://guessthecorrelation.com/")

#assert "Python" in driver.title
# elem = driver.find_element_by_name("q")
# elem.send_keys("pycon")
# elem.send_keys(Keys.RETURN)
# assert "No results found." not in driver.page_source

################################################################################
### Start a game
################################################################################
## Greeted with the start menu, need to start a new game
elem_new_game = driver.find_element_by_id("new-game")
elem_new_game.click()
time.sleep(5)

## Need to create a username initially
alert=driver.switch_to_alert()
alert.accept()


################################################################################
### Play the game
################################################################################
## Only need to fetch the game control elements once since they're persistent
# Guess box controls the guess entry (duh)
elem_guess = driver.find_element_by_id("guess-input")
# Next tag (type <a>) lets us move on from guess result screen
elem_next = driver.find_element_by_id("next-btn")

# Enter our guess for correlation coeff into text box
corr_guess = 6
elem_guess.send_keys(corr_guess)
# And submit the guess
elem_guess.send_keys(Keys.RETURN)
# This takes us to the result page
time.sleep(5)

# Next we need to click on the NEXT button
# The guess element is hidden so sendin keys will not work because
# we're not dealing with an <input> element
elem_next.click()
time.sleep(5)


driver.close()
