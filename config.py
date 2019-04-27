class ConfigForBot(object):
    LOGIN_PAGE = 'https://steamcommunity.com/login/home/?goto='
    USERNAME_FORM = 'username'
    PASSWORD_FORM = 'password'
    TWO_FACTOR_CODE_FORM = 'twofactorcode_entry'

    MAIN_PAGE = "https://steamcommunity.com"
    FORM_FOR_CHECK_LOGIN = 'header_notification_area'

    MAIN_PAGE_FOR_SETTING_STEAM_INVENTORY_HELPER = 'chrome-extension://cmeakgjggjdlcpncigglobpjbkabhmjl/dist/index.html#/' \
                                                   'settings/inventory'
    PAGE_FOR_SETTING_QUICK_BUY_BUTTON = '//*[@id="root"]/div/main/div/div[1]/div/div[1]/ul/li[2]/a'
    LABEL_FOR_SETTING_QUICK_BUY_BUTTON = '//*[@id="root"]/div/main/div/div[1]/div/div[2]/div[1]/label'

    ELEMENT_FOR_CHECK_LOGIN = "header_notification_area"
    ELEMENT_FOR_CHECK_COUNT_STICKERS = '//div[@class="sih-images"]'
    ELEMENT_FOR_CHECK_NAME_TAG = 'preceding-sibling::div[@class="market_listing_item_name_block"]/span[@class="sih-fraud"]'
    STICKERS = 'img'
    PRICE = 'parent::div/preceding-sibling::div[@class="market_listing_price_listings_block"][1]/div' \
            '[@class="market_listing_right_cell market_listing_their_price"]/span/span' \
            '[@class="market_listing_price market_listing_price_with_fee"]'
    ITEMS_NAME = 'preceding-sibling::div[@class="market_listing_item_name_block"]/span' \
                 '[@class="market_listing_item_name economy_item_hoverable"]'
    BUTTON_FOR_BUY_ITEM = 'parent::div/parent::div/div[@class="market_listing_price_listings_block"]/' \
                          'div[@class="market_listing_right_cell market_listing_action_buttons"]/' \
                          'div[@class="market_listing_buy_button"]/a'

    TIME_OUT_FOR_INSTALL_EXTENSION = 2
