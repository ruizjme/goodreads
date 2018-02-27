from selenium import webdriver

driver = webdriver.Chrome()

driver.get('https://yprl.bibliocommons.com/v2/search/availability/S27C722197?frbr=false&locked=false&query=blindspots&searchScope=AUS-YPRL&searchType=smart')

print(driver.find_element_by_xpath("//td[contains(text(), 'Ivanhoe')]").text)