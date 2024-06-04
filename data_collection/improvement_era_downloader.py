from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.request import urlretrieve
from urllib.request import HTTPError

def construct_url(index_val, end):
    start = "https://ia600700.us.archive.org/"
    middle = "/items/conferencereport"
    return f"{start}{index_val}{middle}{end}"

def get_file(year, month, end):
        
    index_val = 1 # most are 31, but not all?
    while True:        
        try: 
            page = urlopen(construct_url(index_val, end))
        except HTTPError:
            index_val += 1
        else:
            break
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    
    file_name = ""
    for tag in soup.find_all("a"):
        if ".txt" in tag.string:
            file_name = tag.string
            break
    if file_name == "":
        print(f"Missing {year}_{month}")
        return 
        
    save_file = f"improvement_era/{year}_{month}.txt"
    file_link = f"{construct_url(index_val, end)}{file_name}"
    print(file_link)
    
    urlretrieve(file_link, save_file)
    print(f"Done with {year}_{month}")


# url = "https://ia600700.us.archive.org/31/items/conferencereport"

months = ["A", "O"]

# Available starting in 1897, up to 1970 or so
for year in range(1912, 1942):
    for month in months:
        if month == "A":
            if year == 1897:
                continue # no april 1897 issue
            end = f"{year}a/"
        else:
            end = f"{year}sa/"
        get_file(year, month, end)
            
        
        
        
        