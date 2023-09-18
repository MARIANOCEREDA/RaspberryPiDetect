import time
from picamera2 import Picamera2, Preview
from picamera2.encoders import H264Encoder

def take_photo(result_path:str, n_photos:int) -> None:

    photo_config = {
        "resolution":{
            "x":3000,
            "y":2000
        }
    }   

    for i in range(n_photos):

        with Picamera2() as picam:

            size = (photo_config["resolution"]["x"], photo_config["resolution"]["y"])

            config = picam.create_preview_configuration(main={"size": size}, lores={"size": (640, 480)}, display="lores")
            picam.configure(config)

            picam.start_preview(Preview.QTGL)

            picam.start()

            time.sleep(1)

            path = result_path + "_3240x2464_8_10_5_mas_cerca" + str(i) + ".jpg"

            picam.capture_file(path)

            picam.close()


def start_video():

    video_config = {
        "resolution":{
            "x":1280,
            "y":720
        }
    }   

    with Picamera2() as picam:

        size = (video_config["resolution"]["x"], video_config["resolution"]["y"])

        video_config = picam.create_preview_configuration(main={"size": size}, lores={"size": (640, 480)}, display="lores")
        picam.configure(video_config)

        encoder = H264Encoder(bitrate=10000000)

        output = "test.h264"

        picam.start_preview(Preview.QTGL)

        picam.start_recording(encoder, output)

        time.sleep(20)

        picam.stop_recording()

        picam.stop_preview()


if __name__ == "__main__":

    take_photo("photos/output.jpg", n_photos = 3)

    # start_video()
