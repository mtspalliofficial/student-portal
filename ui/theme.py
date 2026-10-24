import customtkinter as ctk

ACCENT = "#3B82F6"
ACCENT_HOVER = "#2563EB"
BACKGROUND = ("#F3F4F6", "#111318")
CARD = ("#FFFFFF", "#1C1F26")
MUTED_TEXT = ("#6B7280", "#9CA3AF")
ERROR = "#EF4444"
FONT_FAMILY = "Segoe UI"
HOVER = ("#E5E7EB", "#2A2E37")
SUCCESS = "#22C55E"


def font(size, weight="normal"):
    return ctk.CTkFont(family=FONT_FAMILY, size=size, weight=weight)