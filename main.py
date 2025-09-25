
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import StringProperty, BooleanProperty, NumericProperty, ListProperty
from kivy.storage.jsonstore import JsonStore
from kivy.utils import platform
from kivy.core.window import Window

from kivymd.app import MDApp
from kivymd.uix.snackbar import MDSnackbar
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.textfield import MDTextField

KV = """
#:import hex kivy.utils.get_color_from_hex

<StatChip@MDBoxLayout>:
    adaptive_height: True
    md_bg_color: app.surface
    radius: 12
    padding: 12
    spacing: 8
    MDIcon:
        icon: root.icon if hasattr(root, "icon") else "information-outline"
        theme_text_color: "Custom"
        text_color: app.primary
        size_hint: None, None
        size: "24dp", "24dp"
    MDLabel:
        text: root.text if hasattr(root, "text") else ""
        bold: True
        text_color: app.text
        adaptive_height: True

<SettingRow@MDBoxLayout>:
    adaptive_height: True
    padding: 12
    spacing: 12
    MDIcon:
        icon: root.icon if hasattr(root, "icon") else "cog"
        theme_text_color: "Custom"
        text_color: app.primary
        size_hint: None, None
        size: "24dp", "24dp"
    MDLabel:
        text: root.text if hasattr(root, "text") else ""
        text_color: app.text
        bold: False
    Widget:
    MDSwitch:
        id: sw
        active: root.active if hasattr(root, "active") else False
        on_active: root.on_toggle(self.active) if hasattr(root, "on_toggle") else None

MDScreen:
    md_bg_color: app.bg

    MDTopAppBar:
        id: appbar
        title: "A&A‑Bauservice"
        elevation: 2
        left_action_items: [["hammer-wrench", lambda *_: None]]
        right_action_items: [["account", lambda *_: None]]
        pos_hint: {"top": 1}

    MDBottomNavigation:
        id: tabs
        pos_hint: {"top": .93}
        panel_color: app.surface

        MDBottomNavigationItem:
            name: "home"
            text: "Główna"
            icon: "home-variant"
            MDBoxLayout:
                orientation: "vertical"
                padding: 16
                spacing: 16

                MDCard:
                    style: "elevated"
                    padding: 16
                    radius: 16
                    md_bg_color: app.surface
                    MDBoxLayout:
                        orientation: "vertical"
                        spacing: 12
                        adaptive_height: True

                        MDBoxLayout:
                            adaptive_height: True
                            spacing: 8
                            MDIcon:
                                icon: "clock-outline"
                                theme_text_color: "Custom"
                                text_color: app.primary if app.is_working else app.muted
                            MDLabel:
                                text: "Pracujesz" if app.is_working else "Nie pracujesz"
                                theme_text_color: "Custom"
                                text_color: app.primary if app.is_working else app.text
                                bold: True

                        MDBoxLayout:
                            orientation: "vertical"
                            adaptive_height: True
                            MDLabel:
                                text: app.elapsed_str if app.is_working else "00:00:00"
                                halign: "center"
                                font_style: "H4"
                                theme_text_color: "Custom"
                                text_color: app.primary
                            MDLabel:
                                text: app.current_project
                                halign: "center"
                                theme_text_color: "Custom"
                                text_color: app.muted

                        MDRaisedButton:
                            text: "Zakończ pracę" if app.is_working else "Rozpocznij pracę"
                            md_bg_color: app.error if app.is_working else app.primary
                            on_release: app.toggle_work()

                MDBoxLayout:
                    spacing: 12
                    adaptive_height: True
                    StatChip:
                        icon: "trending-up"
                        text: f"{app.todays_hours:.1f}h Dziś"
                    StatChip:
                        icon: "account-group"
                        text: f"{len(app.employees_working)} aktywni"
                    StatChip:
                        icon: "map-marker"
                        text: f"{len(app.projects)} projekty"

                MDCard:
                    style: "elevated"
                    padding: 16
                    radius: 16
                    md_bg_color: app.surface
                    MDBoxLayout:
                        orientation: "vertical"
                        spacing: 12
                        MDLabel:
                            text: "Ostatnia aktywność"
                            bold: True
                        MDList:
                            OneLineIconListItem:
                                text: "Jan Kowalski rozpoczął pracę"
                                IconLeftWidget:
                                    icon: "circle"
                            OneLineIconListItem:
                                text: "Projekt 'Dom Nowak' zakończony"
                                IconLeftWidget:
                                    icon: "check-circle"
                            OneLineIconListItem:
                                text: "Dodano materiał: Cement (5 worków)"
                                IconLeftWidget:
                                    icon: "package-variant"

        MDBottomNavigationItem:
            name: "time"
            text: "Czas pracy"
            icon: "clock"
            MDBoxLayout:
                orientation: "vertical"
                padding: 16
                spacing: 16

                MDCard:
                    radius: 16
                    padding: 16
                    md_bg_color: app.surface
                    MDBoxLayout:
                        orientation: "vertical"
                        spacing: 12
                        MDLabel:
                            text: "Status"
                            bold: True
                        MDBoxLayout:
                            spacing: 8
                            MDLabel:
                                text: "Pracujesz" if app.is_working else "Nie pracujesz"
                            MDIcon:
                                icon: "circle"
                                theme_text_color: "Custom"
                                text_color: (0,1,0,1) if app.is_working else app.muted

                        MDRaisedButton:
                            text: "Zakończ pracę" if app.is_working else "Rozpocznij pracę"
                            md_bg_color: app.error if app.is_working else app.primary
                            on_release: app.toggle_work()

                MDCard:
                    radius: 16
                    padding: 16
                    md_bg_color: app.surface
                    MDBoxLayout:
                        orientation: "vertical"
                        spacing: 12
                        MDLabel:
                            text: "Projekt"
                            bold: True
                        MDTextField:
                            id: project_input
                            hint_text: "Nazwa projektu"
                            text: app.current_project
                            on_text: app.current_project = self.text

                MDCard:
                    radius: 16
                    padding: 16
                    md_bg_color: app.surface
                    MDBoxLayout:
                        orientation: "vertical"
                        spacing: 12
                        MDLabel:
                            text: "Pojazd"
                            bold: True
                        MDTextField:
                            id: vehicle_input
                            hint_text: "np. Peugeot Boxer - WB 1234A"
                            text: app.selected_vehicle
                            on_text: app.selected_vehicle = self.text

                MDCard:
                    radius: 16
                    padding: 16
                    md_bg_color: app.surface
                    MDBoxLayout:
                        orientation: "vertical"
                        spacing: 12
                        MDLabel:
                            text: "Notatki z pracy"
                            bold: True
                        MDTextField:
                            id: notes_input
                            hint_text: "Opisz wykonane prace..."
                            text: app.work_notes
                            multiline: True
                            on_text: app.work_notes = self.text

                MDCard:
                    radius: 16
                    padding: 16
                    md_bg_color: app.surface
                    MDBoxLayout:
                        orientation: "vertical"
                        spacing: 12
                        MDBoxLayout:
                            adaptive_height: True
                            MDLabel:
                                text: "Użyte materiały"
                                bold: True
                            MDRaisedButton:
                                text: "Dodaj"
                                on_release: app.open_add_material_dialog()
                        MDList:
                            id: materials_list

        MDBottomNavigationItem:
            name: "employees"
            text: "Pracownicy"
            icon: "account-group"
            MDBoxLayout:
                orientation: "vertical"
                padding: 16
                spacing: 16
                MDCard:
                    radius: 16
                    padding: 0
                    md_bg_color: app.surface
                    MDList:
                        id: employees_list

        MDBottomNavigationItem:
            name: "reports"
            text: "Raporty"
            icon: "file-chart"
            MDBoxLayout:
                orientation: "vertical"
                padding: 16
                spacing: 16
                MDCard:
                    radius: 16
                    padding: 16
                    md_bg_color: app.surface
                    MDBoxLayout:
                        orientation: "vertical"
                        spacing: 12
                        MDLabel:
                            text: "Podsumowanie - bieżący miesiąc"
                            bold: True
                        MDGridLayout:
                            cols: 2
                            adaptive_height: True
                            spacing: 12
                            StatChip:
                                icon: "clock-outline"
                                text: f"{app.month_total_hours}h  Łączne godziny"
                            StatChip:
                                icon: "currency-usd"
                                text: f"{app.month_total_cost} zł  Łączny koszt"
                            StatChip:
                                icon: "briefcase"
                                text: f"{len(app.projects)}  Aktywne projekty"
                            StatChip:
                                icon: "check"
                                text: "156  Ukończone zadania"

                MDRaisedButton:
                    text: "Generuj PDF (placeholder)"
                    on_release: app.notify('Raport wygenerowany (demo)')

        MDBottomNavigationItem:
            name: "settings"
            text: "Ustawienia"
            icon: "cog"
            MDBoxLayout:
                orientation: "vertical"
                padding: 16
                spacing: 16
                MDCard:
                    radius: 16
                    padding: 16
                    md_bg_color: app.surface
                    MDLabel:
                        text: "Jan Kowalski — Kierownik budowy\njan.kowalski@aabauservice.pl"
                        theme_text_color: "Custom"
                        text_color: app.text
                MDCard:
                    radius: 16
                    padding: 0
                    md_bg_color: app.surface
                    MDBoxLayout:
                        orientation: "vertical"
                        SettingRow:
                            icon: "bell-outline"
                            text: "Powiadomienia"
                            active: app.notifications_enabled
                            on_toggle: app.set_pref("notifications_enabled", args[1])
                        SettingRow:
                            icon: "map-marker"
                            text: "Lokalizacja GPS"
                            active: app.location_enabled
                            on_toggle: app.set_pref("location_enabled", args[1])
                        SettingRow:
                            icon: "coffee"
                            text: "Automatyczne przerwy"
                            active: app.auto_break
                            on_toggle: app.set_pref("auto_break", args[1])

                MDRaisedButton:
                    text: "Wyloguj się (demo)"
                    md_bg_color: app.error
                    on_release: app.notify("Wylogowano (demo)")
"""

