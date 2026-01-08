from tkinter import Tk, Frame, Label, Entry, Button, BOTH, LEFT, RIGHT, X
from tkinter import messagebox

from excel_auth import authenticate_user, ensure_users_sheet


class LoginWindow:
    """Simple blocking login window.

    Usage:
        win = LoginWindow()
        user_info = win.show()
        if user_info is None:
            # user cancelled / closed
            ...
        else:
            # user_info is dict with username, role, full_name
            ...
    """

    def __init__(self) -> None:
        self.root = Tk()
        self.root.title('Login - Dietary Management System')
        self.root.geometry('360x200')
        self.root.resizable(False, False)

        # Center window
        self.root.update_idletasks()
        w = 360
        h = 200
        x = (self.root.winfo_screenwidth() - w) // 2
        y = (self.root.winfo_screenheight() - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")

        self.user_info = None

        # Ensure Users sheet and default admin exist
        try:
            ensure_users_sheet()
        except Exception:
            pass

        main = Frame(self.root, padx=20, pady=20)
        main.pack(fill=BOTH, expand=True)

        Label(main, text='Dietary Management System', font=('Segoe UI', 12, 'bold')).pack(pady=(0, 10))

        # Username
        user_frame = Frame(main)
        user_frame.pack(fill=X, pady=4)
        Label(user_frame, text='Username:', width=12, anchor='w').pack(side=LEFT)
        self.username_entry = Entry(user_frame)
        self.username_entry.pack(side=RIGHT, fill=X, expand=True)

        # Password
        pw_frame = Frame(main)
        pw_frame.pack(fill=X, pady=4)
        Label(pw_frame, text='Password:', width=12, anchor='w').pack(side=LEFT)
        self.password_entry = Entry(pw_frame, show='•')
        self.password_entry.pack(side=RIGHT, fill=X, expand=True)

        # Buttons
        btn_frame = Frame(main, pady=10)
        btn_frame.pack(fill=X)
        Button(btn_frame, text='Login', width=10, command=self._on_login).pack(side=LEFT, padx=5)
        Button(btn_frame, text='Exit', width=10, command=self._on_exit).pack(side=RIGHT, padx=5)

        # Bind Enter to login
        self.root.bind('<Return>', lambda event: self._on_login())

        # Focus username initially
        self.username_entry.focus_set()

    def _on_login(self) -> None:
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        if not username or not password:
            messagebox.showerror('Login Failed', 'Please enter both username and password.')
            return
        user = authenticate_user(username, password)
        if not user:
            messagebox.showerror('Login Failed', 'Invalid username or password.')
            return
        self.user_info = user
        self.root.destroy()

    def _on_exit(self) -> None:
        self.user_info = None
        self.root.destroy()

    def show(self):
        """Run the login window and return user_info or None."""
        self.root.mainloop()
        return self.user_info
