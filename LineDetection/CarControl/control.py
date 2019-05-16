import cv2
class Control(object):
    def __init__(self, base_url):
        self.base_url = base_url
        
    def next_frame(self):
        cap = cv2.VideoCapture("http://192.168.0.101:8080/?action=stream")
        if cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Error while reading next frame...")
                return
            return frame
    def move_forward(self):
        r = requests.get(self.base_url + "?action=strea")
if __name__ == "__main__":
    cap = cv2.VideoCapture("http://192.168.0.101:8080/?action=stream")
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Error reading frame...")
            break
        cv2.imshow("Image", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Exiting ...")
            break
    print("Exiting")
        
        
