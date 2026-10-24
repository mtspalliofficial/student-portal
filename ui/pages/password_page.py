import customtkinter as ctk

from auth import change_password
from ui import theme


class PasswordPage(ctk.CTkFrame):
    def __init__(self, master, student):
        super().__init__(master, fg_color="transparent")
        self.roll_number = student["roll_number"]

        title = ctk.CTkLabel(self, text="Change Password", font=theme.font(24, "bold"))
        title.pack(anchor="w", padx=24, pady=(24, 0))

        subtitle = ctk.CTkLabel(self, text="Use at least 8 characters. Your default password is your date of birth (DDMMYYYY).",
                                font=theme.font(13), text_color=theme.MUTED_TEXT)
        subtitle.pack(anchor="w", padx=24, pady=(0, 8))

        card = ctk.CTkFrame(self, fg_color=theme.CARD, corner_radius=16)
        card.pack(anchor="w", padx=24, pady=16)

        self.current_entry = self.add_field(card, "Current password")
        self.new_entry = self.add_field(card, "New password")
        self.confirm_entry = self.add_field(card, "Confirm new password")

        self.save_button = ctk.CTkButton(card, text="Update Password", width=320, height=40, corner_radius=10,
                                         font=theme.font(14, "bold"), fg_color=theme.ACCENT,
                                         hover_color=theme.ACCENT_HOVER, command=self.handle_save)
        self.save_button.pack(padx=24, pady=(20, 8))

        self.message_label = ctk.CTkLabel(card, text="", font=theme.font(12))
        self.message_label.pack(pady=(0, 18))

    def add_field(self, parent, label_text):
        label = ctk.CTkLabel(parent, text=label_text, font=theme.font(13), text_color=theme.MUTED_TEXT)
        label.pack(anchor="w", padx=24, pady=(14, 4))

        entry = ctk.CTkEntry(parent, show="•", width=320, height=38, corner_radius=10)
        entry.pack(padx=24)
        return entry

    def handle_save(self):
        current = self.current_entry.get()
        new = self.new_entry.get()
        confirm = self.confirm_entry.get()

        if not current or not new or not confirm:
            self.show_message("Please fill in all three fields", False)
            return

        if new != confirm:
            self.show_message("New passwords do not match", False)
            return

        self.save_button.configure(state="disabled", text="Updating...")
        self.update_idletasks()

        success, message = change_password(self.roll_number, current, new)

        self.save_button.configure(state="normal", text="Update Password")
        self.show_message(message, success)

        if success:
            for entry in (self.current_entry, self.new_entry, self.confirm_entry):
                entry.delete(0, "end")

    def show_message(self, text, success):
        if success:
            color = theme.SUCCESS
        else:
            color = theme.ERROR
        self.message_label.configure(text=text, text_color=color)