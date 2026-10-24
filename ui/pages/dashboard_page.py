import customtkinter as ctk

from ui import theme


class DashboardPage(ctk.CTkFrame):
    def __init__(self, master, student):
        super().__init__(master, fg_color="transparent")

        first_name = student["name"].split()[0]
        title = ctk.CTkLabel(self, text=f"Welcome back, {first_name}", font=theme.font(24, "bold"))
        title.pack(anchor="w", padx=24, pady=(24, 0))

        subtitle = ctk.CTkLabel(self, text="Here's your academic overview",
                                font=theme.font(13), text_color=theme.MUTED_TEXT)
        subtitle.pack(anchor="w", padx=24, pady=(0, 8))

        self.build_stats(student)
        self.build_details(student)

    def build_stats(self, student):
        stats_row = ctk.CTkFrame(self, fg_color="transparent")
        stats_row.pack(fill="x", padx=24, pady=12)

        stats = [
            ("CGPA", student.get("cgpa", "-")),
            ("Semester", student["semester"]),
            ("Admission Year", student["admission_year"]),
        ]

        for column, (label, value) in enumerate(stats):
            stats_row.grid_columnconfigure(column, weight=1)

            card = ctk.CTkFrame(stats_row, fg_color=theme.CARD, corner_radius=16)
            card.grid(row=0, column=column, sticky="ew", padx=(0 if column == 0 else 12, 0))

            label_widget = ctk.CTkLabel(card, text=label, font=theme.font(12), text_color=theme.MUTED_TEXT)
            label_widget.pack(anchor="w", padx=20, pady=(16, 0))

            value_widget = ctk.CTkLabel(card, text=str(value), font=theme.font(28, "bold"), text_color=theme.ACCENT)
            value_widget.pack(anchor="w", padx=20, pady=(0, 16))

    def build_details(self, student):
        address = student.get("address", {})
        personal = [
            ("Date of Birth", student["date_of_birth"].strftime("%d %b %Y")),
            ("Gender", student.get("gender", "-")),
            ("Address", f"{address.get('city', '-')}, {address.get('state', '-')}"),
        ]
        contact = [
            ("Department", f"{student['course']} {student['department']}"),
            ("Email", student["email"]),
            ("Phone", student.get("phone", "-")),
        ]

        details_row = ctk.CTkFrame(self, fg_color="transparent")
        details_row.pack(fill="x", padx=24, pady=(12, 24))
        details_row.grid_columnconfigure((0, 1), weight=1)

        personal_card = self.build_section(details_row, "Personal Details", personal)
        personal_card.grid(row=0, column=0, sticky="nsew", padx=(0, 6))

        contact_card = self.build_section(details_row, "Contact Details", contact)
        contact_card.grid(row=0, column=1, sticky="nsew", padx=(6, 0))

    def build_section(self, parent, title, rows):
        section = ctk.CTkFrame(parent, fg_color=theme.CARD, corner_radius=16)

        heading = ctk.CTkLabel(section, text=title, font=theme.font(16, "bold"))
        heading.grid(row=0, column=0, columnspan=2, sticky="w", padx=20, pady=(18, 10))

        for row_number, (label, value) in enumerate(rows, start=1):
            name_label = ctk.CTkLabel(section, text=label, font=theme.font(13), text_color=theme.MUTED_TEXT)
            name_label.grid(row=row_number, column=0, sticky="w", padx=(20, 16), pady=5)

            value_label = ctk.CTkLabel(section, text=str(value), font=theme.font(13))
            value_label.grid(row=row_number, column=1, sticky="w", padx=(0, 20), pady=5)

        section.grid_rowconfigure(len(rows) + 1, minsize=14)
        return section