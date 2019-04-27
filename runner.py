import os
import re
from time import sleep

from constants import ConstantsForBot as const
from config import ConfigForBot as config

import requests
from requests.exceptions import ReadTimeout

import telegram

from pyvirtualdisplay import Display

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

os.environ["webdriver.chrome.driver"] = const.EXECUTABLE_PATH
chrome_option = Options()
chrome_option.add_argument('--no-sandbox')
chrome_option.add_extension(const.PATH_FOR_EXTENSION)


class SteamBOt(object):
    def __init__(self):
        self.display = Display(visible=0, size=(1024, 768))
        self.display.start()
        self.telegram_bot = telegram.Bot(token=const.TOKEN_FOR_TELEGRAM_BOT)
        self.driver = webdriver.Chrome(executable_path=const.EXECUTABLE_PATH, options=chrome_option)
        self._login()
        self._installation_extension()

    def _login(self):
        self.driver.get(config.LOGIN_PAGE)

        username = self.driver.find_element_by_name(config.USERNAME_FORM)
        username.send_keys(const.LOGIN_FOR_STEAM)

        password = self.driver.find_element_by_name(config.PASSWORD_FORM)
        password.send_keys(const.PASSWORD_FOR_STEAM + Keys.RETURN)

        two_factor_auth = self.driver.find_element_by_id(config.TWO_FACTOR_CODE_FORM)
        two_factor_auth.send_keys(self.get_auth_code() + Keys.RETURN)

        self.assert_login()

    def assert_login(self):
        self.driver.get(config.MAIN_PAGE)
        check_login = self.driver.find_elements_by_id(config.FORM_FOR_CHECK_LOGIN)
        if check_login:
            self.telegram_bot.send_message(const.CHAT_ID_FOR_TELEGRAM_BOT, 'Login success!')
        else:
            self._login()

    def get_auth_code(self):
        update_init = len(self.telegram_bot.get_updates())
        update_second = len(self.telegram_bot.get_updates())
        self.telegram_bot.send_message(chat_id=const.CHAT_ID_FOR_TELEGRAM_BOT, text='INPUT CODE, NIGGA!!!')
        while update_second == update_init:
            update_second = len(self.telegram_bot.get_updates())
            msg = None
            if update_second != update_init:
                msg = self.telegram_bot.get_updates()[-1].message.text
                msg = ''.join(msg.split()).upper()
                if len(msg) == 5:
                    self.telegram_bot.send_message(const.CHAT_ID_FOR_TELEGRAM_BOT, 'I am try to login!')
                    return msg
                else:
                    update_init = update_second
                    self.telegram_bot.send_message(const.CHAT_ID_FOR_TELEGRAM_BOT, 'Be careful! Enter correct code!')

    def _installation_extension(self):
        """ Install extension for check count stickers """
        self.driver.get(config.MAIN_PAGE_FOR_SETTING_STEAM_INVENTORY_HELPER)
        sleep(config.TIME_OUT_FOR_INSTALL_EXTENSION)
        self.driver.find_element_by_xpath(config.PAGE_FOR_SETTING_QUICK_BUY_BUTTON).click()
        sleep(config.TIME_OUT_FOR_INSTALL_EXTENSION)
        self.driver.find_element_by_xpath(config.LABEL_FOR_SETTING_QUICK_BUY_BUTTON).click()
        sleep(config.TIME_OUT_FOR_INSTALL_EXTENSION)

    def get_items_from_api(self):
        time_out = 30
        try:
            response = requests.get(url=const.URL_FOR_GET_ITEMS_FROM_API,
                                    auth=(const.LOGIN_FOR_API, const.PASSWORD_FOR_API),
                                    timeout=5)
            items = [items for items in response.json()['results']]
            return items
        except ReadTimeout:
            self.telegram_bot.send_message(chat_id=const.CHAT_ID_FOR_TELEGRAM_BOT,
                                           text='Something went wrong with api!')
            sleep(time_out)
            return []

    def check_login(self, url):
        try:
            if url:
                self.driver.get(url)
                check_login = self.driver.find_elements_by_id(config.ELEMENT_FOR_CHECK_LOGIN)
                if not check_login:
                    self._login()
                else:
                    pass
        except Exception:
            self.run_bot()

    def check_error_in_browser_title(self):
        time_out = 30
        if 'Error' in self.driver.title or 'Ошибка' in self.driver.title:
            sleep(time_out)
            self.run_bot()
        else:
            pass

    @staticmethod
    def find_name_tag(elements):
        try:
            return elements.find_element_by_xpath(config.ELEMENT_FOR_CHECK_NAME_TAG)
        except NoSuchElementException:
            return None

    def send_message_about_item(self, name_item, imgs, new_price, name_tags):
        stickers = {}
        stickers.update({'Items name': name_item})
        stickers.update({'Count stickers': len(imgs)})
        stickers.update({'Price': new_price})
        if name_tags:
            stickers.update({'Name tag': name_tags.text})
        print(stickers)
        try:
            self.telegram_bot.send_message(
                chat_id=const.CHAT_ID_FOR_TELEGRAM_BOT, text=str(stickers))
        except Exception:  # TODO Catch exception
            self.run_bot()

    @staticmethod
    def get_item_name(elements):
        try:
            item_name = elements.find_element_by_xpath(config.ITEMS_NAME).text
            return ''.join(item_name) if item_name else None
        except NoSuchElementException:
            return None

    @staticmethod
    def get_item_price(imgs, price_for_buy_item):
        price = imgs[0].find_element_by_xpath(config.PRICE).text
        if 'Продано!' not in price:
            converted_price = float((re.compile('[0-9]+,*\.*\d*').findall(price)[0]).replace(',', '.'))
            return converted_price if converted_price <= float(price_for_buy_item) else False
        else:
            return False

    def buy_item(self, imgs, price_for_buy_item, elements, name_tags):
        valid_item_price = self.get_item_price(imgs=imgs, price_for_buy_item=price_for_buy_item)
        if valid_item_price:
            imgs[0].find_element_by_xpath(config.BUTTON_FOR_BUY_ITEM).click()  # Buy item
            self.send_message_about_item(name_item=self.get_item_name(elements),
                                         imgs=imgs,
                                         new_price=valid_item_price,
                                         name_tags=name_tags)

    def find_items_for_buy(self, price_for_buy_item, count_stickers, only_name_tag):
        for elements in self.driver.find_elements_by_xpath(config.ELEMENT_FOR_CHECK_COUNT_STICKERS):
            name_tags = self.find_name_tag(elements)
            imgs = elements.find_elements_by_xpath(config.STICKERS)
            if only_name_tag:
                if name_tags:
                    self.buy_item(imgs=imgs,
                                  price_for_buy_item=price_for_buy_item,
                                  elements=elements,
                                  name_tags=name_tags)
            elif (len(imgs) >= int(count_stickers)) or name_tags:
                self.buy_item(imgs=imgs,
                              price_for_buy_item=price_for_buy_item,
                              elements=elements,
                              name_tags=name_tags)

    def run_bot(self):
        get_items = self.get_items_from_api()
        if get_items:
            for items in get_items:
                url = items.get('item_url')
                count_stickers = items.get('count_stickers')
                price = items.get('price')
                only_name_tag = items.get('only_name_tag')
                self.check_login(url)
                self.check_error_in_browser_title()
                self.find_items_for_buy(
                    price_for_buy_item=price,
                    count_stickers=count_stickers,
                    only_name_tag=only_name_tag,
                )
                sleep(3)


if __name__ == '__main__':
    bot = SteamBOt()
    while True:
        bot.run_bot()
        sleep(10)
