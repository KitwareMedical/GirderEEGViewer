from trame.ui.vuetify3 import VAppLayout
from trame.widgets import rca
from trame.widgets.vuetify3 import VMain
from trame_server import Server


class EEGViewerUI:
    def __init__(self, server: Server):
        self.template_name = "eeg-viewer"
        with VAppLayout(server, template_name=self.template_name), VMain(classes="d-flex flex-column"):
            self.rca = rca.RemoteControlledArea(name="eeg-view", display="image", send_mouse_move=True)
