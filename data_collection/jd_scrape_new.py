from bs4 import BeautifulSoup
from selenium import webdriver

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

import os 

def format_title(title):    
    invalid = '<>:"/\|?*'
    for char in invalid:
        title = title.replace(char, "")
    title = ' '.join(title.split()) # Replace multiple spaces with 1
    title = title.lower().replace(" ", "_") # Now replace spaces with underscores
    title.replace("\n", "") # Get rid of newline characters???
    
    if len(title) > 128:
        title = title[:128] # truncate long titles
    return title

def talk_html(url, conf):
    browser = webdriver.Chrome()
    # browser.implicitly_wait(5)
    browser.get(url)
    # browser.implicitly_wait(10)
    delay = 1 # seconds
    while True:
        try:
            # check if javascript is loaded
            WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.TAG_NAME, "div")))
        except TimeoutException:
            break
        else:
            break

    html = browser.page_source
    return BeautifulSoup(html, features="html.parser")

def write_talk(talk, title, journal):
            
    talk_text = ""
    for elem in talk:
        cur_text = elem.text
        cur_text = cur_text.replace(" \n", " ")
        cur_text = cur_text.replace("\n", " ")
        talk_text += cur_text + "\n\n"
    
    
    file_name = journal + "/" + format_title(title) + ".txt"
    # print("writing", file_name)

    with open(file_name, "w", encoding="utf8") as f:
        # f.write(title + ".\n\n")  # don't actually need title in file
        f.write(talk_text)    
    
def get_talk(url, conf):
    # FORMAT: ... to 1970
    
    soup = talk_html(url, conf)

    try:
        header = soup.find_all("h1")[0]
        title = header.text        
        # print(title)
        
        talk = soup.find_all("div", "paragraph")     
    except IndexError:
        print(f"Having trouble with {url}")
        with open("failures.txt", "a") as f:
            f.write(f"{conf}: having trouble with {url}\n")
        return False  
        
    
    write_talk(talk, title, conf)
        
    return True 


        
def get_ids(journal_number):

    url = "https://journalofdiscourses.com/" + journal_number
    
    browser = webdriver.Chrome()
    # browser.implicitly_wait(5)
    browser.get(url)
    # browser.implicitly_wait(10)
    delay = 1 # seconds
    while True:
        try:
            # check if javascript is loaded
            WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.TAG_NAME, 'div')))
        except TimeoutException:
            break
        else:
            break

    html = browser.page_source
    soup = BeautifulSoup(html, features="html.parser")
    # print(soup)
    
    links = soup.find_all("div", "media")
    
    # Grab info about talk like title and subtitle?
    
    return range(1, len(links) + 1) 

def run_scraper():
    journals = list(map(str, range(7, 27)))
    
    for j in journals:
            
            talk_ids = get_ids(j)
            
            conf_dir = "journal_of_discourses_NEW/" + j
            if not os.path.exists(conf_dir):
                os.makedirs(conf_dir)
                
            print(f"Starting journal {j}")
            
            counter = 0
            for talk in talk_ids:
                url = "https://journalofdiscourses.com/" + j + "/" + str(talk)
                success = get_talk(url, conf_dir)
                if not success:
                    counter += 1 
            print(f"Finished journal {j}")
            print(f"{len(talk_ids) - counter} talks written, {counter} failures")
            print() 
            
if __name__ == '__main__':
    run_scraper()
    # print(get_ids("1"))
                
            
    
            

    


