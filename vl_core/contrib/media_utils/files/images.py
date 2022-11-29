"""
Utility functions for handling images.

Requires Pillow as you might imagine.
"""
import struct
import zlib
from os.path import splitext

from django.core.files import File
import xml.etree.cElementTree as et
from xml.etree.ElementTree import iterparse, XMLParser


class SvgImageFile(File):
    """
    A mixin for use alongside django.core.files.base.File, which provides
    additional features for dealing with images.
    """
    def _get_width(self):
        return self._get_image_dimensions()[0]
    width = property(_get_width)

    def _get_height(self):
        return self._get_image_dimensions()[1]
    height = property(_get_height)

    def _get_image_dimensions(self):
        if not hasattr(self, '_dimensions_cache'):
            close = self.closed
            self.open()
            self._dimensions_cache = get_image_dimensions(self, close=close)
        return self._dimensions_cache

    def is_svg(self):
        if not hasattr(self, '_is_svg_cache'):
            try:
                self._is_svg_cache = splitext(self.path)[1] == '.svg'
            except ValueError:
                return False
        return self._is_svg_cache


def get_image_dimensions(file_or_path, close=False):
    """
    Returns the (width, height) of an image, given an open file or a path.  Set
    'close' to True to close the file at the end if it is initially in an open
    state.
    """
    if hasattr(file_or_path, 'read'):
        file = file_or_path
        file_pos = file.tell()
        file.seek(0)
    else:
        file = open(file_or_path, 'rb')
        close = True

    if file_or_path.is_svg():
        import re

        tag = None
        try:
            parser = XMLParser()

            for event, el in iterparse(file, events=['start'], parser=parser):
                tag = el.tag
                break
        except et.ParseError:
            pass

        # Check that this "tag" is correct
        if tag != '{http://www.w3.org/2000/svg}svg':
            return None, None

        # Do not forget to "reset" file
        file.seek(0)

        width = el.attrib.get('width')
        height = el.attrib.get('height')

        if not width or not height:
            view_box = el.attrib.get('viewBox')
            if view_box:
                parts = view_box.split(' ')
                return float(parts[2]), float(parts[3])

            return None, None

        return list(map(lambda x: float(re.findall('[0-9.]*', x)[0]), [width, height]))

    # native check
    from PIL import ImageFile as PillowImageFile

    p = PillowImageFile.Parser()

    try:
        # Most of the time Pillow only needs a small chunk to parse the image
        # and get the dimensions, but with some TIFF files Pillow needs to
        # parse the whole file.
        chunk_size = 1024
        while 1:
            data = file.read(chunk_size)
            if not data:
                break
            try:
                p.feed(data)
            except zlib.error as e:
                # ignore zlib complaining on truncated stream, just feed more
                # data to parser (ticket #19457).
                if e.args[0].startswith("Error -5"):
                    pass
                else:
                    raise
            except struct.error:
                # Ignore PIL failing on a too short buffer when reads return
                # less bytes than expected. Skip and feed more data to the
                # parser (ticket #24544).
                pass
            if p.image:
                return p.image.size
            chunk_size *= 2
        return None, None
    finally:
        if close:
            file.close()
        else:
            file.seek(file_pos)
