from dataclasses import dataclass

from trame.app import TrameApp
from trame.ui.vuetify3 import VAppLayout
from trame.widgets import client
from trame.widgets import vuetify3 as v3
from trame_server.core import Server
from trame_server.utils.typed_state import TypedState

from .eeg_viewer import EEGViewerLogic, EEGViewerUI
from .file_browser import FileBrowserLogic, FileBrowserUI
from .slicer_viewer import SlicerViewerLogic, SlicerViewerUI


@dataclass
class ViewerState(VAppLayout):
    viewer_name: str | None = None


class ViewerLayout(VAppLayout):
    def __init__(
        self,
        server: Server,
        app_name: str = "GirderEEGViewer",
        **kwargs,
    ):
        super().__init__(server, **kwargs)
        self.state.trame__title = app_name

        with self:
            self.app_bar = v3.VAppBar(height=75)

            self.app_viewer = v3.VMain(classes="main-app d-flex flex-column")

            with v3.VFooter(app=True, classes="my-0 py-0", border=True) as self.footer:
                v3.VProgressCircular(
                    indeterminate=("!!trame__busy",),
                    color="#04a94d",
                    size=16,
                    width=3,
                    classes="ml-n3 mr-1",
                )
                self.footer.add_child(
                    '<a href="https://kitware.github.io/trame/" '
                    'class="text-grey-lighten-1 text-caption text-decoration-none" '
                    'target="_blank">Powered by trame</a>'
                )
                v3.VSpacer()
                reload = self.server.controller.on_server_reload
                if reload.exists():
                    v3.VBtn(
                        size="x-small",
                        density="compact",
                        icon="mdi-autorenew",
                        elevation=0,
                        click=self.on_server_reload,
                        classes="mx-2",
                    )

                self.footer.add_child(
                    '<a href="https://www.kitware.com/" '
                    'class="text-grey-lighten-1 text-caption text-decoration-none" '
                    'target="_blank">© 2025 Kitware Inc.</a>'
                )


class ViewerApp(TrameApp):
    def __init__(self):
        super().__init__()

        self.typed_state = TypedState(self.state, ViewerState)

        self._file_browser_logic = FileBrowserLogic(self.server)

        self._eeg_viewer_logic = EEGViewerLogic(self.server)
        self._eeg_viewer_ui = EEGViewerUI(self.server)

        self._slicer_viewer_logic = SlicerViewerLogic(self.server)
        self._slicer_viewer_ui = SlicerViewerUI(self.server, self._slicer_viewer_logic.layout_manager)

        self._file_browser_logic.eeg_files_selected.connect(self._on_eeg_files_loaded)
        self._file_browser_logic.slicer_files_selected.connect(self._on_slicer_files_loaded)

        self.layout = ViewerLayout(self.server)
        self._build_ui()

        self.set_ui()

    def _on_eeg_files_loaded(self, eeg_file_path: str) -> None:
        self.typed_state.data.viewer_name = self._eeg_viewer_ui.template_name
        self._eeg_viewer_logic.set_file_path(eeg_file_path)

    def _on_slicer_files_loaded(self, slicer_file_paths: list[str]) -> None:
        self.typed_state.data.viewer_name = self._slicer_viewer_ui.template_name
        self._slicer_viewer_logic.set_file_path(slicer_file_paths)

    def _build_ui(self) -> None:
        with self.layout:
            client.Style(
                "html { overflow-y: hidden; } "
                ".main-app { height: 100vh; }"
                ".main-view { display: flex; flex-direction: column; height: 100%; }"
                ".v-input .v-input__prepend .v-icon { color: rgb(var(--v-theme-on-surface)); opacity: 1; }"
                ".v-main .v-application__wrap { min-height: 100%; }"
                ".v-main { max-height: 100%; }"
            )
            with self.layout.app_bar:
                self._file_browser_ui = FileBrowserUI()
                v3.VAppBarTitle(self.state.trame__title, style="flex: 0 1 auto;")

            with self.layout.app_viewer:
                client.ServerTemplate(
                    v_if=(self.typed_state.name.viewer_name,),
                    classes="main-view",
                    name=(self.typed_state.name.viewer_name,),
                )

    def set_ui(self) -> None:
        self._eeg_viewer_logic.set_ui(self._eeg_viewer_ui)
        self._file_browser_logic.set_ui(self._file_browser_ui)
