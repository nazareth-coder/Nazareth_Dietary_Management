import os
import sys
from ttkbootstrap import Window
from ui import InventoryApp
from excel_utils import init_excel
from login_window import LoginWindow

# Resolve resource paths in dev and in PyInstaller onefile builds
def resource_path(relative_path: str) -> str:
    try:
        base_path = sys._MEIPASS  # type: ignore[attr-defined]
    except Exception:
        base_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base_path, relative_path)

def main():
    # Ensure Excel structure (including Users sheet for login) exists
    init_excel()

    # Show login window first (separate simple Tk root)
    login = LoginWindow()
    user_info = login.show()
    if not user_info:
        # User cancelled or closed login
        return

    root = Window(themename='minty')
    try:
        # Use a multi-size .ico containing 16/32/48/256 px for best results
        root.iconbitmap(resource_path('icon.ico'))
    except Exception:
        pass
    display_name = (user_info.get('full_name') or user_info.get('username') or 'Dietary Management System')
    root.title(display_name)
    root.geometry('1366x768')
    app = InventoryApp(root, user_info=user_info)
    root.mainloop()


if __name__ == '__main__':
    main()
