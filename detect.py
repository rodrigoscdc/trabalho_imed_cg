import cv2
from imutils.object_detection import non_max_suppression
import imutils
import numpy as np

def GetContorno(color):
    mascara = cv2.inRange(hsv, color, upper)
    resultado = cv2.bitwise_and(frame, frame, mask=mascara)
    cinza = cv2.cvtColor(resultado, cv2.COLOR_BGR2GRAY)
    _, bordas = cv2.threshold(cinza, 3, 255, cv2.THRESH_BINARY)
    contornos, _ = cv2.findContours(bordas, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    return contornos

laranja = np.array([0, 98,120]) # laranja
upper = np.array([15, 255, 255])

hog = cv2.HOGDeor()
hog.setSVMDetector(cv2.HOGDeor_getDefaultPeopleDetector())

camera = cv2.VideoCapture(0)
while True:
    frame = camera.read()[1]
    #frame = cv2.flip(frame, 1)
    frame = imutils.resize(frame, width=min(400, frame.shape[1]))
    rects, wights = hog.detectMultiScale(
        frame, winStride=(4, 4), padding=(8, 8), scale=1.05)
    
    rects = np.array([[x, y, x+w, y+h] for (x, y, w, h) in rects])
    pick = non_max_suppression(rects, probs=None, overlapThresh=0.85)

    for (xA, yA, xB, yB) in pick:
        print('pessoas')
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        contornos = GetContorno(laranja)
        for contorno in contornos:
            area = cv2.contourArea(contorno)
            if area > 1500:
                cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 2)
                print("[INFO] {} pessoas detectadas".format(len(pick)))
    cv2.imshow("Camera", frame)

    key = cv2.waitKey(10)
    if key == 27:
        break

cv2.destroyAllWindows()
