from google.cloud import vision
from google.cloud.vision import types
import os
import re


# response = client.annotate_image({
#     'image': {'content': file,
#               }, 'features': [
#         {'type': vision.enums.Feature.Type.DOCUMENT_TEXT_DETECTION}]})


def parse_pan_no(text):
    pattern = '[A-Z]{5}[0-9]{4}[A-Z]{1}'
    # key = 'PermanentAccountNumberCard'
    match = re.search(pattern, text)
    if match:
        # text = text.split('|')
        # text = text[1]
        # text = text.strip('PermanentAccountNumberCard')
        text = match.group(0)
        return text
    else:
        return None


def parse_pan_name(text):
    hin_key = ''
    key = 'Name'
    if key in text:
        text = text.split(key)[1]

        if 'Father' in text:
            return {"Father's Name": text.split(key)[1]}

        return {'Name': text}
    else:
        return None


def get_pan_details(text_list):
    details = dict()
    for text in text_list:
        is_pan = parse_pan_no(text)
        is_name = parse_pan_name(text)
        if is_pan:
            details['pan_no'] = parse_pan_no(is_pan)
        elif is_name and 'Name' not in details.keys():
            details.update(is_name)
    return details


def get_text(file_path):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'guestbook-93c84e7825ff.json'
    client = vision.ImageAnnotatorClient()

    file = open(file_path, 'rb').read()
    image = types.Image(content=file)
    response = client.document_text_detection(image=image)
    document = response.full_text_annotation
    all_text = []
    for page in document.pages:
        for block in page.blocks:
            block_words = []
            for paragraph in block.paragraphs:
                block_words.extend(paragraph.words)

            block_symbols = []
            for word in block_words:
                block_symbols.extend(word.symbols)

            block_text = ''
            for symbol in block_symbols:
                block_text = block_text + symbol.text

            all_text.append(block_text)
            # print('Block Content: {}'.format(block_text))
            # print('Block Bounds:\n {}'.format(block.bounding_box))
    # print(all_text)
    return all_text


if __name__ == '__main__':
    # path = '/home/hellrazer/PycharmProjects/ocr-tech-proto/dataset/pan'
    path = '/home/hellrazer/PycharmProjects/ocr-tech-proto/dataset/aadhar'
    for image in os.listdir(path):
        text_list = get_text(os.path.join(path, image))
        details = get_pan_details(text_list)
        if len(details) < 1:
            print(image)
        else:
            print(details)

# import requests
# import json
# import base64
#
# key = 'AIzaSyBK6BXbUnhhOPS0sYtJvgOQUFYsei53N9U'
#
# file = base64.b64encode(open('dataset/Test/passport.jpeg', 'rb').read()).decode('UTF-8')
#
# params = {
#     "requests": [
#         {
#             "image": {
#                 "content": file
#             }},
#         {
#             "features": [
#                 {
#                     "type": "DOCUMENT_TEXT_DETECTION",
#                 }
#             ]
#         }
#     ]
# }
#
# response = requests.post('https://vision.googleapis.com/v1/images:annotate?key={}'.format(key), data=params,
#                          headers={'Content-Type': 'application/json'})
# print(response.content)
