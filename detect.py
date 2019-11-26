import cv2
from imutils.object_detection import non_max_suppression
import imutils
import numpy as np
from requests import Session
from signalr import Connection

def GetContorno(color):
    mascara = cv2.inRange(hsv, color, upper)
    resultado = cv2.bitwise_and(frame, frame, mask=mascara)
    cinza = cv2.cvtColor(resultado, cv2.COLOR_BGR2GRAY)
    _, bordas = cv2.threshold(cinza, 3, 255, cv2.THRESH_BINARY)
    contornos, _ = cv2.findContours(bordas, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    return contornos

with Session() as session:
    connection = Connection("http://25.66.196.232:8088/signalr", session)
    conn = connection.register_hub('step5')
    connection.start()
    #create error handler
    def print_error(error):
        print('error: ', error)
    #process errors
    connection.error += print_error

laranja = np.array([0, 105,120]) # laranja
upper = np.array([15, 255, 255])

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# camera = cv2.VideoCapture('http://192.168.44.109:4747/video')
camera = cv2.VideoCapture(0)
while True:
    frame = camera.read()[1]
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
            x ,y ,w ,h = cv2.boundingRect(contorno)
            if area > 1500:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                print("[INFO] {} pessoas detectadas".format(len(pick)))
                conn.server.invoke('alert', 'Trabalhador na pista.')   
                        
    cv2.imshow("Camera", frame)

    key = cv2.waitKey(5)
    if key == 27:
        break

cv2.destroyAllWindows()
