# %%

# things we need for NLP
import nltk
from nltk.stem.lancaster import LancasterStemmer

stemmer = LancasterStemmer()

# things we need for Tensorflow
import numpy as np
import tflearn
import pandas as pd
import csv
import random

# restore all of our data structures
import pickle

data = pickle.load(open("models/training_data", "rb"))
words = data['words']
classes = data['classes']
train_x = data['train_x']
train_y = data['train_y']

# import our chat-bot intents file
import json

with open('data/intents.json') as json_data:
    intents = json.load(json_data)

# Build neural network
net = tflearn.input_data(shape=[None, len(train_x[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
net = tflearn.regression(net)

# Define model and setup tensorboard
model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')


def clean_up_sentence(sentence):
    # tokenize the pattern
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word
    sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
    return sentence_words


# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bow(sentence, words, show_details=False):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print("found in bag: %s" % w)

    return np.array(bag)


model.load('models/model.tflearn')

context = {}

ERROR_THRESHOLD = 0.25


def classify(sentence):
    # generate probabilities from the model
    results = model.predict([bow(sentence, words)])[0]
    # filter out predictions below a threshold
    results = [[i, r] for i, r in enumerate(results) if r > ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append((classes[r[0]], r[1]))
    # return tuple of intent and probability
    return return_list


def response(sentence, userID='123', show_details=False):
    results = classify(sentence)
    # if we have a classification then find the matching intent tag
    if results:
        # loop as long as there are matches to process
        while results:
            for i in intents['intents']:
                # find a tag matching the first result
                if i['tag'] == results[0][0]:
                    # set context for this intent if necessary
                    if 'context_set' in i:
                        if show_details: print('context:', i['context_set'])
                        context[userID] = i['context_set']

                    # check if this intent is contextual and applies to this user's conversation
                    if not 'context_filter' in i or \
                            (userID in context and 'context_filter' in i and i['context_filter'] == context[userID]):
                        if show_details: print('tag:', i['tag'])
                        # a random response from the intent
                        answer = i['responses']
                        answer = ', '.join(map(str, answer))
                        answer_list = []
                        with open(answer, 'r', encoding="utf-8") as file:
                            reader = csv.reader(file)
                            k = 0
                            for row in reader:
                                answer_list.insert(k, row)
                                k += 1
                        answer = random.sample(answer_list, 10)
                        answer = ', '.join(map(str, answer))
                        answer = answer.replace("[", "")
                        answer = answer.replace("]", "")
                        answer = answer.replace("'", "")
                        tag = random.choice(i['start'])
                        tag = ''.join(map(str, tag))
                        return tag + " " + answer

            results.pop(0)

from tkinter import *

root = Tk()
root.title("Chat Bot")
root.geometry("400x500")
root.resizable(width=FALSE, height=FALSE)

user = StringVar()
bot = StringVar()

main_menu = Menu(root)

# Create the submenu
file_menu = Menu(root)

# Add commands to submenu
file_menu.add_command(label="Can I have some thriller Movies")
file_menu.add_command(label="Can i see some Directors")
file_menu.add_command(label="Can i see some Actors")
main_menu.add_cascade(label="Sample Questions", menu=file_menu)
# Add the rest of the menu options to the main menu
root.config(menu=main_menu)

chatWindow = Label(root, textvariable=bot, wraplength=350, bd=1, bg="white", width="50", height="8", font=("Arial", 15),
                   foreground="black")
chatWindow.place(x=6, y=6, height=385, width=370)

messageWindow = Entry(root, textvariable=user, bd=0, bg="white", font=("Arial", 10), foreground="black")
messageWindow.place(x=128, y=400, height=88, width=260)


def main():
    question = user.get()
    bot.set(response(question))


Button = Button(root, text="Send", width="12", height=5,
                bd=0, bg="#0080ff", activebackground="#00bfff", foreground='#ffffff', font=("Arial", 12), command=main)
Button.place(x=6, y=400, height=88)
root.mainloop()
