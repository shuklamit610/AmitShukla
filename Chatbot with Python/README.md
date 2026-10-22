# Chatbot with Python

This folder was created for the Chatbot with Python project.

# UC Assistant — Terminal Chatbot

## Project Description

UC Assistant is a simple terminal-based chatbot developed
using Python and ChatterBot. It responds to user messages
using a collection of trained conversations.

Django is included as a project dependency to meet the
assignment's environment requirements.

## Features

- Interactive terminal-based conversation
- Training with sample conversation data
- SQLite database for chatbot knowledge
- Graceful exit using "exit" or "quit"
- Comments and functions for code readability

## Requirements

- Python 3.10–3.14
- ChatterBot 1.2.15
- Django 5.2 or later, but below 6.0

## Installation

Create and activate a virtual environment:

python3 -m venv venv
source venv/bin/activate

Install dependencies:

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

## Run the Chatbot

python chatbot.py

## Example

You: Good morning!
Bot: Good morning! How can I help you today?

You: How are you doing?
Bot: I am doing very well, thank you for asking.

You: exit
Bot: Thank you for chatting. Goodbye!
