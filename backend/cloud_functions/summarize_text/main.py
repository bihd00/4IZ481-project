from google.cloud import firestore
import numpy as np
import datetime
import openai
import os

openai.api_key = os.environ['OPENAI_API_KEY']

# Summarizes text added to /texts/{textId}/content 
# Creates a new record in /summaries/{summaryId}
def summarize_text(data, ctx) -> None:
    db = firestore.Client()
    # get fields from new record
    fields = data['value']['fields']
    # fields must include refId & content
    if 'refId' not in fields or 'content' not in fields:
        return
    # check whether refId could be obtained as a string
    content = fields['refId']
    refId = content['stringValue']
    # if not, return
    if not refId:
        return
    # same goes for content
    content = fields['content']
    value = content['stringValue']
    if not value:
        return
    # get summary
    summary = _summarize_with_open_ai(text=value)
    # create summary record data
    data = dict(
        refId=refId,
        content=summary,
        createdAt=datetime.datetime.now().isoformat(),
    ) 
    # create new record in summaries collection
    db.collection('summaries').document().set(data)
    return


def _summarize_with_open_ai(text: str) -> str:
    words = text.split(" ")
    chunks = np.array_split(words, 1)
    sentences = ' '.join(list(chunks[0]))

    summary_responses = []

    for chunk in chunks:    
        sentences = ' '.join(list(chunk))
        prompt = f"{sentences}\n\ntl;dr:"

        response = openai.Completion.create(
            engine="text-davinci-003", 
            prompt=prompt,
            temperature=0.3, 
            max_tokens=140,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=1
        )

        response_text = response["choices"][0]["text"]
        summary_responses.append(response_text)

    return "".join(summary_responses).strip()
