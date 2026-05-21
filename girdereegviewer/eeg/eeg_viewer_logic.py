from .eeg_viewer_ui import EEGViewerUI
from .eeg_viewer_window import EEGViewerWindow


class EEGViewerLogic:
    def __init__(self, data_path: str):
        self.eeg_window = EEGViewerWindow(data_path)

    def set_ui(self, ui: EEGViewerUI) -> None:
        ui.create_view_handler(self.eeg_window)
