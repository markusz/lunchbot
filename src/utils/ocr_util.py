import os
import time
from io import BytesIO

import requests

API_V1_KEY = os.getenv('AZURE_IMAGE_RECOGNITION_API_V1_KEY')
API_V2_KEY = os.getenv('AZURE_IMAGE_RECOGNITION_API_V2_KEY')


# Blocking call
#
# Polls for results of OCR - kinda ugly but does the job.
#
# vision/v2.0/ocr is synchronous, but results are less accurate
# vision/v2.0/recognizeText gives the best results
def poll_azure_cognitive_v2_ocr_result_location_until_result(location, sleep_secs=1):
    while True:
        res = requests.get(location, headers={'Ocp-Apim-Subscription-Key': API_V2_KEY})
        if res.json().get('status') == 'Succeeded':
            return res.json().get('recognitionResult')
        else:
            print('Sleeping for 1 s and retrying')
            time.sleep(sleep_secs)


def submit_recognize_text_request_to_azure_cognitive_v2(image):
    image_as_stream = BytesIO()
    image.save(image_as_stream, format='jpeg')

    r = requests.post(
        'https://westcentralus.api.cognitive.microsoft.com/vision/v2.0/recognizeText',
        data=image_as_stream.getvalue(),
        headers={
            'Content-Type': 'application/octet-stream',
            'Ocp-Apim-Subscription-Key': API_V2_KEY
        },
        params={
            'mode': 'Printed'
        }
    )

    results_location = r.headers.get('Operation-Location')
    return results_location


def get_text_recognition_from_azure_cognitive_v2_sync(image):
    results_location = submit_recognize_text_request_to_azure_cognitive_v2(image)
    ocr_res = poll_azure_cognitive_v2_ocr_result_location_until_result(results_location)

    print(ocr_res)
    return ocr_res
