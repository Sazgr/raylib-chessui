import cv2
from PIL import Image
import numpy as np

img = Image.open("assets/scroll2bg.png")
image = np.array(img)

image_shape = image.shape
print(f"Image dimensions (height, width, channels): {image_shape}")

modified_image = image.copy()
for i in range(0, image.shape[0]):
    for j in range(0, image.shape[1]):
        coord = (i, j)
        print(f"Pixel value at {coord}: {image[coord]} (BGR)")
        if image[coord][0] == 0:
            print("black pixel found")
            modified_image[coord] = [0, 0, 0, 0]  
        print(f"After modifying, pixel value at {coord}: {modified_image[coord]} (BGR)")

newimg = Image.fromarray(modified_image)
newimg.save('assets/scroll2.png', 'PNG')