# This is a sample Python script.

# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from captcha.image import ImageCaptcha
#import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    image = ImageCaptcha(width=200, height=100)
    captcha_text = "a7Bd"
    captcha_image = image.generate(captcha_text)
    image.write(captcha_text, 'captcha.png')

    #Beispiel: Text verzerren (cv2 and numpy)
    #image = np.zeros((200, 400, 3), dtype=np.uint8)
    #cv2.putText(image, "Ihre Nachricht hier", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    #M = cv2.getPerspectiveTransform(np.float32([[50, 100], [350, 100], [50, 150], [350, 150]]),
    #                               np.float32([[50, 100], [350, 120], [50, 150], [350, 130]]))
    #warped = cv2.warpPerspective(image, M, (400, 200))
    #cv2.imwrite('verzerrtes_bild.png', warped)

    # Beispiel: Verwischen eines Texts (mittels Pil)
    image = Image.new('RGB', (200, 100), color=(255, 255, 255))
    d = ImageDraw.Draw(image)
    d.text((10, 10), "a7Bd", fill=(0, 0, 0))
    blurred_image = image.filter(ImageFilter.BLUR)
    blurred_image.save('verwischtes_bild.png')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
