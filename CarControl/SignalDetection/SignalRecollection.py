import cv2
import numpy as np
from scipy.stats import itemfreq
import time

class SignalRecollection(object):

    def __init__(self):
        pass

    def get_dominant_color(self,image, n_colors):
        pixels = np.float32(image).reshape((-1, 3))
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
        flags = cv2.KMEANS_RANDOM_CENTERS
        flags, labels, centroids = cv2.kmeans(
            pixels, n_colors, None, criteria, 10, flags)
        palette = np.uint8(centroids)
        return palette[np.argmax(itemfreq(labels)[:, -1])]


    def signals(self,imgs):
        frame = imgs
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        img = cv2.medianBlur(gray, 27)
        circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT,
                                1, 80, param1=120, param2=40)
        if not circles is None:
            circles = np.uint16(np.around(circles))
            max_r, max_i = 0, 0
            
            for i in range(len(circles[:, :, 2][0])):
                if circles[:, :, 2][0][i] > 50 and circles[:, :, 2][0][i] > max_r:
                    max_i = i
                    max_r = circles[:, :, 2][0][i]
            x, y, r = circles[:, :, :][0][max_i]
            if y > r and x > r:
                square = frame[y-r:y+r, x-r:x+r]
                dominant_color = self.get_dominant_color(square, 2)
                if dominant_color[1] > 120:
                    return 2
                elif dominant_color[2] > 50 and dominant_color[0] > 80:
                    return 3
                else:
                    return 1

            for i in circles[0, :]:
                cv2.circle(frame, (i[0], i[1]), i[2], (0, 255, 0), 2)
                cv2.circle(frame, (i[0], i[1]), 2, (0, 0, 255), 3)
        else:
            return 0
        
        return (x, y, r)

    def get_state(self,img):
        frame = img
        result = self.signals(frame)
        return result

if __name__ == "__main__":
    lf = SignalRecollection()
    cap = cv2.VideoCapture('http://192.168.0.100:8080/?action=stream')
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: 
            break
        state = lf.get_state(frame)

        print(state)

        cv2.imshow("Image", frame)
        time.sleep(0.1)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break