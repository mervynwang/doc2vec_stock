from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


profile = webdriver.FirefoxProfile()
# profile._install_extension("buster_captcha_solver_for_humans-0.7.2-an+fx.xpi", unpack=False)
# profile.set_preference("security.fileuri.strict_origin_policy", False)
# profile.set_preference("general.useragent.override", fua)
profile.update_preferences()
capabilities = webdriver.DesiredCapabilities.FIREFOX
capabilities['marionette'] = True

options = webdriver.FirefoxOptions()
# options.add_option('useAutomationExtension', False)
# options.headless = self.headless

driver = webdriver.Firefox(options=options, capabilities=capabilities, firefox_profile=profile, executable_path='./geckodriver')
driver.set_window_size(1024, 1024)


driver.get('file:///home/mervyn/work/ncu/stock/wsj/index.html')
login = WebDriverWait(driver, 20).until(
	EC.presence_of_element_located((By.CSS_SELECTOR, "header a[href*=accounts]")) #sign-in
)
print(login)

login.click()
