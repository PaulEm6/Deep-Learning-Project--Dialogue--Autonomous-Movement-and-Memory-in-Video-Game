from transformers import pipeline, set_seed
from langchain.chains import TextChain
from langchain.llms import HuggingFaceModel

def main():
    # Initialize the GPT-2 model
    gpt2_model = HuggingFaceModel("gpt2")

    # Create a LangChain TextChain with our model
    conversation_chain = TextChain(llm=gpt2_model)

    # Set seed for reproducibility
    set_seed(42)

    print("You can start chatting with GPT-2. Type 'quit' to exit.")
    
    chat_history = ""  # Initialize chat history
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            break

        # Append user input to chat history
        chat_history += f"User: {user_input}\nGPT-2: "
        
        # Generate a response using the TextChain
        response = conversation_chain(chat_history)
        
        # Clean up the response and update chat history
        response_text = response["generated_text"].split("GPT-2: ")[-1].strip()
        chat_history += f"{response_text}\n"
        
        print(f"GPT-2: {response_text}")

if __name__ == "__main__":
    main()
