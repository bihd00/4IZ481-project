from dotenv import dotenv_values
from google.cloud import firestore, storage
from dataclasses import dataclass
from typing import Optional, List, Any
from base64 import b64decode
from pathlib import Path
from enum import Enum
import numpy as np
import datetime
import openai
import json
import uuid
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
    images = _generate_images_with_open_ai(prompt=value, format=ImageFormat.B64)
    
    # if using openai b64_json output, update image URLs via upload to GCS
    for image in images:
        _add_img_url_via_to_gcs(image)

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
    url: Optional[str] = None
    b64_json: Optional[Any] = None
    refId: Optional[str] = None
    createdAt: Optional[str] = None

    @property
    def data(self):
        return { k:v for k,v in self.__dict__.items() if k not in ['b64_json']}


class ImageFormat(Enum):
    URL = 'url'
    B64 = 'b64_json'


def _generate_images_with_open_ai(
    prompt: str, 
    format: ImageFormat = ImageFormat.URL 
) -> List[Image]:
    size='256'
    response = openai.Image.create(
        prompt=prompt,
        size=f"{size}x{size}",
        n=2,
        response_format=format.value
    )
    return list(map(lambda x: Image(**x), response['data']))


def _add_img_url_via_to_gcs(image: Image, client: storage.Client = None) -> None:
    """
    - Uploads a b64 encoded PNG image to google cloud storage.
    - Sets image.url to its uploaded location on GCS.
    """
    if image.url:
        print('Image already contains url. Skipping')
        return

    if not image.b64_json:
        print('Image does not contain b64_json. Skipping')
        return

    storage_client = client if client else \
        storage.Client.from_service_account_json(os.path.join(ROOT, 'service-account-key.json'))
    image_name_for_upload = 'images/' + str(uuid.uuid4()) + '.png'
    image_base64 = b64decode(image.b64_json)
    
    bucket = storage_client.bucket(bucket_name=ENV['GCS_BUCKET'])
    blob = bucket.blob(blob_name=image_name_for_upload)
    blob.upload_from_string(image_base64, content_type='image/png')

    try:
        blob.make_public()
    except Exception as e:
        print(e)
    
    image.url = blob.public_url
    return
    

def test_generate_images():
    data = json.load(open(os.path.join(ROOT, 'tests/data/summarize_text_data.json'), 'r'))
    data['value']['fields']['content']['stringValue'] = 'a dog riding a bycicle, with a sombrero on its head'
    context = json.load(open(os.path.join(ROOT, 'tests/data/summarize_text_context.json'), 'r'))
    assert generate_images(data, context) is None


def test_generate_images_with_open_ai_url():
    prompt = '4 helicopters having a picnic, playing cards. Friendly'
    images = _generate_images_with_open_ai(prompt)
    assert images[0].url is not None


def test_generate_images_with_open_ai_b64_json():
    prompt = 'telescope image of a planetary system, where ich planet is a fruit. Hundreds of planets, colorful, high-res'
    images = _generate_images_with_open_ai(prompt, ImageFormat.B64)
    assert images[0].b64_json is not None


if __name__ == "__main__":
    pass