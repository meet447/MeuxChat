from Bard import Chatbot
import pytchat
from pytchat import LiveChat, SpeedCalculator
import time
import elevenlabs
import re

video_int = input("Enter the video url: ")

video_id = video_int

token = 'XAhuE6e-3CO0051j1hL9qyQyeHUMofoorKGDEWxoYEE485Q5vA32Xly-uvCQTNMLX9Mhog.'

tts_type = "EL"

prompt = "Remember You are a female streamer Your Name is Meux. you will respond in a mature and " \
         "seductive manner. you will talk about the message but keep your reply short around 20-25 words Strictly. " \
         "you will also flirt.You will act as a human and never mention that you are a ai or llm.If you understand " \
         "reply with 'prompt has been setup'"

bot = Chatbot(token)

promptver = bot.ask(prompt)['content']

print("promt has been setup :", promptver)

print("Token Setup Succesful:", token)

print("Getting youtube Comments from the live stream: ", video_id)

banned_words = ['word1', 'word2', 'word3']

wh_words = ['what', 'meux'] 

def readChat():
    chat = pytchat.create(video_id=video_id)
    schat = pytchat.create(video_id=video_id, processor=SpeedCalculator(capacity=20))

    while chat.is_alive():
        for c in chat.get().sync_items():
            print(f"\n{c.datetime} [{c.author.name}]- {c.message}\n")
            message = c.message

            # Check if the message contains any banned words
            if contains_banned_words(message):
                # Handle the message with banned words (e.g., ignore, delete, etc.)
                handle_banned_message(c)
                continue

            if contains_wh_words(message):
                response = llm(message)
                print(response)

            if schat.get() >= 20:
                chat.terminate()
                schat.terminate()
                return

            time.sleep(1)


def contains_banned_words(message):
    # Convert the message to lowercase for case-insensitive matching
    message_lower = message.lower()

    # Use regular expressions to find any banned word in the message
    pattern = re.compile(r'\b(' + '|'.join(banned_words) + r')\b')
    if re.search(pattern, message_lower):
        return True
    return False


def handle_banned_message(comment):
    # You can implement your desired action here, such as deleting the comment, ignoring it, or sending a warning to the user.
    print("Banned word detected. Comment ignored.")


def contains_wh_words(message):
    message_lower = message.lower()
    for word in wh_words:
        if word in message_lower:
            return True
    return False


def llm(message):
    output = bot.ask(message)['content']

    print(output)

    # voice goes here

    # Generate a response
    response = elevenlabs.generate(output)

    # Speak the response
    elevenlabs.play(response)


while True:
    readChat()

    print("\n\nReset!\n\n")

    time.sleep(2)
