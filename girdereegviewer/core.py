from trame.app import TrameApp
from trame.ui.vuetify3 import VAppLayout
from trame.widgets import client
from trame.widgets import vuetify3 as v3
from trame_server.core import Server

from .eeg import EEGViewerLogic, EEGViewerUI


class ViewerLayout(VAppLayout):
    def __init__(
        self,
        server: Server,
        template_name: str = "main",
        app_name: str = "GirderEEGViewer",
        **kwargs,
    ):
        super().__init__(server, template_name=template_name, **kwargs)
        self.state.trame__title = app_name

        with self:
            self.app_bar = v3.VAppBar(height=75)

            self.app_viewer = v3.VMain(classes="d-flex justify-center align-center")


class ViewerApp(TrameApp):
    def __init__(self):
        super().__init__()
        self.server.cli.add_argument("path")  # Will not be used once girder/filebrowser is set up
        args, _ = self.server.cli.parse_known_args()

        self._eeg_viewer_logic = EEGViewerLogic(args.path)  # Will not be used once girder/filebrowser is set up
        self.layout = ViewerLayout(self.server)
        self._build_ui()

        self.set_ui()

    def _build_ui(self) -> None:
        with self.layout:
            client.Style("html { overflow-y: hidden; } ")
            with self.layout.app_bar:
                v3.VAppBarTitle(self.state.trame__title, style="flex: 0 1 auto;")

            with self.layout.app_viewer:
                self._eeg_viewer_ui = EEGViewerUI()

    def set_ui(self) -> None:
        self._eeg_viewer_logic.set_ui(self._eeg_viewer_ui)
