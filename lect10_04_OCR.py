"""
作者：倪媛
日期：12/11/2018
功能：OCR处理验证码
"""
from PIL import Image
import pytesseract


def main():
    # im = Image.open('captcha.jpg')
    # gray = im.convert('L')
    # # gray.show()
    #
    # threshold = 150
    # table = []
    # for i in range(256):
    #     if i < threshold:
    #         table.append(0)
    #     else:
    #         table.append(1)
    #
    # out = gray.point(table, '1')
    # # out.show()
    # out.save('captcha_threshold.jpg')
    #
    # th = Image.open('captcha_threshold.jpg')
    # print(pytesseract.image_to_string(th))

    name = 'captcha_threshold.jpg'

    fl = open(name, 'rb')
    image = Image.open(fl)
    image.show()
    vcode = pytesseract.image_to_string(image, lang="eng", config="-psm 7")
    print(vcode)
    fl.close()


if __name__ == '__main__':
    main()
