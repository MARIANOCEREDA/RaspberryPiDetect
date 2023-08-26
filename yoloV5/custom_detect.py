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
from utils.general import (LOGGER, Profile, check_file, check_img_size, check_i>
                           increment_path, non_max_suppression, print_args, sca>
from utils.plots import Annotator, colors, save_one_box
from utils.torch_utils import select_device, smart_inference_mode


@smart_inference_mode()
def run_inference(
