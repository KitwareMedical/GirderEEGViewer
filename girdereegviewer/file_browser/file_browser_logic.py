import tempfile
from pathlib import Path
from typing import Any

from trame_server import Server
from trame_server.utils.typed_state import TypedState
from undo_stack import Signal

from .file_browser_ui import File, FileBrowserState, FileBrowserUI

ANNOTATION_FILE_SUFFIX = "annotations.csv"


class FileValidationError(Exception):
    pass


class EEGLoadingError(Exception):
    pass


def are_files_valid(files: list[dict[str, Any]]) -> bool:
    return all(isinstance(file.get("name"), str) and isinstance(file.get("content"), bytes) for file in files)


class FileBrowserLogic:
    eeg_files_selected = Signal(str)

    def __init__(self, server: Server):
        self.server = server
        self.typed_state = TypedState(self.server.state, FileBrowserState)
        self._current_tmpdir: tempfile.TemporaryDirectory[str] | None = None

    @property
    def name(self) -> str:
        return self.typed_state.name

    @property
    def data(self) -> FileBrowserState:
        return self.typed_state.data

    def set_ui(self, ui: FileBrowserUI) -> None:
        ui.files_selected.connect(self._load_files)
        ui.save_clicked.connect(self._save_eeg_annotations)

    def _cleanup_current_tmpdir(self) -> None:
        if self._current_tmpdir is not None:
            self._current_tmpdir.cleanup()
            self._current_tmpdir = None

    def _create_tmp_dir(self) -> None:
        self._cleanup_current_tmpdir()
        self._current_tmpdir = tempfile.TemporaryDirectory()

    def _write_file(self, file_path: Path, file_content: bytes) -> None:
        try:
            file_path.write_bytes(file_content)
        except OSError as e:
            raise OSError(f"Could not write file: {file_path}") from e

    def _write_file_to_tmp_dir(self, file: File) -> str:
        if self._current_tmpdir is None:
            raise RuntimeError("Temporary directory is not initialized")

        file_path = Path(self._current_tmpdir.name) / file.name

        self._write_file(file_path, file.content)

        return str(file_path)

    def _validate_eeg_files(self, eeg_files: list[dict[str, Any]]) -> None:
        if not eeg_files:
            raise FileValidationError("No files selected")

        if len(eeg_files) > 2:
            raise FileValidationError("Too many files selected")

        if not are_files_valid(eeg_files):
            raise FileValidationError("Invalid file format")

        eeg_files.sort(key=lambda d: d["name"])

        self.data.eeg_file = File(
            name=eeg_files[0]["name"],
            content=eeg_files[0]["content"],
        )

        annotation_file_name = f"{self.data.eeg_file.name}.{ANNOTATION_FILE_SUFFIX}"

        has_annotation_file = len(eeg_files) == 2 and eeg_files[1]["name"] == annotation_file_name

        self.data.eeg_annotation_file = File(
            name=annotation_file_name,
            content=eeg_files[1]["content"] if has_annotation_file else None,
        )

    def _load_eeg_files(self) -> None:
        if self.data.eeg_file is None:
            raise EEGLoadingError("EEG file is missing")

        self._create_tmp_dir()

        eeg_file_path = self._write_file_to_tmp_dir(self.data.eeg_file)

        if self.data.eeg_annotation_file.content is not None:
            self._write_file_to_tmp_dir(self.data.eeg_annotation_file)

        try:
            self.eeg_files_selected(eeg_file_path)
        except Exception as e:
            raise EEGLoadingError("Could not load data into EEG Viewer") from e

    def _reset_state(self) -> None:
        self.data.eeg_file = None
        self.data.eeg_annotation_file = None

    def _load_files(self, selected_files: list[dict[str, Any]]) -> None:
        try:
            self._validate_eeg_files(selected_files)
            self._load_eeg_files()

        except FileValidationError:
            self._reset_state()
            raise

        except EEGLoadingError:
            self._reset_state()
            raise

        finally:
            self.data.loading = False

    def _save_eeg_annotations(self) -> None:
        if self._current_tmpdir is None:
            raise RuntimeError("Temporary directory is not initialized")

        annotation_file = self.data.eeg_annotation_file

        if annotation_file is None:
            raise RuntimeError("Annotation file is missing")

        annotation_file_name = annotation_file.name

        tmp_annotation_file_path = Path(self._current_tmpdir.name) / annotation_file_name

        if not tmp_annotation_file_path.exists():
            raise FileNotFoundError(f"Annotation file does not exist: {tmp_annotation_file_path}")

        save_annotation_file_path = Path.cwd() / annotation_file_name

        self._write_file(
            save_annotation_file_path,
            tmp_annotation_file_path.read_bytes(),
        )
