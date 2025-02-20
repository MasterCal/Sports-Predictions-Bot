#Author: Beau Carnes
#Carnes' original source code on GitHub: https://gist.github.com/beaucarnes/51ec37412ab181a2e3fd320ee474b671
#Carnes' video where source code was taken from: https://www.youtube.com/watch?v=SPTfmiYiuok. Timestamp: 58:42

from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Hello. I am alive!"

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
