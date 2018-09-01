from google.cloud import vision
from google.cloud.vision import types
import os


class ocr_text():
    def __init__(self):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(os.getcwd().strip('vision_api'),
                                                                    'guestbook-93c84e7825ff.json')
        self.client = vision.ImageAnnotatorClient()
        self.called = False

    def annotate(self, path):
        self.path = path
        self.file = open(path, 'rb').read()
        image = types.Image(content=self.file)
        self.response = self.client.document_text_detection(image=image)
        self.document = self.response.full_text_annotation

    def display_ids(self):
        pass

    def get_text(self):
        all_text = []
        for page in self.document.pages:
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

    def display_blocks(self):
        for page in self.document.pages:
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

                print('Block Content: {}'.format(block_text))
                print('Block Bounds:\n {}'.format(block.bounding_box))
        self.called = False

    def display_image(self):
        import cv2
        cv2.imshow('Image', cv2.imread(self.path))
        cv2.waitKey(0)

    def __call__(self, *args, **kwargs):
        self.annotate(path=args[0])
        self.called = True


if __name__ == '__main__':
    import os

    text_detector = ocr_text()
    path = '/home/hellrazer/PycharmProjects/ocr-tech-proto/dataset/aadhar'
    # text_detector('/media/hellrazer/ezedox/pdf files/images/passport/imag5.jpg')
    text_detector('/home/hellrazer/PycharmProjects/ocr-tech-proto/dataset/Test/image.jpg')
    text_detector.display_blocks()

    # import os
    # for image in os.listdir(path):
    #     text_detector(os.path.join(path, image))
    #     print(text_detector.get_text())
    #

    # text_detector('/media/hellrazer/ezedox/pdf files/images/passport/imag5.jpg')
    # text_detector.get_text()
