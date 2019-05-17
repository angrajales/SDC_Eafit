import cv2
import numpy as np
import time

class LineFollowing(object):
    def __init__(self):
        self.polyLeft1 = 450
        self.polyRight1 = 320
        self.polyLeft2 = 500
        self.polyRight2 = 320
        self.ignore_mask_color = 255 # White color
    def next_action(self, frame, slope=-1):
        p_next_action = "do_nothing"
        p_next_action_c = "do_nothing"
        canny = self.__do_canny(frame)
        frame_shape = frame.shape
        vertices = np.array([[(0,frame_shape[0]),(self.polyLeft1, self.polyRight1), (self.polyLeft2, self.polyRight2), (frame_shape[1],frame_shape[0])]], dtype=np.int32)
        mask = np.zeros_like(canny)
        cv2.fillPoly(mask, vertices, self.ignore_mask_color)
        masked_edges = cv2.bitwise_and(canny, mask)
        ########################### Parameter Tunning ####################################
        [rho, theta, threshold, min_line_length, max_line_gap] = self.__tune_params()
        line_image = np.copy(frame) * 0
        
        ############################ Finding Lines #######################################
        lines = cv2.HoughLinesP(masked_edges, rho, theta, threshold, np.array([]), min_line_length, max_line_gap)
        ############################ Next Action #########################################
        last_valid_slope = slope
        lines_edges = None
        if lines is None or not lines.any():
            p_next_action = "do_nothing"
        else:
            for line in lines:
                n_slope = last_valid_slope
                for x1, y1, x2, y2 in line:
                    if int(x2 - x1) != 0:
                        n_slope = (y2 - y1) / (x2 - x1)
                        last_valid_slope = n_slope
                    else:
                        n_slope = last_valid_slope
                    text = ""
                    distance = (frame.shape[0] - x1) / frame.shape[0] + (frame.shape[0] - x2) / frame.shape[1]
                    if distance > 0.530:
                        print('Distance -> ',  str(distance), 'ML')
                        p_next_action_c = "ML"
                        text = "Move Left"
                    elif distance < 0.470:
                        print('Distance -> ',  str(distance), 'MR')
                        p_next_action_c = "MR"
                        text = "Move Right"
                    if abs(n_slope) < 1.0:
                        print('slope -> ',  str(abs(n_slope)), 'MLR')
                        text = "Move either left or right"
                        p_next_action = "MLR"
                    else:
                        print('Slope -> ',  str(abs(n_slope)), 'MF')
                        text = "Move forward"
                        p_next_action = "MF"
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    textsize = cv2.getTextSize(text, font, 1, 2)[0]
                    frame_center_x = int((frame.shape[1] - textsize[0]) / 2)
                    frame_center_y = int((frame.shape[0] + textsize[1]) / 2)
                    cv2.line(line_image,(x1,y1),(x2,y2),(0,0,255),10)
                    distance = (frame.shape[1] - x1) / frame.shape[1] + (frame.shape[1] - x2) / frame.shape[1]
                    cv2.putText(frame, text, (frame_center_x, frame_center_y ), font, 1, (0, 255, 0), 5)
            lines_edges = cv2.addWeighted(frame, 0.8, line_image, 1, 0)
        return [lines_edges, p_next_action_c, p_next_action, last_valid_slope]
    def __tune_params(self):
        rho = 2
        theta = np.pi / 180
        threshold = 5
        min_line_length = 40
        max_line_gap = 30
        return [rho, theta, threshold, min_line_length, max_line_gap]

    def __do_canny(self, frame):
        gray_image = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        blurred_image = cv2.GaussianBlur(gray_image, (9, 9), 0)
        canny = cv2.Canny(blurred_image, 50, 150)
        return canny

if __name__ == "__main__":
    lf = LineFollowing()
    cap = cv2.VideoCapture('./out2.avi')
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: 
            break
        [lines_edges, p_next_action_c, p_next_action, last_valid_slope] = lf.next_action(frame)
        if p_next_action != "do_nothing":
            cv2.imshow("Image", line_edges)
            time.sleep(0.1)
        else:
            print("Error while trying the image...")
            continue
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break