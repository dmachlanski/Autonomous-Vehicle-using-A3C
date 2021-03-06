import torchvision.models as models
import torchvision.transforms as transforms
import numpy as np
from PIL import Image
import torch

from helper import load_stuff

is_cuda = torch.cuda.is_available()
is_cuda = False

# densenet121
model = models.vgg16(pretrained=True)

if is_cuda:
   model = model.cuda()

normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])

preprocess = transforms.Compose([
   transforms.Resize(256),
   transforms.CenterCrop(224),
   transforms.ToTensor(),
   normalize
])

if is_cuda:
   preprocess = preprocess.cuda()

def feature_vec(img):
    # temp = np.rollaxis(img, 0, 3)

    temp = np.uint8(img)

    img_pil = Image.fromarray(temp)
    print("infinite loop occurs at at line 38 in model.py, \n'img_tensor = preprocess(img_pil)'")
    img_tensor = preprocess(img_pil)
    print("eroor resolved") 
    img_tensor_ = img_tensor.unsqueeze_(0)
    return model.features(img_tensor_).view(-1)


# img, reward, done = load_stuff("pickled")
# torch.Size([1, 512, 7, 7])
# tensor([0., 0., 0.,  ..., 0., 0., 0.], grad_fn=<ViewBackward>)
# torch.Size([25088])

# feat = feature_vec(img)
# print(feat)
# print(feat.shape)
