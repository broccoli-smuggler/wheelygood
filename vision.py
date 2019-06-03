import cv2
import numpy as np

class VisionLocator:
    def __init__(self, cam_width=640, cam_height=480, threshold=0.85, cam=0, reference_image='cross_b.jpg', pixel_to_encoder=154):
        self.template = cv2.imread(reference_image, 0)
        self.pixel_to_encoder = pixel_to_encoder
        self.cam_height = cam_height
        self.cam_width = cam_width
        self.threshold = threshold
        self.cam = cam
        self.capture = cv2.VideoCapture(cam)
        self.capture.open(cam)
        self.nones = 0
    
    ''' Returns the dx position in frame percent.
    -1 return means not found
    to go out is positive. to go in negitive. return pixels to move frame'''
    def get_chair_dx(self, show_frame=False):
        dx = None
        for i in range(0, 12):
            # for some reason the frames read are delayed so we read a load of them
            ret, frame = self.capture.read()
        if frame is None:
            self.nones+=1
            if self.nones > 10:
                self.capture.release()
                self.capture.open(self.cam)
                print('retry')
            return dx
        h, w = (self.template.shape)
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        gray = cv2.GaussianBlur(gray, (5,5), 0)
        
        #clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        #gray = clahe.apply(gray)
        #gray = cv2.equalizeHist(gray)
        
        res = cv2.matchTemplate(gray, self.template, cv2.TM_CCOEFF_NORMED)
        _, max, minl, maxl = cv2.minMaxLoc(res)
        print(max)
    
        # We have found the template
        if max > self.threshold:
            bott = (maxl[0] + w, maxl[1] +h)
            cv2.rectangle(gray, maxl, bott, 255, 2)
            middle = maxl[1] + h/2
            dx = self.cam_height/2 - middle
            dx *= self.pixel_to_encoder
            
        if cv2.waitKey(1) & 0xFF == ord('b'):
           cv2.imwrite('temp.jpg', gray)
           
        if show_frame:
            cv2.imshow('frame', gray)
            cv2.waitKey(1)
        return dx        
        

if __name__ == '__main__':
    v = VisionLocator()
    
    while True:
        print(v.get_chair_dx(True))
        
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    
'''
template = cv2.imread('cross.jpg', 0)
    cap = cv2.VideoCapture(0)
    print('started')

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
        if max > 0.8:
            bott = (maxl[0] + w, maxl[1] +h)
            cv2.rectangle(gray, maxl, bott, 255, 2)
        
        cv2.imshow('frame', gray)
            
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
'''
