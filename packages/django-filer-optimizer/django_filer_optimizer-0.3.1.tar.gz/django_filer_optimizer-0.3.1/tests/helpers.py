from PIL import Image, ImageDraw
from django.contrib.auth.models import User


def create_superuser():
    superuser = User.objects.create_superuser("admin", "admin@django.it", "secret")
    return superuser


def create_image(mode="RGB", size=(800, 600)):
    image = Image.new(mode, size)
    draw = ImageDraw.Draw(image)
    x_bit, y_bit = size[0] // 10, size[1] // 10
    draw.rectangle((x_bit, y_bit * 2, x_bit * 7, y_bit * 3), "red")
    draw.rectangle((x_bit * 2, y_bit, x_bit * 3, y_bit * 8), "red")
    return image
