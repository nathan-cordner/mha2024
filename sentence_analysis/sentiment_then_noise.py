"""
Script to check sentiment AND noise-level 
"""

from score_sentiment import check_sentiment 
from score_noise import check_noise

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd

def read_sentiment(file_name):
    with open(file_name, encoding="utf-8") as f:
        lines = f.readlines()
        
    results = []
        
    lines = list(filter(lambda x: x != '\n', lines))
    for i in range(0, len(lines), 3):
        entry = lines[i: i + 3]
        category, score = check_sentiment(entry)
        if category == 1: # positive label
            value = score
        else:
            value = 1 - score # negative label
            
        # value / sentence pairs
        results.append((value, entry[1]))

    return results

def read_noise(file_name):
    with open(file_name, encoding="utf-8") as f:
        lines = f.readlines()
        
    results = []
        
    lines = list(filter(lambda x: x != '\n', lines))
    for i in range(0, len(lines), 6):
        entry = lines[i: i + 6]
        label, score = check_noise(entry)
        if label == "quiet":
            value = score 
        else:
            value = 4 - score 
            
        # FILTER
        
            
        results.append((value, entry[1]))
    return results
    
def get_results(keyword, year, keep_word = None, exclude_word = None):
    noise_file = f"noise_results/{keyword}/{year}.txt"
    sentiment_file = f"sentiment_results/{keyword}/{year}.txt"
    
    sentiment_results = read_sentiment(sentiment_file)
    noise_results = read_noise(noise_file)
    
    assert len(sentiment_results) == len(noise_results)  # sanity check
    
    pairs = []
    
    for i in range(len(sentiment_results)):
        noise = noise_results[i]
        sentiment = sentiment_results[i]
        
        
        # CHECK EXAMPLES
        
        if keep_word or exclude_word:
            if exclude_word:
                # MULTIPLE FILTER WORDS FOR EXCLUSION
                flag = False
                for fw in exclude_word:
                    if fw in noise[1].lower():
                        flag = True
                        break
                if not flag:
                    if not keep_word:
                        pairs.append((noise[0], sentiment[0], year)) # NOISE, SENTIMENT PAIR 
                    elif keep_word in noise[1].lower():
                        # SINGLE WORD, FILTER FOR INCLUSION
                        pairs.append((noise[0], sentiment[0], year)) # NOISE, SENTIMENT PAIR
                
            elif keep_word in noise[1].lower():
                # SINGLE WORD, FILTER FOR INCLUSION
                pairs.append((noise[0], sentiment[0], year)) # NOISE, SENTIMENT PAIR
        else:
            pairs.append((noise[0], sentiment[0], year)) # NOISE, SENTIMENT PAIR
    return pairs

def get_all_results(keyword, keep_word = None, exclude_word = None):
    results = []
    for year in range(1850, 2021, 10):
    # for year in range(1950, 2021, 10):    
        cur_results = get_results(keyword, year, keep_word, exclude_word)
        if cur_results:         
            results.extend(cur_results)
    print(f"Total samples:  {len(results)}")

    return results
  


def sampled_keyword(keyword, exclude_word):
    keywords = ["praise", "revere", "worship"]
    keywords += ["shout", "whisper", "noise", "quiet"]
    # keywords += ["sacrament"]
    
    total_results = []

    for k in keywords:
        cur_results = get_all_results(k, keyword, exclude_word)
        total_results.extend(cur_results)
        
    print(f"Total samples:  {len(total_results)}")
      
    
    return total_results
    
    # results_loop(keyword, total_results)
    # line_plots(keyword, total_results)     

    
def grouped_keyword():
    
    """
    ### WORSHIP TERMS
    keyword = "worship terms"
    keywords = ["praise", "revere", "worship"]
    
    total_results = []
    filters = [None, ["prais"], ["prais", "rever"]]
    """
    
    

    ### NOISE TERMS
    keyword = "volume terms"
    keywords = ["noise", "quiet", "shout", "whisper"]
    
    total_results = []
    filters = [None, ["nois"], ["nois", "quiet"], ["nois", "quiet", "shout"]]
    
    
    for i in range(len(keywords)):
        k = keywords[i] 
        f = filters[i]
        cur_results = get_all_results(k, None, f)
        total_results.extend(cur_results)
    
    
    
    ### ----------------  ###   
    
    """
    ### WORSHIP PRACTICES
    keyword = "worship practices"
    keywords = ["temple"]
    
    total_results = get_all_results("sacrament")
    filters = [["sacrament"]]

    # NEED TO FILTER OUT SENTENCES THAT CONTAIN 
    # MORE THAN ONE KEYWORD

    for i in range(len(keywords)):
        k = keywords[i] 
        f = filters[i]
        cur_results = sampled_keyword(k, f)
        total_results.extend(cur_results)
    """
    
    ### ------------------ ###
        
    print(f"Total samples:  {len(total_results)}")
        
    results_loop(keyword, total_results)
    # line_plots(keyword, total_results)



