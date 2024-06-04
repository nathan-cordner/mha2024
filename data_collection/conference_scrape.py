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
            WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'title1')))
        except TimeoutException:
            break
        else:
            break

    html = browser.page_source
    return BeautifulSoup(html, features="html.parser")

def write_talk(talk, title, speaker, conf):
    
    # kill all link elements
    for script in talk(["sup"]):
        script.extract()    # rip it out

    # get text
    title_text = title.get_text()
    speaker_text = speaker.get_text()
    if "by" in speaker_text[:2].lower():
        speaker_text = speaker_text[3:] # remove "By " at the start
    talk_text = talk.get_text()

    last_name = speaker_text.split()[-1].lower()
    # store by date? 
    
    file_name = conf + "/" + last_name + "_" + format_title(title_text) + ".txt"
    # print("writing", file_name)

    with open(file_name, "w", encoding="utf8") as f:
        f.write(title_text + "\n")
        f.write(speaker_text + "\n")
        f.write(talk_text)    
    

def get_talk(url, conf):
    
    # FORMAT: works for 2019 to 2023
    
    soup = talk_html(url, conf)

    try:
        title = soup.find_all("h1")[0]
        speaker = soup.find_all("p", "author-name")[0]
    except IndexError:
        print(f"Having trouble with {url}")
        with open("failures.txt", "a") as f:
            f.write(f"{conf}: having trouble with {url}\n")
        return False  

    """
    try: 
        title = soup.find_all("h1", id="title1")[0]
    except IndexError: 
        try:
            title = soup.find_all("h1", id="title56")[0] # the Uchtdorf Exception
            speaker = soup.find_all("p", id="p4")[0]
        except IndexError:
            try:
                title = soup.find_all("h1", id="p4")[0]
                speaker = soup.find_all("p", id="p5")[0]
            except IndexError:            
                print(f"1. Having trouble with {url}")
                return 
    try:        
        speaker = soup.find_all("p", id="author1")[0]
    except IndexError:
        try:
            speaker = soup.find_all("p", id="p1")[0]
        except IndexError:
             print(f"2. Having trouble with {url}")
             return       
    """
    talk = soup.find_all("div", "body-block")[0]
    
    write_talk(talk, title, speaker, conf)
        
    return True 

def get_talk2(url, conf):
    # FORMAT: 1971 to 2018
    
    soup = talk_html(url, conf)

    try:
        title = soup.find_all("h1")[0]
        speaker_block = soup.find_all("div", "byline")[0]     
        speaker = speaker_block.find_all("p")[0]
        talk = soup.find_all("div", id="primary")[0]     
    except IndexError:
        print(f"Having trouble with {url}")
        with open("failures.txt", "a") as f:
            f.write(f"{conf}: having trouble with {url}\n")
        return False  
        
    
    write_talk(talk, title, speaker, conf)
        
    return True 

def get_talk3(url, conf):
    # FORMAT: ... to 1970
    
    soup = talk_html(url, conf)

    try:
        gchead = soup.find_all("div", "gchead")[0]
        title = gchead.find_all("p")[0]
        speaker = gchead.find_all("p")[1]
        talk = soup.find_all("div", "gcbody")[0]     
    except IndexError:
        print(f"Having trouble with {url}")
        with open("failures.txt", "a") as f:
            f.write(f"{conf}: having trouble with {url}\n")
        return False  
        
    
    write_talk(talk, title, speaker, conf)
        
    return True 


        
def get_ids(year, month):

    url = "https://scriptures.byu.edu/citation_index/gc_ajax/" + year + "/" + month
    
    browser = webdriver.Chrome()
    # browser.implicitly_wait(5)
    browser.get(url)
    # browser.implicitly_wait(10)
    delay = 1 # seconds
    while True:
        try:
            # check if javascript is loaded
            WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'scicrumb')))
        except TimeoutException:
            break
        else:
            break

    html = browser.page_source
    soup = BeautifulSoup(html, features="html.parser")
    # print(soup)
    
    talk_ids = []
    links = soup.find_all("a")
    for link in links:
        attributes = link.attrs
        if "onclick" in attributes:
            if "getTalk" in attributes["onclick"]:
                talk_id = attributes["onclick"].split("'")[1]
                talk_ids.append(talk_id)
    return talk_ids 

def run_scraper():
    years = list(map(str, range(1970, 1941, -1)))
    months = "OA"
    
    for year in years:
        for month in months:
            # if year == "2020" and month == "A":
            #     continue 
            
            talk_ids = get_ids(year, month)
            talk_ids = list(map(hex, map(int, talk_ids)))
            talk_ids = [talk_id[2:] for talk_id in talk_ids if "0x" in talk_id]
            
            conf = year + "_" + month
            conf_dir = "conferences/" + conf
            if not os.path.exists(conf_dir):
                os.makedirs(conf_dir)
                
            print(f"Starting {conf}")
            
            counter = 0
            for talk in talk_ids:
                url = "https://scriptures.byu.edu/#:t" + str(talk)
                success = get_talk3(url, conf_dir)
                if not success:
                    counter += 1 
            print(f"Finished {conf}")
            print(f"{len(talk_ids) - counter} talks written, {counter} failures")
            print() 
            
if __name__ == '__main__':
    run_scraper()
                
            
    
            

    
# print(get_ids("2021", "O"))
   
"""
url = "https://scriptures.byu.edu/#:t21df:gc1"
conf = "conferences/2022_april"

hex_vals = [hex(i)[2:].zfill(2) for i in range(256)]
start = "87"
end = "87"
i = hex_vals.index(start)
while True:
    url = "https://scriptures.byu.edu/#:t21" + hex_vals[i] + ":g8c0"
    get_talk(url, conf)
    if hex_vals[i] == end:
        break
    i += 1
"""

    


