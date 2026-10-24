import customtkinter as ctk

from students_service import update_contact_details
from ui import theme


class ProfilePage(ctk.CTkFrame):
    def __init__(self, master, student, on_saved):
        super().__init__(master, fg_color="transparent")
        self.roll_number = student["roll_number"]
        self.on_saved = on_saved
        address = student.get("address", {})

        title = ctk.CTkLabel(self, text="Edit Profile", font=theme.font(24, "bold"))
        title.pack(anchor="w", padx=24, pady=(24, 0))

        subtitle = ctk.CTkLabel(self, text="Update your contact details. Academic records can only be changed by the admin office.",
                                font=theme.font(13), text_color=theme.MUTED_TEXT)
        subtitle.pack(anchor="w", padx=24, pady=(0, 8))

        card = ctk.CTkFrame(self, fg_color=theme.CARD, corner_radius=16)
        card.pack(anchor="w", padx=24, pady=16)

        self.phone_entry = self.add_field(card, "Phone", student.get("phone", ""))
        self.email_entry = self.add_field(card, "Email", student.get("email", ""))
        self.city_entry = self.add_field(card, "City", address.get("city", ""))
        self.state_entry = self.add_field(card, "State", address.get("state", ""))

        self.save_button = ctk.CTkButton(card, text="Save Changes", width=320, height=40, corner_radius=10,
                                         font=theme.font(14, "bold"), fg_color=theme.ACCENT,
                                         hover_color=theme.ACCENT_HOVER, command=self.handle_save)
        self.save_button.pack(padx=24, pady=(20, 8))

        self.message_label = ctk.CTkLabel(card, text="", font=theme.font(12))
        self.message_label.pack(pady=(0, 18))

    def add_field(self, parent, label_text, value):
        label = ctk.CTkLabel(parent, text=label_text, font=theme.font(13), text_color=theme.MUTED_TEXT)
        label.pack(anchor="w", padx=24, pady=(14, 4))

        entry = ctk.CTkEntry(parent, width=320, height=38, corner_radius=10)
        entry.insert(0, str(value))
        entry.pack(padx=24)
        return entry

    def handle_save(self):
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip().lower()
        city = self.city_entry.get().strip()
        state = self.state_entry.get().strip()

        success, message, updated_student = update_contact_details(self.roll_number, phone, email, city, state)
        self.show_message(message, success)

        if success:
            self.on_saved(updated_student)

    def show_message(self, text, success):
        if success:
            color = theme.SUCCESS
        else:
            color = theme.ERROR
        self.message_label.configure(text=text, text_color=color)