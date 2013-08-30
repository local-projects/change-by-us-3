import os
from PIL import Image
from PIL import ImageOps
from flask import current_app


class NamedImage():
    def __init__(self, name=None, image=None ):
        self.name = name
        self.image = image


class ImageManipulator():
    def __init__(self, dict_name = None, converter = None, prefix = None):
        self.dict_name = dict_name
        self.converter = converter
        self.prefix = prefix


def generate_thumbnail( filepath, size ):
    """
    ABOUT
        Routine that will take a full sized image path and generate
        an x,y sized thumbnail with the naming convention 
        name_thumb.extension
    INPUT
        Path to an image, any standard extension
    OUTPUT
        File path for an image of 1020,320 pixels
    TODO
        Make the image output size a parameter
    """

    # note if you change these guys you need to change templates and the project model

    # TODO change it so it only takes a size

    try:

        images = []

        img = Image.open(filepath)

        path, image = os.path.split(filepath)
        base, extension = os.path.splitext(image)

        for size in sizes:
            sizeStr = ".{0}.{1}".format( sizes[0], sizes[1] )
            name = base + sizeStr + extension
            img = ImageOps.fit( image=img, size=size, method=Image.ANTIALIAS )

            resource = NamedImage( image=img, name=name )
            images.push_back(resource)

        return images

    except IOError as e:

        current_app.logger.exception(e)

        return []


def generate_blurred_bg():
    # LV TODO
    pass

def generate_circled_crop():
    # LV TODO
    pass
