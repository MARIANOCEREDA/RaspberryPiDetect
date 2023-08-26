import sys

if __name__ == "__main__":

    sys.path.append(f"C:/Users/merem/Documents/TESIS/code/deploy/RaspberryPiDetect/yoloV5/utils")
    sys.path.append(f"C:/Users/merem/Documents/TESIS/code/deploy/RaspberryPiDetect/yoloV5")
    sys.path.append(f"C:/Users/merem/Documents/TESIS/code/deploy/RaspberryPiDetect/yoloV5/models")

    from yoloV5.custom_detect import main

    main()