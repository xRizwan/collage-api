from PIL import Image
from PIL.Image import Image as ImageType
from fastapi import UploadFile
from typing import List

IMAGE_OFFSET = 200

def save_images(images: List[UploadFile]) -> List[str]:
    saved_images_path: List[str] = []

    for image in images:
        try:
            with open(image.filename, 'wb') as f:
                while contents := image.file.read(1024 * 1024):
                    f.write(contents)
                saved_images_path.append(f.name)
        except Exception:
            return {"message": "There was an error uploading the file(s)"}
        finally:
            image.file.close()
    return saved_images_path

def open_images(images_path: List[str]) -> List[ImageType]:
    opened_images = []
    for image_path in images_path:
        opened_images.append(Image.open(image_path))
    return opened_images

def create_new_image(images_path: List[str], offset: int) -> ImageType:
    opened_images = open_images(images_path)
    base_image = opened_images[0]

    base_width = base_image.size[0] + offset
    base_height = base_image.size[1]
    total_images = len(opened_images)

    new_image = Image.new('RGB',(total_images*base_width, base_height), (250,250,250))

    last_width = 0 + offset

    for image in opened_images:
        new_image.paste(image, (last_width, 0))
        last_width += image.size[0] + offset

    return new_image

def merge_images(images_path: List[str]) -> ImageType:
    new_image = create_new_image(images_path, IMAGE_OFFSET)
    new_image.save("images/merged_image.jpg","JPEG")
    new_image.show()

    return new_image