import os

import numpy as np
from PIL import Image

from trame_rca.utils import AbstractWindow
import libeegviz


class EEGWindow(AbstractWindow):
    def __init__(self, data_path, **kwargs):
        if not os.path.exists(data_path):
            raise Exception("Path does not exist")
        self._context = libeegviz.create(data_path)
        self._events = ["MouseMove", "LeftButtonPress", "RightButtonPress", "KeyDown"]
        self._keys = [
            " ",
            "a",
            "ArrowDown",
            "ArrowLeft",
            "ArrowRight",
            "ArrowUp",
            "c",
            "d",
            "Enter",
            "Escape",
            "i",
            "k",
            "n",
            "p",
            "q",
            "r",
            "Tab",
            "u",
            "v",
            "z",
        ]

    def _move(self, x, y):
        libeegviz.move(self._context, x, y)

    def _click(self, button):
        libeegviz.click(self._context, button)

    def _keydown(self, key):
        libeegviz.key(self._context, key)

    def rgba_to_rgb(self, rgba_image_array):
        """Convert an RGBA image array to an RGB image array by alpha blending over a white background."""
        rgba_image_array = rgba_image_array.astype(np.float32) / 255.0
        rgb_array = rgba_image_array[..., :3]
        alpha_array = rgba_image_array[..., 3:]
        bg = np.array([1.0, 1.0, 1.0], dtype=np.float32)
        out_rgb = alpha_array * rgb_array + (1 - alpha_array) * bg # blending
        return (out_rgb * 255).astype(np.uint8)

    @property
    def img_cols_rows(self):
        byte_image, cols, rows, _ = libeegviz.update(self._context)
        image = Image.frombytes(mode="RGBA", size=(cols, rows), data=byte_image)
        np_image = np.asarray(image)
        np_image = self.rgba_to_rgb(np_image)
        return (
            np_image,
            cols,
            rows,
        )

    def process_resize_event(self, width, height):
        libeegviz.resize(self._context, width, height)

    def process_interaction_event(self, event):
        _, cols, rows, _ = libeegviz.update(self._context)
        event_type = event["type"]

        if event_type not in self._events:
            return False

        if event_type == "MouseMove":
            if 0 < event["x"] <= cols and 0 < event["y"] <= rows:
                self._move(int(event["x"]), rows - int(event["y"]))
        elif event_type == "LeftButtonPress":
            if 0 < event["x"] <= cols and 0 < event["y"] <= rows:
                self._click(0)
        elif event_type == "RightButtonPress":
            if 0 < event["x"] <= cols and 0 < event["y"] <= rows:
                self._click(1)
        elif event_type == "KeyDown":
            key = event.get("key", "")
            if key in self._keys:
                self._keydown(key)
            else:
                return False
        return True
