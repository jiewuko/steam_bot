import os

chrome_driver = os.getcwd() + '/extensions/' + 'chromedriver'
inventory_helper = os.getcwd() + '/extensions/' + 'configured_steam_inventory_helper.crx'


class ConstantsForBot(object):

    """
    TOKEN_FOR_TELEGRAM_BOT - string
    CHAT_ID_FOR_TELEGRAM_BOT - string

    FOR EXAMPLE:
    TOKEN_FOR_TELEGRAM_BOT = '678881790:AAH67SWnC5AF-tKE_ZvpLUO-BXGWb3l0-pE'
    CHAT_ID_FOR_TELEGRAM_BOT = '433565899'
    """

    TOKEN_FOR_TELEGRAM_BOT = ''
    CHAT_ID_FOR_TELEGRAM_BOT = ''

    EXECUTABLE_PATH = chrome_driver
    PATH_FOR_EXTENSION = inventory_helper

    """
    LOGIN_FOR_STEAM - string
    PASSWORD_FOR_STEAM - string
    
    FOR EXAMPLE:
    LOGIN_FOR_STEAM = 'user'
    PASSWORD_FOR_STEAM = 'secret'
    """

    LOGIN_FOR_STEAM = ''
    PASSWORD_FOR_STEAM = ''

    """
    URL_FOR_GET_ITEMS_FROM_API - string
    LOGIN_FOR_API - string
    PASSWORD_FOR_API - string
    
    FOR EXAMPLE:
    URL_FOR_GET_ITEMS_FROM_API = http://18.224.140.66:9001/items/
    LOGIN_FOR_API = 'user'
    PASSWORD_FOR_API = 'secret'
    """

    URL_FOR_GET_ITEMS_FROM_API = ''
    LOGIN_FOR_API = ''
    PASSWORD_FOR_API = ''
