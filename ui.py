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
        self.create_widgets()
        self.load_data()
        self.refresh_table()
        # Auto-backup scheduling
        self._auto_backup_after_id: Optional[str] = None
        if self.settings.get('auto_backup_enabled', False):
            self._schedule_next_backup()

    def create_widgets(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Treeview', font=('Segoe UI', 10), rowheight=24)
        style.configure('Treeview.Heading', font=('Segoe UI', 11, 'bold'))
        style.configure('TButton', font=('Segoe UI', 10), padding=6)
        style.configure('TLabel', font=('Segoe UI', 10))
        style.configure('TEntry', font=('Segoe UI', 10))

        # Title
        title = ttk.Label(self.root, text='Dietary Management System', font=('Segoe UI', 18, 'bold'), background='#f4f6fa', foreground='#333')
        title.pack(pady=(10, 0))
        
        # Footer with copyright
        footer_frame = ttk.Frame(self.root, style='Footer.TFrame')
        footer_frame.pack(side=BOTTOM, fill=X, pady=(0, 0))
        
        current_year = datetime.now().year
        footer_label = ttk.Label(
            footer_frame, 
            text=f'© {current_year} Daito.dev. All rights reserved.',
            font=('Segoe UI', 8, 'italic'),
            foreground='#666666',
            background='#f4f6fa',
            padding=(0, 2, 0, 2)  # Reduced vertical padding
        )
        footer_label.pack()
        
        # Configure footer style
        style.configure('Footer.TFrame', background='#f4f6fa')

        # Entry fields (auto-generated for all columns)
        frame = ttk.Frame(self.root, padding=10)
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
                widget = ttk.Entry(frame, width=30)
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

        # Buttons
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=5)
        self.add_button = ttk.Button(btn_frame, text='Add Patient', command=self.add_item)
        self.add_button.grid(row=0, column=0, padx=3)
        ttk.Button(btn_frame, text='Update Patient', command=self.update_item).grid(row=0, column=1, padx=3)
        ttk.Button(btn_frame, text='Delete Patient', command=self.delete_item).grid(row=0, column=2, padx=3)
        ttk.Button(btn_frame, text='Open Extractor', command=self.open_extractor).grid(row=0, column=3, padx=3)
        ttk.Button(btn_frame, text='Export to Excel', command=self.export_excel).grid(row=0, column=4, padx=3)

        # Auto-update summary toggle (persisted)
        default_auto = True if not isinstance(self.settings.get('auto_summary'), bool) else self.settings.get('auto_summary')
        self.auto_summary_var = BooleanVar(value=default_auto)
        self.auto_summary_chk = ttk.Checkbutton(
            btn_frame,
            text='Auto-update summary',
            variable=self.auto_summary_var,
            command=self.on_auto_summary_toggle
        )
        self.auto_summary_chk.grid(row=0, column=5, padx=(12, 0))

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

        # Add Summary Table button
        self.summary_button = ttk.Button(self.root, text="Add Summary Table", command=self.add_summary_table)
        self.summary_button.pack(pady=(10, 0))

        # Search bar (filters table)
        search_frame = ttk.Frame(self.root)
        search_frame.pack(padx=10, pady=(6, 0), fill=X)
        ttk.Label(search_frame, text='Search:').pack(side=LEFT)
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        self.search_entry.pack(side=LEFT, padx=(6, 6))
        ttk.Button(search_frame, text='Clear', command=self.clear_search).pack(side=LEFT)
        # Live filtering
        self.search_entry.bind('<KeyRelease>', self.on_search)

        # Table (single instance)
        table_frame = ttk.Frame(self.root)
        table_frame.pack(padx=10, pady=10, fill=BOTH, expand=True)

        self.tree = ttk.Treeview(table_frame, columns=COLUMNS, show='headings', style='Treeview')
        for col in COLUMNS:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor=W)
        self.tree.grid(row=0, column=0, sticky='nsew')
        # Bind selection event to input population
        self.tree.bind('<<TreeviewSelect>>', self.on_row_select)

        # Scrollbars for the table
        vscrollbar = ttk.Scrollbar(table_frame, orient=VERTICAL, command=self.tree.yview)
        hscrollbar = ttk.Scrollbar(table_frame, orient=HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscroll=vscrollbar.set, xscroll=hscrollbar.set)
        vscrollbar.grid(row=0, column=1, sticky='ns')
        hscrollbar.grid(row=1, column=0, sticky='ew')

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
                val = self.entries[col].get()
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
        # Optionally regenerate summary tables
        if getattr(self, 'auto_summary_var', None) and self.auto_summary_var.get():
            try:
                from excel_utils import add_summary_table_to_all_sheets
                add_summary_table_to_all_sheets()
            except ExcelFileOpenError as e:
                messagebox.showwarning('Summary Not Updated', f'Summary was not updated because the Excel file is open:\n{e}')
            except Exception as e:
                messagebox.showwarning('Summary Not Updated', f'Unexpected error while updating summary:\n{e}')
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
                updated_item.append(self.entries[col].get())
        try:
            update_patient(item_id, updated_item)
        except DatabaseError as e:
            messagebox.showerror('Database Error', str(e))
            return
        # Optionally regenerate summary tables
        if getattr(self, 'auto_summary_var', None) and self.auto_summary_var.get():
            try:
                from excel_utils import add_summary_table_to_all_sheets
                add_summary_table_to_all_sheets()
            except ExcelFileOpenError as e:
                messagebox.showwarning('Summary Not Updated', f'Summary was not updated because the Excel file is open:\n{e}')
            except Exception as e:
                messagebox.showwarning('Summary Not Updated', f'Unexpected error while updating summary:\n{e}')
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
        try:
            with open(self.settings_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        except Exception:
            # Non-fatal; ignore write errors
            pass

    def on_auto_summary_toggle(self):
        # Update settings and persist
        self.settings['auto_summary'] = bool(self.auto_summary_var.get())
        self.save_settings()

    def backup_now(self):
        try:
            from backup_utils import backup_all
            backup_dir = self.settings.get('backup_dir') or os.path.join(self.settings_dir, 'backups')
            os.makedirs(backup_dir, exist_ok=True)
            results = backup_all(backup_dir, with_excel=True)
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
            backup_all(backup_dir, with_excel=True)
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

    def add_summary_table(self):
        from excel_utils import add_summary_table_to_all_sheets
        add_summary_table_to_all_sheets()
        messagebox.showinfo('Success', 'Summary table has been added to all sheets.')

    def open_extractor(self):
        # Opens the extractor/merger window defined in extractor.py
        try:
            open_extractor_window(self.root)
        except Exception as e:
            messagebox.showerror('Extractor Error', f'Unable to open extractor window:\n{e}')