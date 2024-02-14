import random
import json
import torch
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize
import datetime
from googleSheets import chatbotInsert

flag = True
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
with open('intents.json', 'r', encoding='utf-8') as f:
    intents = json.load(f)

FILE = 'data.pth'
data = torch.load(FILE)

input_size = data['input_size']
hidden_size = data['hidden_size']
output_size = data['output_size']
all_words = data['all_words']
tags = data['tags']
model_state = data['model_state']

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

# Filtro de acentos
def acentos(sentences):
    """
    Funcion que cambia las vocales con acentos a la vocal sin ellos.
    """
    acentos = ["á","é","í","ó","ú"]
    flag = False
    for i in sentences:
        if i in acentos:
            flag = True
    if (flag):
        sentences = sentences.replace('á', 'a')
        sentences = sentences.replace('é', 'e')
        sentences = sentences.replace('í', 'i')
        sentences = sentences.replace('ó', 'o')
        sentences = sentences.replace('ú', 'u')
        return sentences
    return sentences

# Saludo segun la hora del dia
currentTime = datetime.datetime.now()
currentTime.hour
greeting = ""
if currentTime.hour < 12:
    greeting = "Buenos dias"
elif 12 <= currentTime.hour <= 18:
    greeting = "Buenos tardes"
else:
    greeting = "Buenos noches"

bot_name = 'Pablo'
print(f"{greeting}, ¡Comencemos!")

def get_response(msg):
    sentece = msg
    sentece = acentos(sentece)
    sentence = tokenize(sentece)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    print(prob.item())

    if prob.item() > 0.85:
        for intent in intents['intents']:
            if tag == intent['tag']:
                print(tag)
                return random.choice(intent['responses'])
    elif prob.item() > 0.65:
        for intent in intents['intents']:
            if tag == intent['tag']:
                chatbotInsert(tag, msg)
                return "No te entendí muy bien, pero guardaré tu pregunta para contestarla despues"
    return "Perdón, no te entiendo."

if __name__ == "__main__":
    print("Let's chat! (type 'quit' to exit)")
    while True:
        sentence = input("You: ")
        if sentence == "quit":
            break

        resp = get_response(sentence)
        print(resp)
        
# Hacer metodo para ingresar datos al json