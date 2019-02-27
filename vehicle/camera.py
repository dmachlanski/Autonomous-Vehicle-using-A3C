import cv2

class Camera:
    def __init__(self):
        self.vc = cv2.VideoCapture(0)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.vc.release()
        cv2.destroyAllWindows()

    def shoot(self, width, height):
        _, frame = self.vc.read()
        return cv2.resize(frame, (width, height))

    def shoot_and_save(self, file_name, width, height):
        img = self.shoot(width, height)
        cv2.imwrite(file_name, img)