def results_loop(keyword, result_list = None):
    """
    Results are in (noise, sentiment) pairs
    noise ranges from 0 (loud) to 4 (quiet)
    sentiment ranges from 0 (neg) to 1 (pos)

    """
    
    if not result_list:
        results = get_all_results(keyword)
    else:
        results = result_list
    # results.extend(get_all_results("quiet"))
    
    x = [val[0] for val in results]
    y = [val[1] for val in results]
    
    # TOTALS
    quiet_pos = 0
    quiet_neg = 0
    loud_pos = 0
    loud_neg = 0
    
    for val in results:
        if val[0] < 2 and val[1] < 0.5:
            loud_neg += 1
        elif val[0] < 2 and val[1] > 0.5:
            loud_pos += 1
        elif val[0] > 2 and val[1] < 0.5:
            quiet_neg += 1
        elif val[0] > 2 and val[1] > 0.5:
            quiet_pos += 1 
            
    hypothesis = loud_neg + quiet_pos 
    other = quiet_neg + loud_pos 
    total = hypothesis + other 
    
    print("Loud Negative:", loud_neg / total)
    print("Quiet Positive:", quiet_pos / total)
    print() 
    print("Quiet Negative:", quiet_neg / total)
    print("Loud Positive:", loud_pos / total)
    print() 
    
    print("Hypothesis:", hypothesis / total)
    print("Other", other / total)
    
    sns_heatmap(loud_neg, loud_pos, quiet_neg, quiet_pos, total, keyword)
    
    
    
    
    # print(len(x))
    # print(len(y))
    
    
    # plt.scatter(x, y, color="r", marker="o")

def line_plots(keyword, result_list = None):
    """
    Results are in (noise, sentiment) pairs
    noise ranges from 0 (loud) to 4 (quiet)
    sentiment ranges from 0 (neg) to 1 (pos)

    """
    
    if not result_list:
        results = get_all_results(keyword)
    else:
        results = result_list
    # results.extend(get_all_results("quiet"))
    
    x = [val[0] for val in results]
    y = [val[1] for val in results]
    
    loud_pos_dict = {}
    pos_total_dict = {}
    for year in range(1850, 2021, 10):
        loud_pos_dict[year] = 0
        pos_total_dict[year] = 0
        

    
    
    # TOTALS
    quiet_pos = 0
    quiet_neg = 0
    loud_pos = 0
    loud_neg = 0
    
    for val in results:
        if val[0] < 2 and val[1] < 0.5:
            loud_neg += 1
        elif val[0] < 2 and val[1] > 0.5:
            loud_pos += 1
            loud_pos_dict[val[2]] += 1
            pos_total_dict[val[2]] += 1
        elif val[0] > 2 and val[1] < 0.5:
            quiet_neg += 1
        elif val[0] > 2 and val[1] > 0.5:
            quiet_pos += 1 
            pos_total_dict[val[2]] += 1
            
            
    labels = list(range(1850, 2021, 10))
    heights = []
    
    x_coords = []
    y_coords = []
    
    total = 0
    
    for year in labels:
        try: 
            cur_value = loud_pos_dict[year] / pos_total_dict[year] * 100.0
        except ZeroDivisionError:
            cur_value = 0  
        heights.append(cur_value)
        
        num_pts = pos_total_dict[year]
        print(year, num_pts)
        
        x_val = [year] * num_pts
        y_val = [cur_value] * num_pts
        x_coords.extend(x_val)
        y_coords.extend(y_val)
        
        total += num_pts
        
    avg_pts = total / len(labels)
    print("Average", avg_pts)
    
    sizes = [400 * (loud_pos_dict[year] / avg_pts) for year in labels]
        
            
        
    
    
    
    
    ### SCATTER PLOT WITH REGRESSION LINE
    # https://python-graph-gallery.com/scatterplot-with-regression-fit-in-matplotlib/
        
    # Initialize layout
    fig, ax = plt.subplots()
    
    
    
    
    # Add scatterplot
    ax.scatter(labels, heights, s=sizes, alpha=0.7, edgecolors="k")
    
    # Fit linear regression via least squares with numpy.polyfit
    # It returns an slope (b) and intercept (a)
    # deg=1 means linear fit (i.e. polynomial of degree 1)
    b, a = np.polyfit(x_coords, y_coords, deg=1)
    
    # Create sequence of 100 numbers from 0 to 100
    xseq = np.linspace(1850, 2020, num=1000)
    
    # Plot regression line
    
    ax.set_ylabel('Percent of total positive (%)')
    ax.set_title(f'Loud Positive ({keyword})')
    
    ax.set_ylim(20, 50)
    
    ax.plot(xseq, a + b * xseq, color="k", lw=2.5)
    
    
    
    """
    ### BAR CHART
    fig, ax = plt.subplots()
    
    idx = [i for i in range(len(labels))]

    ax.bar(idx, heights)
    ax.set_xticks(idx)
    ax.set_xticklabels(labels , rotation=45)
    
    ax.set_ylabel('Percent of total positive (%)')
    ax.set_title(f'Loud Positive ({keyword})')
    # ax.legend(title='Fruit color')
    
    plt.show()
    """
    
    
    
