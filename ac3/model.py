import torchvision.models as models
import torchvision.transforms as transforms
import numpy as np
from PIL import Image

from helper import load_stuff

# densenet121
model = models.vgg16(pretrained=True)

normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])

preprocess = transforms.Compose([
   transforms.Resize(256),
   transforms.CenterCrop(224),
   transforms.ToTensor(),
   normalize
])


def feature_vec(img):
    # temp = np.rollaxis(img, 0, 3)

    temp = np.uint8(img)

    img_pil = Image.fromarray(temp)

    img_tensor = preprocess(img_pil)
    print("four") 
    img_tensor_ = img_tensor.unsqueeze_(0)
    print("five") 
    # print(model)
    return model.features(img_tensor_).view(-1)


# img, reward, done = load_stuff("pickled")
# torch.Size([1, 512, 7, 7])
# tensor([0., 0., 0.,  ..., 0., 0., 0.], grad_fn=<ViewBackward>)
# torch.Size([25088])

# feat = feature_vec(img)
# print(feat)
# print(feat.shape)
