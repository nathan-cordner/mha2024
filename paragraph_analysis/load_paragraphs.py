"""
Script to read in paragraphs from given file

FORMAT: 
    -- First line is a title (to be skipped)
    -- paragraphs separated by one or more blank lines 
"""

import os


def get_paragraphs(file_name):
    paragraphs = []
    
    with open(file_name, encoding="utf-8") as f:
        #next(f) 
        #next(f) # get rid of blank line 
        cur_paragraph = ""
        for line in f:
            val = line.strip() 
            if val:
                cur_paragraph += f"{val} "
            else:
                if cur_paragraph:
                    paragraphs.append(cur_paragraph)
                cur_paragraph = ""
        if cur_paragraph:
            paragraphs.append(cur_paragraph) # just in case
        
    return paragraphs 

"""
p = get_paragraphs("jfs/1890/1897_o.txt")
for s in p:
    print(s)
    print()
"""

def check_list(keyword, nonwords, p):
    
    if not keyword in p:
        return False
    
    for k in nonwords:
        if k in p:
            return False 
    return True

prophet = "nelson"
keyword = "prais"
nonwords = ["reverence", "reverent", "worship"]

years = range(1980, 2021, 10)

counter = 0

with open(f"{prophet}_praise_paragraphs.txt", "w", encoding="utf-8") as f:
    for year in years:
        # print(f"Starting {year}")
        in_dir = f"{prophet}/{year}/"
        # out_dir = f"drive/MyDrive/Colab Notebooks/{prophet}_results/{year}/"
    
        files = os.listdir(in_dir)
        for my_file in files:
            paragraphs = get_paragraphs(f"{in_dir}{my_file}")
            flag = False 
            for p in paragraphs: 
                if check_list(keyword, nonwords, p.lower()):
                    counter += 1
                    if not flag:
                        flag = True
                        f.write(my_file + "\n\n")
                    f.write(p + "\n\n")
                    # print(p)
                    # print()
                    break
                # if flag:
                #     print(my_file)
                #     break
print(counter)
            
        
    

print("Finished!")