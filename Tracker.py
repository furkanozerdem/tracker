import cv2 
import time

cap = cv2.VideoCapture(0)

#tracker = cv2.TrackerMOSSE_create()
tracker = cv2.TrackerCSRT_create()
time.sleep(2)
success, img = cap.read() 

if not success:
    print("Kamera görüntüsü alınamadı.")
    exit()

bounding_box = cv2.selectROI("Tracking",img,False)
print("Seçilen bounding box:", bounding_box)

if bounding_box[2] > 0 and bounding_box[3] > 0:
    # Görüntü boyutlarını kontrol et
    height, width = img.shape[:2]
    print("Görüntü boyutu:", (width, height))
    
    # Bounding box'u int'e çevir ve sınırları kontrol et
    bounding_box = tuple(int(v) for v in bounding_box)
    if bounding_box[0] + bounding_box[2] > width or bounding_box[1] + bounding_box[3] > height:
        print("Bounding box görüntü sınırları dışında.")
        exit()
    
    tracker.init(img, bounding_box)
else:
    print("Geçersiz bounding box seçildi.")
    exit()

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
    