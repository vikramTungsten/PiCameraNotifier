
__author__ = 'vkmchandel'

import os
from base64 import b64encode
from os import makedirs
import json
import requests



ENDPOINT_URL = 'https://vision.googleapis.com/v1/images:annotate'
RESULTS_DIR = 'jsons'
#makedirs(RESULTS_DIR, exist_ok=True)


def make_image_data(image_filename):
    with open(image_filename, 'rb') as f:
        ctxt = b64encode(f.read()).decode()
        request={
                'image': {'content': ctxt},
                'features': [{
                    'type': 'LABEL_DETECTION',
                    'maxResults': 15
                }]
            }
    return json.dumps({"requests": request}).encode()

def request_ocr(api_key, image_filenames):
    response = requests.post(ENDPOINT_URL,
                             data=make_image_data(image_filenames),
                             params={'key': api_key},
                             headers={'Content-Type': 'application/json'})
    return response


def imageToTextByGoogleAPI(api_key,image_file):
    result=''
    response = request_ocr(api_key, image_file)
    if response.status_code != 200 or response.json().get('error'):
        print('Error OCR operation failed '+image_file)
    else:
        print(response.json())
        labels = response.json()['responses'][0]['labelAnnotations']
        for label in labels:
            if result.strip():
                result= result+' , '+ label['description']
            else:
                result= label['description']
    return result



if __name__ == '__main__':
    api_key='*****************************************'
    in_dir = 'input/dog_01.jpg'
    result=imageToTextByGoogleAPI(api_key,in_dir)
    print(result)




