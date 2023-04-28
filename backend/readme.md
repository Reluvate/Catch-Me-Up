# Endpoints

# 1. /summarize [POST]
- Don't need to pass in anything
- After called, gets url of the website that sent the endpoint
- Gets latest transcription of the url in db
- Summarizes transcription and sends back {'answer': answer, 'status': 1}
- If fail, status will be 0 and error key will be provided {'error': error}


# 2. /segment [POST]
- Same as summarize
- Returns the same thing as segment but the answer key will be a list of segmented paragraphs from the transcript


# 3. /questioning [POST]
- Pass in question
- Gets transcript from database
- Passes both transcript and question to ai
- Returns the same thing as summarize