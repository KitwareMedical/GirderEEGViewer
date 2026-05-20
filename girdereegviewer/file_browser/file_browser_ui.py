from dataclasses import dataclass
from typing import Any

from trame.widgets import html
from trame.widgets import vuetify3 as v3
from trame_server.utils.typed_state import TypedState
from undo_stack import Signal


@dataclass
class FileBrowserState:
    loading_busy: bool = False
    display_button_tooltip: bool = False


class FileBrowserUI(html.Div):
    files_selected = Signal(list[Any], str)

    def __init__(self):
        super().__init__(classes="d-flex flex-row justify-center align-center", style="width: 50px; height: 50px;")
        self.typed_state = TypedState(self.state, FileBrowserState)

        with self:
            v3.VTooltip(
                v_model=(self.typed_state.name.display_button_tooltip,),
                text="Load file",
                activator="parent",
                transition="slide-y-transition",
                location="bottom start",
            )
            v3.VFileInput(
                v_if=(f"!{self.typed_state.name.loading_busy}",),
                change=(
                    f"{self.typed_state.name.loading_busy} = true; {self.typed_state.name.display_button_tooltip} = false;"
                    "trigger('"
                    f"{self.ctrl.trigger_name(self.files_selected)}"
                    f"', [$event.target.files, '{self.typed_state.name.loading_busy}']"
                    ")"
                ),
                prepend_icon="mdi-file-plus-outline",
                multiple=False,
                hide_input=True,
            )
            v3.VProgressCircular(v_else=True, indeterminate=True, size=24)
