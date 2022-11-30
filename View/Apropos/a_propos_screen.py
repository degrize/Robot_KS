from kivymd.uix.screen import MDScreen

from View.Apropos.components import CustomChip


class AproposView(MDScreen):
    def on_enter(self):
        pass

    def removes_marks_all_chips(
            self, selected_instance_chip, active_state: bool
    ) -> None:
        for instance_chip in self.ids.chip_size_box.children:
            if instance_chip != selected_instance_chip:
                instance_chip.active = False
