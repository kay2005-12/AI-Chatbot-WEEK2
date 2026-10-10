import re
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

def optimize_query(user_input):
    # Receive only lower case
    text = user_input.lower()
    # Keep Letters , numbers and spaces
    text = re.sub(r"[^a-z0-9\s]", " ", text)

    # Normalizing the extra spaces 
    words = text.split()
    
    optimized_word = [lemmatizer.lemmatize(word) for word in words]\
    
    return "".join(optimized_word)