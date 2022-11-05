import cv2 as cv
import time
import numpy as np
import serial

Conf_threshold = 0.4
NMS_threshold = 0.4
COLORS = [(0, 255, 0), (0, 0, 255), (255, 0, 0),
          (255, 255, 0), (255, 0, 255), (0, 255, 255)]

class_name = []
with open('classes-custom.txt', 'r') as f:
    class_name = [cname.strip() for cname in f.readlines()]

net = cv.dnn.readNet('yolov4-tiny-custom_best727.weights','yolov4-tiny-custom714.cfg')

#net.setPreferableBackend(cv.dnn.DNN_BACKEND_CUDA)
#net.setPreferableTarget(cv.dnn.DNN_TARGET_CUDA_FP16)

model = cv.dnn_DetectionModel(net)
model.setInputParams(size=(216, 216), scale=1 / 255, swapRB=True)

cap = cv.VideoCapture(0)
starting_time = time.time()
frame_counter = 0


ser = serial.Serial(
    port = '/dev/ttyAMA0',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
    )

def detection(degree):
    if degree.isdigit():
        ser.write(degree.encode())
        
    else :
        print("text error")

while True:
    
   
    ret, frame = cap.read()

    frame_counter += 1

    frame = cv.resize(frame, dsize=(416, 416), interpolation=cv.INTER_AREA)

    if ret == False:
        break

    classes, scores, boxes = model.detect(frame, Conf_threshold, NMS_threshold)
    

    for (classid, score, box) in zip(classes, scores, boxes):
          print(class_name[classid])
          color = COLORS[int(classid) % len(COLORS)]
          label = '%d' % (class_name[classid])
          cv.rectangle(frame, box, color, 1)
          cv.putText(frame, "this", (box[0], box[1] - 10),
                   cv.FONT_HERSHEY_COMPLEX, 0.5, color, 2)
         if(class_name[classid] = "R"):
             detection('1')
         else if(class_name[classid] = "G"):
             detection('2')
         else if(class_name[classid] = "B"):
             detection('3')
         else :
             print("error")
#    endingTime = time.time() - starting_time
#     fps = int(frame_counter/endingTime)
#     cv.putText(frame, f'FPS : {fps}', (20, 50), cv.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)

    cv.imshow('frame', frame)
    key = cv.waitKey(1)
    if key == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
