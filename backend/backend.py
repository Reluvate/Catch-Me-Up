from flask import Flask, render_template, request, session
from flask_cors import CORS, cross_origin
import ai21
# import psycopg
import requests
import redis

r = redis.Redis(
    host='redis-14946.c23738.us-east-1-mz.ec2.cloud.rlrcp.com',
    port=14946,
    password='g9e5H3aUeAYVOKHnYDMEQoy4QidRElPR')

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
connection = "postgres://limzhenyang12345:joBnw8vO9kGs@ep-late-bonus-548123.ap-southeast-1.aws.neon.tech/Reluvate"
ai21.api_key = "XFH1V0mQnGohm79g5NXvn87AERqXRbJI"


def get_transcription(url: str) -> str:
    value = r.get(url)
    if value is None:
        return ""
    else:
        return value.decode("utf-8")
    
def append_transcription(url: str, transcript: str):
    # if url in r: append to existing
    # else: create new
    existing = r.get(url)
    if existing is None:
        r.set(url, transcript)
    else:
        existing = existing.decode("utf-8")
        r.set(url, existing + ' ' + transcript)

@app.route('/summarize', methods=["POST"])
def summarise():
    if request.method == "POST":
        #data = request.data
        #data = data.decode("utf-8")
        # data = eval(data) #data should only have one argument
        url = request.get_json()['url']
        transcript = get_transcription(url)
        try:
            summary = ai21.Summarize.execute(
                source=transcript,
                sourceType="TEXT"
            )
        except Exception as e:
            return (str(e), 400)

        return ({'summary':summary["summary"]}, 200)

    else:
        pass


@app.route('/segment', methods=["POST"])
def segment():
    if request.method == "POST":
        body = request.get_json()
        url = body['url']
        transcript = get_transcription(url)
        try:
            segmented = ai21.Segmentation.execute(
                source=transcript,
                sourceType="TEXT"
            )
            segmented = segmented["segments"]
        except Exception as e:
            return (str(e), 400)

        return ({"answer": [i['segmentText'] for i in segmented]}, 200)

    else:
        pass


@app.route('/questioning', methods=["POST"])
def questioning():
    if request.method == "POST":
        body = request.get_json()
        question = body['question']
        url = body['url']
        transcript = get_transcription(url)
        headers = {"Authorization": f"Bearer {ai21.api_key}",
                   "Content-Type": "application/json"}
        payload = {
            "context": transcript,
            "question": question
        }
        endpoint = "https://api.ai21.com/studio/v1/experimental/answer"
        try:
            result = requests.post(endpoint, json=payload, headers=headers)
            result = result.json()
            answer = result["answer"]
        except Exception as e:
            return (str(e), 400)

        return ({'answer':answer}, 200)

    else:
        pass

@app.route('/append-transcript', methods=["POST"])
def appendTranscript():
    if request.method == 'POST':
        body = request.get_json()
        if 'url' in body and 'stream' in body:
            append_transcription(body['url'], body['stream'])
            return ('OK', 200)
        else:
            return ('Bad Request', 400)

@app.route('/get-transcript', methods=["POST"])
def getTranscript():
    if request.method == 'POST':
        body = request.get_json()
        if 'url' in body:
            value = get_transcription(body['url'])
            return (value, 200)
        else:
            return ('Bad Request', 400)


if __name__ == '__main__':
    # conn_dict = psycopg.conninfo.conninfo_to_dict(connection)
    app.run(debug=True)
