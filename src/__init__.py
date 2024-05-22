from os import getenv

base_url = getenv('BASE_URL', 'https://demoqa.com')
user_name, password = getenv('USER_NAME', 'hellodemoqa'), getenv('PASSWORD', 'rarNRBR_WH5_JYA$')

appium_url = getenv('APPIUM_URL', 'http://127.0.0.1:4723')
