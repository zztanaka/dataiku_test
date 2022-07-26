# Note: this processor hides colors appearing in text in a case-insensitive manner.

def process(row):
    
    # List of colors to hide (ensure case-insensitive)
    colors_to_hide = ["white", "pink", "blue", "red", "yellow"] 
    colors_to_hide = [w.casefold() for w in colors_to_hide]
    
    # Retrieve the user-defined input column
    text_column = params["input_column"]

    # Hide colors from list
    text_list = row[text_column].split(" ")
    text_list_hide = [w if w.casefold() not in colors_to_hide else "****" for w in text_list]
    
    return " ".join(text_list_hide)