import cv2 
import time

cap = cv2.VideoCapture(0)

#tracker = cv2.TrackerMOSSE_create()
tracker = cv2.TrackerCSRT_create()
time.sleep(2)
success, img = cap.read() 

bounding_box = cv2.selectROI("Tracking",img,False)
tracker.init(img,bounding_box)

def drawBox(img, bbox):  #bbox içinde 4 int içeren bir tupledır
   
    x, y, w, h = int(bbox[0]),int(bbox[1]), int(bbox[2]), int(bbox[3])
    cv2.rectangle(img,(x,y),((x+w),(y+h)),(0,255,0),3,1 )
    cv2.putText(img,"Tracking",(400,50),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)




while True:
    timer = cv2.getTickCount()
    success, img = cap.read() 

    success, bounding_box= tracker.update(img)

    if success:
        drawBox(img,bounding_box)
    else:
        cv2.putText(img,"There is no object",(400,50),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,8,231),2)


    fps = cv2.getTickFrequency() / (cv2.getTickCount()-timer)
    cv2.putText(img,str(int(fps)),(75,50),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,8,231),2)
    cv2.imshow("Tracking",img)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break

