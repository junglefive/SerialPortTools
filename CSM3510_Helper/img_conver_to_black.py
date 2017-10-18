from PIL import  Image
import  numpy as np

img_name = "logo.png"
img = Image.open(img_name).convert('L')
img.show()
img_arry = np.array(img)

rows,cols = img_arry.shape
for i in range(rows):
    for j in range(cols):
        if img_arry[i,j] <= 20:
            img_arry[i,j] = 0
        else:
            img_arry[i,j] = 255
img_save = Image.fromarray(img_arry)
img_save.save(img_name)