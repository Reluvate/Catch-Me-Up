from flask import Flask, render_template, request, session
from flask_cors import CORS, cross_origin
import ai21
import psycopg
import requests

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
connection = "postgres://limzhenyang12345:joBnw8vO9kGs@ep-late-bonus-548123.ap-southeast-1.aws.neon.tech/Reluvate"
ai21.api_key = "XFH1V0mQnGohm79g5NXvn87AERqXRbJI"

def get_transcription(url : str) -> str:
    with psycopg.connect(**conn_dict) as conn:
            # get text from url in database
            pass

@app.route('/summarize', methods=["POST"])
def answer():
    if request.method == "POST":
        #data = request.data 
        #data = data.decode("utf-8")
        #data = eval(data) #data should only have one argument
        url = request.url
        transcript = get_transcription(url)
        try:
            summary = ai21.Summarize.execute(
                source=transcript
            )
        except Exception as e:
            return {"status" : 0, "error": f"{type(e)} {e}"}
        
        return {"answer": summary, "status": 1}
    
    else:
        pass

@app.route('/segment', methods=["POST"])
def answer():
    if request.method == "POST":
        #data = request.data 
        #data = data.decode("utf-8")
        #data = eval(data) #data should only have one argument
        url = request.url
        transcript = get_transcription(url)
        try:
            segmented = ai21.Segmentation.execute(
                source=transcript
            )
        except Exception as e:
            return {"status" : 0, "error": f"{type(e)} {e}"}
        
        return {"answer": segmented, "status": 1}
    
    else:
        pass

@app.route('/questioning', methods=["POST"])
def answer():
    if request.method == "POST":
        data = request.data 
        data = data.decode("utf-8")
        data = eval(data) #data should only have one argument
        question = data[0]
        url = request.url
        transcript = get_transcription(url)
        payload = {
            "context": transcript,
            "question": question
        }
        endpoint = "https://api.ai21.com/studio/v1/experimental/answer"
        try:
            result = requests.post(endpoint, json = payload)
            result = result.json()
            answer = result["answer"]
        except Exception as e:
            return {"status" : 0, "error": f"{type(e)} {e}"}
        
        return {"answer": answer, "status": 1}
    
    else:
        pass


if __name__ == '__main__':
    conn_dict = psycopg.conninfo.conninfo_to_dict(connection)
    app.run(debug = True)
