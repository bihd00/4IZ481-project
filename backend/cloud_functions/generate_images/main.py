from google.cloud import firestore, storage
from dataclasses import dataclass
from typing import Optional, List, Any
from base64 import b64decode
from enum import Enum
import datetime
import openai
import uuid
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
    images = _generate_images_with_open_ai(prompt=value, format=ImageFormat.B64)
    
    # if using openai b64_json output, update image URLs via upload to GCS
    gcs_client = storage.Client()
    for image in images:
        _add_img_url_via_to_gcs(image, client=gcs_client)

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
        storage.Client()
    image_name_for_upload = 'images/' + str(uuid.uuid4()) + '.png'
    image_base64 = b64decode(image.b64_json)
    
    bucket = storage_client.bucket(bucket_name=os.environ['GCS_BUCKET'])
    blob = bucket.blob(blob_name=image_name_for_upload)
    blob.upload_from_string(image_base64, content_type='image/png')

    try:
        blob.make_public()
    except Exception as e:
        print(e)
    
    image.url = blob.public_url
    return
    