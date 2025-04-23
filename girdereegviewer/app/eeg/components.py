import eegviz.lib.libpyeegviz as eegviz
import numpy as np
import os
from PIL import Image
from trame_rca.utils import AbstractWindow


class EEGWindow(AbstractWindow):
    def __init__(self, data_path, **kwargs):
        if not os.path.exists(data_path):
            raise Exception("Path does not exist")

        self._context = eegviz.create(data_path)
        self._events = ["MouseMove", "LeftButtonPress", "RightButtonPress", "KeyDown"]
        self._keys = [
            "a",
            "z",
            "i",
            "ArrowRight",
            "ArrowLeft",
            "u",
            "d",
            "ArrowDown",
            "ArrowUp",
            "k",
            "v",
            "q",
            "Tab",
            "Enter",
            "n",
            "p",
            "Escape",
        ]

    def _move(self, x, y):
        eegviz.move(self._context, x, y)

    def _click(self, button):
        eegviz.click(self._context, button)

    def _keydown(self, key):
        eegviz.key(self._context, key)

    @property
    def img_cols_rows(self):
        byte_image, cols, rows, _ = eegviz.update(self._context)
        image = Image.frombytes(mode="RGBA", size=(cols, rows), data=byte_image)
        np_image = np.asarray(image)
        np_image = np_image[:, :, :3] # Remove alpha
        return (
            np_image,
            cols,
            rows,
        )

    def process_resize_event(self, width, height):
        # eegviz.resize(self._context, width, height, 60)
        pass

    def process_interaction_event(self, event):
        _, cols, rows, _ = eegviz.update(self._context)
        event_type = event["type"]

        if event_type not in self._events:
            return False

        if event_type == "MouseMove":
            if 0 < event["x"] <= cols and 0 < event["y"] <= rows:
                self._move(int(event["x"]), int(event["y"]))
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
