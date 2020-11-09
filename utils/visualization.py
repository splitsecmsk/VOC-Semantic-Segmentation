import numpy as np
import matplotlib.pyplot as plt
import torch

from train import predict

color_dict = range(100, 1000, 25)
color_dict = [*color_dict][:21]
num_class = 21
# print("Color dict: ", color_dict)

# https://github.com/zijundeng/pytorch-semantic-segmentation/blob/master/datasets/voc.py

palette = [[0, 0, 0], [128, 0, 0], [0, 128, 0], [128, 128, 0], [0, 0, 128], [128, 0, 128], [0, 128, 128],
           [128, 128, 128], [64, 0, 0], [192, 0, 0], [64, 128, 0], [192, 128, 0], [64, 0, 128], [192, 0, 128],
           [64, 128, 128], [192, 128, 128], [0, 64, 0], [128, 64, 0], [0, 192, 0], [128, 192, 0], [0, 64, 128]]

def labelVisualize(img):
    img_out = np.zeros(img.shape + (3,))

    for i in range(num_class):
        img_out[img == i] = palette[i]
    return img_out

def visualizePrediction(model, images, labels, heatmap=False):

    if (len(images.shape) == 3 and len(labels.shape) == 2):
        images = np.expand_dims(images, axis=0)
        labels = np.expand_dims(labels, axis=0)

    image_count = len(images)


    # fig = plt.figure(figsize=(20, 20))

    preds = predict(model, images)

    ind = 1
    for i in range(image_count):
        plt.subplots(1, 3, figsize=(15, 15))  # specifying the overall grid size

        plt.subplot(1, 3, ind)
        # plt.imshow(images[i])

        # fig.add_subplot(image_count, 3, ind)
        plt.imshow(images[i])

        ind += 1

        # print("Label: ", labels[i])
        # print("Label Unique: ", np.unique(labels[i]))

        plt.subplot(1, 3, ind)
        # fig.add_subplot(image_count, 3, ind)

        if heatmap:
            plt.imshow(labels[i], cmap='hot')
        else:
            plt.imshow(labelVisualize(labels[i]))

        ind += 1

        if torch.cuda.is_available():
            # print(i, " unique: ", np.unique(preds[i].cpu().detach()))
            pred = preds[i].cpu().detach().numpy().argmax(0)
            # print(i, "after argmax unique: ", np.unique(pred))
        else:
            # print(i, " unique: ", np.unique(preds[i].detach()))
            pred = preds[i].detach().numpy().argmax(0)
            # print(i, "after argmax unique: ", np.unique(pred))

        # print("Pred: ", pred)
        # print("Label Unique Pred: ", np.unique(pred))
        plt.subplot(1, 3, ind)
        # fig.add_subplot(image_count, 3, ind)

        # plt.imshow(pred, cmap='hot')
        if heatmap:
            plt.imshow(pred, cmap='hot')
        else:
            plt.imshow(labelVisualize(pred))
        ind = 1

    plt.show()
