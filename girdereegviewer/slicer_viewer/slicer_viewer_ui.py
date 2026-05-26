from dataclasses import dataclass

from trame.ui.vuetify3 import VAppLayout
from trame.widgets import vuetify3 as v3
from trame_server import Server
from trame_server.utils.typed_state import TypedState
from trame_slicer.app.ui import (
    ControlButton,
    FlexContainer,
    LayoutButton,
    MarkupsButton,
    MprInteractionButton,
    VolumePropertyUI,
)
from trame_slicer.app.ui.slab_button import SlabButton
from trame_slicer.core import LayoutManager


@dataclass
class SlicerViewerState:
    is_drawer_visible: bool = False
    active_tool: str | None = None


class SlicerViewerLayout(VAppLayout):
    def __init__(
        self,
        server: Server,
        template_name: str,
        is_drawer_visible: bool = False,
    ):
        super().__init__(server, template_name=template_name)
        self.typed_state = TypedState(self.state, SlicerViewerState)
        self.typed_state.data.is_drawer_visible = is_drawer_visible

        with self:
            with v3.VMain():
                self.content = FlexContainer(row=True, fill_height=True)

            self.drawer = v3.VNavigationDrawer(
                disable_resize_watcher=True,
                disable_route_watcher=True,
                permanent=True,
                location="left",
                v_model=(self.typed_state.name.is_drawer_visible,),
                width=350,
            )

            with (
                v3.VNavigationDrawer(
                    disable_resize_watcher=True,
                    disable_route_watcher=True,
                    permanent=True,
                    width=40,
                    location="left",
                ),
                FlexContainer(fill_height=True),
            ):
                self.toolbar = FlexContainer(classes="py-2", align="center")
                v3.VDivider()
                v3.VSpacer()
                v3.VDivider()
                self.undo_redo = FlexContainer(classes="py-2", align="center")


class SlicerViewerUI:
    def __init__(self, server: Server, layout_manager: LayoutManager):
        self.template_name = "slicer_viewer"
        self.tool_registry = {}
        with SlicerViewerLayout(server, template_name=self.template_name) as self.layout:
            with self.layout.drawer:
                self._build_drawer()

            with self.layout.toolbar:
                self._build_toolbar()

            with self.layout.content:
                layout_manager.initialize_layout_grid(self.layout)

    @property
    def data(self) -> SlicerViewerState:
        return self.layout.typed_state.data

    @property
    def name(self) -> SlicerViewerState:
        return self.layout.typed_state.name

    def _build_drawer(self) -> None:
        self._register_tool_ui(VolumePropertyUI)

    def _build_toolbar(self) -> None:
        self._create_tool_button(
            icon="mdi-tune-variant",
            name="Volume Properties",
            tool_ui_type=VolumePropertyUI,
        )
        self.layout_button = LayoutButton()
        self.markups_button = MarkupsButton()
        self.slab_button = SlabButton()
        self.mpr_interaction_button = MprInteractionButton()

    def _is_tool_active(self, tool_ui_type: type) -> str:
        return f"{self.name.active_tool} === '{tool_ui_type.__name__}'"

    def _is_tool_drawer_visible(self, tool_ui_type: type) -> str:
        return f"{self._is_tool_active(tool_ui_type)} && {self.name.is_drawer_visible}"

    def _register_tool_ui(self, tool_ui_type: type) -> None:
        tool_instance = tool_ui_type(v_if=(self._is_tool_active(tool_ui_type),))
        self.tool_registry[tool_ui_type] = tool_instance

    def _create_tool_button(self, name: str, icon: str | tuple, tool_ui_type: type) -> None:
        async def change_drawer_ui() -> None:
            is_drawer_visible = not self.data.is_drawer_visible or self.data.active_tool != tool_ui_type.__name__
            self.data.is_drawer_visible = is_drawer_visible
            self.data.active_tool = tool_ui_type.__name__ if is_drawer_visible else None

        ControlButton(
            icon=icon,
            name="{{ " + f"{self._is_tool_drawer_visible(tool_ui_type)} ? 'Close {name}' : 'Open {name}'" + " }}",
            click=change_drawer_ui,
            active=(self._is_tool_active(tool_ui_type),),
        )
