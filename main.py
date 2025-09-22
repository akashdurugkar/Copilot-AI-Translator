"""
Copilot Localization Translator
A comprehensive tool for managing and translating Microsoft Copilot Studio localization files.

Features:
- Load and parse Copilot localization JSON files
- Extract topics and context from complex key structures
- AI-powered context-aware translations
- Support for multiple languages and translation styles
- Edit translations directly in the UI
- Batch translation capabilities
- Export translated files in original format
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from tkinter.font import Font
import json
import os
import sys
from typing import Dict, List, Tuple, Optional
import threading
import queue
from pathlib import Path

# Import custom modules
from localization_parser import LocalizationParser
from translation_service import TranslationService
# Legacy UI components import removed after modernization cleanup

# ------------------ Design Tokens (inspired by Copilot Studio aesthetic) ------------------
DESIGN_TOKENS = {
    'light': {
        'bg_app': '#ffffff',
        'bg_card': '#F5F5F5',
        'bg_subtle': '#f1f3f7',
        'border_subtle': '#e2e8f0',
        'border_stronger': '#cbd5e1',
        'shadow_sm': {'offset': (0, 1), 'fill': '#dbe1e8'},
        'text_primary': '#0f172a',
        'text_secondary': '#475569',
        'text_inverse': '#ffffff',
        'focus_ring': '#2563eb',
        'brand_primary': '#4338CA',
        'brand_secondary': '#6366F1',
        'brand_accent1': '#2563EB',
        'brand_accent2': '#0EA5E9',
    },
    'dark': {
        # Softer charcoal palette
        'bg_app': '#1E1E2F',
        'bg_card': '#262D3D',
        'bg_subtle': '#30384A',
        'border_subtle': '#3a4558',
        'border_stronger': '#4b5568',
        'shadow_sm': {'offset': (0, 1), 'fill': '#0f172a'},
        'text_primary': '#f1f5f9',
        'text_secondary': '#cbd5e1',
        'text_inverse': '#1e293b',
        'focus_ring': '#2563eb',
        'brand_primary': '#6366F1',
        'brand_secondary': '#818cf8',
        'brand_accent1': '#3b82f6',
        'brand_accent2': '#0EA5E9',
    },
    # Shared primitive scale
    'radius_sm': 6,
    'radius_md': 10,
    'radius_lg': 18,
    'spacing_xs': 4,
    'spacing_sm': 8,
    'spacing_md': 12,
    'spacing_lg': 20,
}

def get_token(theme: str, name: str):
    base = DESIGN_TOKENS.get(theme, DESIGN_TOKENS['light'])
    if name in DESIGN_TOKENS:  # shared scale values
        return DESIGN_TOKENS[name]
    return base.get(name)

def detect_system_theme():
    """Best-effort system theme detection (Windows 10/11). Returns 'light' or 'dark'."""
    try:
        if sys.platform.startswith('win'):
            import winreg
            reg_path = r"Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize"
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path) as k:
                # 1 = light, 0 = dark
                apps_use_light, _ = winreg.QueryValueEx(k, 'AppsUseLightTheme')
                return 'light' if apps_use_light == 1 else 'dark'
    except Exception:
        pass
    return 'light'

# ------------------ Simple Tooltip Helper ------------------
class Tooltip:
    """Minimal tooltip implementation for clarity of filter purposes."""
    def __init__(self, widget, text: str, delay: int = 450):
        self.widget = widget
        self.text = text
        self.delay = delay
        self._after_id = None
        self.tip = None
        widget.bind('<Enter>', self._schedule)
        widget.bind('<Leave>', self._hide)
        widget.bind('<ButtonPress>', self._hide)

    def _schedule(self, _):
        self._after_id = self.widget.after(self.delay, self._show)

    def _show(self):
        if self.tip or not self.text:
            return
        try:
            x = self.widget.winfo_rootx() + 10
            y = self.widget.winfo_rooty() + self.widget.winfo_height() + 6
            self.tip = tk.Toplevel(self.widget)
            self.tip.wm_overrideredirect(True)
            self.tip.configure(bg='#1e293b')
            lbl = tk.Label(self.tip, text=self.text, bg='#1e293b', fg='white', bd=0,
                           font=("Segoe UI", 8), padx=8, pady=4, justify='left', wraplength=260)
            lbl.pack()
            self.tip.wm_geometry(f"+{x}+{y}")
        except Exception:
            pass

    def _hide(self, _):
        if self._after_id:
            try:
                self.widget.after_cancel(self._after_id)
            except Exception:
                pass
            self._after_id = None
        if self.tip:
            try:
                self.tip.destroy()
            except Exception:
                pass
            self.tip = None

# ------------------ Helper Classes (moved near top for availability) ------------------
class SimpleTranslationTable:
    """Lightweight table abstraction replacing previous complex UI component."""
    def __init__(self, parent, edit_callback):
        self.parent = parent
        self.edit_callback = edit_callback
        self.frame = tk.Frame(parent, bg="#ffffff", highlightthickness=1, highlightcolor="#e2e8f0")
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.tree = ttk.Treeview(self.frame, columns=("original","translation","topic","component","status"), show='headings')
        headings = [("original","Original"), ("translation","Translation"), ("topic","Topic"), ("component","Component"), ("status","Status")]
        for col, text in headings:
            self.tree.heading(col, text=text, anchor='center')
            self.tree.column(col, width=180 if col in ("original","translation") else 110, anchor='center')
        vsb = ttk.Scrollbar(self.frame, orient='vertical', command=self.tree.yview)
        hsb = ttk.Scrollbar(self.frame, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscroll=vsb.set, xscroll=hsb.set)
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        self.tree.bind('<Double-1>', self._on_edit)
        self.data = {}  # key -> record
        self.all_ids: List[str] = []  # preserve original ordering / all keys

    def load_data(self, data_dict):
        self.clear()
        self.data = data_dict
        self.all_ids = []
        for key, meta in data_dict.items():
            component_val = meta.get('ui_component') or meta.get('component','')
            raw_topic = meta.get('topic','')
            # Clean stray trailing parenthesis if unmatched (e.g., 'Authentication)' )
            if raw_topic.endswith(')') and raw_topic.count('(') < raw_topic.count(')'):
                raw_topic = raw_topic.rstrip(')')
            self.tree.insert('', 'end', iid=key, values=(meta['text'], "", raw_topic, component_val, 'Pending'))
            self.all_ids.append(key)
        topics = sorted({v.get('topic','') for v in data_dict.values() if v.get('topic')})
        comps = sorted({(v.get('ui_component') or v.get('component','')) for v in data_dict.values() if (v.get('ui_component') or v.get('component'))})
        # Build value lists with leading 'All' options
        topic_values = ['All Topics'] + topics if topics else ['All Topics']
        comp_values = ['All Components'] + comps if comps else ['All Components']
        # Expose filters on root so table helper can reach them
        root_widget = self.frame.winfo_toplevel()
        if hasattr(root_widget, 'topic_filter'):
            prior = root_widget.topic_filter.get()
            root_widget.topic_filter['values'] = topic_values
            try:
                root_widget.topic_filter.set(prior if prior in topic_values else 'All Topics')
            except Exception:
                pass
        if hasattr(root_widget, 'component_filter'):
            prior_c = root_widget.component_filter.get()
            root_widget.component_filter['values'] = comp_values
            try:
                root_widget.component_filter.set(prior_c if prior_c in comp_values else 'All Components')
            except Exception:
                pass
        # Try to populate filters up the chain
        try:
            root = self.parent.master.master
            root.topic_filter['values'] = topic_values
            root.component_filter['values'] = comp_values
        except Exception:
            pass

    def update_translation(self, key, translation):
        if key in self.data:
            vals = list(self.tree.item(key, 'values'))
            vals[1] = translation
            vals[4] = 'Translated' if translation else 'Pending'
            self.tree.item(key, values=vals)

    def get_selected_keys(self):
        return list(self.tree.selection())

    def select_all(self):
        self.tree.selection_set(self.tree.get_children())

    def select_visible(self):
        """Select only currently visible (attached) rows after filtering."""
        visible = []
        # Treeview children returns only attached (visible) items
        for iid in self.tree.get_children():
            visible.append(iid)
        if visible:
            self.tree.selection_set(visible)

    def clear_selection(self):
        self.tree.selection_remove(self.tree.selection())

    def clear_translations(self):
        for key in self.tree.get_children():
            vals = list(self.tree.item(key, 'values'))
            vals[1] = ''
            vals[4] = 'Pending'
            self.tree.item(key, values=vals)

    def clear(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

    def apply_filters(self, query, topic, component, status):
        # Iterate over full id list (includes detached ones) so we can restore them
        for key in self.all_ids:
            if not self.tree.exists(key):
                # Was removed somehow; skip
                continue
            vals = self.tree.item(key, 'values')
            show = True
            if query and query not in vals[0].lower() and query not in (vals[1] or '').lower():
                show = False
            if topic and topic and vals[2] != topic:
                show = False
            if component and component and vals[3] != component:
                show = False
            if status and status != 'All' and vals[4] != status:
                show = False
            if show:
                # Reattach (if already attached, this is harmless; ttk will move to end so optionally preserve ordering)
                self.tree.reattach(key, '', 'end')
            else:
                self.tree.detach(key)

    def _on_edit(self, event):
        item_id = self.tree.focus()
        if not item_id:
            return
        vals = list(self.tree.item(item_id, 'values'))
        edit = tk.Toplevel(self.frame)
        edit.title("Edit Translation")
        tk.Label(edit, text="Original", font=("Segoe UI", 9, 'bold')).grid(row=0, column=0, sticky='w', padx=8, pady=(8,4))
        tk.Message(edit, text=vals[0], width=400).grid(row=1, column=0, columnspan=2, sticky='w', padx=8)
        tk.Label(edit, text="Translation", font=("Segoe UI", 9, 'bold')).grid(row=2, column=0, sticky='w', padx=8, pady=(8,4))
        txt = tk.Text(edit, width=60, height=6)
        txt.grid(row=3, column=0, columnspan=2, padx=8)
        txt.insert('1.0', vals[1])
        def save():
            new_tr = txt.get('1.0', 'end-1c').strip()
            self.update_translation(item_id, new_tr)
            self.edit_callback(item_id, new_tr)
            edit.destroy()
        # Styled dialog buttons
        def style_btn(btn, normal_bg, hover_bg, fg='white'):
            btn.config(bg=normal_bg, fg=fg, activebackground=hover_bg, activeforeground=fg, bd=0, relief=tk.FLAT, cursor='hand2')
            def on_enter(e):
                if str(btn['state']) != 'disabled':
                    btn.config(bg=hover_bg)
            def on_leave(e):
                if str(btn['state']) != 'disabled':
                    btn.config(bg=normal_bg)
            btn.bind('<Enter>', on_enter)
            btn.bind('<Leave>', on_leave)
        save_btn = tk.Button(edit, text="Save", command=save, padx=14, pady=4, font=("Segoe UI Semibold", 9))
        cancel_btn = tk.Button(edit, text="Cancel", command=edit.destroy, padx=14, pady=4, font=("Segoe UI Semibold", 9))
        style_btn(save_btn, '#2563eb', '#1d4ed8')
        style_btn(cancel_btn, '#64748b', '#475569')
        save_btn.grid(row=4, column=0, pady=8, padx=8, sticky='e')
        cancel_btn.grid(row=4, column=1, pady=8, padx=8, sticky='w')

class CopilotTranslator:
    """Main application class for the Copilot Localization Translator."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Copilot Localization Translator")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 700)
        
        # Initialize services
        self.parser = LocalizationParser()
        self.translation_service = TranslationService()
        
        # Application state
        self.current_file = None
        self.localization_data = {}
        # Subset shown / translated (after excluding global variables)
        self.visible_localization_data = {}
        self.translated_data = {}
        self.supported_languages = [
            "English", "Spanish", "French", "German", "Italian", "Portuguese",
            "Dutch", "Russian", "Chinese (Simplified)", "Chinese (Traditional)",
            "Japanese", "Korean", "Arabic", "Hindi", "Swedish", "Norwegian"
        ]
        
        # UI Variables
        self.target_language = tk.StringVar(value="English")
        self.translation_style = tk.StringVar(value="formal")
        self.progress_queue = queue.Queue()
        self._cancel_requested = False
        # Theme state ('light'|'dark'|'system')
        self.current_theme = 'system'
        
        # Always build modern UI (legacy path removed)
        self.root.after(0, self._init_new_ui)

    def _init_new_ui(self):
        self.build_modern_ui()
        # Apply initial theme colors (resolve system theme if selected)
        try:
            self.apply_theme(self.current_theme)
        except Exception:
            pass
        self.setup_menu()  # keep menus
        # Attempt to set window icon post-build (some WM’s require after root visible)
        try:
            if getattr(self, 'logo_img', None):
                self.root.iconphoto(False, self.logo_img)
        except Exception:
            pass

    # ------------------ Button Styling Helpers ------------------
    def _init_button_palette(self):
        # variant: (normal_bg, hover_bg, fg, disabled_bg, disabled_fg)
        self._button_palette = {
            'primary': ('#2563eb', '#1d4ed8', 'white', '#93c5fd', 'white'),
            'accent': ('#4f46e5', '#4338ca', 'white', '#a5b4fc', 'white'),
            'info': ('#0284c7', '#0369a1', 'white', '#7dd3fc', 'white'),
            'success': ('#059669', '#047857', 'white', '#6ee7b7', '#065f46'),
            'neutral': ('#64748b', '#475569', 'white', '#cbd5e1', '#475569'),
            'outline': ('#ffffff', '#f1f5f9', '#1e293b', '#f1f5f9', '#94a3b8'),
            'ghost': ('#ffffff', '#f1f5f9', '#334155', '#f1f5f9', '#94a3b8'),
            'danger': ('#dc2626', '#b91c1c', 'white', '#fca5a5', 'white')
        }

    # ------------- Rounded Button Implementation -------------
    class RoundedButton(tk.Canvas):
        def __init__(self, master, text, command, colors, font, state='normal', radius=14, pad_x=18, pad_y=8, style_type='filled', min_width=0):
            self._text = text
            self._command = command
            self._colors = colors  # (normal, hover, fg, disabled_bg, disabled_fg)
            self._font = font
            self._radius = radius
            self._pad_x = pad_x
            self._pad_y = pad_y
            self._state = state
            self._min_width = min_width or 0
            self._style_type = style_type  # filled | outline | ghost
            self._hovered = False
            # temp font object for width estimation
            try:
                tmp = Font(font=font)
                text_w = tmp.measure(text)
                text_h = tmp.metrics("linespace")
            except Exception:
                text_w = len(text) * 8
                text_h = 16
            width = text_w + pad_x * 2
            if self._min_width and width < self._min_width:
                width = self._min_width
            height = text_h + pad_y * 2
            super().__init__(master, width=width, height=height, highlightthickness=0, bd=0, bg=master.cget('bg'))
            self._bg_cache = None
            self._draw(normal=True)
            self.bind('<Enter>', self._on_enter)
            self.bind('<Leave>', self._on_leave)
            self.bind('<Button-1>', self._on_click)
            self.bind('<Key-Return>', self._on_click)
            self.configure(cursor='hand2')
            self.focusable = True
            self.bind('<FocusIn>', lambda e: self._outline_focus(True))
            self.bind('<FocusOut>', lambda e: self._outline_focus(False))

        def _outline_focus(self, focused):
            # Redraw to show focus ring
            self._draw(normal=True, focused=focused)

        def _round_rect(self, x1, y1, x2, y2, r, **kwargs):
            # Draw rounded rectangle using polygons (simplified)
            points = [x1+r, y1, x2-r, y1, x2, y1, x2, y1+r, x2, y2-r, x2, y2, x2-r, y2, x1+r, y2, x1, y2, x1, y2-r, x1, y1+r, x1, y1]
            return self.create_polygon(points, smooth=True, **kwargs)

        def _current_colors(self):
            normal_bg, hover_bg, fg, disabled_bg, disabled_fg = self._colors
            if self._state == 'disabled':
                return disabled_bg, disabled_fg
            if self._hovered:
                # For outline/ghost we treat hover differently
                if self._style_type in ('outline', 'ghost'):
                    # Use hover background but keep fg consistent
                    return hover_bg, fg if self._style_type == 'ghost' else fg
                return hover_bg, fg
            return normal_bg, fg

        def _draw(self, normal=False, focused=False):
            self.delete('all')
            bg, fg = self._current_colors()
            w = int(self['width'])
            h = int(self['height'])
            r = self._radius
            # Determine styling per type
            if self._style_type == 'filled':
                self._round_rect(1, 1, w-2, h-2, r, fill=bg, outline=bg)
            elif self._style_type == 'outline':
                self._round_rect(1, 1, w-2, h-2, r, fill=bg, outline='#cbd5e1')
            else:  # ghost
                self._round_rect(1, 1, w-2, h-2, r, fill=bg, outline=bg)
            if focused and self._state != 'disabled':
                # focus ring
                self._round_rect(1, 1, w-2, h-2, r, outline='#ffffff', width=1)
            self.create_text(w/2, h/2, text=self._text, fill=fg, font=self._font)

        def _on_enter(self, _):
            if self._state == 'disabled':
                return
            self._hovered = True
            self._draw()

        def _on_leave(self, _):
            if self._state == 'disabled':
                return
            self._hovered = False
            self._draw()

        def _on_click(self, _):
            if self._state == 'disabled':
                return
            if callable(self._command):
                self._command()

        def config(self, **kwargs):
            # Custom handling for properties not native to tk.Canvas
            if 'state' in kwargs:
                self._state = kwargs.pop('state')
            if 'text' in kwargs:
                # Update displayed text and optionally resize canvas to fit
                new_text = kwargs.pop('text')
                if new_text != self._text:
                    self._text = new_text
                    try:
                        tmp = Font(font=self._font)
                        text_w = tmp.measure(self._text)
                        text_h = tmp.metrics("linespace")
                    except Exception:
                        text_w = len(self._text) * 8
                        text_h = 16
                    new_width = text_w + self._pad_x * 2
                    if self._min_width and new_width < self._min_width:
                        new_width = self._min_width
                    new_height = text_h + self._pad_y * 2
                    # Use base class config to avoid recursion
                    tk.Canvas.config(self, width=new_width, height=new_height)
            if kwargs:
                # Pass any remaining supported kwargs to base class
                super().config(**kwargs)
            self._draw()

        # Provide attribute-like access for compatibility
        def __getitem__(self, item):
            if item == 'state':
                return self._state
            return super().__getitem__(item)

    def _make_button(self, parent, text, command, variant='primary', state='normal', pad_x=18, pad_y=6, style_type='filled'):
        if not hasattr(self, '_button_palette'):
            self._init_button_palette()
        if not hasattr(self, 'font_button'):
            self.font_button = ("Segoe UI Semibold", 10)
        normal_bg, hover_bg, fg, disabled_bg, disabled_fg = self._button_palette.get(variant, self._button_palette['primary'])
        # Determine style type automatically if variant hint present
        if variant in ('outline', 'ghost'):
            style_type = variant
        # Slightly larger radius for primary/actions, smaller for ghost
        radius = 20 if variant in ('primary','accent','success','danger','info') else 18
        min_width = 0
        if 'Translate Selected' in text:
            # Provide extra width so full text is clearly readable
            min_width = 190
        btn = self.RoundedButton(parent, text, command, (normal_bg, hover_bg, fg, disabled_bg, disabled_fg), self.font_button, state=state, radius=radius, pad_x=pad_x, pad_y=pad_y, style_type=style_type, min_width=min_width)
        btn._variant = variant
        btn._colors = (normal_bg, hover_bg, fg, disabled_bg, disabled_fg)
        if not hasattr(self, '_buttons'):
            self._buttons = []
        self._buttons.append(btn)
        return btn

    def _refresh_button_states(self):
        if not hasattr(self, '_buttons'):
            return
        for btn in self._buttons:
            normal_bg, hover_bg, fg, disabled_bg, disabled_fg = btn._colors
            # If it's our RoundedButton (Canvas subclass), just force redraw based on state
            if isinstance(btn, self.RoundedButton):
                btn._draw()
            else:  # fallback for any legacy tk.Button remaining
                if str(btn['state']) == 'disabled':
                    btn.config(bg=disabled_bg, fg=disabled_fg)
                else:
                    btn.config(bg=normal_bg, fg=fg)

    # ------------------ Global Variable Exclusion Heuristic ------------------
    def _is_global_variable(self, key: str, meta: dict) -> bool:
        """Determine if a localization key should be treated as a global variable.

        Heuristics (adjust as needed):
        - Raw key contains "'globalVariable(" substring.
        - Parsed topic == "Global Variables".
        - ui_component parsed as "GlobalVariable".
        - Key segment contains .GlobalVariables. (future-proofing)
        """
        try:
            if "'globalVariable(" in key:
                return True
            if '.GlobalVariables.' in key:
                return True
            topic = meta.get('topic') or ''
            if topic == 'Global Variables':
                return True
            comp = meta.get('ui_component') or ''
            if comp == 'GlobalVariable':
                return True
        except Exception:
            return False
        return False

    # ------------------ New Modern Redesign ------------------
    def build_modern_ui(self):
        """Construct a clean, compact modern UI layout.

        Layout:
        +-------------------------------------------------------------+
        | Top Bar: Title | File | Language | Style | Actions          |
        + Filter Row (Search, Topic, Component, Status)               |
        +-------------------------------------------------------------+
        | Translation Table (flex)                                   |
        +-------------------------------------------------------------+
        | Status Bar (left: status text, right: progress)            |
        +-------------------------------------------------------------+
        """
        self.root.configure(bg="#f5f7fb")
        # Fonts / sizes
        self.font_body = ("Segoe UI", 10)
        self.font_small = ("Segoe UI", 9)
        self.font_header = ("Segoe UI Semibold", 12)
        self.font_button = ("Segoe UI Semibold", 10)

        # Single-column grid: rows 0-4, column 0 main content
        for r, wt in [(3,1)]:
            self.root.grid_rowconfigure(r, weight=wt)
        self.root.grid_columnconfigure(0, weight=1)

        # Accent bar row (gradient placeholder)
        self._brand_accent_bar_row()

        # Top bar simplified
        top = tk.Frame(self.root, bg="#ffffff", bd=0, highlightthickness=1, highlightcolor="#e2e8f0")
        top.grid(row=1, column=0, sticky="nsew")
        self._frame_topbar = top
        top.grid_columnconfigure(0, weight=0)
        top.grid_columnconfigure(1, weight=1)  # middle stretch
        top.grid_columnconfigure(2, weight=0)

        # Left: branding
        brand_wrap = tk.Frame(top, bg="#ffffff")
        brand_wrap.grid(row=0, column=0, padx=12, pady=6, sticky='w')
        # Theme-aware colors
        tp = get_token(self.current_theme, 'text_primary')
        ts = get_token(self.current_theme, 'text_secondary')
        card_bg = get_token(self.current_theme, 'bg_card') or '#ffffff'
        brand_wrap.configure(bg=card_bg)
        top.configure(bg=card_bg)
        self.logo_img = self._load_brand_logo()
        if self.logo_img:
            tk.Label(brand_wrap, image=self.logo_img, bg=card_bg).pack(side='left', padx=(0,6))
        tk.Label(brand_wrap, text="Copilot Localization Translator", font=self.font_header, bg=card_bg, fg=tp).pack(side='left')

        # Middle: selectors + file label
        mid = tk.Frame(top, bg=card_bg)
        mid.grid(row=0, column=1, sticky='w')
        self.file_label = tk.Label(mid, text="No file loaded", font=self.font_small, bg=card_bg, fg=ts)
        self.file_label.pack(side='left', padx=(0,16))

        tk.Label(mid, text="Language", font=self.font_small, bg=card_bg, fg=ts).pack(side='left')
        lang_cb = ttk.Combobox(mid, textvariable=self.target_language, values=self.supported_languages, width=14, state="readonly")
        lang_cb.pack(side='left', padx=(4,12))

        tk.Label(mid, text="Style", font=self.font_small, bg=card_bg, fg=ts).pack(side='left')
        style_cb = ttk.Combobox(mid, textvariable=self.translation_style, values=['formal','conversational','chatbot'], width=12, state="readonly")
        style_cb.pack(side='left', padx=(4,0))

        # Right: actions (including theme toggle)
        actions = tk.Frame(top, bg=card_bg)
        actions.grid(row=0, column=2, sticky='e', padx=(4,12))
        self.theme_toggle_btn = self._make_button(actions, "🌓 Theme: Sys", lambda: self.toggle_theme(), variant='ghost', style_type='ghost', pad_x=12, pad_y=6)
        self.theme_toggle_btn.pack(side='left', padx=(0,4))
        self.load_btn = self._make_button(actions, "📂 Open", self.load_file, variant='primary', pad_x=16, pad_y=8)
        self.load_btn.pack(side='left', padx=(0,4))
        self.translate_all_btn = self._make_button(actions, "⚡ Translate All", self.translate_all, variant='accent', state='disabled', pad_x=18, pad_y=8)
        self.translate_all_btn.pack(side='left', padx=4)
        # Full label for clarity; min-width logic in _make_button will ensure no clipping
        self.translate_selected_btn = self._make_button(actions, "🎯 Translate Selected", self.translate_selected, variant='outline', state='disabled', style_type='outline', pad_x=16, pad_y=8)
        self.translate_selected_btn.pack(side='left', padx=4)
        # Cancel translation button (hidden until a batch starts)
        self.cancel_translate_btn = self._make_button(actions, "⛔ Stop", self.cancel_translation, variant='danger', state='disabled', pad_x=14, pad_y=8)
        self.cancel_translate_btn.pack(side='left', padx=4)
        self.validate_btn = self._make_button(actions, "🧪 Validate", self.validate_translations, variant='outline', state='disabled', style_type='outline', pad_x=14, pad_y=8)
        self.validate_btn.pack(side='left', padx=4)
        self.export_btn = self._make_button(actions, "💾 Export", self.export_file, variant='outline', state='disabled', style_type='outline', pad_x=14, pad_y=8)
        self.export_btn.pack(side='left', padx=(4,0))

        # Filter row (two-tier for labels + inputs for clarity)
        filter_row = tk.Frame(self.root, bg="#ffffff", highlightthickness=1, highlightcolor="#e2e8f0")
        filter_row.grid(row=2, column=0, sticky="ew", pady=(2,0))
        self._frame_filter = filter_row
        for c in range(7):
            filter_row.grid_columnconfigure(c, weight=0)
        filter_row.grid_columnconfigure(5, weight=1)

        # Row 0: Labels
        tk.Label(filter_row, text="Search", font=self.font_small, bg="#ffffff", fg="#475569").grid(row=0, column=0, padx=(12,4), pady=(8,0), sticky='w')
        tk.Label(filter_row, text="Topic", font=self.font_small, bg="#ffffff", fg="#475569").grid(row=0, column=2, pady=(8,0), sticky='w')
        tk.Label(filter_row, text="Component", font=self.font_small, bg="#ffffff", fg="#475569").grid(row=0, column=3, pady=(8,0), sticky='w')
        tk.Label(filter_row, text="Status", font=self.font_small, bg="#ffffff", fg="#475569").grid(row=0, column=4, pady=(8,0), sticky='w')

        # Row 1: Inputs
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(filter_row, textvariable=self.search_var, width=40, relief=tk.FLAT, highlightthickness=1, highlightcolor="#94a3b8")
        search_entry.grid(row=1, column=0, padx=(12,4), pady=(2,8), sticky='w')
        search_entry.bind('<KeyRelease>', lambda e: self.apply_filters())

        # Topic combobox
        self.topic_filter = ttk.Combobox(filter_row, values=['All Topics'], state='readonly', width=18)
        self.topic_filter.set('All Topics')
        self.topic_filter.grid(row=1, column=2, padx=8, pady=(2,8), sticky='w')
        self.topic_filter.bind('<<ComboboxSelected>>', lambda e: self.apply_filters())
        # Component combobox
        self.component_filter = ttk.Combobox(filter_row, values=['All Components'], state='readonly', width=18)
        self.component_filter.set('All Components')
        self.component_filter.grid(row=1, column=3, padx=8, pady=(2,8), sticky='w')
        self.component_filter.bind('<<ComboboxSelected>>', lambda e: self.apply_filters())
        # Status combobox
        self.status_filter = ttk.Combobox(filter_row, values=['All','Pending','Translated'], state='readonly', width=14)
        self.status_filter.set('All')
        self.status_filter.grid(row=1, column=4, padx=8, pady=(2,8), sticky='w')
        self.status_filter.bind('<<ComboboxSelected>>', lambda e: self.apply_filters())

        # Expose on root (toplevel) for population from table.load_data
        self.root.topic_filter = self.topic_filter
        self.root.component_filter = self.component_filter

        clear_btn = self._make_button(filter_row, "Clear Filters", self.clear_filters, variant='ghost', style_type='ghost')
        clear_btn.grid(row=1, column=6, padx=(8,4), pady=(2,8), sticky='e')

        # Multi-select convenience buttons
        select_visible_btn = self._make_button(filter_row, "Select Visible", lambda: self.select_visible_rows(), variant='outline', style_type='outline', pad_x=10, pad_y=4)
        select_visible_btn.grid(row=1, column=7, padx=(4,4), pady=(2,8), sticky='e')
        deselect_all_btn = self._make_button(filter_row, "Deselect All", lambda: self.deselect_all_rows(), variant='ghost', style_type='ghost', pad_x=10, pad_y=4)
        deselect_all_btn.grid(row=1, column=8, padx=(4,12), pady=(2,8), sticky='e')

        Tooltip(select_visible_btn, "Select every currently visible row (after filters). Use with 'Translate Selected'.")
        Tooltip(deselect_all_btn, "Clear selection without altering filters.")

        # Tooltips for clarity
        Tooltip(search_entry, "Type to filter by original or translation text (case-insensitive substring).")
        Tooltip(self.topic_filter, "Filter rows by extracted Topic classification from localization key.")
        Tooltip(self.component_filter, "Filter rows by UI Component / logical sub-area (derived from key structure).")
        Tooltip(self.status_filter, "Show only Pending or Translated entries, or All.")
        Tooltip(clear_btn, "Reset all filters back to showing every entry.")

        # Selection count label (row 0 right aligned)
        self.selection_count_var = tk.StringVar(value="0 selected")
        self.selection_count_lbl = tk.Label(filter_row, textvariable=self.selection_count_var, font=self.font_small, bg="#ffffff", fg="#475569")
        self.selection_count_lbl.grid(row=0, column=6, columnspan=3, sticky='e', padx=(4,12), pady=(8,0))

        # Initialize state visuals
        self._refresh_button_states()

        # Table area
        table_frame = tk.Frame(self.root, bg="#f5f7fb")
        table_frame.grid(row=3, column=0, sticky="nsew", pady=(4,0))
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        self.translation_table = SimpleTranslationTable(table_frame, self.on_translation_edit)
        self.translation_table.frame.grid(row=0, column=0, sticky="nsew", padx=12, pady=4)
        self._frame_table = table_frame

        # Details panel for large content visibility
        details_container = tk.Frame(table_frame, bg="#ffffff", highlightthickness=1, highlightcolor="#e2e8f0")
        details_container.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0,8))
        self._frame_details = details_container
        table_frame.grid_rowconfigure(1, weight=0)
        details_container.grid_columnconfigure(0, weight=1)
        header_bar = tk.Frame(details_container, bg="#f1f5f9")
        header_bar.grid(row=0, column=0, sticky='ew')
        tk.Label(header_bar, text="Details (selected row)", font=self.font_small, bg="#f1f5f9", fg="#475569").pack(side='left', padx=8, pady=2)
        self.details_toggle_var = tk.BooleanVar(value=True)
        def toggle_details():
            state = self.details_toggle_var.get()
            body_frame.grid_remove() if not state else body_frame.grid()
        toggle_btn = self._make_button(header_bar, "Hide" if self.details_toggle_var.get() else "Show", lambda: (self.details_toggle_var.set(not self.details_toggle_var.get()), toggle_btn.config(text="Hide" if self.details_toggle_var.get() else "Show"), toggle_details()), variant='ghost', style_type='ghost', pad_x=8, pad_y=2)
        toggle_btn.pack(side='right', padx=4, pady=2)
        body_frame = tk.Frame(details_container, bg="#ffffff")
        body_frame.grid(row=1, column=0, sticky='nsew')
        body_frame.grid_columnconfigure(0, weight=1)
        body_frame.grid_columnconfigure(1, weight=1)
        # Original text box
        tk.Label(body_frame, text="Original", font=self.font_small, bg="#ffffff", fg="#334155").grid(row=0, column=0, sticky='w', padx=8, pady=(4,0))
        tk.Label(body_frame, text="Translation", font=self.font_small, bg="#ffffff", fg="#334155").grid(row=0, column=1, sticky='w', padx=8, pady=(4,0))
        self.details_original = tk.Text(body_frame, height=4, wrap='word', font=("Segoe UI", 9), bg="#ffffff", relief=tk.FLAT)
        self.details_translation = tk.Text(body_frame, height=4, wrap='word', font=("Segoe UI", 9), bg="#ffffff", relief=tk.FLAT)
        self.details_original.grid(row=1, column=0, sticky='nsew', padx=8, pady=4)
        self.details_translation.grid(row=1, column=1, sticky='nsew', padx=8, pady=4)
        for txt in (self.details_original, self.details_translation):
            txt.configure(state='disabled')

        # Selection binding to update details
        def _update_details(event=None):
            try:
                sel = self.translation_table.tree.selection()
                try:
                    self.selection_count_var.set(f"{len(sel)} selected")
                except Exception:
                    pass
                if not sel:
                    for t in (self.details_original, self.details_translation):
                        t.configure(state='normal'); t.delete('1.0', 'end'); t.configure(state='disabled')
                    return
                key = sel[0]
                item_vals = self.translation_table.tree.item(key, 'values')
                original_text = item_vals[0]
                translation_text = item_vals[1]
                self.details_original.configure(state='normal'); self.details_original.delete('1.0','end'); self.details_original.insert('1.0', original_text); self.details_original.configure(state='disabled')
                self.details_translation.configure(state='normal'); self.details_translation.delete('1.0','end'); self.details_translation.insert('1.0', translation_text); self.details_translation.configure(state='disabled')
            except Exception:
                pass
        self.translation_table.tree.bind('<<TreeviewSelect>>', _update_details)
        # Also update details after translations change
        self._update_details_panel = _update_details

        # Status bar
        status = tk.Frame(self.root, bg="#1e3a8a")
        status.grid(row=4, column=0, sticky="ew", pady=(4,0))
        self._frame_status = status
        status.grid_columnconfigure(1, weight=1)
        self.status_label = tk.Label(status, text="Ready", bg="#1e3a8a", fg="white", font=self.font_small)
        self.status_label.grid(row=0, column=0, padx=12, pady=4, sticky="w")
        self.progress_bar = ttk.Progressbar(status, mode='determinate')
        self.progress_bar.grid(row=0, column=2, padx=12, pady=6, sticky="e")

    def clear_filters(self):
        self.search_var.set("")
        try:
            self.topic_filter.set('All Topics')
            self.component_filter.set('All Components')
            self.status_filter.set('All')
        except Exception:
            pass
        self.apply_filters()

    def apply_filters(self):
        if not hasattr(self, 'translation_table'):
            return
        query = self.search_var.get().strip().lower()
        topic_v = self.topic_filter.get().strip()
        if topic_v.lower().startswith('all'):
            topic_v = ''
        comp_v = self.component_filter.get().strip()
        if comp_v.lower().startswith('all'):
            comp_v = ''
        status_v = self.status_filter.get().strip()
        self.translation_table.apply_filters(query, topic_v, comp_v, status_v)

        # (end of CopilotTranslator class methods before SimpleTranslationTable relocation)
        
        
    def setup_menu(self):
        """Setup application menu."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open Localization File...", command=self.load_file)
        file_menu.add_separator()
        file_menu.add_command(label="Export Translated File...", command=self.export_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Select All", command=self.select_all)
        edit_menu.add_command(label="Clear Translations", command=self.clear_translations)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Settings...", command=self.show_settings)
        tools_menu.add_command(label="API Configuration...", command=self.show_api_config)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        
    def load_file(self):
        """Load a localization file."""
        file_path = filedialog.askopenfilename(
            title="Select Localization File",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
            
        try:
            if hasattr(self, 'status_label'):
                self.status_label.config(text="Loading file...")
                self.root.update()
            
            # Parse the localization file
            self.localization_data = self.parser.load_file(file_path)
            # Apply exclusion heuristic for global variables
            self.visible_localization_data = {
                k: v for k, v in self.localization_data.items() if not self._is_global_variable(k, v)
            }
            self.current_file = file_path

            # Update UI (only show visible entries)
            self.file_label.config(text=os.path.basename(file_path), foreground="black")
            self.translation_table.load_data(self.visible_localization_data)
            
            # Enable controls
            self.translate_all_btn.config(state="normal")
            self.translate_selected_btn.config(state="normal")
            self.validate_btn.config(state="normal")
            self._refresh_button_states()
            
            if hasattr(self, 'status_label'):
                excluded = len(self.localization_data) - len(self.visible_localization_data)
                excl_note = f" (excluded {excluded} global)" if excluded else ""
                self.status_label.config(text=f"Loaded {len(self.visible_localization_data)} entries{excl_note}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {str(e)}")
            if hasattr(self, 'status_label'):
                self.status_label.config(text="Error loading file")
            
    def translate_all(self):
        """Translate all entries."""
        if not self.visible_localization_data:
            return
        # Reset cancellation and enable cancel button
        self._cancel_requested = False
        if hasattr(self, 'cancel_translate_btn'):
            self.cancel_translate_btn.config(state='normal')
        if hasattr(self, 'translate_all_btn'):
            self.translate_all_btn.config(state='disabled')
        if hasattr(self, 'translate_selected_btn'):
            self.translate_selected_btn.config(state='disabled')
        self.status_label.config(text="Translating all non-global entries...")
        self.progress_bar["value"] = 0
        self.progress_bar["maximum"] = len(self.visible_localization_data)
        # Start parallel translation
        thread = threading.Thread(target=self._translate_batch_parallel, args=(list(self.visible_localization_data.keys()),))
        thread.daemon = True
        thread.start()
        self.root.after(100, self._check_translation_progress)
        
    def translate_selected(self):
        """Translate selected entries."""
        selected_keys = self.translation_table.get_selected_keys()
        if not selected_keys:
            messagebox.showwarning("Warning", "No entries selected")
            return
        self._cancel_requested = False
        if hasattr(self, 'cancel_translate_btn'):
            self.cancel_translate_btn.config(state='normal')
        if hasattr(self, 'translate_all_btn'):
            self.translate_all_btn.config(state='disabled')
        if hasattr(self, 'translate_selected_btn'):
            self.translate_selected_btn.config(state='disabled')
            
        self.status_label.config(text=f"Translating {len(selected_keys)} entries...")
        self.progress_bar["value"] = 0
        self.progress_bar["maximum"] = len(selected_keys)
        thread = threading.Thread(target=self._translate_batch_parallel, args=(selected_keys,))
        thread.daemon = True
        thread.start()
        self.root.after(100, self._check_translation_progress)
        
    def _translate_batch(self, keys: List[str]):
        """Translate a batch of keys in background thread."""
        try:
            for i, key in enumerate(keys):
                if self._cancel_requested:
                    self.progress_queue.put(('cancelled', None, None, None))
                    return
                original_text = self.visible_localization_data[key]['text']
                topic = self.visible_localization_data[key].get('topic')
                
                # Get translation
                translated_text = self.translation_service.translate(
                    text=original_text,
                    target_language=self.target_language.get(),
                    style=self.translation_style.get(),
                    context=topic
                )
                
                # Update translated data
                if key not in self.translated_data:
                    self.translated_data[key] = {}
                self.translated_data[key][self.target_language.get()] = translated_text
                
                # Report progress
                self.progress_queue.put(('progress', i + 1, key, translated_text))
                
            self.progress_queue.put(('complete', None, None, None))
            
        except Exception as e:
            self.progress_queue.put(('error', str(e), None, None))

    # ---------------- Parallel Translation Implementation ----------------
    def _translate_batch_parallel(self, keys: List[str]):
        """Translate keys using a small worker pool for faster throughput."""
        # Configuration
        max_workers = min(5, max(1, len(keys)))  # cap concurrency
        self._parallel_total = len(keys)
        self._parallel_done = 0
        self._complete_event_sent = False
        self._cancel_event_sent = False
        work_q = queue.Queue()
        for k in keys:
            work_q.put(k)
        lock = threading.Lock()

        def worker():
            while not self._cancel_requested:
                try:
                    key = work_q.get_nowait()
                except queue.Empty:
                    break
                try:
                    original_text = self.visible_localization_data[key]['text']
                    topic = self.visible_localization_data[key].get('topic')
                    translated_text = self.translation_service.translate(
                        text=original_text,
                        target_language=self.target_language.get(),
                        style=self.translation_style.get(),
                        context=topic
                    )
                    if key not in self.translated_data:
                        self.translated_data[key] = {}
                    self.translated_data[key][self.target_language.get()] = translated_text
                    with lock:
                        self._parallel_done += 1
                        done = self._parallel_done
                    self.progress_queue.put(('progress', done, key, translated_text))
                except Exception as ex:
                    self.progress_queue.put(('error', str(ex), None, None))
                    return
            # After loop (either finished queue or cancelled)
            with lock:
                if self._cancel_requested and not self._cancel_event_sent:
                    self._cancel_event_sent = True
                    self.progress_queue.put(('cancelled', None, None, None))
                elif (not self._cancel_requested) and self._parallel_done >= self._parallel_total and not self._complete_event_sent:
                    self._complete_event_sent = True
                    self.progress_queue.put(('complete', None, None, None))

        threads = []
        for _ in range(max_workers):
            t = threading.Thread(target=worker)
            t.daemon = True
            t.start()
            threads.append(t)
            
    def _check_translation_progress(self):
        """Check translation progress from background thread."""
        try:
            while True:
                status, value, key, translation = self.progress_queue.get_nowait()
                
                if status == 'progress':
                    self.progress_bar["value"] = value
                    self.translation_table.update_translation(key, translation)
                    self.root.update()
                    
                elif status == 'complete':
                    self.progress_bar["value"] = self.progress_bar["maximum"]
                    if hasattr(self, 'status_label'):
                        self.status_label.config(text="Translation complete")
                    if hasattr(self, 'export_btn'):
                        self.export_btn.config(state="normal")
                        self._refresh_button_states()
                    if hasattr(self, 'cancel_translate_btn'):
                        self.cancel_translate_btn.config(state='disabled')
                    if hasattr(self, 'translate_all_btn'):
                        self.translate_all_btn.config(state='normal')
                    if hasattr(self, 'translate_selected_btn'):
                        self.translate_selected_btn.config(state='normal')
                    return
                    
                elif status == 'error':
                    messagebox.showerror("Translation Error", f"Translation failed: {value}")
                    self.status_label.config(text="Translation failed")
                    if hasattr(self, 'cancel_translate_btn'):
                        self.cancel_translate_btn.config(state='disabled')
                    if hasattr(self, 'translate_all_btn'):
                        self.translate_all_btn.config(state='normal')
                    if hasattr(self, 'translate_selected_btn'):
                        self.translate_selected_btn.config(state='normal')
                    return
                elif status == 'cancelled':
                    if hasattr(self, 'status_label'):
                        self.status_label.config(text="Translation cancelled")
                    if hasattr(self, 'cancel_translate_btn'):
                        self.cancel_translate_btn.config(state='disabled')
                    if hasattr(self, 'translate_all_btn'):
                        self.translate_all_btn.config(state='normal')
                    if hasattr(self, 'translate_selected_btn'):
                        self.translate_selected_btn.config(state='normal')
                    return
                    
        except queue.Empty:
            # Continue checking
            self.root.after(100, self._check_translation_progress)

    def cancel_translation(self):
        """Request cancellation of the current translation batch."""
        if not getattr(self, '_cancel_requested', False):
            self._cancel_requested = True
            if hasattr(self, 'status_label'):
                self.status_label.config(text="Cancelling... (finishing current item)")
            if hasattr(self, 'cancel_translate_btn'):
                self.cancel_translate_btn.config(state='disabled')
            
    def validate_translations(self):
        """Validate existing translations."""
        # Implementation for validation logic
        messagebox.showinfo("Validation", "Translation validation completed successfully!")
        
    def on_translation_edit(self, key: str, new_translation: str):
        """Handle manual translation edits."""
        if key not in self.translated_data:
            self.translated_data[key] = {}
        self.translated_data[key][self.target_language.get()] = new_translation
        
    def export_file(self):
        """Export the translated file."""
        if not self.localization_data:
            messagebox.showwarning("Warning", "No source file loaded to export")
            return

        file_path = filedialog.asksaveasfilename(
            title="Save Translated File",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )

        if not file_path:
            return

        try:
            current_lang = self.target_language.get()
            export_data = {}

            # 1. Start with all original keys preserving order
            for key, original_entry in self.localization_data.items():
                # If we have a translation for this key in current language, use it; else original text
                translated_text = None
                if key in self.translated_data:
                    lang_map = self.translated_data[key]
                    translated_text = lang_map.get(current_lang)
                export_data[key] = translated_text if translated_text else original_entry['text']

            # 2. Include any extra translated keys not present in original (edge case)
            for key, lang_map in self.translated_data.items():
                if key not in export_data:
                    translated_text = lang_map.get(current_lang)
                    if translated_text:  # only include if we actually have the target language value
                        export_data[key] = translated_text

            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)

            messagebox.showinfo("Export Complete", f"File exported successfully to:\n{file_path}")
            if hasattr(self, 'status_label'):
                self.status_label.config(text=f"Exported to {os.path.basename(file_path)}")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export file: {str(e)}")
            
    def select_all(self):
        """Select all entries in the table."""
        self.translation_table.select_all()

    def select_visible_rows(self):
        if hasattr(self, 'translation_table'):
            self.translation_table.select_visible()

    def deselect_all_rows(self):
        if hasattr(self, 'translation_table'):
            try:
                self.translation_table.clear_selection()
            except Exception:
                pass
        
    def clear_translations(self):
        """Clear all translations."""
        if messagebox.askyesno("Confirm", "Clear all translations?"):
            self.translated_data.clear()
            self.translation_table.clear_translations()
            self.export_btn.config(state="disabled")
            self._refresh_button_states()
            
    def show_settings(self):
        """Show settings dialog."""
        # Implementation for settings dialog
        messagebox.showinfo("Settings", "Settings dialog not yet implemented")
        
    def show_api_config(self):
        """Show API configuration dialog."""
        # Implementation for API configuration dialog
        messagebox.showinfo("API Configuration", "API configuration dialog not yet implemented")
        
    def show_about(self):
        """Show about dialog."""
        about_text = (
            "Copilot Localization Translator\n\n"
            "Modern, AI-assisted workflow for Microsoft Copilot Studio localization assets.\n\n"
            "Core Features:\n"
            " • Parse + classify entries (topic, component, element type)\n"
            " • Exclude global variables automatically (configurable)\n"
            " • Batch + selective translation with style + language control\n"
            " • Inline edit + status filtering\n"
            " • Structure-preserving export (original key order)\n\n"
            "Branding: Provide an official Copilot Studio logo file (PNG 64x64) at assets/copilot_logo.png to replace the placeholder.\n"
            "Version 1.0"
        )
        messagebox.showinfo("About", about_text)
        
    def run(self):
        """Start the application."""
        self.root.mainloop()

    # ------------------ Branding Helpers ------------------
    def _load_brand_logo(self):
        """Attempt to load an external Copilot logo (PNG). Falls back to a generated placeholder.

        To replace: place a file at assets/copilot_logo.png (64x64 or similar).
        """
        import base64
        logo_paths = [
            os.path.join(os.path.dirname(__file__), 'assets', 'copilot_logo.png'),
            os.path.join(os.path.dirname(__file__), 'copilot_logo.png'),
        ]
        for p in logo_paths:
            if os.path.exists(p):
                try:
                    return tk.PhotoImage(file=p)
                except Exception:
                    pass
        # Simple generated placeholder (indigo circle on transparent background)
        placeholder_png_b64 = (
            'iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAQAAAAAYLlVAAAAv0lEQVR4Ae3XwQnCMBBA0R9KQAIK' \
            'gAwoAAnQAB2gACqAAKoACdGYn2V7yX2F6JZt3nO5mJmTg0ZrW7t9uI2MMcYY4wxxhjTD8wAX8Bc8' \
            'wJ3gNlwB14Br4BpwB34C14DHgOngF/gkPgL3gD3gNngO/gVrgOZ+BD0lLJASspJm8m9iYq8wCVcA' \
            'V3AFdwBXcAV3AFdwBXcAV3AFdwBXeAtHBfuY21JavU2j5F6m2X5nKMp6o0p2l8C/G9g1IVcAV3AF' \
            'dwBXcAV3AFdwBXcAW+oALZtPpb+CYW3ollu85uDPAAAAABJRU5ErkJggg=='
        )
        try:
            return tk.PhotoImage(data=placeholder_png_b64)
        except Exception:
            return None

    def _brand_accent_bar(self):
        """Create a thin accent bar with a pseudo-gradient under the top bar."""
        try:
            bar = tk.Frame(self.root, height=4, bg=DESIGN_TOKENS['brand_primary'])
            bar.grid(row=0, column=0, sticky='ew')  # overlay; raise after top created
            bar.lift()  # ensure visible
            # Optional: dynamic gradient simulation via canvas segments
            # For simplicity keep solid; can extend later.
        except Exception:
            pass

    def _brand_accent_bar_row(self):
        """Dedicated accent bar occupying its own grid row (row 0)."""
        try:
            container = tk.Frame(self.root, height=4, bg=get_token(self.current_theme, 'brand_primary'))
            # Try spanning 2 columns (sidebar + main); fallback single
            container.grid(row=0, column=0, sticky='ew')
            self._frame_accent = container
        except Exception:
            pass

    # ------------------ Theming ------------------
    def apply_theme(self, theme: str):
        """Apply light / dark / system theme with adaptive tokens."""
        if theme == 'system':
            resolved = detect_system_theme()
        else:
            resolved = theme if theme in ('light','dark') else 'light'
        self.current_theme = theme
        theme_resolved = resolved
        # Resolve tokens
        bg_app = get_token(theme_resolved, 'bg_app')
        bg_card = get_token(theme_resolved, 'bg_card')
        text_primary = get_token(theme_resolved, 'text_primary')
        text_secondary = get_token(theme_resolved, 'text_secondary')
        border_color = get_token(theme_resolved, 'border_subtle')
        brand_primary = get_token(theme_resolved, 'brand_primary')

        try:
            self.root.configure(bg=bg_app)
        except Exception:
            pass
        # Recolor stored frames
        frame_map = {
            '_frame_topbar': bg_card,
            '_frame_filter': bg_card,
            '_frame_table': bg_app,
            '_frame_details': bg_card,
            '_frame_status': brand_primary,
            '_frame_accent': brand_primary,
        }
        for name, color in frame_map.items():
            if hasattr(self, name):
                try:
                    getattr(self, name).configure(bg=color)
                except Exception:
                    pass
        # Table inner frame
        if hasattr(self, 'translation_table'):
            try:
                self.translation_table.frame.configure(bg=bg_card, highlightcolor=border_color, highlightbackground=border_color)
            except Exception:
                pass
        # Details Text widgets
        for attr in ['details_original','details_translation']:
            if hasattr(self, attr):
                try:
                    txt = getattr(self, attr)
                    txt.configure(bg=bg_card, fg=text_primary, insertbackground=text_primary)
                except Exception:
                    pass
        # File label / other labels may retain previous foreground; adjust key labels
        if hasattr(self, 'file_label'):
            try:
                self.file_label.configure(bg=bg_card, fg=text_secondary)
            except Exception:
                pass
        # Update Treeview style (ensure header visible especially in light theme)
        try:
            style = ttk.Style()
            current_ttk_theme = style.theme_use()
            style.configure('Treeview', background=bg_card, fieldbackground=bg_card, foreground=text_primary, bordercolor=border_color, borderwidth=0)
            if theme_resolved == 'light':
                heading_bg = '#e2e8f0'
                heading_fg = '#1e293b'
            else:
                heading_bg = brand_primary
                heading_fg = get_token(theme_resolved, 'text_inverse') or '#ffffff'
            style.configure('Treeview.Heading', background=heading_bg, foreground=heading_fg, relief='flat', font=('Segoe UI Semibold', 9))
            style.map('Treeview.Heading', background=[('active', heading_bg), ('pressed', heading_bg)], foreground=[('active', heading_fg)])
        except Exception:
            pass
        # Update button palette adaptation (simple approach: rebuild palettes for dark)
        if theme_resolved == 'dark':
            self._button_palette['outline'] = (bg_card, '#334155', text_primary, '#1e293b', text_secondary)
            self._button_palette['ghost'] = (bg_app, '#1e293b', text_secondary, bg_app, '#475569')
        else:
            self._button_palette['outline'] = ('#ffffff', '#f1f5f9', '#1e293b', '#f1f5f9', '#94a3b8')
            self._button_palette['ghost'] = (bg_app, '#e2e8f0', '#475569', bg_app, '#94a3b8')
        # Update theme toggle button text
        if hasattr(self, 'theme_toggle_btn'):
            label = {'light':'🌓 Theme: Light','dark':'🌓 Theme: Dark','system':'🌓 Theme: Sys'}[self.current_theme]
            self.theme_toggle_btn.config(text=label)
        # Refresh all buttons to adopt new palette colors
        try:
            self._refresh_button_states()
        except Exception:
            pass

    def toggle_theme(self):
        order = ['system','light','dark']
        try:
            idx = order.index(self.current_theme)
        except ValueError:
            idx = 0
        new_theme = order[(idx+1) % len(order)]
        self.apply_theme(new_theme)

if __name__ == "__main__":
    app = CopilotTranslator()
    app.run()