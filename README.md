# RaspberryPiDetect
Detection of wooden sticks with a Raspberry PI 4 Model B

## Tools

1. RaspberryPi 4
   * Model: B
   * OS: Raspbian (64 bit)
   * RAM: 2GB
2. RaspberryPi Camera V2.1
3. LCD Touch display 7''

## Troubleshooting

1. For the raspberry pi to detect the Camera V2.1:
* Go to the file '/boost/config.txt' and be sure that the line:

    ```
    # Automatically load overlays for detected cameras
    camera_auto_detect=1

    # Automatically load overlays for detected DSI displays
    display_auto_detect=1

    # Enable DRM VC4 V3D driver
    # dtoverlay=vc4-kms-v3d
    ```

    is present.

* Reboot the raspberry pi.
* Run the command 
    ```
    libcamera-hello --list-cameras
    ```
    if you get an output different than "No cameras available!", then everything is ok.

More info: https://forums.raspberrypi.com/viewtopic.php?t=330943

2. To be able to take images with python, then install the library **picamera2** with the command:
   ```
   pip install picamera2
   ```
   picamera is not fully functional with raspberry pi 4 model B.

3. Ensure that the **numpy** version is **1.25.1**

4. PyQt and Opencv have problems when running together. Then, remove the file __libqxcb__ from 
"(virtual-env)/lib/python3.9/site-packages/cv2/qt/plugins/platforms"

More info: https://github.com/NVlabs/instant-ngp/discussions/300 
