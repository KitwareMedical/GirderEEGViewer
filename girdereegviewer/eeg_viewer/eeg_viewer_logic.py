from trame_rca.utils import RcaViewAdapter
from trame_server import Server

from .eeg_viewer_ui import EEGViewerUI
from .eeg_viewer_window import EEGViewerWindow


class EEGViewerLogic:
    view_handler: RcaViewAdapter

    def __init__(self, server: Server):
        self.server = server
        self.eeg_window = EEGViewerWindow()

    def set_ui(self, ui: EEGViewerUI) -> None:
        self.view_handler = ui.rca.create_view_handler(self.eeg_window)

    def set_file_path(self, file_path: str) -> None:
        self.eeg_window.set_file_path(file_path)
        self.view_handler.update_size(None, self.eeg_window.window_size)
