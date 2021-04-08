import os

UPLOADS_IMAGES = os.path.join(os.path.abspath(os.curdir), 'images')


def upload_image(image, name):
    image.save(os.path.join(UPLOADS_IMAGES, name))
    return 0


def upload_user_image(image, name):
    user_dir = os.path.join(UPLOADS_IMAGES, 'users')
    if not os.path.exists(user_dir):
        os.makedirs(user_dir)
    image.save(os.path.join(user_dir, name))
    return 0


def upload_product_image(image, pid, name):
    place_dir = os.path.join(UPLOADS_IMAGES, 'products')
    if not os.path.exists(place_dir):
        os.makedirs(place_dir)
    image.save(os.path.join(place_dir, name))
    return 0
