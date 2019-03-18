import time
from camera import Camera

if __name__ == "__main__":
    fps = 2.0
    sleep_time = 1.0/fps
    count = 1
    width = 200
    height = 200

    with Camera() as cam:
        while True:
            time.sleep(sleep_time)
            file_name = f"images/img{count}.png"

            cam.shoot_and_save(file_name, width, height)
    
            print(f"Image {count} taken")
            count += 1