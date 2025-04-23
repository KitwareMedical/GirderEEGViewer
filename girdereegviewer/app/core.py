from .eeg.components import EEGWindow
from trame.app.testing import enable_testing
from trame.decorators import TrameApp
from trame.app import get_server
from trame.ui.vuetify import SinglePageLayout
from trame.widgets import vuetify as v, rca, client

@TrameApp()
class EEGApp:
    def __init__(self, server=None):
        self.server = get_server(server, client_type="vue2")

        self.server.cli.add_argument("path") # Will not be used once girder/filebrowser is set up
        args, _ = self.server.cli.parse_known_args()

        self.window = EEGWindow(args.path) # Will not be used once girder/filebrowser is set up
        self._build_ui()

    @property
    def state(self):
        return self.server.state

    @property
    def ctrl(self):
        return self.server.controller

    def _build_ui(self):
        with SinglePageLayout(self.server, full_height=True) as layout:
            client.Style("div { position: unset !important };") # Make the RCA fit the image
            layout.title.set_text("EEG Viewer")

            with layout.content:
                with v.VContainer(
                    fluid=True,
                    classes="fill-height d-flex justify-center align-center",
                ):
                    view = rca.RemoteControlledArea(
                        name="eeg-view",
                        display="image",
                        send_mouse_move=True,
                        image_style=({},),
                        style="width: auto; height: auto;" # Make the RCA fit the image
                    )

                    self.view_handler = view.create_view_handler(
                        self.window,
                    )


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    app = EEGApp()
    enable_testing(app.server)
    app.server.start()
