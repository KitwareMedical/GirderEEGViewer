from typing import Any

from trame_server import Server
from trame_slicer.app.logic import BaseLogic, MarkupsButtonLogic, VolumePropertyLogic
from trame_slicer.app.logic.layout_button_logic import LayoutButtonLogic
from trame_slicer.app.logic.mpr_interaction_button_logic import (
    MprInteractionButtonLogic,
)
from trame_slicer.app.ui import VolumePropertyUI
from trame_slicer.core import LayoutManager, SlicerApp
from trame_slicer.rca_view import register_rca_factories

from .slicer_viewer_ui import SlicerViewerState, SlicerViewerUI


class SlicerViewerLogic(BaseLogic[SlicerViewerState]):
    def __init__(self, server: Server):
        slicer_app = SlicerApp()
        super().__init__(server, slicer_app, SlicerViewerState)

        # Register the RCA view creation
        register_rca_factories(self._slicer_app.view_manager, self._server)

        # Create the application logic
        self._volume_properties_logic = VolumePropertyLogic(server, slicer_app)
        self._layout_button_logic = LayoutButtonLogic(server, slicer_app)
        self._markups_logic = MarkupsButtonLogic(server, slicer_app)
        self._mpr_logic = MprInteractionButtonLogic(server, slicer_app)

    @property
    def layout_manager(self) -> LayoutManager:
        return self._layout_button_logic.layout_manager

    def set_ui(self, ui: SlicerViewerUI) -> None:
        self._volume_properties_logic.set_ui(ui.tool_registry[VolumePropertyUI])
        self._layout_button_logic.set_ui(ui.layout_button)
        self._markups_logic.set_ui(ui.markups_button)
        self._mpr_logic.set_ui(ui.mpr_interaction_button)

    def _show_largest_volume(self, volumes: list[Any]) -> None | Any:
        if not volumes:
            return None

        def bounds_volume(v: Any) -> float:
            b = [0] * 6
            v.GetImageData().GetBounds(b)
            return (b[1] - b[0]) * (b[3] - b[2]) * (b[5] - b[4])

        volumes = sorted(volumes, key=bounds_volume)
        volume_node = volumes[-1]

        self._slicer_app.display_manager.show_volume(
            volume_node,
            do_reset_views=True,
        )
        return volume_node

    def set_file_path(self, file_paths: list[str]) -> None:
        self._slicer_app.scene.Clear()

        volumes = self._slicer_app.io_manager.load_volumes(file_paths)
        if not volumes:
            return
        volume_node = self._show_largest_volume(volumes)
        if volume_node is not None:
            self._volume_properties_logic.on_volume_changed(volume_node)
