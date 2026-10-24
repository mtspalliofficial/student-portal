import customtkinter as ctk

from auth import authenticate
from ui import theme


class LoginFrame(ctk.CTkFrame):
    def __init__(self, master, on_login_success):
        super().__init__(master, fg_color=theme.BACKGROUND)
        self.on_login_success = on_login_success

        card = ctk.CTkFrame(self, fg_color=theme.CARD, corner_radius=16)
        card.place(relx=0.5, rely=0.5, anchor="center")

        logo = ctk.CTkLabel(card, text="SP", width=64, height=64, corner_radius=32,
                            fg_color=theme.ACCENT, text_color="white", font=theme.font(22, "bold"))
        logo.pack(pady=(32, 12))

        title = ctk.CTkLabel(card, text="Student Portal", font=theme.font(26, "bold"))
        title.pack(padx=40)

        subtitle = ctk.CTkLabel(card, text="Sign in with your roll number",
                                font=theme.font(13), text_color=theme.MUTED_TEXT)
        subtitle.pack(pady=(2, 24))

        self.roll_entry = ctk.CTkEntry(card, placeholder_text="Roll Number",
                                       width=280, height=40, corner_radius=10)
        self.roll_entry.pack(padx=40, pady=6)

        self.password_entry = ctk.CTkEntry(card, placeholder_text="Password (DDMMYYYY)", show="•",
                                           width=280, height=40, corner_radius=10)
        self.password_entry.pack(padx=40, pady=6)

        self.show_password = ctk.CTkCheckBox(card, text="Show password", font=theme.font(12),
                                             checkbox_width=18, checkbox_height=18,
                                             command=self.toggle_password)
        self.show_password.pack(padx=40, pady=(4, 0), anchor="w")

        self.login_button = ctk.CTkButton(card, text="Sign In", width=280, height=42, corner_radius=10,
                                          font=theme.font(14, "bold"), fg_color=theme.ACCENT,
                                          hover_color=theme.ACCENT_HOVER, command=self.handle_login)
        self.login_button.pack(padx=40, pady=(20, 8))

        self.error_label = ctk.CTkLabel(card, text="", text_color=theme.ERROR, font=theme.font(12))
        self.error_label.pack(pady=(0, 20))

        self.roll_entry.bind("<Return>", lambda event: self.password_entry.focus())
        self.password_entry.bind("<Return>", lambda event: self.handle_login())
        self.after(100, self.roll_entry.focus)

    def toggle_password(self):
        if self.show_password.get():
            self.password_entry.configure(show="")
        else:
            self.password_entry.configure(show="•")

    def handle_login(self):
        roll_number = self.roll_entry.get().strip().upper()
        password = self.password_entry.get()

        if not roll_number or not password:
            self.error_label.configure(text="Please enter roll number and password")
            return

        self.login_button.configure(state="disabled", text="Signing in...")
        self.update_idletasks()

        student = authenticate(roll_number, password)

        self.login_button.configure(state="normal", text="Sign In")

        if student is None:
            self.error_label.configure(text="Invalid roll number or password")
            self.password_entry.delete(0, "end")
            return

        self.on_login_success(student)