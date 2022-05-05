import sys
import cv2
from typing import Union
from pyzbar.pyzbar import decode


class BarcodeReader:
    def read(image_path) -> Union[bytes, None]:
        img = cv2.imread(image_path)
        detected = decode(img)
        if not detected:
            return None
        else:
            return detected[0].data


if __name__ == "__main__":
    image = sys.path[0] + "/Img.jpg"
    print(BarcodeReader.read(image).decode() == "7896004006482")
