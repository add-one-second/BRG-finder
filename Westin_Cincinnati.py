''' trying to find hotel BRG opportunity by monitoring hotel website rate VS third party rates

'''

import requests, bs4, os, time, re
from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


print(chr(27) + "[2J") # clear screen

driver = webdriver.Firefox()
driver.maximize_window()
driver.get("https://www.google.com/")
# hotel_name_list = ['Four Points by Sheraton Philadelphia City Center', 'Sheraton Philadelphia Downtown Hotel', 'Aloft Philadelphia Downtown', \
#     'The Westin Philadelphia', 'Fairfield Inn by Marriott Philadelphia Downtown/Center City', 'Sheraton Philadelphia Society Hill Hotel',\
#     'Courtyard by Marriott Philadelphia City Avenue', 'Courtyard by Marriott Philadelphia Downtown', 'The Westin Mount Laurel', \
#     'Aloft Philadelphia Airport', 'Four Points by Sheraton Philadelphia Airport', 'Sheraton Suites Philadelphia Airport', 'Fairfield Inn Philadelphia Airport', \
#     'Courtyard Philadelphia Airport', 'renaissance philadelphia airport hotel', 'Aloft Mount Laurel']
hotel_name_list = ['Seattle Airport Marriott', 'Courtyard Seattle south center', 'Residence Inn by Marriott Seattle Sea-Tac Airport', 'Residence Inn by Marriott Seattle South/Tukwila', \
    'Aloft Seattle Sea-Tac Airport', 'Fairfield Inn Seattle Sea-Tac Airport', 'Townplace suites seattle southcenter', 'Courtyard Seattle Sea-Tac Area', \
    'Four Points by Sheraton Seattle Airport South', 'Townplace suites seattle south', 'SpringHill suites seattle south']
# hotel_name_list = ['renaissance seattle hotel', 'w seattle', 'Sheraton seattle Hotel', 'The Westin seattle', 'Sheraton seattle waterfront', 'MOXY Seattle Downtown']
# click for the checkin checkout date
checkin_dates = ['13 Jul']
checkout_dates = ['14 Jul']
# checkin_dates = ['2 May', '26 May']
# checkout_dates = ['20 May', '28 May']
is_initaite = True # initiate with both days
is_curr_last_date = False # after initaitaion search, skip the current search date

# retrive rates inner function
def retrive_rates(available_prices):
    # inputs with all available rates, process
    # skip hotel and dates with none or only 1 (official) website avaible
    if len(available_prices)<=2:
        print('Found less than two prices')
        print('')
        print('')
        return

    available_prices[len(available_prices)-1].click()
    available_prices = driver.find_elements_by_class_name('B4MzEf')
    print('found additional', len(available_prices), 'prices')
    price_list = list()
    official_site_price = []
    for price in available_prices:
        # print(price.text)
        # print(price.text.splitlines())
        # print('')
        try:
            hotel_lines = price.text.splitlines()
            hotel_price = [re.findall(r'\d+', i)[0] for i in hotel_lines if bool(re.search(r'\d', i))]
            if len(hotel_lines)>2:
                if hotel_lines[2]=='Official site':
                    official_site_price = int(hotel_price[0])
            elif len(hotel_lines)==1: # only one result line -- result might be sentance "DEAL43% less than usual"
                print(hotel_lines)
                continue

            # print(hotel_lines)
            price_list.append(int(hotel_price[0]))
            # price_list.append(int(re.findall(r'\d+', price.text.splitlines()[0])[0]))
        except:
            print('something not right in extracting price')
            print(price.text)
            print(price.text.splitlines())
            print('')
    if not official_site_price: # No official price found
        print('No offcial rate found for this hotel')
        if len(available_prices)>5:
            for price in available_prices:
                print(price.text.splitlines())
            input('found more than 5 rates without official rate')
        print('')
        return

    print(price_list)
    if official_site_price-min(price_list)>2:
        input('BRG chance found')
    else:
        print('better luck next time')
        print('')
        print('')

