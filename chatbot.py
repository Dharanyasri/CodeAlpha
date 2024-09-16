import spacy

# Load the spaCy English model
nlp = spacy.load("en_core_web_sm")

# Define the chatbot responses
def chatbot_response(user_input):
    doc = nlp(user_input.lower())

    # Keywords and intents matching
    if any(token.lemma_ in ["hi", "hello"] for token in doc):
        return "Hello! How can I assist you today?"

    elif any(token.lemma_ in ["how", "you"] for token in doc):
        return "I'm just a program, but I'm doing well! How about you?"

    elif any(token.lemma_ in ["name"] for token in doc):
        return "I am a friendly chatbot. What's your name?"

    elif any(token.lemma_ in ["bye", "exit"] for token in doc):
        return "Goodbye! Have a great day!"

    else:
        return "I'm sorry, I didn't understand that. Could you please rephrase?"

# Main chatbot loop
def chatbot():
    print("Chatbot: Hello! I'm here to chat. Type 'bye' to exit.")

    while True:
        user_input = input("You: ")
        
        if "bye" in user_input.lower() or "exit" in user_input.lower():
            print("Chatbot: Goodbye!")
            break

        response = chatbot_response(user_input)
        print(f"Chatbot: {response}")

# Run the chatbot
chatbot()
