import secrets
import string
import time
import os
import sys
import random
import threading
from datetime import date
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import requests

log_file = "log.txt"

def status(text):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\033[1;34m" + text + "\033[0m")
    with open(log_file, 'a') as log:
        log.write(text + "\n")

# Config
Accounts = 1  # how many accounts
MaxWindows = 3
ActualWindows = 0

# URLs
first_names_url = "https://raw.githubusercontent.com/H20CalibreYT/RobloxAccountCreator/main/firstnames.txt"
last_names_url = "https://raw.githubusercontent.com/H20CalibreYT/RobloxAccountCreator/main/lastnames.txt"
roblox_url = "https://www.roblox.com/"

status("Getting first names...")
first_names_response = requests.get(first_names_url)
status("Getting last names...")
last_names_response = requests.get(last_names_url)

# Check if name loading was successful
if first_names_response.status_code == 200 and last_names_response.status_code == 200:
    first_names = list(set(first_names_response.text.splitlines()))
    last_names = list(set(last_names_response.text.splitlines()))
else:
    status("Name loading failed. Re-Execute the script.")
    sys.exit()

# File paths
files_path = os.path.dirname(os.path.abspath(sys.argv[0]))
text_files_folder = os.path.join(files_path, "Accounts")
text_file = os.path.join(text_files_folder, f"Accounts_{date.today()}.txt")
text_file2 = os.path.join(text_files_folder, f"AltManagerLogin_{date.today()}.txt")

# Create folder if it does not exist
if not os.path.exists(text_files_folder):
    os.makedirs(text_files_folder)

# Lists of days, months and years
days = [str(i + 1) for i in range(10, 28)]
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
years = [str(i + 1) for i in range(1980, 2004)]

# Password generator
def gen_password(length):
    status("Generating a password...")
    chars = string.ascii_letters + string.digits + "Ññ¿?¡!#$%&/()=\/¬|°_-[]*~+"
    password = ''.join(secrets.choice(chars) for _ in range(length))
    return password

# Username generator
def gen_user(first_names, last_names):
    status("Generating a username...")
    first = secrets.choice(first_names)
    last = secrets.choice(last_names)
    full = f"{first}{last}_{secrets.choice([i for i in range(1, 999)]):03}"
    return full

def create_account(url, first_names, last_names):
    global ActualWindows
    try:
        status("Starting to create an account...")
        cookie_found = False
        username_found = False
        elapsed_time = 0

        status("Initializing webdriver...")
        driver = webdriver.Edge()
        driver.set_window_size(1200, 800)
        driver.set_window_position(0, 0)
        driver.get(url)
        time.sleep(2)

        # HTML items
        status("Searching for items on the website")
        username_input = driver.find_element("id", "signup-username")
        username_error = driver.find_element("id", "signup-usernameInputValidation")
        password_input = driver.find_element("id", "signup-password")
        day_dropdown = driver.find_element("id", "DayDropdown")
        month_dropdown = driver.find_element("id", "MonthDropdown")
        year_dropdown = driver.find_element("id", "YearDropdown")
        male_button = driver.find_element("id", "MaleButton")
        female_button = driver.find_element("id", "FemaleButton")
        register_button = driver.find_element("id", "signup-button")

        status("Selecting day...")
        Selection = Select(day_dropdown)
        Selection.select_by_value(secrets.choice(days))
        time.sleep(0.3)

        status("Selecting month...")
        Selection = Select(month_dropdown)
        Selection.select_by_value(secrets.choice(months))
        time.sleep(0.3)

        status("Selecting year...")
        Selection = Select(year_dropdown)
        Selection.select_by_value(secrets.choice(years))
        time.sleep(0.3)

        while not username_found:
            status("Selecting username...")
            username = gen_user(first_names, last_names)
            username_input.clear()
            username_input.send_keys(username)
            time.sleep(1)
            if username_error.text.strip() == "":
                username_found = True
        
        status("Selecting password...")
        password = gen_password(25)
        password_input.send_keys(password)
        time.sleep(0.3)

        status("Selecting gender...")
        gender = secrets.choice([1,2])
        if gender == 1:
            male_button.click()
        else:
            female_button.click()
        time.sleep(0.5)

        status("Registering account...")
        register_button.click()
        time.sleep(3)

        # Wait until the account creation limit is reset
        try:
            driver.find_element("id", "GeneralErrorText")
            driver.quit()
            for i in range(360):
                status(f"Limit reached, waiting... {i+1}/{360}")
                time.sleep(1)
        except:
            pass

        # Wait until the cookie is found or the maximum time has passed
        while not cookie_found and elapsed_time < 180:
            status("Waiting for the cookie...")
            time.sleep(3)
            elapsed_time += 3
            for cookie in driver.get_cookies():
                if cookie.get('name') == '.ROBLOSECURITY':
                    cookie_found = True
                    break
        if cookie_found:
            status("Cookie found...")
            result = [cookie.get('value'), username, password]
            save_account_info(result)
            save_altmanager_login(result)
            if result is not None:
                status("Ready!")
                time.sleep(3)
                ActualWindows -= 1
                status(f"Pestanas abiertas: {ActualWindows}")
                pass

    except:
        status(f"Pestanas abiertas: {ActualWindows}")
        ActualWindows -= 1

# Save account information to text file
def save_account_info(account_info):
    status("Saving account info...")
    with open(text_file, 'a') as file:
        file.write(f"Username: {account_info[1]}\nPassword: {account_info[2]}\nCookie: {account_info[0]}\n\n\n")

# Save login information for AltManager
def save_altmanager_login(account_info):
    with open(text_file2, 'a') as file:
        status("Saving account login (for alt manager)...")
        file.write(f"{account_info[1]}:{account_info[2]}\n")

        # Create accounts
        for _ in range(Accounts):
         while ActualWindows >= MaxWindows:
             status(f"Esperando... {ActualWindows}/{MaxWindows}")

             try:
              status("Starting to login...")
              if cookie_found:
                          status("Cookie found...")
                          result = [cookie.get('value'), account_info[1], account_info[2]]
                          save_account_info(result)
                          save_altmanager_login(result)
                          # Loguearse y establecer la descripción de perfil
                          status("Logging in...")
                          driver = webdriver.Edge()
                          driver.set_window_size(1200, 800)
                          driver.set_window_position(0, 0)
                          status("Logged in")
                          driver.get(roblox_url)
                          driver.add_cookie({'name': '.ROBLOSECURITY', 'value': result[0], 'domain': '.roblox.com'})
                          driver.refresh()
                          time.sleep(2)
                          status("Setting description...")

                          set_profile_description(driver, "aaaaa")

                          driver.quit()

                          status("Successfully login and profile description set!")
                          time.sleep(10)
                          ActualWindows -= 1
                          status(f"Pestanas abiertas: {ActualWindows}")

             except Exception as e:
                   status(f"Error: {e}")
                   ActualWindows -= 1
                   time.sleep(1)
        ActualWindows += 1
    account_thread = threading.Thread(target=create_account, args=(roblox_url, first_names, last_names))
    account_thread.start()





    
    time.sleep(1)
def set_profile_description(driver, description):
    try:
        status("Setting profile description...")
        driver.get("https://www.roblox.com/my/account")
        time.sleep(2)
        edit_profile_button = driver.find_element_by_xpath("//a[@data-stat-label='Profile_Description']")
        edit_profile_button.click()
        time.sleep(2)
        description_input = driver.find_element_by_id("AboutTextArea")
        description_input.clear()
        description_input.send_keys(description)
        save_button = driver.find_element_by_id("AboutSaveButton")
        save_button.click()
        status("Profile description set successfully!")
    except Exception as e:
        status("Failed to set profile description: " + str(e))

# Función para generar una descripción aleatoria de perfil
def gen_profile_description():
    return random.choice(profile_descriptions)


            
