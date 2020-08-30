import os

UPLOADS_IMAGES = os.path.join(os.path.abspath(os.curdir), 'uploads')


def upload_image(image, name):
    image.save(os.path.join(UPLOADS_IMAGES, name))
    return 0


def upload_user_image(image, name):
    image.save(os.path.join(UPLOADS_IMAGES, 'users', name))
    return 0


def upload_place_image(image, pid, name):
    image.save(os.path.join(UPLOADS_IMAGES, 'places', pid, name))
    return 0
