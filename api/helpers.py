from PIL import Image
from PIL.Image import Image as ImageType
from fastapi import UploadFile
from typing import List, Literal
from datetime import datetime

IMAGE_OFFSET = 200
IMAGE_SIZE = 300
OrientationType = Literal["vertical", "horizontal"]

def get_new_image_path() -> str:
    date = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
    image_path = f"images/{date}.png"
    return image_path

def save_images(images: List[UploadFile]) -> List[str]:
    saved_images_path: List[str] = []

    for image in images:
        path_name = get_new_image_path()
        try:
            with open(path_name, 'wb') as f:
                while contents := image.file.read(1024 * 1024):
                    f.write(contents)
                saved_images_path.append(path_name)
        except Exception:
            return {"message": "There was an error uploading the file(s)"}
        finally:
            image.file.close()
    return saved_images_path

def resize_images(images: List[str])-> List[str]:
    resized_images_paths = []
    for image in images:
        image = Image.open(image).convert('RGBA').resize((IMAGE_SIZE, IMAGE_SIZE))
        image_path = get_new_image_path()
        image.save(image_path)
        resized_images_paths.append(image_path)
    return resized_images_paths

def open_images(images_path: List[str]) -> List[ImageType]:
    opened_images = []
    for image_path in images_path:
        opened_images.append(Image.open(image_path))
    return opened_images

def generate_new_sizes(base_image: ImageType, offset: int, total_images: int, is_horizontal: bool) -> dict:
    base_width = base_image.size[0] + offset if is_horizontal else base_image.size[0]
    base_height = base_image.size[1] if is_horizontal else base_image.size[1] + offset

    new_image_total_width = total_images * base_width + offset if is_horizontal else base_width
    new_image_total_height = base_height if is_horizontal else total_images * base_height + offset

    return {"width": new_image_total_width, "height": new_image_total_height}

def create_new_image(images_path: List[str], orientation: OrientationType, offset: int | None = IMAGE_OFFSET, color: str | None = (255, 255, 255)) -> ImageType:
    opened_images = open_images(images_path)
    base_image = opened_images[0]
    total_images = len(opened_images)

    is_horizontal = orientation == "horizontal"
    new_sizes = generate_new_sizes(base_image, offset, total_images, is_horizontal)

    new_image = Image.new('RGB',(new_sizes['width'], new_sizes['height']), color)

    if is_horizontal:
        last_width = 0 + offset
        for image in opened_images:
            new_image.paste(image, (last_width, 0))
            last_width += image.size[0] + offset

    else:
        last_height = 0 + offset
        for image in opened_images:
            new_image.paste(image, (0, last_height))
            last_height += image.size[1] + offset


    return new_image

def merge_images(images_path: List[str], orientation: OrientationType, border: int | None, color: str | None) -> str:
    new_image = create_new_image(images_path, orientation=orientation, offset=border, color=color)
    new_image.save("mergedimages/merged_image.jpg","JPEG")
    new_image.show()

    return "merged_image.jpg"