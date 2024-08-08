import discord
from PIL.Image import Image
import io


def image_to_file(image: Image, filename:str = "result.png"):
    with io.BytesIO() as image_binary:
        image.save(image_binary, "PNG")
        image_binary.seek(0)
        file = discord.File(fp=image_binary, filename=filename)
    return file
