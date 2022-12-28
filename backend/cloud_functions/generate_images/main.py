from google.cloud import firestore
from dataclasses import dataclass
from typing import Union, List
import datetime
import openai
import os

openai.api_key = os.environ['OPENAI_API_KEY']


# Generates images from summaries/{summaryId}/content 
# Creates a new record in /images/{imageId}
def generate_images(data, ctx) -> None:
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
    