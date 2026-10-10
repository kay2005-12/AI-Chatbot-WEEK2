import random
from sklearn.metrics.pairwise import cosine_similarity
from pathlib import Path
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from query_preprocess import optimize_query


base_dir = Path(__file__).resolve().parent
data_path = base_dir / "intents.json"

with data_path.open("r",encoding ="utf-8") as fpr:
    data = json.load(fpr)
    

intents = data['intents']


# Intialization
vectorized = TfidfVectorizer() 

# Making the pattern vectors of all of the patterns present in the intent
patterns = []
tags = []
for intent in intents:
    for pattern in intent["patterns"]:
            patterns.append(pattern)
            tags.append(intent["tag"])

pattern_vectors = vectorized.fit_transform(patterns)
print("The vectorization is sucessful")    
    
def get_responses(user_input):
    
    user_input = user_input.strip()
    if not user_input:
        return{
            "intent":"empty_input",
            "response":"please enter a messege",
            "confidence":0.0
        }
    
    user_input = optimize_query(user_input)    
    
    # Making the user query vectorized 
    user_vector = vectorized.transform([user_input])

    
    # Calculating the similarities 
    similarities = cosine_similarity(
        user_vector,
        pattern_vectors
    )[0]
    
    # Finding the most similar pattern
    best_index = similarities.argmax()
    best_score = float(similarities[best_index])
    predicted_tag = tags[best_index] 
    
    
    # Messege for unknown queries 
    if best_score < 0.25:
        return {
            "intent": "unknown",
            "response": (
                "Sorry, I couldn't understand that. "
                "Could you rephrase your question?"
            ),
            "confidence": best_score
        }
        
    # Matching the responses
    for intent in intents:
        if intent["tag"] == predicted_tag:
            return {
                "intent":predicted_tag,
                "response":random.choice(intent["responses"]),
                "confidence":best_score
            }
    
    
    # FallBack Custom
    return {
        "intent": "unknown",
        "response": "Sorry, I couldn't find a suitable answer.",
        "confidence": best_score
    }
    
    
    
if __name__ == "__main__":
    while True:
        user_input = input("your input ::")
        if user_input.lower().strip() in ["exit","quit","bye"]:
            print("Have a good day sir !")
            break
    
        
        result = get_responses(user_input)
        print("Bot:", result["response"])
        print("Intent:", result["intent"])
        print("Similarity:", round(result["confidence"], 2))

