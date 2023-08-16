import os
import platform
import sys
from pathlib import Path
import matplotlib.pyplot as plt
import torch
import yaml
import numpy as np

from models.common import DetectMultiBackend
from utils.dataloaders import IMG_FORMATS, VID_FORMATS, LoadImages
from utils.general import (LOGGER, Profile, check_file, check_img_size, check_imshow, check_requirements, colorstr, cv2,
                           increment_path, non_max_suppression, print_args, scale_boxes, strip_optimizer, xyxy2xywh)
from utils.plots import Annotator, colors, save_one_box
from utils.torch_utils import select_device, smart_inference_mode


@smart_inference_mode()
def run_inference(
        weights,
        source,
        data,
        imgsz,# inference size (height, width)
        conf_thres, # confidence threshold
        iou_thres, # NMS IOU threshold
        max_det, # maximum detections per image
        device, # cuda device, i.e. 0 or 0,1,2,3 or cpu
        view_img,  # show results
        save_txt,  # save results to *.txt
        save_conf,  # save confidences in --save-txt labels
        save_crop,  # save cropped prediction boxes
        nosave,  # do not save images/videos
        classes,  # filter by class: --class 0, or --class 0 2 3
        agnostic_nms,  # class-agnostic NMS
        augment,  # augmented inference
        visualize,  # visualize features
        update,  # update all models
        project,  # save results to project/name
        exist_ok,  # existing project/name ok, do not increment
        line_thickness,  # bounding box thickness (pixels)
        hide_labels,  # hide labels
        hide_conf,  # hide confidences
        half,  # use FP16 half-precision inference
        dnn,  # use OpenCV DNN for ONNX inference
        vid_stride,  # video frame-rate stride
):

    source = str(source)
    save_img = not nosave and not source.endswith('.txt')  # save inference images
    is_file = Path(source).suffix[1:] in (IMG_FORMATS + VID_FORMATS)

    # Directories
    save_dir = Path(project)
    (save_dir / 'labels' if save_txt else save_dir).mkdir(parents=True, exist_ok=True)  # make dir

    # Load model
    device = select_device(device)
    model = DetectMultiBackend(weights, device=device, dnn=dnn, data=data, fp16=half)
    stride, names, pt = model.stride, model.names, model.pt
    imgsz = check_img_size(imgsz, s=stride)  # check image size

    # Dataloader
    bs = 1  # batch_size
    dataset = LoadImages(source, img_size=imgsz, stride=stride, auto=pt, vid_stride=vid_stride)
    vid_path, vid_writer = [None] * bs, [None] * bs

    # Run inference
    model.warmup(imgsz=(1 if pt or model.triton else bs, 3, *imgsz))  # warmup
    seen, windows, dt = 0, [], (Profile(), Profile(), Profile())
    for path, im, im0s, vid_cap, s in dataset:
        with dt[0]:
            im = torch.from_numpy(im).to(model.device)
            im = im.half() if model.fp16 else im.float()  # uint8 to fp16/32
            im /= 255  # 0 - 255 to 0.0 - 1.0
            if len(im.shape) == 3:
                im = im[None]  # expand for batch dim

        # Inference
        with dt[1]:
            visualize = increment_path(save_dir / Path(path).stem, mkdir=True) if visualize else False
            pred = model(im, augment=augment, visualize=visualize)
    
        # NMS
        with dt[2]:
            pred = non_max_suppression(pred, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)

        # Process predictions
        for i, det in enumerate(pred):  # per image
            seen += 1
            p, im0, frame = path, im0s.copy(), getattr(dataset, 'frame', 0)

            p = Path(p)  # to Path
            save_path = str(save_dir / p.name)  # im.jpg
            txt_path = str(save_dir / 'labels' / p.stem) + ('' if dataset.mode == 'image' else f'_{frame}')  # im.txt
            s += '%gx%g ' % im.shape[2:]  # print string
            gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
            imc = im0.copy() if save_crop else im0  # for save_crop
            annotator = Annotator(im0, line_width=line_thickness, example=str(names))
            if len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_boxes(im.shape[2:], det[:, :4], im0.shape).round()

                # Print results
                for c in det[:, 5].unique():
                    n = (det[:, 5] == c).sum()  # detections per class
                    s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string

                # Write results
                for *xyxy, conf, cls in reversed(det):
                    if save_txt:  # Write to file
                        xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # normalized xywh
                        line = (cls, *xywh, conf) if save_conf else (cls, *xywh)  # label format
                        with open(f'{txt_path}.txt', 'a') as f:
                            f.write(('%g ' * len(line)).rstrip() % line + '\n')

                    if save_img or save_crop or view_img:  # Add bbox to image
                        c = int(cls)  # integer class
                        label = None if hide_labels else (names[c] if hide_conf else f'{names[c]} {conf:.2f}')
                        annotator.box_label(xyxy, label, color=colors(c, True))
                    if save_crop:
                        save_one_box(xyxy, imc, file=save_dir / 'crops' / names[c] / f'{p.stem}.jpg', BGR=True)

            # Stream results
            im0 = annotator.result()
            if view_img:
                if platform.system() == 'Linux' and p not in windows:
                    windows.append(p)
                    cv2.namedWindow(str(p), cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)  # allow window resize (Linux)
                    cv2.resizeWindow(str(p), im0.shape[1], im0.shape[0])
                cv2.imshow(str(p), im0)
                cv2.waitKey(1)  # 1 millisecond

            # Save results (image with detections)
            if save_img:
                if dataset.mode == 'image':
                    cv2.imwrite(save_path, im0)
                else:  # 'video' or 'stream'
                    if vid_path[i] != save_path:  # new video
                        vid_path[i] = save_path
                        if isinstance(vid_writer[i], cv2.VideoWriter):
                            vid_writer[i].release()  # release previous video writer
                        if vid_cap:  # video
                            fps = vid_cap.get(cv2.CAP_PROP_FPS)
                            w = int(vid_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                            h = int(vid_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                        else:  # stream
                            fps, w, h = 30, im0.shape[1], im0.shape[0]
                        save_path = str(Path(save_path).with_suffix('.mp4'))  # force *.mp4 suffix on results videos
                        vid_writer[i] = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))
                    vid_writer[i].write(im0)

        # Print time (inference-only)
        LOGGER.info(f"{s}{'' if len(det) else '(no detections), '}{dt[1].dt * 1E3:.1f}ms")

    # Print results
    t = tuple(x.t / seen * 1E3 for x in dt)  # speeds per image
    LOGGER.info(f'Speed: %.1fms pre-process, %.1fms inference, %.1fms NMS per image at shape {(1, 3, *imgsz)}' % t)
    if save_txt or save_img:
        s = f"\n{len(list(save_dir.glob('labels/*.txt')))} labels saved to {save_dir / 'labels'}" if save_txt else ''
        LOGGER.info(f"Results saved to {colorstr('bold', save_dir)}{s}")
    if update:
        strip_optimizer(weights[0])  # update model (to fix SourceChangeWarning)



