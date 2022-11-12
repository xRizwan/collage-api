from PIL import Image
from PIL.Image import Image as ImageType

def create_new_image(images: list[ImageType], offset: int) -> ImageType:
    base_width = images[0].size[0] + offset
    base_height = images[0].size[1]
    total_images = len(images)

    new_image = Image.new('RGB',(total_images*base_width, base_height), (250,250,250))

    last_width = 0 + offset

    for image in images:
        new_image.paste(image, (last_width, 0))
        last_width += image.size[0] + offset

    return new_image

def mergeImages():
    offset = 200

    image1 = Image.open("images/back.png")
    images = [image1, image1, image1]

    new_image = create_new_image(images, offset)
    new_image.save("images/merged_image.jpg","JPEG")
    new_image.show()

mergeImages()