def sns_heatmap(loud_neg, loud_pos, quiet_neg, quiet_pos, total, keyword):
    vol_labels = ["loud", "quiet"]
    sen_labels = ["positive", "negative"]

    loud_pos = round(100 * loud_pos / total, 1)
    quiet_pos = round(100 * quiet_pos / total, 1)
    loud_neg = round(100 * loud_neg / total, 1)
    quiet_neg = round(100 * quiet_neg / total, 1)
    
    
    df = pd.DataFrame([[loud_pos, quiet_pos], [loud_neg, quiet_neg]], sen_labels, vol_labels)
    
    
    plt.figure(figsize = (10,8))
    plt.rcParams.update({'font.size': 16})
    # sns.color_palette("light:b", as_cmap=True)
    sns.heatmap(df, cmap="Reds", vmin = 0, vmax = 100, annot=True, fmt=".1f", square=True, linewidths=.5)  # cmap = 'coolwarm', 
    plt.title(f"Keyword: {keyword} (%)")
    # plt.savefig(f"GC_{keyword}_heatmap.png")
    
    plt.show()
    
    
def make_heatmap(loud_neg, loud_pos, quiet_neg, quiet_pos, total):
    vol_labels = ["loud", "quiet"]
    sen_labels = ["positive", "negative"]
    
    loud_pos = round(100 * loud_pos / total, 1)
    quiet_pos = round(100 * quiet_pos / total, 1)
    loud_neg = round(100 * loud_neg / total, 1)
    quiet_neg = round(100 * quiet_neg / total, 1)


    values = np.array([[loud_pos, quiet_pos],
                        [loud_neg, quiet_neg]])

    fig, ax = plt.subplots()
    im = ax.imshow(values)
    
    # Show all ticks and label them with the respective list entries
    ax.set_xticks(np.arange(len(vol_labels)), labels=vol_labels)
    ax.set_yticks(np.arange(len(sen_labels)), labels=sen_labels)
    
    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), ha="center")
    
    # Loop over data dimensions and create text annotations.
    for i in range(len(sen_labels)):
        for j in range(len(vol_labels)):
            text = ax.text(j, i, f"{values[i, j]} %",
                           ha="center", va="center", color="w")
    
    ax.set_title("Keyword: noise (%)")
    fig.tight_layout()
    plt.colorbar()
    plt.show()    
    
    
# sampled_keyword("pray")
# line_plots("sacrament")
grouped_keyword()
    
    
"""    
keywords = ["praise", "revere", "worship"]
keywords += ["shout", "whisper", "noise", "quiet"]
keywords += ["sacrament"]

for k in keywords:
    results_loop(k)
    
# keyword = "sacrament"
# results_loop(keyword)

samples = ["temple", "spirit"]
for k in samples:
    sampled_keyword(k)
"""


# TODO: gather all entries as (noise, sentiment) pairs
#  -- find correlation, plot points on grid, do clustering, etc.



"""
year = 1850

noise_file = f"noise_results/{keyword}/{year}.txt"
sentiment_file = f"sentiment_results/{keyword}/{year}.txt"

sentiment_results = read_sentiment(sentiment_file)
noise_results = read_noise(noise_file)

assert len(sentiment_results) == len(noise_results)  # sanity check

quiet_positive = 0
quiet_negative = 0
loud_positive = 0
loud_negative = 0

for i in range(len(sentiment_results)):
    noise = noise_results[i]
    sentiment = sentiment_results[i]

    # Hypothesis:  entries tend to be quiet and positive, or loud and negative
    
    # CASE:  quiet and positive
    if noise[0] > 2 and sentiment[0] > 0.5:
        quiet_positive += 1
    elif noise[0] > 2 and sentiment[0] < 0.5:
        quiet_negative += 1
    elif noise[0] < 2 and sentiment[0] > 0.5:
        loud_positive += 1
    elif noise[0] < 2 and sentiment[0] < 0.5:
        loud_negative += 1
        
total = quiet_positive + quiet_negative + loud_positive + loud_negative
    
print("Quiet and Positive:", quiet_positive)
print("Quiet and negative:", quiet_negative)
print("Loud and positive:", loud_positive)
print("Loud and negative:", loud_negative)
print("Total:", total)
    
    
"""   





        
        
        