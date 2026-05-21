from trame.widgets import rca


class EEGViewerUI(rca.RemoteControlledArea):
    def __init__(self):
        super().__init__(name="eeg-view", display="image", send_mouse_move=True)
