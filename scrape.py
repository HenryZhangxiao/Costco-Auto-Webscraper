import os
import time
import argparse
import requests
import platform
import shutil
import stat
from discordwebhook import Discord
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from webdriver_auto_update.webdriver_manager import WebDriverManager

DISCORD_WEBHOOK = 'https://discord.com/api/webhooks/1296690849270206527/qZCQNQcx6ShnyWYD-lBxhTEMXgoctMyb-NySIjClH9ff8rQ07O7xikGoqIs1rupMTCgz'

# Target directory to store chromedriver
if platform.system() == "Windows":
    driver_directory = 'drivers\windows'
elif platform.system() == "Darwin":
    driver_directory = 'drivers/mac'
elif platform.system() == "Linux":
    driver_directory = 'drivers/linux'

# Create an instance of WebdriverAutoUpdate
driver_manager = WebDriverManager(driver_directory)


parser = argparse.ArgumentParser(description='An automated booking script for Carleton Library rooms')

parser.add_argument('--headless', action='store_true', default=False, required=False,
                    help='Runs the program in headless mode (Does not open the browser). Default is false')
args = parser.parse_args()


class Browser:
    #browser, service, options = None, None, Options()
    
    def __init__(self, driver: str):
        self.service = Service(driver)
        self.options = Options()
        self.options.add_argument("--log-level=1")
        if args.headless == True:
            self.options.add_argument("--headless=new")
            self.options.add_argument("--log-level=1")
        self.browser = webdriver.Chrome(service=self.service, options=self.options)

    #Opens the desired page to [url]
    def open_page(self, url: str):
        self.browser.get(url)

    #Closes the browser
    def close_browser(self): 
        self.browser.close()
    
    def refresh(self):
        self.browser.get(self.browser.current_url)
        self.browser.refresh

    #Adds input [text] to element [value]
    def add_input(self, by: By, value: str, text: str):
        field = self.browser.find_element(by=by, value=value)
        field.send_keys(text)
        time.sleep(0.5)
        
    #Clicks button found by [by] with identifier [value]
    def click_button(self, by: By, value: str): 
        button = self.browser.find_element(by=by, value=value)
        button.click()
        time.sleep(1)
        
    #Books the room
    def scrape(self):
        global name

        browser.open_page('https://tires.costco.ca/')
        self.click_button(by=By.ID, value='scheduleappointment') #Select dropdown menu

        select = Select(self.browser.find_element(by=By.ID,value='ddlYearAppointments'))
        select.select_by_value('2018')

        select = Select(self.browser.find_element(by=By.ID,value='ddlMakeAppointments'))
        select.select_by_value('Toyota')

        select = Select(self.browser.find_element(by=By.ID,value='ddlModelAppointments'))
        select.select_by_value('RAV4')

        select = Select(self.browser.find_element(by=By.ID,value='ddlOptionAppointments'))
        select.select_by_value('XLE')
        
        self.add_input(by=By.ID, value='txtZipCodeByVehicleApts', text='K2K 0E8')

        self.click_button(by=By.ID, value='btnVehicleSelApts')
        time.sleep(5)
        
        self.click_button(by=By.XPATH, value='/html/body/div[2]/div/div/div[2]/div[1]/div[3]/div[1]/ol/li[1]/div[3]/button')
        time.sleep(2)
        self.open_page('https://waitwhile.com/locations/costcotire-00541/services/services?registration=booking&OMHRMzzTYuLW47ZlM2kD=2018+Toyota+RAV4+XLE&service=8Npus5b4JBG4Xsg4EWNc')

        time.sleep(2)
    
        self.click_button(by=By.XPATH, value='/html/body/div/div/div/div/div/div/div[2]/form/div[1]/div/div/div/div[2]/fieldset/div/div/div[2]/button[5]')
        time.sleep(2)
        try:
            while "No available times for the next" in self.browser.find_element(by=By.XPATH, value='/html/body/div[1]/div/div/div/div/div/div[2]/form/div[1]/div/div/div[2]/div[2]/fieldset/div/div/div/div/div[4]/p[2]').text:
                print("Waiting")
                time.sleep(600)
                browser.refresh()
                time.sleep(5)
            discord.post(content="Booking available")
        except:
            discord.post(content="Booking available")
            

# Main Function
if __name__ == '__main__':

    discord = Discord(url=DISCORD_WEBHOOK)

    # Call the main method to manage chromedriver
    print("\n---ENSURING LATEST VERSION OF CHROMEDRIVER---\n")
    driver_manager.main()
    time.sleep(2)

    #Support for different architectures
    if platform.system() == "Windows":
        try:
            shutil.move("drivers\windows\chromedriver-win64\chromedriver.exe", "drivers\windows\chromedriver.exe")
            try:
                shutil.rmtree('drivers\windows\chromedriver-win64')
            except OSError as e:
                print("Error: %s - %s." % (e.filename, e.strerror))
        except:
            pass
        os.chmod('drivers\windows\chromedriver.exe', stat.S_IRWXU)
        browser = Browser('drivers\windows\chromedriver.exe')
    elif platform.system() == "Darwin":
        try:
            shutil.move("drivers/mac/chromedriver-mac-arm64/chromedriver", "drivers/mac/chromedriver")
            try:
                shutil.rmtree('drivers/mac/chromedriver-mac-arm64')
            except OSError as e:
                print("Error: %s - %s." % (e.filename, e.strerror))
        except:
            pass
        os.chmod('drivers/mac/chromedriver', stat.S_IRWXU)
        browser = Browser('drivers/mac/chromedriver')
    elif platform.system() == "Linux":
        try:
            shutil.move("drivers/linux/chromedriver-linux64/chromedriver", "drivers/linux/chromedriver")
            try:
                shutil.rmtree('drivers/linux/chromedriver-linux64')
            except OSError as e:
                print("Error: %s - %s." % (e.filename, e.strerror))
        except:
            pass
        os.chmod('drivers/linux/chromedriver', stat.S_IRWXU)
        browser = Browser('drivers/linux/chromedriver')

    print("\n-------OPENING PAGE-------\n")
    try:
        browser.scrape()
        print("-------------------SUCCESS-------------------\n\n\n")
    except:
        print("-----------FAILED TO SCRAPE-----------\n")
        print("---------------EXITING PROGRAM---------------\n\n")
        exit()
