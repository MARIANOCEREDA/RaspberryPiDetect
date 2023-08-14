import torch
import torchvision
import torchvision.transforms as T
import numpy as np
import matplotlib.pyplot as plt
import requests
from PIL import Image
from models.common import DetectMultiBackend

def preprocess(image, size=640):
    transform = T.Compose([
        T.Resize((size,size)),
        T.ToTensor(),
        T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        T.Lambda(lambda x: x[None]),
    ])
    return transform(image)

'''
    Y = (X - μ)/(σ) => Y ~ Distribution(0,1) if X ~ Distribution(μ,σ)
    => Y/(1/σ) follows Distribution(0,σ)
    => (Y/(1/σ) - (-μ))/1 is actually X and hence follows Distribution(μ,σ)
'''
def deprocess(image):
    transform = T.Compose([
        T.Lambda(lambda x: x[0]),
        T.Normalize(mean=[0, 0, 0], std=[4.3668, 4.4643, 4.4444]),
        T.Normalize(mean=[-0.485, -0.456, -0.406], std=[1, 1, 1]),
        T.ToPILImage(),
    ])
    return transform(image)

def show_img(PIL_IMG):
    plt.imshow(np.asarray(PIL_IMG))

# Load pre-trained YOLOv5 model
weights = "./yolov5n_sticks.pt"
model = DetectMultiBackend(weights, device=torch.device("cuda"), dnn=False, data=None, fp16=False)

for param in model.parameters():
    param.requires_grad = False

# Load and preprocess an image
image_path = r'C:/Users/merem/Documents/TESIS/code/tesis\dataset\sticks/val/images/20230602_182315.jpg'

img = Image.open(image_path) 

# Enable gradient calculation
X = preprocess(img)

# Forward pass
scores = model(X.to("cuda"))

print()

# Get the index corresponding to the maximum score and the maximum score itself.
score_max_index = scores[0].argmax()
score_max = scores[0][0, score_max_index]

'''
backward function on score_max performs the backward pass in the computation graph and calculates the gradient of 
score_max with respect to nodes in the computation graph
'''
score_max.backward()

'''
Saliency would be the gradient with respect to the input image now. But note that the input image has 3 channels,
R, G and B. To derive a single class saliency value for each pixel (i, j),  we take the maximum magnitude
across all colour channels.
'''
saliency, _ = torch.max(X.grad.data.abs(),dim=1)

# Visualize saliency map
plt.imshow(saliency[0], cmap=plt.cm.hot)
plt.axis('off')
plt.show()
