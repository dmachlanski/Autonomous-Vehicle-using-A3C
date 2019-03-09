import torchvision.models as models
import torchvision.transforms as transforms
import numpy as np
from PIL import Image


resnet18 = models.resnet18(pretrained=True)

normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])

preprocess = transforms.Compose([
   transforms.Resize(256),
   transforms.CenterCrop(224),
   transforms.ToTensor(),
   normalize
])


def feature_vec(img):
    img_pil = Image.fromarray(np.rollaxis(img, 0, 3))
    img_tensor = preprocess(img_pil)
    img_tensor_ = img_tensor.unsqueeze_(0)
    return resnet18.features(img_tensor_)
