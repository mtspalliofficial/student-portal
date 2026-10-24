import customtkinter as ctk

from students_service import get_marks
from ui import theme


class MarksPage(ctk.CTkFrame):
    def __init__(self, master, student):
        super().__init__(master, fg_color="transparent")
        self.records = {record["semester"]: record for record in get_marks(student["roll_number"])}

        title = ctk.CTkLabel(self, text="Marks", font=theme.font(24, "bold"))
        title.pack(anchor="w", padx=24, pady=(24, 0))

        subtitle = ctk.CTkLabel(self, text=f"CGPA {student.get('cgpa', '-')} across {len(self.records)} completed semesters",
                                font=theme.font(13), text_color=theme.MUTED_TEXT)
        subtitle.pack(anchor="w", padx=24, pady=(0, 8))

        if not self.records:
            empty = ctk.CTkLabel(self, text="No results published yet.", font=theme.font(14))
            empty.pack(anchor="w", padx=24, pady=16)
            return

        labels = [f"Semester {number}" for number in self.records]
        self.selector = ctk.CTkSegmentedButton(self, values=labels, command=self.show_semester,
                                               font=theme.font(13), selected_color=theme.ACCENT,
                                               selected_hover_color=theme.ACCENT_HOVER)
        self.selector.pack(anchor="w", padx=24, pady=(8, 12))

        self.table_card = ctk.CTkFrame(self, fg_color=theme.CARD, corner_radius=16)
        self.table_card.pack(fill="x", padx=24, pady=(0, 24))
        self.table_card.grid_columnconfigure(0, weight=1)

        latest = labels[-1]
        self.selector.set(latest)
        self.show_semester(latest)

    def show_semester(self, label):
        semester = int(label.split()[-1])
        record = self.records[semester]

        for widget in self.table_card.winfo_children():
            widget.destroy()

        for column, heading in enumerate(["Subject", "Marks", "Grade"]):
            header = ctk.CTkLabel(self.table_card, text=heading, font=theme.font(13, "bold"),
                                  text_color=theme.MUTED_TEXT)
            header.grid(row=0, column=column, sticky="w", padx=20, pady=(16, 8))

        for row, subject in enumerate(record["subjects"], start=1):
            if subject["grade"] == "F":
                grade_color = theme.ERROR
            else:
                grade_color = theme.ACCENT

            name_label = ctk.CTkLabel(self.table_card, text=subject["subject"], font=theme.font(14))
            name_label.grid(row=row, column=0, sticky="w", padx=20, pady=6)

            marks_label = ctk.CTkLabel(self.table_card, text=f"{subject['marks']}/100", font=theme.font(14))
            marks_label.grid(row=row, column=1, sticky="w", padx=20, pady=6)

            grade_label = ctk.CTkLabel(self.table_card, text=subject["grade"], font=theme.font(14, "bold"),
                                       text_color=grade_color)
            grade_label.grid(row=row, column=2, sticky="w", padx=20, pady=6)

        sgpa_label = ctk.CTkLabel(self.table_card, text=f"SGPA: {record['sgpa']}", font=theme.font(16, "bold"))
        sgpa_label.grid(row=len(record["subjects"]) + 1, column=0, columnspan=3, sticky="w", padx=20, pady=(12, 18))