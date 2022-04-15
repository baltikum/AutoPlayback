from flask import Flask,request,render_template,redirect,json,jsonify
import vobject
import re
import Vcard
import html,json

cardList = []
brokenCards = []
parsedCards = []
vcardlist = []
jsoncontacts = []
jsonStr = ''
app = Flask(__name__)



@app.route('/')
def index():
    return render_template("index.html",contacts=json)


@app.route("/load", methods = ['POST'] )
def load_contacts():
    global cardList,brokenCards,parsedCards

    fil = request.get_data(True,True,False)

    data = str(fil)
    data = data.splitlines()
    count = 0
    if data:
        start = False
        card = False
        for line in data:

            if not card:
                newCard = ''

            if line.startswith('BEGIN:VCARD'):
                start = True
                card = True
            elif line.startswith('END:VCARD'):
                card = False

            if start:
                newCard = newCard + line + '\n'
            
            if not card :
                if start:
                    cardList.append(newCard)

       
        for entry in cardList:
            try:
                temp = vobject.readOne(entry)
                parsedCards.append(temp)
            except:
                brokenCards.append(entry)

        cardList = []
        for i in range(len(parsedCards)):

            try:
                n = parsedCards[i].n.value
            except AttributeError as e:
                n = ''
            try:
                fn = parsedCards[i].fn.value
            except AttributeError as e:
                fn = ''
            try:
                tel = parsedCards[i].tel.value
            except AttributeError as e:
                tel = ''

            temp = Vcard.vcard(n,fn,tel)
            vcardlist.append(temp)
            print(f'name:{n},  lastname:{fn},  tel:{tel}')


    return redirect('/')


@app.route("/get", methods = ['GET'] )
def get_contacts():
    global vcardlist,jsonStr

    jsonStr = json.dumps([entry.get_json() for entry in vcardlist])

    return jsonStr



@app.route("/clear", methods = ['GET'] )
def clear_contacts():
    global cardList,parsedCards,brokenCards
    cardList = []
    parsedCards = []
    brokenCards = []
    vcardlist = []
    return {'contacts': ' empty'}





if __name__ == "__main__":
    app.run(debug=True)

