from vision_api.vision_wraper import ocr_text
import re
from PIL import Image
# import zbarlight,cv2
# from vision_api import qr_extractor as reader
# import pyzbar.pyzbar as pyzbar
import zbar
from vision_api import verhoeff_verification


def get_aadhar_no(text):
    pattern = r'\d{4}\d{4}\d{4}'
    match = re.match(pattern, string=text)
    if match:
        no = match.group(0)
        return no

    else:
        return None


def get_qrcode(image_path):
    # image = cv2.imread(image_path)
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY, dstCn=0)
    pil = Image.open(image_path)
    width, height = pil.size
    raw = pil.tobytes()
    scanner = zbar.ImageScanner()
    image = zbar.Image(width, height, 'Y800', raw)
    result = scanner.scan(image)
    print(result)


if __name__ == '__main__':
    text_detector = ocr_text()
    path = '/home/hellrazer/PycharmProjects/ocr-tech-proto/dataset/aadhar'
    # text_detector('/media/hellrazer/ezedox/pdf files/images/passport/imag5.jpg')
    # text_detector('/home/hellrazer/PycharmProjects/ocr-tech-proto/dataset/Test/image.jpg')
    import os

    for image in os.listdir(path):
        text_detector(os.path.join(path, image))
        texts = text_detector.get_text()
        for text in texts:
            get_aadhar = get_aadhar_no(text)
            if get_aadhar:
                verhoeff_verify = verhoeff_verification.is_valid(int(get_aadhar))
                if verhoeff_verify:
                    print("the aadhar no {} is valid".format(get_aadhar))
                else:
                    print('aadhar no {} is not valid'.format(get_aadhar))
        get_qrcode(os.path.join(path, image))
