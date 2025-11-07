import os
import sys
from ttkbootstrap import Window
from ui import InventoryApp
from db_utils import init_db

# Resolve resource paths in dev and in PyInstaller onefile builds
def resource_path(relative_path: str) -> str:
    try:
        base_path = sys._MEIPASS  # type: ignore[attr-defined]
    except Exception:
        base_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base_path, relative_path)

def main():
    init_db()
    root = Window(themename='minty')
    app = InventoryApp(root)
    root.mainloop()


if __name__ == '__main__':
    init_db()
    root = Window(themename='minty')
    try:
        # Use a multi-size .ico containing 16/32/48/256 px for best results
        root.iconbitmap(resource_path('icon.ico'))
    except Exception:
        pass
    root.title('Daito.dev')
    root.geometry('1366x768')
    app = InventoryApp(root)
    root.mainloop()
