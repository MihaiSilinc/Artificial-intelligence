# load and show an image with Pillow
from PIL import Image
from matplotlib import image as i
from matplotlib import pyplot

# load the image
image = Image.open('f1.jpg')
# summarize some details about the image
print(image.format)
print(image.mode)
print(image.size)
# show the image
image.show()
# load and display an image with Matplotlib

# load image as pixel array
data = i.imread('f1.jpg')
# summarize shape of the pixel array
print(data.dtype)
print(data.shape)
# display the array of pixels as an image
pyplot.imshow(data)
pyplot.show()

# create a thumbnail of an image
# load the image
image = Image.open('males2/1-11.jpg')
# report the size of the image
print(image.size)
# create a thumbnail and preserve aspect ratio
image.thumbnail((100, 100))
# report the size of the thumbnail
print(image.size)
