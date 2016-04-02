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
from datetime import datetime
# Need to pull out point coords from html
import re
# To calculate the actual correlation coeff
from numpy import corrcoef
# Selenium's find_element method is too slow
import lxml.html

num_points = 100


################################################################################
### Calculate correlation coeff
################################################################################
# Note x(0,1.0)=(0,360), y(0,1.0)=(320,0)
def calc_corr_coeff(driver):
	x_coords = []
	y_coords = []

	root = lxml.html.fromstring(driver.page_source)
	for i in range(0, num_points):
		#t = datetime.now()
		# Fetch the coords from html of each point
		#point = driver.find_element_by_class_name("nv-point-"+str(i))
		#attr_val = point.get_attribute("transform")
		attr_val = root.xpath('//path[@class="nv-point nv-point-'+str(i)+'"]/@transform')

		# diff = datetime.now() - t
		# print("Time to get elements:\t" + str(diff.total_seconds()))
		# Pull out just the x-y coords
		coords = re.split('\(|\)|,',str(attr_val))[1:3]
		# Scale them down to between 0-1 and adjust the y-vals (flip)
		x_coords.append(float(coords[0])/360.0)
		y_coords.append(abs(float(coords[1])-320.)/320.)
	# Now we have all the coords calculate correlation coeff
	#return numpy.corrcoef(x_coords,y_coords)[0, 1]
	return corrcoef(x_coords,y_coords)[0, 1]


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
#time.sleep(5)
num_games = int(raw_input("How many games should we play?"))

## Need to create a username initially (not working in Chrome?)
# alert=driver.switch_to_alert()
# alert.accept()


################################################################################
### Play the game
################################################################################
## Only need to fetch the game control elements once since they're persistent
# Guess box controls the guess entry (duh)
elem_guess = driver.find_element_by_id("guess-input")
# Next tag (type <a>) lets us move on from guess result screen
elem_next = driver.find_element_by_id("next-btn")

for i in xrange(num_games):
	# Calculate the correlation coeff for this plot
	corr_guess = calc_corr_coeff(driver)

	# Handle any coefficients outside the allowed bounds
	if corr_guess > 1.0:
		corr_guess = 1.0
	elif corr_guess < 0.0:
		corr_guess = 0.0
	# Just keep two decimal places, don't need more
	corr_guess_string = "{:.2f}".format(corr_guess)

	# Clear the text box
	elem_guess.send_keys(Keys.BACKSPACE)
	elem_guess.send_keys(Keys.BACKSPACE)
	# Enter our guess for correlation coeff into text box
	elem_guess.send_keys(corr_guess_string)
	# And submit the guess
	elem_guess.send_keys(Keys.RETURN)
	# This takes us to the result page
	#time.sleep(5)

	# Next we need to click on the NEXT button
	# The guess element is hidden so sendin keys will not work because
	# we're not dealing with an <input> element
	elem_next.click()
	#time.sleep(5)

# Now that we've finished need to die to register score
# Should make guess entry a function
for i in xrange(3):
	corr_guess_string = 0
	# Clear the text box
	elem_guess.send_keys(Keys.BACKSPACE)
	elem_guess.send_keys(Keys.BACKSPACE)
	# Enter our guess for correlation coeff into text box
	elem_guess.send_keys(corr_guess_string)
	# And submit the guess
	elem_guess.send_keys(Keys.RETURN)
	# This takes us to the result page

	# Next we need to click on the NEXT button
	# The guess element is hidden so sendin keys will not work because
	# we're not dealing with an <input> element
	elem_next.click()

# Finish up when user is ready
wait = raw_input("All done?")

driver.close()
