from scipy.misc import imshow, imsave
from passporteye import read_mrz
from PIL import Image
import cv2
import pytesseract
import os


# import textract

def preprocess_image(path):
    image = cv2.imread(path)
    # converting the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # tapplying threshold to preprocess the image
    # gray = cv2.threshold(gray,0,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # removing noise or blur using median blur
    gray = cv2.medianBlur(gray, 3)
    # cv2.imwrite('test_roi.png', gray)
    cv2.imwrite('test_pass.png', gray)


def detect_mrz(image_path):
    preprocess_image(image_path)
    try:
        mrz = read_mrz('test_pass.png', save_roi=True)
    except Exception as e:
        print(e)
        return True
    if not mrz:
        return False
    imsave('test_roi.png', mrz.aux['roi'])
    # preprocess_image()
    text = pytesseract.image_to_string(Image.open('test_roi.png'))
    return mrz


def process_text(text):
    name = text.names
    pass_no = text.number
    dob = text.date_of_birth
    is_valid = text.valid
    return text


if __name__ == '__main__':
    image_dir = '/media/hellrazer/ezedox/pdf files/images/passport'
    count = []
    cant_read = []
    for img in os.listdir(image_dir):
        mrz = detect_mrz(os.path.join(image_dir, img))
        if not mrz:
            count.append(img)

        elif mrz == True:
            cant_read.append(img)

    print("Gave falsified:/n/t {}".format(count))
    print("gave Error :/n/t {}".format(cant_read))
    print "data length is {}".format(os.listdir(image_dir))
