import tempfile
from pathlib import Path
from typing import Any

from trame_server import Server
from trame_server.utils.typed_state import TypedState
from undo_stack import Signal

from .file_browser_ui import FileBrowserState, FileBrowserUI


class FileBrowserLogic:
    files_selected = Signal(str)

    def __init__(self, server: Server):
        self.server = server
        self.typed_state = TypedState(self.server.state, FileBrowserState)

    def set_ui(self, ui: FileBrowserUI) -> None:
        ui.files_selected.connect(self._load_files)

    def _load_files(self, selected_files: list[Any], loading_name: str) -> None:
        if len(selected_files) == 1:
            selected_file = selected_files[0]
            with tempfile.TemporaryDirectory() as tmpdir:
                file_path = Path(tmpdir) / selected_file["name"]
                content = selected_file["content"]
                with file_path.open("wb") as f:
                    f.write(content)
                self.files_selected(str(file_path))

        self.server.state[loading_name] = False
