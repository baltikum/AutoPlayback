from encodings import utf_8
from flask import Flask,Response,make_response
import chardet
app = Flask(__name__)

@app.route('/')
def hello():
    return "Looks like it works!"


@app.route('/live/<url>', methods=['GET'])
def live(url):
    filename = ('./static/' + url)
    with open(filename,'r') as file:
        temp = file.read()

    #resp = make_response(temp)
    #resp.headers['Access-Control-Allow-Origin'] = '*'
    return Response(temp,headers={ 'Access-Control-Allow-Origin': '*' })


if __name__=='__main__':
    app.run(host='localhost', port=5000, debug=True, threaded=True)