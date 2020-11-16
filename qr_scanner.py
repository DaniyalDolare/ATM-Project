import pyqrcode
import cv2
import time

class Scanner():
    
    def scan(self):
        # Capture video from web cam
        video_capture = cv2.VideoCapture(0)

        qrCodeDetector = cv2.QRCodeDetector()

        start_time = time.perf_counter()
        while True:

            ret, frame = video_capture.read()

            # Text is decoded text and points is location of detected qr code 
            text,points,optional = qrCodeDetector.detectAndDecode(frame)

            # if points is not None:
            #     print(text)

            cv2.imshow('Scan QR code', frame)

            stop_time = time.perf_counter() - start_time

            if cv2.waitKey(1) and stop_time > 5:
                if text or stop_time > 10:
                    break

        video_capture.release()
        cv2.destroyAllWindows()
        received_data = text.split(" ")
        for data in received_data:
            if(len(data)==16):
                return data[0:6]
        # return text


    def create(self):
        
        text="Hey,i am glad to get scanned!!"

        # Converting text to qr code
        qr = pyqrcode.create(text)

        # Saving generated qr code in png file
        qr.png("horn.png", scale=6)

#Scanner.scan(Scanner)