"""
Script to interpret NLP results for sentiment classification
"""

import numpy as np

def open_file(file_name):
    with open(file_name, encoding="utf-8") as f:
        lines = f.readlines()
        
    total = 0
    positive = 0
    values = []
        
    lines = list(filter(lambda x: x != '\n', lines))
    for i in range(0, len(lines), 3):
        entry = lines[i: i + 3]
        category, score = check_sentiment(entry)
        if category == 1:
            values.append(score)
        else:
            values.append(1 - score) # negative label
        
        positive += category
        total += 1

    return positive, total, values
        
def check_sentiment(entry):
    """
    Format: 0 = original file
            1 = sample sentence
            2 = sentiment
    
    """    
    
    results = entry[2].split()
    sentiment = results[0]
    score = float(results[-1])
    
    if sentiment == "POSITIVE":
        return 1, score
    return 0, score


if __name__ == "__main__":
    keyword = "noise"
    
    total_pos = 0
    total_tot = 0
    all_values = []
    
    for i in range(1850, 2021, 10): 
        
        file_name = f"sentiment_results/{keyword}/{i}.txt"
        positive, total, values = open_file(file_name)
        total_pos += positive 
        total_tot += total 
        all_values.extend(values)
        
        result = f"{i}: {positive} / {total}"
        
        if total > 0:
            result += f" ({positive / total})"
        print(result)
        
    print(f"Overall: {total_pos} / {total_tot} ({total_pos / total_tot})")
    
    print()
    print(f"Mean:  {np.mean(all_values)}")
    print(f"St Dev:  {np.std(all_values)}")
    
    all_values.sort()
    vals = [round(x, 3) for x in all_values]
    print(vals)









    
    
    

