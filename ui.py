# ui.py
from tkinter import *
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import json
import os
import sys
import platform
from constants import *
from extractor import open_extractor_window
from db_utils import DatabaseError
from excel_utils import ExcelFileOpenError
from typing import Optional

class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.entries = {}
        # Search state
        self.search_var = StringVar()
        self.search_after_id = None  # for debounced search
        # Cached data for table to avoid loading Excel on every keystroke
        self.all_rows = []
        # Settings (store in user-writable config dir)
        self.settings_dir = self._get_user_config_dir('Dietary_Management_System')
        try:
            os.makedirs(self.settings_dir, exist_ok=True)
        except Exception:
            pass
        self.settings_path = os.path.join(self.settings_dir, 'settings.json')
        self.settings = self.load_settings()
        # Apply saved theme early if running under ttkbootstrap Window
        try:
            self._apply_theme(self.settings.get('theme'))
        except Exception:
            pass
        self.create_widgets()
        self.load_data()
        self.refresh_table()
        # Auto-backup scheduling
        self._auto_backup_after_id: Optional[str] = None
        if self.settings.get('auto_backup_enabled', False):
            self._schedule_next_backup()
            
        # Clean up old settings if they exist
        if 'auto_summary' in self.settings:
            del self.settings['auto_summary']
            self.save_settings()

    def create_widgets(self):
        style = ttk.Style()
        # Use the active theme (ttkbootstrap sets this); don't override here
        style.configure('Treeview', font=('Segoe UI', 10), rowheight=24)
        style.configure('Treeview.Heading', font=('Segoe UI', 11, 'bold'))
        style.configure('TButton', font=('Segoe UI', 10), padding=6)
        style.configure('TLabel', font=('Segoe UI', 10))
        style.configure('TEntry', font=('Segoe UI', 10))

        # --- Scrollable container for the whole page ---
        container = ttk.Frame(self.root)
        container.pack(fill=BOTH, expand=True)
        canvas = Canvas(container, highlightthickness=0)
        vscroll = ttk.Scrollbar(container, orient=VERTICAL, command=canvas.yview)
        canvas.configure(yscrollcommand=vscroll.set)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        vscroll.pack(side=RIGHT, fill=Y)
        # Inner content frame that will scroll
        self.content = ttk.Frame(canvas)
        content_window = canvas.create_window((0, 0), window=self.content, anchor='nw')

        def _on_content_configure(event):
            try:
                canvas.configure(scrollregion=canvas.bbox('all'))
            except Exception:
                pass
        self.content.bind('<Configure>', _on_content_configure)

        def _on_canvas_configure(event):
            try:
                # Make content frame width track the canvas width
                canvas.itemconfigure(content_window, width=event.width)
            except Exception:
                pass
        canvas.bind('<Configure>', _on_canvas_configure)

        # Optional: mouse wheel support (Windows)
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), 'units')
        try:
            canvas.bind_all('<MouseWheel>', _on_mousewheel)
        except Exception:
            pass

        # Title
        title = ttk.Label(self.content, text='Dietary Management System', font=('Segoe UI', 18, 'bold'))
        title.pack(pady=(10, 0))
        
        # Footer with copyright
        footer_frame = ttk.Frame(self.content)
        footer_frame.pack(side=BOTTOM, fill=X, pady=(0, 0))
        
        current_year = datetime.now().year
        footer_label = ttk.Label(
            footer_frame, 
            text=f' Daito.dev. All rights reserved.',
            font=('Segoe UI', 8, 'italic'),
            padding=(0, 2, 0, 2)
        )
        footer_label.pack()
        
        # Footer style inherits from theme; no explicit colors to respect dark mode

        # Entry fields (auto-generated for all columns)
        frame = ttk.Frame(self.content, padding=10)
        frame.pack(padx=10, pady=10)

        # Widget references for all fields
        self.entries = {}
        # Combobox options for some fields (imported from constants.py)
        sex_options = SEX_OPTIONS
        age_group_options = AGE_GROUP_OPTIONS
        ward_options = WARD_OPTIONS
        subspecialty_options = SUBSPECIALTY_OPTIONS
        type_of_visit_options = TYPE_OF_VISIT_OPTIONS
        purpose_of_visit_options = PURPOSE_OPTIONS
        nutrition_support_options = NUTRITION_SUPPORT_OPTIONS
        nutritional_status_options = NUTRITIONAL_STATUS_OPTIONS
        bowel_movement_options = BOWEL_MOVEMENT_OPTIONS
        emesis_options = EMESIS_OPTIONS
        abdominal_distention_options = ABDOMINAL_DISTENTION_OPTIONS
        biochemical_parameters_options = BIOCHEMICAL_PARAMETERS_OPTIONS
        rnd_dietary_management_options = RND_DIETARY_MANAGEMENT_OPTIONS
        encoded_by_options = ENCODED_BY_OPTIONS
        

        # Improved grid layout: 4 fields per row, label and entry adjacent
        max_fields_per_row = 4
        row = 0
        col = 0
        for idx, colname in enumerate(COLUMNS):
            if colname in ['Patient ID', 'Last Updated']:
                continue  # Patient ID is auto, Last Updated is auto-filled
            label = ttk.Label(frame, text=colname)
            label.grid(row=row, column=col*2, sticky=W, padx=(0,2), pady=6)
            # Choose widget type
            if colname == 'Sex':
                widget = ttk.Combobox(frame, values=SEX_OPTIONS, width=16, state='readonly')
            elif colname == 'Age Group':
                widget = ttk.Combobox(frame, values=AGE_GROUP_OPTIONS, width=16, state='readonly')
            elif colname == 'Ward':
                widget = ttk.Combobox(frame, values=WARD_OPTIONS, width=16)
            elif colname == 'Subspecialty':
                widget = ttk.Combobox(frame, values=SUBSPECIALTY_OPTIONS, width=16)
            elif colname == 'Type Of Visit':
                widget = ttk.Combobox(frame, values=TYPE_OF_VISIT_OPTIONS, width=16)
            elif colname == 'Purpose of Visit':
                widget = ttk.Combobox(frame, values=PURPOSE_OPTIONS, width=16)
            elif colname == 'With Nutrition Support':
                widget = ttk.Combobox(frame, values=NUTRITION_SUPPORT_OPTIONS, width=10)
            elif colname == 'Nutritional Status':
                widget = ttk.Combobox(frame, values=NUTRITIONAL_STATUS_OPTIONS, width=16)
            elif colname == 'Bowel Movement':
                widget = ttk.Combobox(frame, values=BOWEL_MOVEMENT_OPTIONS, width=24)
            elif colname == 'Emesis':
                widget = ttk.Combobox(frame, values=EMESIS_OPTIONS, width=12)
            elif colname == 'Abdominal Distention':
                widget = ttk.Combobox(frame, values=ABDOMINAL_DISTENTION_OPTIONS, width=12)
            elif colname == 'Biochemical Parameters':
                widget = ttk.Combobox(frame, values=BIOCHEMICAL_PARAMETERS_OPTIONS, width=30)
            elif colname == 'RND Dietary Management':
                widget = ttk.Combobox(frame, values=RND_DIETARY_MANAGEMENT_OPTIONS, width=30)
            elif colname == 'Diet Prescriptions(Current)':
                # Handled below as a multi-line Text field; skip placing in the grid
                continue
            elif colname == 'With Documents':
                widget = ttk.Combobox(frame, values=WITH_DOCUMENTS_OPTIONS, width=10)
            elif colname == 'Given NCP':
                widget = ttk.Combobox(frame, values=GIVEN_NCP_OPTIONS, width=10)
            elif colname == 'Encoded By':
                widget = ttk.Combobox(frame, values=ENCODED_BY_OPTIONS, width=16)
            elif colname in ['Ward Admission Date', 'Date of Visit', 'Encoded Date']:
                # Date dropdowns: year, month, day
                date_frame = ttk.Frame(frame)
                current_year = datetime.now().year
                years = [str(y) for y in range(2030, 2009, -1)]
                months = [f'{m:02d}' for m in range(1, 13)]
                days = [f'{d:02d}' for d in range(1, 32)]
                year_cb = ttk.Combobox(date_frame, values=years, width=6, state='readonly')
                month_cb = ttk.Combobox(date_frame, values=months, width=4, state='readonly')
                day_cb = ttk.Combobox(date_frame, values=days, width=4, state='readonly')
                year_cb.grid(row=0, column=0, padx=(0,3))
                month_cb.grid(row=0, column=1, padx=(0,3))
                day_cb.grid(row=0, column=2, padx=(0,3))
                self.entries[colname] = (year_cb, month_cb, day_cb)
                widget = date_frame
            else:
                widget = ttk.Entry(frame, width=18)
            widget.grid(row=row, column=col*2+1, sticky=EW, padx=(0,12), pady=6)
            if colname not in ['Ward Admission Date', 'Date of Visit', 'Encoded Date']:
                self.entries[colname] = widget
            col += 1
            if col >= max_fields_per_row:
                row += 1
                col = 0
        # Make columns expand evenly
        for i in range(max_fields_per_row*2):
            frame.grid_columnconfigure(i, weight=1)

        # Long text field below the grid: Diet Prescriptions(Current)
        long_frame = ttk.Frame(self.content, padding=(10, 0, 10, 0))
        long_frame.pack(padx=10, pady=(0, 10))
        ttk.Label(long_frame, text='Diet Prescriptions(Current)').grid(row=0, column=0, sticky=W)
        dp_text = Text(long_frame, height=4, width=100, wrap='word')
        dp_scroll = ttk.Scrollbar(long_frame, orient=VERTICAL, command=dp_text.yview)
        dp_text.configure(yscrollcommand=dp_scroll.set)
        dp_text.grid(row=1, column=0, sticky='nw', pady=(4, 0))
        dp_scroll.grid(row=1, column=1, sticky='ns', pady=(4, 0))
        long_frame.grid_columnconfigure(0, weight=0)
        self.entries['Diet Prescriptions(Current)'] = dp_text

        # Buttons
        btn_frame = ttk.Frame(self.content)
        btn_frame.pack(pady=5)
        self.add_button = ttk.Button(btn_frame, text='Add Patient', command=self.add_item)
        self.add_button.grid(row=0, column=0, padx=3)
        ttk.Button(btn_frame, text='Update Patient', command=self.update_item).grid(row=0, column=1, padx=3)
        ttk.Button(btn_frame, text='Delete Patient', command=self.delete_item).grid(row=0, column=2, padx=3)
        ttk.Button(btn_frame, text='Open Extractor', command=self.open_extractor).grid(row=0, column=3, padx=3)
        ttk.Button(btn_frame, text='Export to Excel', command=self.export_excel).grid(row=0, column=4, padx=3)

        # Backup controls
        ttk.Button(btn_frame, text='Backup Now', command=self.backup_now).grid(row=0, column=6, padx=(12, 3))
        self.auto_backup_var = BooleanVar(value=bool(self.settings.get('auto_backup_enabled', False)))
        self.auto_backup_chk = ttk.Checkbutton(
            btn_frame,
            text='Auto-backup',
            variable=self.auto_backup_var,
            command=self.on_auto_backup_toggle
        )
        self.auto_backup_chk.grid(row=0, column=7, padx=(6, 3))
        # Interval
        ttk.Label(btn_frame, text='every (min):').grid(row=0, column=8, padx=(6, 3))
        self.backup_interval_var = StringVar(value=str(self.settings.get('backup_interval_minutes', 60)))
        self.backup_interval_entry = ttk.Entry(btn_frame, textvariable=self.backup_interval_var, width=5)
        self.backup_interval_entry.grid(row=0, column=9, padx=(0, 3))
        self.backup_interval_entry.bind('<FocusOut>', lambda e: self.on_backup_interval_change())
        self.backup_interval_entry.bind('<Return>', self.on_backup_interval_enter)
        # Refresh button to reload data and update table
        ttk.Button(btn_frame, text='Refresh', command=self.refresh_now).grid(row=0, column=10, padx=(6, 3))
        # Settings button (theme selector, etc.)
        ttk.Button(btn_frame, text='Settings', command=self.open_settings).grid(row=0, column=11, padx=(6, 3))

        # Search bar (filters table)
        search_frame = ttk.Frame(self.content)
        search_frame.pack(padx=10, pady=(6, 0), fill=X)
        ttk.Label(search_frame, text='Search:').pack(side=LEFT)
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        self.search_entry.pack(side=LEFT, padx=(6, 6))
        ttk.Button(search_frame, text='Clear', command=self.clear_search).pack(side=LEFT)
        # Live filtering
        self.search_entry.bind('<KeyRelease>', self.on_search)

        # Table (single instance)
        table_frame = ttk.Frame(self.content)
        table_frame.pack(padx=10, pady=10, fill=BOTH, expand=True)

        # Configure treeview with better spacing
        style = ttk.Style()
        style.configure('Treeview', rowheight=28)  # Increased row height
        style.configure('Treeview.Heading', font=('Segoe UI', 10, 'bold'))
        
        # Create treeview with horizontal scrollbar
        self.tree = ttk.Treeview(
            table_frame, 
            columns=COLUMNS, 
            show='headings', 
            style='Treeview',
            selectmode='browse',
            height=20  # Show 20 rows by default
        )
        
        # Configure column widths based on content
        col_widths = {
            'Patient ID': 100,
            'Last Name': 120,
            'First Name': 120,
            'Middle Name': 120,
            'Age': 60,
            'Sex': 80,
            'Room': 80,
            'Diet Type': 150,
            'Allergies': 200,
            'Diet Prescriptions': 250,
            'Notes': 300,
            'Last Updated': 150
        }
        
        # Set up columns with appropriate widths
        for col in COLUMNS:
            width = col_widths.get(col, 120)  # Default width 120 if not specified
            self.tree.heading(col, text=col, anchor=W)
            self.tree.column(col, width=width, minwidth=80, stretch=NO, anchor=W)
        
        # Bind selection event to input population
        self.tree.bind('<<TreeviewSelect>>', self.on_row_select)

        # Scrollbars for the table
        vscrollbar = ttk.Scrollbar(table_frame, orient=VERTICAL, command=self.tree.yview)
        hscrollbar = ttk.Scrollbar(table_frame, orient=HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=vscrollbar.set, xscrollcommand=hscrollbar.set)
        
        # Grid layout with proper expansion
        self.tree.grid(row=0, column=0, sticky='nsew')
        vscrollbar.grid(row=0, column=1, sticky='ns')
        hscrollbar.grid(row=1, column=0, sticky='ew')
        
        # Configure grid weights for proper resizing
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

    def on_row_select(self, event):
        selected = self.tree.focus()
        if not selected:
            return
        values = self.tree.item(selected, 'values')
        if values:
            for idx, col in enumerate(COLUMNS):
                if col in ['Patient ID', 'Last Updated']:
                    continue
                widget = self.entries[col]
                value = values[idx] if idx < len(values) else ''
                if col in ['Ward Admission Date', 'Date of Visit', 'Encoded Date']:
                    year_cb, month_cb, day_cb = widget
                    if value and '-' in value:
                        parts = value.split('-')
                        if len(parts) == 3:
                            year_cb.set(parts[0])
                            month_cb.set(parts[1])
                            day_cb.set(parts[2])
                        else:
                            year_cb.set('')
                            month_cb.set('')
                            day_cb.set('')
                    else:
                        year_cb.set('')
                        month_cb.set('')
                        day_cb.set('')
                elif isinstance(widget, ttk.Combobox):
                    widget.set(value)
                elif isinstance(widget, Text):
                    widget.delete('1.0', END)
                    widget.insert('1.0', value)
                else:
                    widget.delete(0, END)
                    widget.insert(0, value)
            # Disable Add button when a row is selected
            if hasattr(self, 'add_button'):
                self.add_button['state'] = 'disabled'


    def add_item(self):
        # Compose item in the order of COLUMNS
        from db_utils import add_patient, load_patients
        # Auto-increment Patient ID
        patients = load_patients()
        existing_ids = [row[0] for row in patients if isinstance(row[0], int) or (isinstance(row[0], str) and str(row[0]).isdigit())]
        next_id = max([int(i) for i in existing_ids], default=0) + 1 if existing_ids else 1
        item = []
        for col in COLUMNS:
            if col == 'Patient ID':
                item.append(next_id)
            elif col == 'Last Updated':
                item.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            elif col in ['Ward Admission Date', 'Date of Visit', 'Encoded Date']:
                year_cb, month_cb, day_cb = self.entries[col]
                y = year_cb.get()
                m = month_cb.get()
                d = day_cb.get()
                val = f"{y}-{m}-{d}" if y and m and d else ''
                item.append(val)
            else:
                w = self.entries[col]
                if isinstance(w, Text):
                    val = w.get('1.0', 'end-1c')
                else:
                    val = w.get()
                item.append(val)
        if not all(item[1:6]):
            messagebox.showerror('Error', 'All fields except Patient ID and Last Updated are required.')
            return
        try:
            add_patient(item)
        except DatabaseError as e:
            messagebox.showerror('Database Error', str(e))
            return
        # Optionally regenerate summary tables
        if getattr(self, 'auto_summary_var', None) and self.auto_summary_var.get():
            # Placeholder: when exporting from DB, summary will be generated on export
            pass
        # Reload cache once after data changes, then refresh view
        self.load_data()
        self.refresh_table()
        self.clear_fields()  # Clear fields after adding
        messagebox.showinfo('Success', f'Patient added successfully. Assigned Patient ID: {next_id}')

    def clear_fields(self):
        for col in COLUMNS:
            if col in ['Patient ID', 'Last Updated']:
                continue
            widget = self.entries[col]
            if col in ['Ward Admission Date', 'Date of Visit', 'Encoded Date']:
                year_cb, month_cb, day_cb = widget
                year_cb.set('')
                month_cb.set('')
                day_cb.set('')
            elif isinstance(widget, ttk.Combobox):
                widget.set('')
            elif isinstance(widget, Text):
                widget.delete('1.0', END)
            else:
                widget.delete(0, END)
        # Re-enable Add button when fields are cleared
        if hasattr(self, 'add_button'):
            self.add_button['state'] = 'normal'

    def delete_item(self):
        from db_utils import delete_patient
        selected = self.tree.focus()
        if not selected:
            messagebox.showerror('Error', 'Please select a patient to delete.')
            return
        values = self.tree.item(selected, 'values')
        if not values:
            messagebox.showerror('Error', 'No patient selected.')
            return
        item_id = values[0]
        try:
            delete_patient(item_id)
        except DatabaseError as e:
            messagebox.showerror('Database Error', str(e))
            return
        self.load_data()
        self.refresh_table()
        self.clear_fields()
        self.tree.selection_remove(self.tree.selection())
        messagebox.showinfo('Success', 'Patient deleted successfully.')

    def update_item(self):
        from db_utils import update_patient
        selected = self.tree.focus()
        if not selected:
            messagebox.showerror('Error', 'Please select a patient to update.')
            return
        values = self.tree.item(selected, 'values')
        if not values:
            messagebox.showerror('Error', 'No patient selected.')
            return
        item_id = values[0]
        updated_item = []
        for col in COLUMNS:
            if col == 'Patient ID':
                updated_item.append(item_id)
            elif col == 'Last Updated':
                updated_item.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            elif col in ['Ward Admission Date', 'Date of Visit', 'Encoded Date']:
                year_cb, month_cb, day_cb = self.entries[col]
                y = year_cb.get()
                m = month_cb.get()
                d = day_cb.get()
                updated_item.append(f"{y}-{m}-{d}" if y and m and d else '')
            else:
                w = self.entries[col]
                if isinstance(w, Text):
                    updated_item.append(w.get('1.0', 'end-1c'))
                else:
                    updated_item.append(w.get())
        try:
            update_patient(item_id, updated_item)
        except DatabaseError as e:
            messagebox.showerror('Database Error', str(e))
            return
        # Summary tables are now handled by export functionality
        self.load_data()
        self.refresh_table()
        self.clear_fields()  # Clear fields after update

    def load_data(self):
        # Load patients from Excel once; other operations use this cache
        from db_utils import load_patients
        try:
            self.all_rows = load_patients()
        except Exception:
            self.all_rows = []

    def refresh_table(self):
        # Use cached rows to avoid expensive I/O during typing
        all_rows = getattr(self, 'all_rows', [])
        # Apply text filter across all columns if provided
        query = (self.search_var.get() if hasattr(self, 'search_var') else '').strip().lower()
        if query and len(query) >= 2:
            def matches(row):
                return any((str(cell).lower().find(query) != -1) for cell in row)
            rows = [r for r in all_rows if matches(r)]
        else:
            rows = all_rows
        # Rebuild table
        for i in self.tree.get_children():
            self.tree.delete(i)
        for row in rows:
            self.tree.insert('', END, values=row)

    def on_search(self, event=None):
        # Debounce: wait a short moment after typing stops
        if self.search_after_id is not None:
            try:
                self.root.after_cancel(self.search_after_id)
            except Exception:
                pass
        self.search_after_id = self.root.after(250, self.refresh_table)

    def clear_search(self):
        self.search_var.set('')
        self.refresh_table()

    def refresh_now(self):
        # Reload data from source and refresh the table view
        self.load_data()
        self.refresh_table()

    # --- Settings persistence ---
    def load_settings(self):
        # Try preferred location
        try:
            with open(self.settings_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, dict):
                    return data
        except Exception:
            pass
        # Backward compatibility: try old settings next to script (pre-build)
        try:
            legacy_path = os.path.join(os.path.dirname(__file__), 'settings.json')
            with open(legacy_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, dict):
                    return data
        except Exception:
            pass
        return {}

    def save_settings(self):
        data = dict(self.settings)
        # Ensure current auto summary value is stored
        data['auto_summary'] = bool(self.auto_summary_var.get()) if hasattr(self, 'auto_summary_var') else data.get('auto_summary', True)
        # Backup settings
        if hasattr(self, 'auto_backup_var'):
            data['auto_backup_enabled'] = bool(self.auto_backup_var.get())
        if hasattr(self, 'backup_interval_var'):
            try:
                data['backup_interval_minutes'] = max(1, int(self.backup_interval_var.get()))
            except Exception:
                data['backup_interval_minutes'] = data.get('backup_interval_minutes', 60)
        # Default backup dir inside settings dir if not set
        if not data.get('backup_dir'):
            data['backup_dir'] = os.path.join(self.settings_dir, 'backups')
        # Persist theme if present
        if 'theme' in self.settings and self.settings.get('theme'):
            data['theme'] = self.settings.get('theme')
        try:
            with open(self.settings_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        except Exception:
            # Non-fatal; ignore write errors
            pass

    # --- Theme management ---
    def _apply_theme(self, theme_name: Optional[str]):
        if not theme_name:
            return
        try:
            # ttkbootstrap Window exposes .style with theme_use
            current = self.root.style.theme_use()
            if current != theme_name:
                # Ensure the theme exists; fallback if not
                available = set(self.root.style.theme_names())
                if theme_name in available:
                    self.root.style.theme_use(theme_name)
                else:
                    # Fallback to a safe default if requested theme missing
                    self.root.style.theme_use('darkly' if 'darkly' in available else current)
        except Exception:
            # If not a ttkbootstrap Window, ignore
            pass

    def open_settings(self):
        top = Toplevel(self.root)
        top.title('Settings')
        top.transient(self.root)
        top.resizable(False, False)
        # Make modal and center over parent
        try:
            top.update_idletasks()
            parent_x = self.root.winfo_rootx()
            parent_y = self.root.winfo_rooty()
            parent_w = self.root.winfo_width()
            parent_h = self.root.winfo_height()
            win_w = top.winfo_width()
            win_h = top.winfo_height()
            if win_w <= 1 or win_h <= 1:
                # Toplevel may not be laid out yet; assume a reasonable default size
                win_w, win_h = 360, 140
            x = parent_x + max(0, (parent_w - win_w) // 2)
            y = parent_y + max(0, (parent_h - win_h) // 2)
            top.geometry(f"+{x}+{y}")
            top.grab_set()
            top.focus_set()
        except Exception:
            pass
        pad = {'padx': 10, 'pady': 8}

        ttk.Label(top, text='Theme').grid(row=0, column=0, sticky='w', **pad)
        # Get available themes from current style
        try:
            themes = list(self.root.style.theme_names())
        except Exception:
            themes = []
        self.theme_var = StringVar(value=self.settings.get('theme') or (self.root.style.theme_use() if hasattr(self.root, 'style') else ''))
        theme_cb = ttk.Combobox(top, values=themes, textvariable=self.theme_var, state='readonly', width=18)
        theme_cb.grid(row=0, column=1, sticky='w', **pad)

        btns = ttk.Frame(top)
        btns.grid(row=1, column=0, columnspan=2, sticky='e', padx=10, pady=(0,10))
        ttk.Button(btns, text='Apply', command=lambda: self._on_theme_apply(top)).grid(row=0, column=0, padx=(0,6))
        ttk.Button(btns, text='Close', command=top.destroy).grid(row=0, column=1)

    def _on_theme_apply(self, dialog):
        theme = self.theme_var.get().strip()
        if theme:
            self.settings['theme'] = theme
            self._apply_theme(theme)
            self.save_settings()

    def backup_now(self):
        try:
            from backup_utils import backup_all
            backup_dir = self.settings.get('backup_dir') or os.path.join(self.settings_dir, 'backups')
            os.makedirs(backup_dir, exist_ok=True)
            results = backup_all(backup_dir, with_excel=False)
            msg = "Backup created:\n"
            if 'sql' in results:
                msg += f"- SQL: {results['sql']}\n"
            if 'excel' in results:
                msg += f"- Excel: {results['excel']}\n"
            messagebox.showinfo('Backup', msg.rstrip())
        except DatabaseError as e:
            messagebox.showerror('Database Error', f'Backup failed due to database error:\n{e}')
        except Exception as e:
            messagebox.showerror('Backup Error', f'Unexpected error during backup:\n{e}')

    def on_auto_backup_toggle(self):
        enabled = bool(self.auto_backup_var.get())
        self.settings['auto_backup_enabled'] = enabled
        self.save_settings()
        # Cancel any existing schedule
        if self._auto_backup_after_id is not None:
            try:
                self.root.after_cancel(self._auto_backup_after_id)
            except Exception:
                pass
            self._auto_backup_after_id = None
        if enabled:
            self._schedule_next_backup()

    def on_backup_interval_change(self):
        try:
            minutes = max(1, int(self.backup_interval_var.get()))
        except Exception:
            minutes = 60
        self.settings['backup_interval_minutes'] = minutes
        self.save_settings()
        if self.auto_backup_var.get():
            # reschedule
            if self._auto_backup_after_id is not None:
                try:
                    self.root.after_cancel(self._auto_backup_after_id)
                except Exception:
                    pass
                self._auto_backup_after_id = None
            self._schedule_next_backup()

    def on_backup_interval_enter(self, event=None):
        # Reuse existing change logic, then inform the user
        self.on_backup_interval_change()
        try:
            minutes = int(self.settings.get('backup_interval_minutes', 60))
        except Exception:
            minutes = 60
        try:
            messagebox.showinfo('Auto-backup', f'Backup interval updated to {minutes} minute(s).')
        except Exception:
            pass

    def _schedule_next_backup(self):
        minutes = int(self.settings.get('backup_interval_minutes', 60))
        delay_ms = max(1, minutes) * 60 * 1000
        # Schedule
        self._auto_backup_after_id = self.root.after(delay_ms, self._run_auto_backup_tick)

    def _run_auto_backup_tick(self):
        # Perform backup quietly; surface errors
        try:
            from backup_utils import backup_all
            backup_dir = self.settings.get('backup_dir') or os.path.join(self.settings_dir, 'backups')
            os.makedirs(backup_dir, exist_ok=True)
            backup_all(backup_dir, with_excel=False)
        except Exception as e:
            # Non-fatal: show a brief warning
            try:
                messagebox.showwarning('Auto-backup', f'Auto-backup encountered an error:\n{e}')
            except Exception:
                pass
        finally:
            # Schedule next run if still enabled
            if self.settings.get('auto_backup_enabled', False):
                self._schedule_next_backup()

    def _get_user_config_dir(self, app_name: str) -> str:
        system = platform.system()
        home = os.path.expanduser('~')
        if system == 'Windows':
            base = os.environ.get('APPDATA') or os.path.join(home, 'AppData', 'Roaming')
            return os.path.join(base, app_name)
        elif system == 'Darwin':
            return os.path.join(home, 'Library', 'Application Support', app_name)
        else:
            base = os.environ.get('XDG_CONFIG_HOME') or os.path.join(home, '.config')
            return os.path.join(base, app_name)

    def export_excel(self):
        from exporter import export_db_to_excel
        export_path = filedialog.asksaveasfilename(defaultextension='.xlsx', filetypes=[('Excel files', '*.xlsx')])
        if export_path:
            try:
                export_db_to_excel(export_path)
                messagebox.showinfo('Exported', f'Inventory exported to {export_path}')
            except DatabaseError as e:
                messagebox.showerror('Database Error', f'Failed to export from DB:\n{e}')
            except Exception as e:
                messagebox.showerror('Export Error', f'Unexpected error during export:\n{e}')

    def open_extractor(self):
        # Opens the extractor/merger window defined in extractor.py
        try:
            open_extractor_window(self.root)
        except Exception as e:
            messagebox.showerror('Extractor Error', f'Unable to open extractor window:\n{e}')