from ui import theme
import customtkinter as ctk

from db import check_connection
from ui.login_window import LoginFrame
from ui.portal_window import PortalFrame


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.configure(fg_color=theme.BACKGROUND)
        self.title("Student Portal")
        self.geometry("420x480")
        self.current_frame = None
        self.show_login()

    def switch_frame(self, frame):
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = frame
        self.current_frame.pack(fill="both", expand=True)

    def show_login(self):
        self.geometry("860x600")
        self.switch_frame(LoginFrame(self, on_login_success=self.show_portal))

    def show_portal(self, student):
        self.geometry("980x620")
        self.switch_frame(PortalFrame(self, student, on_logout=self.show_login))


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    check_connection()
    app = App()
    app.mainloop()