def read_results_from_txt(file_path):

    data_list = []

    # Open the file in read mode

    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            for line in file:
                # Split the line into a list of strings using spaces as separators
                line_data = line.strip().split()
                data_list.append(line_data)

    # Convert the list of lists to a NumPy array
    return np.array(data_list).astype(float)

def get_main_package(packages:np.array) -> np.array:

    main_package = np.empty((1, 4))

    if len(packages) > 1:

        areas = np.array([ p[3] * p[4] for p in packages])
        max_area_index = np.argmax(areas)
        main_package = packages[max_area_index]
    
    else:
        main_package = packages

    return main_package

            
def filter_sticks_within_package(sticks:np.array, package:np.array) -> np.array:

    _, x, y, w, h = package

    x_max = x + w / 2
    x_min = x - w / 2
    y_max = y + h / 2
    y_min = y - h / 2

    filtered_data = []

    for stick in sticks:

        _, x_s, y_s, w_s, h_s = sticks


    pass



def main():

    CONFIG_FILE = os.path.dirname(__file__) + "/config.yaml"
    with open(CONFIG_FILE) as f:
        config_data = yaml.safe_load(f)

    FILE = Path(__file__).resolve()
    print(FILE)
    ROOT = FILE.parents[0]  #  root directory
    if str(ROOT) not in sys.path:
        sys.path.append(str(ROOT))  # add ROOT to PATH
    ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

    # Run for sticks 

    print(config_data)

    for key, value in config_data.items():

        if key == "sticks" or key == "packages":

            run_inference(weights=config_data[key]["weights"],  # model path or triton URL
                source=config_data["source"],  # file/dir/URL/glob/screen/0(webcam)
                data=ROOT / 'data/coco128.yaml',  # dataset.yaml path
                imgsz=(config_data["img_size"], config_data["img_size"]),  # inference size (height, width)
                conf_thres=config_data[key]["conf_thres"],  # confidence threshold
                iou_thres=config_data[key]["iou_thres"],  # NMS IOU threshold
                max_det=1000,  # maximum detections per image
                device=config_data["device"],  # cuda device, i.e. 0 or 0,1,2,3 or cpu
                view_img=False,  # show results
                save_txt=config_data["save_txt"],  # save results to *.txt
                save_conf=False,  # save confidences in --save-txt labels
                save_crop=False,  # save cropped prediction boxes
                nosave=False,  # do not save images/videos
                classes=None,  # filter by class: --class 0, or --class 0 2 3
                agnostic_nms=False,  # class-agnostic NMS
                augment=False,  # augmented inference
                visualize=False,  # visualize features
                update=False,  # update all models
                project=config_data[key]["results"],  # save results to project/name
                exist_ok=False,  # existing project/name ok, do not increment
                line_thickness=config_data["line_thickness"],  # bounding box thickness (pixels)
                hide_labels=config_data["hide_labels"],  # hide labels
                hide_conf=False,  # hide confidences
                half=False,  # use FP16 half-precision inferenc2e
                dnn=False,  # use OpenCV DNN for ONNX inference
                vid_stride=1,  # video frame-rate stride
            )

    sticks_results_path = os.path.dirname(__file__) + "/" + config_data["sticks"]["results"] + "/labels/image.txt"
    packages_results_path = os.path.dirname(__file__) + "/" + config_data["packages"]["results"] + "/labels/image.txt"

    sticks = read_results_from_txt(sticks_results_path)
    packages = read_results_from_txt(packages_results_path)

    main_package = get_main_package(packages)

    print(main_package)



if __name__ == '__main__':
    main()

