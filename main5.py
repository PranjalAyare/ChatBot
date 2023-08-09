import nltk
import spacy
from google.cloud import dialogflow
from nltk.chat import util as nltk_chat_util
import os
from tkinter import *
from tkinter import ttk
import random

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\Users\\HI\\OneDrive\\Desktop\\chatbot2\\dwizzy-uo9p-76720bde6bdd.json"

# Initial greeting or prompt
initial_messages = [
    "Hello, how can I assist you today?",
    "Welcome! How may I help you?",
    "Long time no see! What can I do for you?"
]

# Prepare the training data
pairs = [
    [
        r"my order is (.*)",
        ["Your order %1 is being processed. It will be delivered soon."]
    ],
    [
        r"where is my order\??",
        ["Please provide your order number, so I can check the status for you."]
    ],
    [
        r"how can I contact customer support\??",
        ["You can reach our customer support team at 1-800-123-4567."]
    ],
    [
        r"(.*) (delay|late)",
        ["We apologize for the inconvenience caused. Our team is working to resolve the issue."]
    ],
    [
        r"(.*) (cancel|refund) my order",
        ["To cancel or request a refund for your order, please contact our customer support team."]
    ],
    # Add more patterns and responses as needed
]

# Create the chatbot
def chatbot_response(user_input):
    reflections = {
        "myself": "yourself",
        "am": "are",
        "your": "my",
        "yours": "mine",
        "you": "me",
        "I": "you",
        "me": "you"
    }
    chat = nltk_chat_util.Chat(pairs, reflections)
    chat._nlp = spacy.load("en_core_web_sm")

    if user_input.strip() == "":
        # If user input is empty, select a random initial message
        initial_message = random.choice(initial_messages)
        return initial_message

    # Pass user input to Dialogflow for intent detection and response generation
    dialogflow_response = detect_intent_with_dialogflow("dwizzy-uo9p", "unique_session_id", user_input)

    # Pass user input to the chatbot for pattern matching
    chat_response = chat.respond(user_input)

    if dialogflow_response:
        return dialogflow_response
    elif chat_response:
        return chat_response
    else:
        return "Sorry, I don't understand."


# Function to interact with Dialogflow
def detect_intent_with_dialogflow(project_id, session_id, message):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=message, language_code="en-US")
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(request={"session": session, "query_input": query_input})

    return response.query_result.fulfillment_text


# GUI interface
root = Tk()
root.title("Chatbot")

# Create a frame for the chat history
chat_frame = Frame(root, bg="white")
chat_frame.pack(expand=True, fill=BOTH)

# Create a scrollbar for the chat history
scrollbar = Scrollbar(chat_frame)
scrollbar.pack(side=RIGHT, fill=Y)

# Create a text widget to display the chat history
chat_history_text = Text(chat_frame, wrap=WORD, bg="white", bd=2, relief="solid", yscrollcommand=scrollbar.set)
chat_history_text.pack(expand=True, fill=BOTH)

# Configure the scrollbar to work with the chat history text widget
scrollbar.config(command=chat_history_text.yview)

# Create a frame for the user input
user_input_frame = Frame(root, bg="white")
user_input_frame.pack(side=BOTTOM, pady=10)

# Create a label for the user input
user_input_label = Label(user_input_frame, text="You:", bg="white", fg="blue", wraplength=200, anchor="w")

user_input_label.pack(side=LEFT)


# Create an entry widget for the user input
user_input_entry = ttk.Entry(user_input_frame, width=50, style="User.TEntry")
user_input_entry.pack(side=LEFT, expand=True, fill=X)

# Configure the styles for the rectangular text boxes
style = ttk.Style()
style.configure("User.TEntry", background="light blue", foreground="black")
style.configure("Bot.TEntry", background="light green", foreground="black")

# Initial greeting or prompt
initial_messages = [
    "Hello, how can I assist you today?",
    "Welcome! How may I help you?",
    "Long time no see! What can I do for you?"
]

# Display initial prompt from the bot
initial_prompt = random.choice(initial_messages)
chat_history_text.configure(state=NORMAL)
chat_history_text.insert(END, "Bot: " + initial_prompt + "\n", "bot")
chat_history_text.configure(state=DISABLED)

# Function to handle sending a message
def send_message(event=None):
    user_input = user_input_entry.get()
    if user_input.strip() != "":
        chat_history_text.configure(state=NORMAL)
        chat_history_text.insert(END, "You: " + user_input + "\n", "user")
        chat_history_text.insert(END, "Bot: " + chatbot_response(user_input) + "\n", "bot")
        chat_history_text.insert(END, "\n")  # Add a line break between the messages
        chat_history_text.see(END)  # Scroll to the latest message
        chat_history_text.configure(state=DISABLED)

    user_input_entry.delete(0, END)

# Bind the Enter key to send the message
user_input_entry.bind("<Return>", send_message)

# Create a button to send the message
send_button = Button(user_input_frame, text="Send", command=send_message, bg="light blue", fg="white")
send_button.pack(side=LEFT)

# Configure the text tags for styling
chat_history_text.tag_config("user", justify="right", background="light blue", foreground="black", relief="solid")
chat_history_text.tag_config("bot", justify="left", background="light green", foreground="black", relief="solid")

root.mainloop()
