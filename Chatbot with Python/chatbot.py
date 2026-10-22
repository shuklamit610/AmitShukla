
"""
Project: Terminal Chatbot
Course: MSCS-633-M20

Description:
A terminal-based chatbot built with Python and ChatterBot.
Django is included in the project dependencies as specified
in the assignment.
"""

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer


def create_chatbot():
    """Create and train the chatbot with sample conversations."""

    # Use a local SQLite database to preserve conversation knowledge.
    bot = ChatBot(
        "UC Assistant",
        database_uri="sqlite:///chatbot.sqlite3"
    )

    # Provide sample conversation pairs for the initial training.
    conversation = [
        "Good morning!",
        "Good morning! How can I help you today?",
        "How are you doing?",
        "I am doing very well, thank you for asking.",
        "Thank you.",
        "You're welcome.",
        "What is your name?",
        "I am Assistant, a Python chatbot.",
        "Do you like hats?",
        "I think hats can be a fun fashion accessory!",
        "Goodbye",
        "Goodbye! Have a wonderful day."
    ]

    # Train the chatbot using the supplied sample conversation.
    trainer = ListTrainer(bot)
    trainer.train(conversation)

    return bot


def main():
    """Run the interactive terminal chat session."""

    print("=" * 45)
    print(" Welcome to the Assistant Chatbot")
    print(" Type 'exit' or 'quit' to end the chat.")
    print("=" * 45)

    # Initialize the chatbot before accepting user input.
    bot = create_chatbot()

    while True:
        try:
            # Read a message from the user.
            user_input = input("\nYou: ").strip()

            # Ignore empty messages.
            if not user_input:
                print("Bot: Please enter a message.")
                continue

            # End the session when the user requests it.
            if user_input.lower() in {"exit", "quit"}:
                print("Bot: Thank you for chatting. Goodbye!")
                break

            # Generate and display a response.
            response = bot.get_response(user_input)
            print(f"Bot: {response}")

        except (EOFError, KeyboardInterrupt):
            # Exit gracefully when the user interrupts the session.
            print("\nBot: Chat session ended. Goodbye!")
            break


if __name__ == "__main__":
    main()
