from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from time import sleep, time
from datetime import datetime, timedelta
import random

def wait_for(driver, xpath, timeout=30):
    try:
        return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
    except TimeoutException:
        print("Loading took too much time!")

def _get_drop_date(sneaker_url):
    opt = Options()
    opt.headless = True
    driver = webdriver.Firefox(options=opt)
    drop_date_xpath = '/html/body/div[2]/div/div/div[1]/div/div[2]/div[2]/div/div[1]/section/div[2]/div/div/div[2]/div'
    while True:
        driver.get(sneaker_url)
        drop_date_elem = wait_for(driver, drop_date_xpath)
        if drop_date_elem:
            _tmp = drop_date_elem.text
            _tmp = _tmp.split('Verfügbar am ')[-1].split(' ')
            del _tmp[1]
            _tmp = datetime.strptime(str(datetime.now().year) + ':' +''.join(_tmp), "%Y:%d.%m.%H:%M")
            driver.close()
            return _tmp.isoformat()
        print('Refreshing page')


def get_drop_date(bot_config):
    return _get_drop_date(bot_config['sneakers'][0]['url'])
        


def __get_sneaker(target_sneaker, amount, credentials, headless, closing_delay, debug=True):
    print(f'DEBUG={debug}\nHEADLESS={headless}\nSNEAKER={target_sneaker}\nAMOUNT={amount}\nPAYMENT_METHOD={credentials["payment_method"]}')

    upcoming_url = 'https://www.nike.com/de/launch?s=upcoming'
    instock_url = 'https://www.nike.com/de/launch?s=in-stock'

    size_xpath = '/html/body/div[2]/div/div/div[1]/div/div[2]/div[2]/div/section[1]/div[2]/aside/div/div[2]/div/div[2]/ul/li[14]/button'
    cart_xpath = '/html/body/div[2]/div/div/div[1]/div/div[2]/div[2]/div/section[1]/div[2]/aside/div/div[2]/div/div[2]/div/button'
    checkout_xpath = '/html/body/div[2]/div/div/div[2]/div/div/div/div/div[3]/button[2]'
    checkout_guest_xpath = '/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[2]/button'

    fn_xpath = '/html/body/div[1]/div/div[3]/div/div[2]/div/div/main/section[2]/div/div[2]/form/div/div/div/div[1]/div[1]/input'
    addr_xpath = '/html/body/div[1]/div/div[3]/div/div[2]/div/div/main/section[2]/div/div[2]/form/div/div/div/div[1]/div[3]/div/div[1]/div/div/input'

    save_addr_xpath = '/html/body/div[1]/div/div[3]/div/div[2]/div/div/main/section[2]/div/div[2]/form/div/div/div/div[2]/button'
    to_payment_xpath = '/html/body/div[1]/div/div[3]/div/div[2]/div/div/main/section[2]/div/div[3]/div/button'

    credit_card_xpath =   '/html/body/div[1]/div/div[3]/div/div[2]/div/div/main/section[3]/div/div[1]/div[2]/div[3]/div/div[1]/div/div/label'
    ccn_xpath = '/html/body/form/div/div[1]/input'
    credit_card_order_review_xpath = '/html/body/div[1]/div/div[3]/div/div[2]/div/div/main/section[3]/div/div[1]/div[2]/div[5]/button'

    paypal_xpath =        '/html/body/div[1]/div/div[3]/div/div[2]/div/div/main/section[3]/div/div[1]/div[2]/div[3]/div/div[2]/div/div/label'
    paypal_order_review_xpath = '/html/body/div[1]/div/div[3]/div/div[2]/div/div/main/section[3]/div/div[1]/div[2]/div[4]/div/div[2]/button'

    wire_transfer_xpath = '/html/body/div[1]/div/div[3]/div/div[2]/div/div/main/section[3]/div/div[1]/div[2]/div[3]/div/div[3]/div/div/label'
    wire_order_review_xpath =   '/html/body/div[1]/div/div[3]/div/div[2]/div/div/main/section[3]/div/div[1]/div[2]/div[4]/div/div[2]/button'

    klarna_xpath =        '/html/body/div[1]/div/div[3]/div/div[2]/div/div/main/section[3]/div/div[1]/div[2]/div[3]/div/div[4]/div/div/label'
    klarna_birthday_xpath = '/html/body/div[2]/span/div/div/div/div/div/div/div[2]/div/div/div/span/div/div[3]/div[2]/div/label/div/div/span/input'
    klarna_order_review_xpath = '/html/body/div[1]/div/div[3]/div/div[2]/div/div/main/section[3]/div/div[2]/section[2]/div/button'
    klarna_submit_xpath = '/html/body/div[2]/span/div/div/div/div/div/div/div[3]/div/div/button/div/div[1]'

    confirm_order_xpath = '/html/body/div[1]/div/div[3]/div/div[2]/div/div/main/section[4]/div/div/div/div/section[2]/div/button'
    
    options = Options()
    options.headless = headless

    start_time = time()

    driver = webdriver.Firefox(options=options)
    attempt = 0
    while True:
        attempt += 1
        print(f'[{time()}] Attempt #{attempt}')
        driver.get(target_sneaker)
        size_elem = wait_for(driver, size_xpath, timeout=2)
        if size_elem:
            size_elem.click()
            break
        state = driver.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/div/div[2]/div[2]/div/section[1]/div[2]/aside/div/div[2]/div')
        print(f'sneaker_status={state.text}')
        if state.text == 'Ausverkauft':
            driver.close()
            return
    wait_for(driver, cart_xpath).click()
    wait_for(driver, checkout_xpath).click()
    wait_for(driver, checkout_guest_xpath).click()
    fn_elem = wait_for(driver, fn_xpath)
    fn_elem.click()
    fn_elem.clear()
    driver.find_element_by_xpath('//*[@id="addressSuggestionOptOut"]').click()
    fn_elem.send_keys(Keys.TAB.join([credentials['first_name'], credentials['last_name']]))
    addr_elem = driver.find_element_by_xpath('//*[@id="address1"]')
    addr_elem.click()
    addr_elem.clear()
    addr_elem.send_keys(Keys.TAB.join([credentials['street'], Keys.TAB+credentials['zip_code'], credentials['city'], credentials['email'], credentials['phone']]))

    wait_for(driver, save_addr_xpath).click()
    sleep(.5)
    wait_for(driver, '/html/body/div[1]/div/div[3]/div/div[2]/div/div/main/section[2]/div/div[2]/div[2]/div/div/div/div/label/span[2]')
    wait_for(driver, to_payment_xpath).click()

    if credentials['payment_method'] == 'CREDITCARD':
        wait_for(driver, credit_card_xpath).click()
        iframe = wait_for(driver, '/html/body/div[1]/div/div[3]/div/div[2]/div/div/main/section[3]/div/div[1]/div[2]/div[4]/div/div[1]/div[2]/iframe')
        driver.switch_to.frame(iframe)
        ccn_elem = wait_for(driver, '/html/body/form/div/div[1]/input')
        ccn_elem.click()
        ccn_elem.send_keys(Keys.TAB.join([credentials['credit_card'], credentials['expiry'], credentials['ccv']]))
        driver.switch_to.default_content()    
        wait_for(driver, credit_card_order_review_xpath).click()
        confirm_order = wait_for(driver, confirm_order_xpath)
    elif credentials['payment_method'] == 'PAYPAL':
        wait_for(driver, paypal_xpath).click()
        wait_for(driver, paypal_order_review_xpath).click()
        confirm_order = wait_for(driver, confirm_order_xpath)
    elif credentials['payment_method'] == 'KLARNA':
        wait_for(driver, klarna_xpath).click()
        wait_for(driver, klarna_order_review_xpath).click()
        sleep(.5)
        bday_elem = wait_for(driver, klarna_birthday_xpath)
        bday_elem.click()
        bday_elem.clear()
        bday_elem.send_keys(credentials['bday'])
        confirm_order = wait_for(driver, klarna_submit_xpath)
    elif credentials['payment_method'] == 'SOFORT':
        wait_for(driver, wire_transfer_xpath).click()
        wait_for(driver, wire_order_review_xpath).click()
        confirm_order = wait_for(driver, confirm_order_xpath)
    end_time = time()
    if not debug:
        confirm_order.click()

    total_time = end_time-start_time
    print(f"This took {(total_time)} seconds")
    open('info.log', 'a').write(f'[{start_time}]: HEADLESS={headless} TOTAL_TIME={total_time}\n')
    print(f'Waiting {closing_delay} seconds before closing')
    sleep(closing_delay)
    driver.close()
    return 0

