from PIL import Image
from PIL import ImageOps

# image = Image.open("resources/images/brick_texture_256.jpg")
# image = image.crop((200, 0, 300, 256))
# image = ImageOps.fit(image, (image.width, 448))
# print(image.size)
# image.show()


image_path = "resources\images\\brick_texture_256.jpg"

img = Image.open(image_path)
img_1 = None
img_2 = None

left = 128
right = 128 + 256
x_offset = int((left + right) / 2)

if (right) > img.width:
    img_2 = Image.open(image_path)
    img_1 = img
    extra_x = right - img.width

    img_1.crop((left, 0, x_offset, img_1.height))
    img_2.crop((0, 0, extra_x, img_2.height))

    img = Image.new("RGBA", (img_1.width + img_2.width, img_1.height))
    img.paste(img_1)
    img.paste(img_2, (img_1.width, 0))

img.show()