class AABauserviceApp(MDApp):
    # Theme colors
    primary = ListProperty([0.10, 0.46, 0.82, 1])  # #1976D2
    surface = ListProperty([1, 1, 1, 1])
    bg = ListProperty([0.95, 0.96, 0.97, 1])
    text = ListProperty([0.11, 0.11, 0.12, 1])
    muted = ListProperty([0.53, 0.53, 0.57, 1])
    error = ListProperty([0.96, 0.23, 0.19, 1])

    # App state
    is_working = BooleanProperty(False)
    elapsed_seconds = NumericProperty(0)
    elapsed_str = StringProperty("00:00:00")
    current_project = StringProperty("Budowa domu - ul. Kwiatowa 15")
    selected_vehicle = StringProperty("Peugeot Boxer - WB 1234A")
    work_notes = StringProperty("")
    materials = ListProperty([])
    employees = ListProperty([
        {"name": "Jan Kowalski", "position": "Kierownik budowy", "phone": "+48 123 456 789", "status": "Pracuje", "hours": "6h 30min"},
        {"name": "Anna Nowak", "position": "Murarz", "phone": "+48 987 654 321", "status": "Przerwa", "hours": "4h 15min"},
        {"name": "Piotr Wiśniewski", "position": "Elektryk", "phone": "+48 555 666 777", "status": "Nie pracuje", "hours": "0h"},
        {"name": "Maria Dąbrowska", "position": "Malarz", "phone": "+48 111 222 333", "status": "Pracuje", "hours": "7h 45min"},
    ])
    projects = ListProperty(["Kwiatowa 15", "Główna 22", "Leśna 8"])

    # Stats
    todays_hours = NumericProperty(8.5)
    month_total_hours = NumericProperty(1248)
    month_total_cost = NumericProperty(62400)

    # Prefs
    notifications_enabled = BooleanProperty(True)
    location_enabled = BooleanProperty(True)
    auto_break = BooleanProperty(False)

    def build(self):
        self.title = "A&A‑Bauservice"
        self.theme_cls.material_style = "M3"
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.primary_hue = "700"
        self.store = JsonStore(self.user_data_dir + "/store.json")
        self.load_state()
        root = Builder.load_string(KV)
        Clock.schedule_once(lambda *_: self.refresh_lists(), 0)
        self.timer_ev = Clock.schedule_interval(self._tick, 1)
        return root

    def on_stop(self):
        self.save_state()

    def _tick(self, dt):
        if self.is_working:
            self.elapsed_seconds += 1
            h = self.elapsed_seconds // 3600
            m = (self.elapsed_seconds % 3600) // 60
            s = self.elapsed_seconds % 60
            self.elapsed_str = f"{h:02d}:{m:02d}:{s:02d}"

    def toggle_work(self):
        self.is_working = not self.is_working
        if self.is_working:
            self.notify("Rozpoczęto pracę — rejestruję czas")
            self.elapsed_seconds = 0
        else:
            self.notify("Zakończono pracę — zapisano sesję")
        self.save_state()

    def refresh_lists(self):
        # Materials list
        mat_list = self.root.ids.get("materials_list")
        if mat_list:
            mat_list.clear_widgets()
            from kivymd.uix.list import OneLineIconListItem, IconLeftWidget
            for m in self.materials:
                it = OneLineIconListItem(text=f'{m["name"]} — {m["quantity"]} {m["unit"]}')
                it.add_widget(IconLeftWidget(icon="package-variant"))
                mat_list.add_widget(it)
        # Employees list
        emp_list = self.root.ids.get("employees_list")
        if emp_list:
            emp_list.clear_widgets()
            from kivymd.uix.list import ThreeLineAvatarListItem, ImageLeftWidget
            for e in self.employees:
                item = ThreeLineAvatarListItem(text=e["name"], secondary_text=e["position"],
                                               tertiary_text=f'Dziś: {e["hours"]} — {e["status"]}')
                item.add_widget(ImageLeftWidget(source=""))
                emp_list.add_widget(item)

    def open_add_material_dialog(self):
        self._mat_name = MDTextField(hint_text="Nazwa materiału", text="Cement")
        self._mat_qty = MDTextField(hint_text="Ilość", text="5", input_filter="int")
        self._mat_unit = MDTextField(hint_text="Jednostka (np. worki, kg, szt.)", text="worki")
        self.dialog = MDDialog(
            title="Dodaj materiał",
            type="custom",
            content_cls=MDBoxLayout(
                orientation="vertical",
                spacing="12dp",
                children=[self._mat_unit, self._mat_qty, self._mat_name],
            ),
            buttons=[
                MDFlatButton(text="Anuluj", on_release=lambda *_: self.dialog.dismiss()),
                MDRaisedButton(text="Dodaj", on_release=lambda *_: self._confirm_add_material()),
            ],
        )
        self.dialog.open()

    def _confirm_add_material(self):
        name = self._mat_name.text.strip()
        qty = self._mat_qty.text.strip() or "0"
        unit = self._mat_unit.text.strip() or "szt."
        if name and qty:
            self.materials.append({"name": name, "quantity": qty, "unit": unit})
            self.save_state()
            self.refresh_lists()
            self.notify("Dodano materiał")
        self.dialog.dismiss()

    @property
    def employees_working(self):
        return [e for e in self.employees if e["status"] in ("Pracuje", "Przerwa")]

    def notify(self, text):
        MDSnackbar(text=text, duration=1.6).open()

    def save_state(self):
        self.store.put("state",
            is_working=self.is_working,
            elapsed_seconds=int(self.elapsed_seconds),
            current_project=self.current_project,
            selected_vehicle=self.selected_vehicle,
            work_notes=self.work_notes,
            materials=self.materials,
            notifications_enabled=self.notifications_enabled,
            location_enabled=self.location_enabled,
            auto_break=self.auto_break,
        )

    def load_state(self):
        if self.store.exists("state"):
            s = self.store.get("state")
            self.is_working = s.get("is_working", False)
            self.elapsed_seconds = s.get("elapsed_seconds", 0)
            self.current_project = s.get("current_project", self.current_project)
            self.selected_vehicle = s.get("selected_vehicle", self.selected_vehicle)
            self.work_notes = s.get("work_notes", "")
            self.materials = s.get("materials", [])
            self.notifications_enabled = s.get("notifications_enabled", True)
            self.location_enabled = s.get("location_enabled", True)
            self.auto_break = s.get("auto_break", False)

    def set_pref(self, key, value):
        setattr(self, key, value)
        self.save_state()
        self.notify("Zapisano ustawienie.")

if __name__ == "__main__":
    # Optional: set a desktop size for quick testing
    if platform not in ("android", "ios"):
        Window.size = (420, 840)
    AABauserviceApp().run()
