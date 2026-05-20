from trame.app import TrameApp
from trame.ui.vuetify3 import VAppLayout
from trame.widgets import client
from trame.widgets import vuetify3 as v3
from trame_server.core import Server

from .eeg import EEGViewerLogic, EEGViewerUI
from .file_browser import FileBrowserLogic, FileBrowserUI


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

        self._file_browser_logic = FileBrowserLogic(self.server)
        self._eeg_viewer_logic = EEGViewerLogic(self.server)

        self._file_browser_logic.files_selected.connect(self._eeg_viewer_logic.set_file_path)
        self.layout = ViewerLayout(self.server)
        self._build_ui()

        self.set_ui()

    def _build_ui(self) -> None:
        with self.layout:
            client.Style(
                "html { overflow-y: hidden; } "
                ".v-input .v-input__prepend .v-icon { color: rgb(var(--v-theme-on-surface)); opacity: 1; }"
            )
            with self.layout.app_bar:
                self._file_browser_ui = FileBrowserUI()
                v3.VAppBarTitle(self.state.trame__title, style="flex: 0 1 auto;")

            with self.layout.app_viewer:
                self._eeg_viewer_ui = EEGViewerUI()

    def set_ui(self) -> None:
        self._eeg_viewer_logic.set_ui(self._eeg_viewer_ui)
        self._file_browser_logic.set_ui(self._file_browser_ui)