def date_box_click(checkin_date, checkout_date):
    # inner function for check in and check out date inputs
    print('checkin date:', checkin_date, 'checkout date:', checkout_date)
    elems = driver.find_elements_by_class_name("lxhdrtxt")
    elems[0].click()
    time.sleep(1)
    elems = driver.find_elements_by_class_name("hudp-nextMonth").click()
    # elems[0]
    # time.sleep(1)
    driver.find_element_by_xpath("//td[@aria-label='" + checkin_date + "']").click()
    time.sleep(1)
    # elems = driver.find_elements_by_class_name("hudp-nextMonth")
    # elems[0].click()
    # time.sleep(1)
    driver.find_element_by_xpath("//td[@aria-label='" + checkout_date + "']").click()
    time.sleep(3)
    # driver.find_element_by_xpath
    return driver

def hotel_name_input(hotel_name):
    print('working on', hotel_name)
    elem = driver.find_element_by_id("gbqfbb")
    elem.click()
    elem.click()
    time.sleep(3)
    elem.clear()
    elem.send_keys(hotel_name)
    elem.send_keys(Keys.RETURN)
    time.sleep(3)

for hotel_name in hotel_name_list:
    hotel_name_input(hotel_name)
    if hotel_name == hotel_name_list[0]:
        # first hotel, initiate, loop all dates
        for checkin_date, checkout_date in zip(checkin_dates, checkout_dates):
            driver = date_box_click(checkin_date, checkout_date)
            # check if price exist
            if  "Contact this property for rates and availability" in driver.page_source:
                print('price not exist')
                print('')
                print('')
                continue
            available_prices = driver.find_elements_by_class_name('lhpr-content-item')
            retrive_rates(available_prices)
    else:

        if  "Contact this property for rates and availability" in driver.page_source:
            print('price not exist')
            print('')
            print('')
            continue
        available_prices = driver.find_elements_by_class_name('lhpr-content-item')
        retrive_rates(available_prices)

        # for checkin_date, checkout_date in zip(checkin_dates, checkout_dates):
        #     driver = date_box_click(checkin_date, checkout_date)
        #     # check if price exist



driver.close()


# TODO -- all hotels around me


