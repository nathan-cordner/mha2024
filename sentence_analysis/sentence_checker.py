"""
  Python script to pull sentences from text file based on word pattern
  
  Modified from https://stackoverflow.com/questions/55553423/using-a-keyword-to-print-a-sentence-in-python
"""

import re, os
from colorama import Fore, Back, Style

def load_sentences(file):
    with open(file, encoding="utf-8") as f:
        lines = f.readlines()
        
    filtered = [line.strip() for line in lines if not ".txt" in line]
    filtered = [line for line in filtered if line] # remove empty strings
    return filtered

def sentence_bound(text, place, end_place, left, right):
    """
    keyword is found in text[place:end_place]    
    """
    line_end_chars = ["!", "?", "."] #, ";"]
    
    lower_bound = 0
    left_text = text[left:place]
    
    for char in line_end_chars:
        val = left_text.rfind(char)
        if val > lower_bound:
            lower_bound = val 
    lower_bound += left + 1 # adjust to full string    
        
    upper_bound = right
    right_text = text[end_place:right]
    
    for char in line_end_chars:
        val = right_text.find(char)
        if val < upper_bound and val != -1:
            upper_bound = val
    upper_bound += end_place
    
    return lower_bound, upper_bound 
    

def find_sentences(file, keyword, out_file):
    
    WINDOW = 500
    
    with open(file, encoding="utf-8") as f:
        text = f.read()
    text = text.replace("\n", " ") # get rid of pesky newline characters
    
    with open(out_file, "a", encoding="utf-8") as f:
        found = False 
        get_next = True # initial setting
        index = 0
        
        while get_next:
            get_next = False 
            reduced = text[index:]
            
            
            if keyword in reduced:                
                
                place = reduced.index(keyword) # get next occurance
                place += index # factor in cut-off part
                end_place = place + len(keyword)
                
                index = end_place # prepare for next iteration
                get_next = True
                
                left = place - WINDOW
                if place < WINDOW:
                    left = 0
                right = place + WINDOW 
                if place + WINDOW > len(text):
                    right = len(text)              
                
                print("Context: ")
                
                """
                TODO:  highlight predicted sentence
                -- fix loop to look at more than one instance
                   of keyword in file
                
                """
                
                lower_bound, upper_bound = sentence_bound(text, place, end_place, left, right)
                
                
                print(text[left:lower_bound], end="")
                print(Back.YELLOW + text[lower_bound:upper_bound], end ="")
                print(Style.RESET_ALL, end="")
                print(text[upper_bound:right])
                line = input("Text to save: ")
                
                if line: # skip empty lines
                    if not found:
                        found = True
                        f.write("\n\n" + file)
                    f.write("\n\n" + line)
                print()
                