def test():
    for i in range(50):    
        headless = bool(random.getrandbits(1))
        closing_delay = 0
        get_sneaker(target_sneaker, amount, credentials, headless, closing_delay, debug)

def days_hours_minutes(td):
    return f'{td.days} days {td.seconds//3600} hours and {(td.seconds//60)%60} minutes'

def __wait_for_drop(sneaker_url, sneaker_name, drop_time, amount, credentials, headless, closing_delay, debug):
    print(sneaker_url)
    drop_date = datetime.fromisoformat(drop_time)
    while True:
        td = drop_date - datetime.now()
        print(f'Time until drop: {days_hours_minutes(td)}')
        _seconds = int(td.total_seconds())
        if _seconds > 600:
            _wait = _seconds // 2
            print("Sleeping for:", days_hours_minutes(datetime.fromtimestamp(_wait)-datetime(1970,1,1)))
            sleep(_wait)
        else:
            break
    return __get_sneaker(sneaker_url, amount, credentials, headless, closing_delay, debug)
    
def _wait_for_drop():
    return __wait_for_drop(target_sneaker, drop_time, amount, credentials, headless, closing_delay, debug)

def _get_sneaker():
    return __get_sneaker(target_sneaker, amount, credentials, headless, closing_delay, debug)

def wait_for_drop(bot_config):
    return __wait_for_drop(
            bot_config['sneakers'][0]['url'], 
            bot_config['sneakers'][0]['name'],
            bot_config['sneakers'][0]['drop_time'],
            bot_config['sneakers'][0]['amount'], 
            bot_config['credentials'], 
            bot_config['headless'], 
            bot_config['closing_delay'], 
            bot_config['debug']
    )

def get_sneaker(bot_config):
    return __get_sneaker(
            bot_config['sneakers'][0]['url'], 
            bot_config['sneakers'][0]['amount'], 
            bot_config['credentials'], 
            bot_config['headless'], 
            bot_config['closing_delay'], 
            bot_config['debug']
    )

if __name__ == '__main__':
    _wait_for_drop()