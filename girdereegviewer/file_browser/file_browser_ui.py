from dataclasses import dataclass, field
from typing import Any

from trame.widgets import html
from trame.widgets import vuetify3 as v3
from trame_server.utils.typed_state import TypedState
from undo_stack import Signal


@dataclass
class File:
    name: str
    content: bytes | None = None


@dataclass
class FileBrowserState:
    loading: bool = False
    display_button_tooltip: bool = False
    eeg_file: File | None = None
    eeg_annotation_file: File | None = None
    slicer_files: list[File] = field(default_factory=list)


class FileBrowserUI(html.Div):
    files_selected = Signal(list[dict[str, Any]])
    save_clicked = Signal()

    def __init__(self):
        super().__init__(classes="d-flex flex-row align-center")
        self.typed_state = TypedState(self.state, FileBrowserState)
        self._build_ui()

    def _build_ui(self) -> None:
        with self:
            with html.Div(classes="d-flex flex-row justify-center align-center", style="width: 50px; height: 50px;"):
                v3.VTooltip(
                    v_model=(self.typed_state.name.display_button_tooltip,),
                    text="Load file",
                    activator="parent",
                    transition="slide-y-transition",
                    location="bottom start",
                )
                v3.VFileInput(
                    v_if=(f"!{self.typed_state.name.loading}",),
                    change=(
                        f"{self.typed_state.name.loading} = true; {self.typed_state.name.display_button_tooltip} = false; "
                        f"trigger('{self.ctrl.trigger_name(self.files_selected)}', [$event.target.files]);"
                    ),
                    prepend_icon="mdi-file-plus-outline",
                    multiple=True,
                    hide_input=True,
                )
                v3.VProgressCircular(v_else=True, indeterminate=True, size=24)

            with html.Div(classes="d-flex flex-row justify-center align-center", style="width: 50px; height: 50px;"):
                v3.VTooltip(
                    v_if=(self.typed_state.name.eeg_annotation_file,),
                    text="Save annotations",
                    activator="parent",
                    transition="slide-y-transition",
                    location="bottom start",
                )
                v3.VBtn(
                    click=self.save_clicked,
                    disabled=(f"!{self.typed_state.name.eeg_annotation_file}",),
                    icon="mdi-content-save-outline",
                )