'''
curr_path = os.path.dirname(os.path.realpath(__file__))
hotel_web_link = 'https://www.starwoodhotels.com/preferredguest/room.html?lpqRatePlanName=DAILY&bTax=true&departureDate=2018-05-06&arrivalDate=2018-05-05&propertyId=1044&numberOfRooms=1&numberOfAdults=2&currencyCode=USD&numberOfChildren=0&site=localuniversal&SWAQ=3TBM&lpqTotalRate=280.83&taxAmount=41.83&language=en_US&localeCode=en_US&deviceType=desktop&dateType=selected&hmGUID=42b36366-a22f-49ca-b774-387c74dc9e7f&refskin=SPG'
booking_url = 'https://www.booking.com/hotel/us/westin-cincinnati.html?aid=356929;label=metagha-link-localuniversalUS-hotel-379229_dev-desktop_los-1_bw-22_dow-Saturday_defdate-0_room-0_lang-en_curr-USD_gstadt-2_rateid-0_cid-;sid=fcf0e7461ab9e724bee9f2f30250833e;all_sr_blocks=37922901_91834395_2_0_0;bshb=2;checkin=2018-05-05;checkout=2018-05-06;dest_id=20097593;dest_type=city;dist=0;group_adults=2;group_children=0;hapos=1;highlighted_blocks=37922901_91834395_2_0_0;hpos=1;no_rooms=1;room1=A%2CA;sb_price_type=total;srepoch=1523662788;srfid=fb976f1ab838e7298ba9e3ed59787983961b2a5aX1;srpvid=362ea661a9c00045;type=total;ucfs=1&#hotelTmpl'
https://www.expedia.com/Cincinnati-Hotels-The-Westin-Cincinnati.h2972.Hotel-Information?chkin=5%2F5%2F2018&chkout=5%2F6%2F2018&rm1=a2&hwrqCacheKey=87fe693a-484c-4f0e-99bb-3b9d778ca916HWRQ1523665152558&regionId=943&vip=false&c=5c91d4fb-1ea2-4473-aeab-393bfbfe9c4b&mctc=10&exp_dp=269&exp_ts=1523665154432&exp_curr=USD&swpToggleOn=false&exp_pg=HSR
https://www.trip.com/hotels/cincinnati-hotel-detail-2870082/the-westin-cincinnati/?checkin=2018-05-05&checkout=2018-05-06&adult=1&children=0&ages=&city=1184&label=fM1_EzxxUUWNfeYsPPAmog&salestype=0&page=0&position=1&minprice=239&mproom=136313525_136311380&mincurr=USD&HighPrice=-1&LowPrice=-1&allianceid=15214&sid=1209572&ouid=05_05_2018_1_localuniversal_2870082_US_desktop_selected&pnotax=6_275000000;1499_725&from_page=searchResults&module=list&pctoken=&psource=top&link=book&tproom=136313525&tpshadow=0&tprate=711721402
https://vacation.hotwire.com/Cincinnati-Hotels-The-Westin-Cincinnati.h2972.Hotel-Information?chkin=5%2F5%2F2018&chkout=5%2F6%2F2018&rm1=a2&hwrqCacheKey=46535170-22fd-4a23-9051-ecb978d55dc6HWRQ1523665404356&regionId=178249&vip=false&c=c4af3cd0-22f0-438b-b8a9-8d7612eace8b&mctc=10&exp_dp=269.43&exp_ts=1523665404995&exp_curr=USD&swpToggleOn=false&exp_pg=HSR
https://www.priceline.com/stay/search/hotels/3000016793/20180505/20180506/1/?preferredHotelIds=51115&utm_medium=SHOP_PPC&utm_source=PLGOOGLEMSS&utm_campaign=HList&utm_content=META&utm_term=US_HP%7C51115_localuniversal_1%7C20180505%7Cdesktop%7Cuserdate%7Cpublic%7C490134989&refid=PLGOOGLEMSS&refclickid=US_HP%7C51115_localuniversal_1%7C20180505%7Cdesktop%7Cuserdate%7Cpublic%7C490134989&meta-id=HikTmzVyIHRZTnOK8sKqpZv-p9WEWwb-Ho6nRIAMGfFeXsAr3o3Mr56XGYtA_Rm9oHkK_4AZIciWvAhnFRfehds_YEn7L1LwJaypqxHStL9m-UBiYsiujJRtZb6-r8U5bEiKV_tpFPaXxwSQ7lIdr4Gly8oCiqAf-TCXWbwaH04Qo2p3CwM1zfgEN46jxG_2wZY1utXpHRkWFNB5M2LIcvSOEUD6RJT_DqpekllAq2SNEqvxEfar24ZVimx6M394ggZVcGCpyTzB7_hPbALkDgUtoOhSBvAY7t2EWpeehyZdlkNtaeivzzpSAlvlQ__NCsuuSMiKJUNpAmFrJGRKSJK3uPwcZnuLqbXLZV4HCiA0BqL7VoMPZkCWTIAUtP70rkSSJmlLT3qXl6cTJrUktVXu5Cdns4_JZkajTHpb4Q1SMypkz7YdTn-kuljw0gAgNf8ygmD1UgkwdR_Us6559jYnP02rKnkWjhF3QRsdRemfEUnULXQvALN9LY4igHMJO82DC2vzVVpQMe10QmFBBkUiyzSiNr5d_7xBjkTpktf4t2bS5bdun2UYx6rrlVK4&prefSource=EXTERNAL&currency=USD&displayedExchangeRate=1.0000&displayedCurr=USD&displayedCurrPrice=280.39&displayedTaxFees=41.39&pOSCountryCode=US&taxDisplayMode=BP&slingshot=1404
https://www.orbitz.com/Hotel-Search?MDPCID=ORBITZ-US.META.HPA.CORESEARCH-localuniversal-desktop.HOTEL&MDPDTL=htl.2972.20180505.20180506.DDF.22.CID.&mctc=10&startDate=5/5/2018&endDate=5/6/2018&selected=2972&adults=2&paandi=true
https://www.orbitz.com/Cincinnati-Hotels-The-Westin-Cincinnati.h2972.Hotel-Information?chkin=5%2F5%2F2018&chkout=5%2F6%2F2018&rm1=a2&hwrqCacheKey=42a02036-a8b0-419d-94a6-1e223df7c3e0HWRQ1523665765113&regionId=943&vip=false&c=3d155cef-f00a-48e7-83a4-94658eb982b1&mctc=10&exp_dp=269.43&exp_ts=1523665765899&exp_curr=USD&swpToggleOn=false&exp_pg=HSR
https://www.travelocity.com/Cincinnati-Hotels-The-Westin-Cincinnati.h2972.Hotel-Information?MDPCID=travelocity-US.META.HPA.CORESEARCH-localuniversal.HOTEL&MDPDTL=HTL.2972.20180505.20180506.DDF.22.CID.950332239&mctc=10&chkin=5/5/2018&chkout=5/6/2018&rm1=a2&paandi=true


# browser = webdriver.PhantomJS()
# browser.get(hotel_web_link)
# time.sleep(5)
#
# # wait = WebDriverWait(browser, 10)
# # # wait for the content to be present
# # class element_has_css_class(object):
# #   """An expectation for checking that an element has a particular css class.
# #
# #   locator - used to find the element
# #   returns the WebElement once it has the particular css class
# #   """
# #   def __init__(self, locator, css_class):
# #     self.locator = locator
# #     self.css_class = css_class
# #
# #   def __call__(self, driver):
# #     element = driver.find_element(*self.locator)   # Finding the referenced element
# #     if self.css_class in element.get_attribute("class"):
# #         return element
# #     else:
# #         return False
# # element = wait.until(element_has_css_class((By.ID, 'primary1'), "alertMessage"))
#
# file = open(curr_path+'/soup.txt','w')
# file.write(browser.page_source)
# file.close()
#
# if (browser.page_source.find('roomRate'))==-1:
#     input('roomRate not found in webpage, not waiting long enough?')
#
#
# soup = bs4.BeautifulSoup(browser.page_source)
# # print(soup.prettify())
# mydivs = soup.findAll("span", {"class": "roomRate"})
# print(mydivs)
# print(type(mydivs))
# print(len(mydivs))
# all_rates = []
# for tag in mydivs:
#     rates_str_list = re.findall(r'\d+', tag.string)
#     if len(rates_str_list)==1:
#         all_rates.append(rates_str_list[0])
#     elif len(rates_str_list)>1:
#         print('current tag has multiple numbers')
#         print(tag)
#     else:
#         print('no number found in current tag')
#         print(tag)
# print(all_rates)
# print(min(all_rates))

browser = webdriver.PhantomJS()
browser.get(booking_url)
time.sleep(10)
file = open(curr_path+'/booking.txt','w')
file.write(browser.page_source)
file.close()
#
# if (browser.page_source.find('roomRate'))==-1:
#     input('roomRate not found in webpage, not waiting long enough?')
#
# result = requests.get(booking_url)
# print(result.status_code)
# # print(result.headers)
# c = result.content
# soup = bs4.BeautifulSoup(c, "html.parser")
# print(soup.prettify())
# file = open(curr_path+'/booking.txt','w')
# file.write(soup.prettify())
# file.close()
'''
