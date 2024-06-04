"""
Script to interpret NLP results for noise-level classification
"""

def open_file(file_name):
    with open(file_name, encoding="utf-8") as f:
        lines = f.readlines()
        
    lines = list(filter(lambda x: x != '\n', lines))
    for i in range(0, len(lines), 6):
        entry = lines[i: i + 6]
        check_noise(entry)
        
def check_noise(entry):
    """
    Format: 0 = original file
            1 = sample sentence
            2 = quiet vs loud
            3 = soft vs loud
            4 = quiet vs noisy
            5 = soft vs noisy 
    
    """    
    
    loud = 0
    quiet = 0
    
    for i in range(2, 6):
        cur_entry = entry[i].strip()
        # Extract labels
        lists = cur_entry.split(" received scores ")
        label_extract = lists[0][1:-1].split(", ")
        labels = [x[1:-1] for x in label_extract]
        
        number_extract = lists[1][1:-1].split(", ")
        numbers = [float(x) for x in number_extract]
        
        if labels[0] == "quiet" or labels[0] == "soft":
            quiet += numbers[0]
            loud += numbers[1]
        else:
            quiet += numbers[1]
            loud += numbers[0]
    
    if quiet > loud:
        return "quiet", quiet
    elif loud > quiet:
        return "loud", loud     
    else:
        return "neither", quiet
    
if __name__ == "__main__":   
    file_name = "noise_results/noise/1850.txt"
    open_file(file_name)
    
    
    
    
    
    