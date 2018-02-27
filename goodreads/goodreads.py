'''
remove subtitles after colon and ()
'''

import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


def load_all_items(driver):
	'''
	Scroll down all the way in order to load all the items in the category.
	'''

	time.sleep(1)

	SCROLL_PAUSE_TIME = 1

	# Get scroll height
	last_height = driver.execute_script("return document.body.scrollHeight")

	while True:
		# Scroll down to bottom
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

		# Wait to load page
		time.sleep(SCROLL_PAUSE_TIME)

		# Calculate new scroll height and compare with last scroll height
		new_height = driver.execute_script("return document.body.scrollHeight")
		if new_height == last_height:
			break
		last_height = new_height




time0 = time.time()

driver = webdriver.Chrome()

# driver.get('https://www.goodreads.com/user/sign_in')

# print('Trying to log in...')

# driver.find_element_by_id('user_email').send_keys('jaimeruizno@gmail.com')
# driver.find_element_by_id('user_password').send_keys('password******', Keys.ENTER)

# print('Login successful')
print('Accessing Goodreads...')
driver.get('https://www.goodreads.com/review/list/63564236-helena?utf8=%E2%9C%93&shelf=to-read&per_page=infinite')

print('Loading items...')
load_all_items(driver)

books = [elem.text for elem in driver.find_elements_by_css_selector('.title .value')]

print('Searching library database...')

books_searched = []

for book in books:
	driver.get('https://yprl.bibliocommons.com/v2/search?custom_edit=false&query=title%3A%28'+book.replace(' ','+')+'%29+++formatcode%3A%28BK+%29&searchType=bl&suppress=true')
	print('–')
	try:
		driver.find_element_by_class_name('cp-empty-search-result')
		print('{:<20}{}'.format('Not found', book[:70]))
		books_searched.append('–')
	except NoSuchElementException:

		book_title = driver.find_element_by_css_selector('.cp-title .sr-only').text

		books_searched.append(book_title)

		driver.find_element_by_class_name('cp-availability-trigger').click()
		time.sleep(2)
	
		try:
			driver.find_element_by_xpath("//td[contains(text(), 'Ivanhoe')]").text
			print('{:<20}{}'.format('Ivanhoe', book[:70]))
		except NoSuchElementException:
			print('{:<20}{}'.format('In other libraries', book[:70]))

		try:
			driver.find_element_by_xpath("//td[contains(text(), 'Rosanna')]").text
			print('{:<20}{}'.format('Rosanna', book[:70]))
		except NoSuchElementException:
			print('{:<20}{}'.format('In other libraries', book[:70]))



		# availabilities = [elem.text for elem in driver.find_elements_by_class_name('cp-availability-status')]

		# for i in range(min(len(books_available), 3)):
			# print('{:<20}{}'.format(availabilities[i], books_available[i][:70]))

		

driver.quit()

for i in range(len(books)):
	print('{:<50}{:<50}'.format(books[i][:50], books_searched[i][:50]))

print('Total time: {} s'.format(time.time() - time0))