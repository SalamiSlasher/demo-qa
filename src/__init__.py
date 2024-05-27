from os import getenv

base_url = getenv('BASE_URL', 'https://demoqa.com')

# API
user_name, password = getenv('USER_NAME', 'hellodemoqa'), getenv('PASSWORD', 'rarNRBR_WH5_JYA$')

# ANDROID
appium_url = getenv('APPIUM_URL', 'http://127.0.0.1:4723')

# WEB
use_selenoid = True
selenoid_url = getenv('SELENOID_URL', 'http://localhost:4444/wd/hub')
