import cv2 as cv

print("Starting")
net=cv.dnn.readNet('last.xml','last.bin')

net.setPreferableTarget(cv.dnn.DNN_TARGET_MYRIAD)

frame=cv.imread('/home/pi/Downloads/image1.jpeg')
blob=cv.dnn.blobFromImage(frame,size=(672,384),ddepth=cv.CV_8U)
net.setInput(blob)
out=net.forward()

for detection in out.reshape(-1,7):
   
    confidence=float(detection[2])

    xmin=int(detection[3]*frame.shape[1])
    ymin=int(detection[4]*frame.shape[0])

    xmax=int(detection[5]*frame.shape[1])
    ymax=int(detection[6]*frame.shape[0])

    if confidence>0.25:
        cv.rectangle(frame,(xmin,ymin),(xmax,ymax),color=(255,0,0))
        print('detection:====>'+str(detection))
cv.imwrite('./output.jpg',frame)
print("End and Saved")
