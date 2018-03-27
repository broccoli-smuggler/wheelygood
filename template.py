import cv2
import numpy as np

template = cv2.imread('chair.jpg', 0)
cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if frame is None:
        continue
    
    h, w = (template.shape)
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    res = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
    _, max, minl, maxl = cv2.minMaxLoc(res)
    print(max)
    
    if cv2.waitKey(1) & 0xFF == ord('b'):
       cv2.imwrite('temp.jpg', gray)
    
    # We have found the template
    if max > 0.4:
        bott = (maxl[0] + w, maxl[1] +h)
        cv2.rectangle(gray, maxl, bott, 255, 2)
    
    cv2.imshow('frame', gray)

    # Display the resulting frame
        
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()