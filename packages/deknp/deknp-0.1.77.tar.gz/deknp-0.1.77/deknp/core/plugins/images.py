import os
from dektools.file import read_file
from dekmedia.image.core import resize_image
from dekmedia.image.svg import load_svg
from .base import Plugin


class PluginImages(Plugin):
    dek_key_images = 'images'

    def run(self):
        images = self.merge_from_key(self.dek_key_images)
        for s, dll in images.items():
            src = os.path.join(self.project_dir, s)
            if os.path.isfile(src) and dll:
                for d, dl in dll.items():
                    if dl is not None:
                        dl = [int(x) for x in dl]
                        sizes = None
                        if len(dl) % 2:
                            dl = [*dl, dl[-1]]
                        if len(dl) > 0:
                            sizes = list(zip(dl[::2], dl[1::2]))
                        image = load_svg(read_file(src), width=max(x[0] for x in sizes) if sizes else None)
                        if not sizes:
                            sizes = [image.size]
                        resize_image(image, os.path.join(self.project_dir, d), sizes)
