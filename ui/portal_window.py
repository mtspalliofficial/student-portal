import customtkinter as ctk

from ui import theme
from ui.pages.dashboard_page import DashboardPage
from ui.pages.password_page import PasswordPage
from ui.pages.profile_page import ProfilePage
from ui.pages.marks_page import MarksPage


class PlaceholderPage(ctk.CTkFrame):
    def __init__(self, master, title):
        super().__init__(master, fg_color="transparent")

        title_label = ctk.CTkLabel(self, text=title, font=theme.font(24, "bold"))
        title_label.pack(anchor="w", padx=24, pady=(24, 4))

        info_label = ctk.CTkLabel(self, text="Coming soon", font=theme.font(13), text_color=theme.MUTED_TEXT)
        info_label.pack(anchor="w", padx=24)


class PortalFrame(ctk.CTkFrame):
    def __init__(self, master, student, on_logout):
        super().__init__(master, fg_color=theme.BACKGROUND)
        self.student = student
        self.current_page = None
        self.nav_buttons = {}

        self.pages = {
            "Dashboard": lambda: DashboardPage(self.content, self.student),
            "Marks": lambda: MarksPage(self.content, self.student),
            "Edit Profile": lambda: ProfilePage(self.content, self.student, on_saved=self.update_student),
            "Change Password": lambda: PasswordPage(self.content, self.student),
        }

        self.build_sidebar(on_logout)

        self.content = ctk.CTkFrame(self, fg_color="transparent")
        self.content.pack(side="left", fill="both", expand=True)

        self.show_page("Dashboard")

    def build_sidebar(self, on_logout):
        sidebar = ctk.CTkFrame(self, width=220, fg_color=theme.CARD, corner_radius=0)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        initials = "".join(part[0] for part in self.student["name"].split()[:2]).upper()
        avatar = ctk.CTkLabel(sidebar, text=initials, width=56, height=56, corner_radius=28,
                              fg_color=theme.ACCENT, text_color="white", font=theme.font(20, "bold"))
        avatar.pack(pady=(28, 8))

        name_label = ctk.CTkLabel(sidebar, text=self.student["name"], font=theme.font(15, "bold"), wraplength=190)
        name_label.pack(padx=12)

        roll_label = ctk.CTkLabel(sidebar, text=self.student["roll_number"],
                                  font=theme.font(12), text_color=theme.MUTED_TEXT)
        roll_label.pack(pady=(0, 24))

        for page_name in self.pages:
            button = ctk.CTkButton(sidebar, text=page_name, anchor="w", height=38, corner_radius=8,
                                   font=theme.font(14), fg_color="transparent",
                                   text_color=("gray20", "gray85"), hover_color=theme.HOVER,
                                   command=lambda name=page_name: self.show_page(name))
            button.pack(fill="x", padx=12, pady=2)
            self.nav_buttons[page_name] = button

        logout_button = ctk.CTkButton(sidebar, text="Logout", height=36, corner_radius=8,
                                      fg_color="transparent", border_width=1, border_color=theme.ERROR,
                                      text_color=theme.ERROR, hover_color=("#FEE2E2", "#3B1C1C"),
                                      command=on_logout)
        logout_button.pack(side="bottom", fill="x", padx=12, pady=(8, 24))

        self.theme_switch = ctk.CTkSwitch(sidebar, text="Dark mode", font=theme.font(12),
                                          command=self.toggle_theme)
        self.theme_switch.pack(side="bottom", anchor="w", padx=16, pady=8)
        if ctk.get_appearance_mode() == "Dark":
            self.theme_switch.select()

    def show_page(self, page_name):
        if self.current_page is not None:
            self.current_page.destroy()
        self.current_page = self.pages[page_name]()
        self.current_page.pack(fill="both", expand=True)

        for name, button in self.nav_buttons.items():
            if name == page_name:
                button.configure(fg_color=theme.ACCENT, text_color="white", hover_color=theme.ACCENT_HOVER)
            else:
                button.configure(fg_color="transparent", text_color=("gray20", "gray85"), hover_color=theme.HOVER)
   
    def update_student(self, updated_student):
        self.student = updated_student
   
    def toggle_theme(self):
        if self.theme_switch.get():
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")