def remove_scripture_reference(line, text, lower_bound, upper_bound):
    first = True
    remove_next = False
    keep = []    
    
    if ":" in line:
        # check to see if it's a reference
        words = line.split()
        
        for i in range(len(words)):
            word = words[i]
            
            if remove_next:
                if not word[-1] == ",":
                    remove_next = False
                continue
            
            if word.lower() == "(see" or word.lower() == "[see":
                continue
            
            if ":" in word:
                parts = word.split(":")
                if len(parts) > 1:
                    x = parts[0]
                    y = parts[1]
                    if y == '':
                        # : appears at end
                        keep.append(word)
                
                    elif x.isnumeric() or y.isnumeric():
                        if len(keep) >= 1:
                            # pop off previous value
                            last = keep.pop().lower()
                            
                            
                            if len(keep) >= 1 and keep[-1].isnumeric():
                                # 1, 2, 3, 4 Nephi etc.
                                keep.pop()                         
                            
                            elif last == "f" or last == "covenants":
                                # A of F, Doctrine and Covenants
                                keep.pop()
                                keep.pop()
                            # last = keep[-1]
                            # if last == "(see":
                            #     keep.pop()                        
                
                        
                        if first: # INDENT ONE MORE??
                            # print("BEFORE")
                            # print(line)
                            # print()
                            first = False
                        
                            
                        if y[-1] == ",":
                            remove_next = True
                            
                        
                else:
                    keep.append(word)
            else:
                keep.append(word)
                
    WINDOW = 500
    recursion_result = ''            
                
    if not keep:
        keep = line.split()
    
    # PEEK AT NEXT WORD AFTER SENTENCE
    if not upper_bound >= len(text) - 2:
        right_text = text[upper_bound:upper_bound + WINDOW]
        right_words = right_text.split()
        if right_words and ":" in right_words[0]:
            # check for scripture reference 
            parts = right_words[0].split(":")
            if len(parts) > 1:
                x = parts[0]
                y = parts[1]
                if y == '':
                    # : appears at end, do nothing
                    pass 
                
                elif x.isnumeric() or y.isnumeric():
                    if len(keep) >= 1:
                        # pop off previous value
                        last = keep.pop().lower()  
                        
                        
                          
                        if len(keep) >= 1 and keep[-1].isnumeric():
                            # 1, 2, 3, 4 Nephi etc.
                            keep.pop()                         
                          
                        elif last == "f" or last == "covenants":
                            # A of F, Doctrine and Covenants
                            keep.pop()
                            keep.pop()
                        last = keep[-1].lower()
                        if last == "(see" or last == "[see":
                            keep.pop()  
                        
                        if first:                            
                            first = False
                            
        elif "." in right_text[0]:
            
            # Check for middle initial or abbreviation
            if keep and (len(keep[-1].replace(".", "")) == 1 or keep[-1].lower().replace(".", "") == "st"):
                # IT'S RECURSION TIME!!!!!!!!!!!!!!!!!
                # print("recursion")
                line_end_chars = ["!", "?", "."]
                
                right_text = text[upper_bound+1:]
                
                right_bound = len(text)
                
                for char in line_end_chars:
                    val = right_text.find(char)
                    if val < right_bound and val != -1:
                        right_bound = val
                right_bound += upper_bound + 1
                
                new_line = text[upper_bound + 1:right_bound]
                
                recursion_result, new_index = remove_scripture_reference(new_line, text, lower_bound, right_bound)
                if new_index > upper_bound:
                    upper_bound = new_index
                # print("result", recursion_result)
    
                
    if not first:
        print("BEFORE")
        print(line)
        print()
        
        line = " ".join(keep)


    if line and line[0] == '”':
        line = line[1:] # get rid of extraneous unicode quote 

    if not first:
        print("AFTER")
        print(line + recursion_result)
        print()               
        
    return line + recursion_result, upper_bound
    
def tester(file, keyword):
    with open(file, encoding="utf-8") as f:
        text = f.read()
    text = text.replace("\n", " ") # get rid of pesky newline characters

    WINDOW = 1000

    found = False 
    get_next = True # initial setting
    index = 0
        
    while get_next:
        get_next = False 
        reduced = text[index:]
            
        if keyword in reduced:                
                
            place = reduced.index(keyword) # get next occurance
            place += index # factor in cut-off part
            end_place = place + len(keyword)
                
            index = end_place # prepare for next iteration
            get_next = True
                
            left = place - WINDOW
            if place < WINDOW:
                left = 0
            right = place + WINDOW 
            if place + WINDOW > len(text):
                right = len(text)              
                                                
            lower_bound, upper_bound = sentence_bound(text, place, end_place, left, right)
                
            line = text[lower_bound:upper_bound+1]
            clean_result, index = remove_scripture_reference(line, text, lower_bound, upper_bound)
            
            
            

def search_doctrine_and_covenants(keyword):
    out_file = f"keyword_searches/{keyword}/doctrine_and_covenants.txt"
    for i in range(1, 138):
        file = f"doctrine_and_covenants/section_{i}.txt"
        find_sentences(file, keyword, out_file)   

def search_journal_of_discourses(keyword):
    out_file = f"keyword_searches/{keyword}/journal_of_discourses.txt"
    for i in range(1, 27):
        print(f"Staring volume {i}")
        directory = f"journal_of_discourses/{i}/"
        files = os.listdir(directory)
        for file in files:
            find_sentences(directory + file, keyword, out_file)
            
def search_improvement_era(keyword):
    title = "improvement_era"
    out_file = f"keyword_searches/{keyword}/{title}.txt"
    directory = f"{title}_edits/"
    files = os.listdir(directory)
    for file in files:
        find_sentences(directory + file, keyword, out_file)
        
def search_conferences(keyword):
    title = "conferences"
    out_file = f"keyword_searches/{keyword}/{title}.txt"
    for i in range(1942, 2024):
        print(i)
        for letter in "AO":                
            directory = f"{title}_NEW/{i}_{letter}/"
            files = os.listdir(directory)
            for file in files:
                # find_sentences(directory + file, keyword, out_file)
                tester(directory + file, keyword)

keyword = "worship"
# search_doctrine_and_covenants(keyword)
# search_journal_of_discourses(keyword)
# search_improvement_era(keyword)
search_conferences(keyword)



# lines = load_sentences(f"keyword_searches/{keyword}/journal_of_discourses.txt")
# for line in lines:
#     print(line)








