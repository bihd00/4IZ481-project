from dotenv import dotenv_values
from google.cloud import firestore
from dataclasses import dataclass
from typing import Union, List
from pathlib import Path
import numpy as np
import datetime
import openai
import json
import os

ROOT = Path(__file__).resolve().parent.parent
ENV = dotenv_values(os.path.join(ROOT, '.env'))
openai.api_key = ENV['OPENAI_API_KEY']


# Summarizes text added to /texts/{textId}/content 
# Creates a new record in /summaries/{summaryId}
def summarize_text(data, ctx) -> None:
    db = firestore.Client.from_service_account_json(os.path.join(ROOT, 'service-account-key.json'))
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


def test_summarize_text():
    data = json.load(open(os.path.join(ROOT, 'tests/data/summarize_text_data.json'), 'r'))
    context = json.load(open(os.path.join(ROOT, 'tests/data/summarize_text_context.json'), 'r'))
    assert summarize_text(data, context) is None


# Generates images from summaries/{summaryId}/content 
# Creates a new record in /images/{imageId}
def generate_images(data, ctx) -> None:
    db = firestore.Client.from_service_account_json(os.path.join(ROOT, 'service-account-key.json'))
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
    # get generated images
    images = _generate_images_with_open_ai(prompt=value)
    # create records in images collection
    batch = db.batch()
    for image in images:
        image.refId = refId
        image.createdAt = datetime.datetime.now().isoformat()
        img_ref = db.collection('images').document()
        batch.set(img_ref, image.data)
    batch.commit()
    return


@dataclass
class Image:
    url: Union[str, None]
    refId: Union[str, None] = None
    createdAt: Union[str, None] = None

    @property
    def data(self):
        return self.__dict__


def _generate_images_with_open_ai(prompt: str) -> List[Image]:
    size='256'
    response = openai.Image.create(
        prompt=prompt,
        n=2,
        size=f"{size}x{size}"
    )
    return list(map(lambda x: Image(**x), response['data']))
    

def test_generate_images():
    data = json.load(open(os.path.join(ROOT, 'tests/data/summarize_text_data.json'), 'r'))
    data['value']['fields']['content']['stringValue'] = 'a dog riding a bycicle, with a sombrero on its head'
    context = json.load(open(os.path.join(ROOT, 'tests/data/summarize_text_context.json'), 'r'))
    assert generate_images(data, context) is None


if __name__ == "__main__":
    pass