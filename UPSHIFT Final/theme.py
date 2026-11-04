LIGHT = {
    "name": "Light",
    "bg": "#F5F7FB",
    "sidebar": "#172033",
    "sidebar_text": "#F8FAFC",
    "sidebar_muted": "#A7B0C0",
    "card": "#FFFFFF",
    "text": "#1D2433",
    "muted": "#667085",
    "border": "#E2E8F0",
    "accent": "#6C63FF",
    "accent_2": "#FF7A59",
    "green": "#25A97A",
    "blue": "#3B82F6",
    "yellow": "#E0A514",
    "red": "#E05260",
    "input": "#F8FAFC"
}

DARK = {
    "name": "Dark",
    "bg": "#10131A",
    "sidebar": "#171B24",
    "sidebar_text": "#F8FAFC",
    "sidebar_muted": "#98A2B3",
    "card": "#1C212C",
    "text": "#F4F6FA",
    "muted": "#A6ADBB",
    "border": "#2C3442",
    "accent": "#8B83FF",
    "accent_2": "#FF8B6A",
    "green": "#40C693",
    "blue": "#63A4FF",
    "yellow": "#F2C14E",
    "red": "#FF6B78",
    "input": "#242A36"
}


def get_theme(name):
    if name == "Dark":
        return DARK
    return LIGHT
