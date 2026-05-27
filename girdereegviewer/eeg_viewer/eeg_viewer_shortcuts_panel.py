from trame.widgets import vuetify3 as v3
from trame.widgets.html import Div, Span

SHORTCUTS = {
    "selection": [
        (["alpha-a"], "Select all"),
        (["alpha-z"], "Select none"),
        (["alpha-i"], "Invert selection"),
    ],
    "modes": [
        (["keyboard-tab"], "Switch mode"),
        (["alpha-c"], "Toggle calibration"),
    ],
    "tools": [
        (["chevron-left", "chevron-right"], "Move time"),
        (["alpha-u", "alpha-d"], "Scale time up and down"),
        (["chevron-up", "chevron-down"], "Scale or calibrate up and down"),
        (["alpha-r"], "Reset scale"),
        (["keyboard-space"], "Next profile"),
        (["alpha-v"], "Next filter"),
    ],
    "annotations": [
        (["keyboard-return"], "Add annotation"),
        (["alpha-k"], "Delete annotation"),
        (["alpha-p", "alpha-n"], "Change annotation type"),
        (["keyboard-esc"], "Cancel annotation"),
    ],
}


class ShortcutInfo(Div):
    def __init__(self, icons: list[str], desc: str, **kwargs) -> None:
        super().__init__(classes="d-flex justify-space-between pa-2", **kwargs)
        with self:
            with Div(classes="d-flex", style="gap: 8px;"):
                for icon in icons:
                    v3.VIcon(icon=f"mdi-{icon}")
            Span(desc, classes="text-body-2")


class ShortcutsPanel(Div):
    def __init__(self, **kwargs) -> None:
        super().__init__(
            classes="d-flex justify-end ma-7", style="inset: 0; position: absolute; pointer-events: none;", **kwargs
        )

        self._build_ui()

    def _build_ui(self) -> None:
        with self, v3.VDialog(width=400):
            with (
                v3.Template(v_slot_activator="{ props : activatorProps }"),
                v3.VBtn(
                    v_bind="activatorProps",
                    icon="mdi-plus",
                    raw_attrs=['tabindex="-1"'],
                    color="white",
                    style="pointer-events: visible;",
                    size="small",
                ),
            ):
                v3.VTooltip(
                    activator="parent",
                    close_delay=100,
                    open_delay=500,
                    text="Keyboard shortcuts",
                )
                v3.VIcon(icon="mdi-information-outline")

            with v3.VCard(), v3.VCardText():
                for shortcut_theme, shortcuts in SHORTCUTS.items():
                    Div(shortcut_theme, classes="text-uppercase text-overline")
                    for shortcut_icons, shortcut_desc in shortcuts:
                        ShortcutInfo(shortcut_icons, shortcut_desc)
