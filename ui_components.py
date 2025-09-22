"""
UI Components Module
Modern UI components for the Copilot Localization Translator application.
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, font
from typing import Dict, List, Callable, Optional, Any
import threading

class ModernStyle:
    """Advanced modern UI styling constants inspired by contemporary design."""
    
    # Primary Color Palette (inspired by reference UI)
    PRIMARY_BLUE = "#2563eb"      # Modern bright blue
    PRIMARY_PURPLE = "#7c3aed"    # Vibrant purple
    ACCENT_CYAN = "#06b6d4"       # Bright cyan
    ACCENT_GREEN = "#10b981"      # Success green
    ACCENT_ORANGE = "#f59e0b"     # Warning orange
    ACCENT_RED = "#ef4444"        # Error red
    ACCENT_PINK = "#ec4899"       # Pink accent
    ACCENT_TEAL = "#14b8a6"       # Teal accent
    
    # Background Colors (sophisticated gradients)
    BG_GRADIENT_START = "#f8fafc"  # Very light blue-gray
    BG_GRADIENT_END = "#e2e8f0"    # Light blue-gray
    BG_DARK = "#1e293b"           # Dark slate
    BG_LIGHT = "#f8fafc"          # Ultra light
    BG_CARD = "#ffffff"           # Pure white cards
    BG_SECONDARY = "#f1f5f9"      # Light secondary
    BG_SIDEBAR = "#1e40af"        # Deep blue sidebar
    
    # Text Colors (refined hierarchy)
    TEXT_PRIMARY = "#0f172a"      # Almost black
    TEXT_SECONDARY = "#64748b"    # Medium gray
    TEXT_WHITE = "#ffffff"        # Pure white
    TEXT_MUTED = "#94a3b8"        # Light gray
    TEXT_ACCENT = "#3b82f6"       # Blue accent text
    
    # Border & Shadow Colors (tkinter compatible)
    BORDER_LIGHT = "#e2e8f0"      # Very light border
    BORDER_MEDIUM = "#cbd5e1"     # Medium border
    BORDER_FOCUS = "#3b82f6"      # Focus blue
    SHADOW_LIGHT = "#f1f5f9"      # Very light shadow substitute
    SHADOW_MEDIUM = "#e2e8f0"     # Medium shadow substitute
    
    # Status Colors (refined)
    STATUS_SUCCESS = "#dcfce7"    # Light green
    STATUS_WARNING = "#fef3c7"    # Light yellow
    STATUS_ERROR = "#fee2e2"      # Light red
    STATUS_INFO = "#dbeafe"       # Light blue
    
    # Category Colors (like reference UI)
    CATEGORY_PURPLE = "#8b5cf6"   # Purple category
    CATEGORY_TEAL = "#14b8a6"     # Teal category
    CATEGORY_PINK = "#ec4899"     # Pink category
    CATEGORY_BLUE = "#3b82f6"     # Blue category
    
    # Typography (refined hierarchy)
    HEADER_FONT = ("Segoe UI", 18, "bold")
    SUBHEADER_FONT = ("Segoe UI", 14, "bold")
    BODY_FONT = ("Segoe UI", 11)
    BUTTON_FONT = ("Segoe UI", 11, "bold")
    SMALL_FONT = ("Segoe UI", 10)
    CAPTION_FONT = ("Segoe UI", 9)
    
    # Spacing & Dimensions (modern standards)
    CARD_RADIUS = 12              # Border radius for cards
    BUTTON_RADIUS = 8             # Border radius for buttons  
    CARD_PADDING = 20             # Internal card padding
    SECTION_SPACING = 24          # Space between sections
    ITEM_SPACING = 16             # Space between items
    
    @staticmethod
    def configure_style():
        """Configure modern UI styles with enhanced visual effects."""
        style = ttk.Style()
        
        # Use a modern theme as base
        style.theme_use('clam')
        
        # Configure default font for all tkinter widgets
        import tkinter as tk
        tk.font.nametofont("TkDefaultFont").configure(family="Segoe UI", size=11)
        tk.font.nametofont("TkTextFont").configure(family="Segoe UI", size=11)
        tk.font.nametofont("TkFixedFont").configure(family="Consolas", size=11)
        tk.font.nametofont("TkMenuFont").configure(family="Segoe UI", size=10)
        tk.font.nametofont("TkHeadingFont").configure(family="Segoe UI", size=14, weight="bold")
        tk.font.nametofont("TkCaptionFont").configure(family="Segoe UI", size=9)
        tk.font.nametofont("TkSmallCaptionFont").configure(family="Segoe UI", size=8)
        tk.font.nametofont("TkIconFont").configure(family="Segoe UI", size=11)
        tk.font.nametofont("TkTooltipFont").configure(family="Segoe UI", size=10)
        
        # Configure default ttk styles with modern fonts
        style.configure(".", font=ModernStyle.BODY_FONT)
        style.configure("TLabel", font=ModernStyle.BODY_FONT, background=ModernStyle.BG_CARD)
        style.configure("TFrame", background=ModernStyle.BG_CARD)
        style.configure("TEntry", font=ModernStyle.BODY_FONT, fieldbackground=ModernStyle.BG_CARD)
        style.configure("TCombobox", font=ModernStyle.BODY_FONT)
        style.configure("Treeview", font=ModernStyle.BODY_FONT, background=ModernStyle.BG_CARD)
        style.configure("Treeview.Heading", font=ModernStyle.SUBHEADER_FONT)
        
        # Modern Primary Button
        style.configure("ModernPrimary.TButton",
                       background=ModernStyle.PRIMARY_BLUE,
                       foreground=ModernStyle.TEXT_WHITE,
                       font=ModernStyle.BUTTON_FONT,
                       padding=(20, 12),
                       relief="flat",
                       borderwidth=0)
        
        # Modern frame styles
        style.configure("Modern.TFrame",
                       background=ModernStyle.BG_CARD,
                       relief="flat",
                       borderwidth=0)
        
        style.configure("Card.TFrame",
                       background=ModernStyle.BG_CARD,
                       relief="flat", 
                       borderwidth=0)
        
        # Modern combobox
        style.configure("Modern.TCombobox",
                       font=ModernStyle.BODY_FONT,
                       fieldbackground=ModernStyle.BG_SECONDARY)

class ModernCard:
    """Modern card widget with rounded corners and shadow effect."""
    
    @staticmethod
    def create_card(parent, bg_color=None, shadow=True, padding=None):
        """Create a modern card with shadow effect."""
        if bg_color is None:
            bg_color = ModernStyle.BG_CARD
        if padding is None:
            padding = ModernStyle.CARD_PADDING
            
        # Create container for card and shadow
        container = tk.Frame(parent, bg=ModernStyle.BG_GRADIENT_START)
        
        # Shadow container (simulates drop shadow)
        if shadow:
            shadow_frame = tk.Frame(container, bg=ModernStyle.SHADOW_LIGHT, height=2)
            shadow_frame.pack(fill=tk.X, padx=(2, 0), pady=(0, 2))
        
        # Main card frame
        card_frame = tk.Frame(container, bg=bg_color, relief=tk.FLAT, bd=0)
        card_frame.pack(fill=tk.BOTH, expand=True)
        
        # Content area with padding
        content_frame = tk.Frame(card_frame, bg=bg_color)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=padding, pady=padding)
        
        return content_frame
    
    @staticmethod
    @staticmethod
    def create_category_card(parent, title, icon, color, count=None, command=None):
        """Create a colorful category card like in the reference UI."""
        # Card container with enhanced shadow effect
        card_container = tk.Frame(parent, bg=ModernStyle.BG_GRADIENT_START)
        card_container.pack(side=tk.LEFT, padx=(0, ModernStyle.ITEM_SPACING))
        
        # Enhanced shadow with multiple layers for depth
        shadow_bottom = tk.Frame(card_container, bg=ModernStyle.SHADOW_MEDIUM, height=3)
        shadow_bottom.pack(fill=tk.X, padx=3, pady=(3, 0))
        
        shadow_mid = tk.Frame(card_container, bg=ModernStyle.SHADOW_LIGHT, height=2)
        shadow_mid.pack(fill=tk.X, padx=2, pady=(0, 0))
        
        # Main card with enhanced styling
        card = tk.Button(card_container,
                        bg=color,
                        relief=tk.FLAT,
                        bd=0,
                        highlightthickness=0,
                        cursor="hand2" if command else "arrow",
                        command=command)
        card.pack()
        
        # Card content with better spacing
        card_content = tk.Frame(card, bg=color)
        card_content.pack(padx=25, pady=25)
        
        # Icon with enhanced styling
        icon_label = tk.Label(card_content,
                             text=icon,
                             font=("Segoe UI", 28, "normal"),
                             fg=ModernStyle.TEXT_WHITE,
                             bg=color)
        icon_label.pack(pady=(0, 8))
        
        # Title with modern font
        title_label = tk.Label(card_content,
                              text=title,
                              font=ModernStyle.BUTTON_FONT,
                              fg=ModernStyle.TEXT_WHITE,
                              bg=color)
        title_label.pack(pady=(8, 0))
        
        # Count if provided
        if count is not None:
            count_label = tk.Label(card_content,
                                  text=f"{count} files",
                                  font=ModernStyle.SMALL_FONT,
                                  fg="#e2e8f0",  # Light gray instead of alpha
                                  bg=color)
            count_label.pack()
        
        return card_container

class ModernSidebar:
    """Modern sidebar navigation inspired by the reference UI."""
    
    def __init__(self, parent, width=250):
        self.parent = parent
        self.width = width
        self.setup_sidebar()
        
    def setup_sidebar(self):
        """Create the modern sidebar with navigation items."""
        # Main sidebar frame
        self.sidebar = tk.Frame(self.parent, 
                               bg=ModernStyle.BG_SIDEBAR, 
                               width=self.width)
        self.sidebar.grid(row=0, column=0, sticky="ns")
        self.sidebar.grid_propagate(False)
        
        # Configure sidebar for content layout
        self.sidebar.grid_rowconfigure(1, weight=1)  # Navigation area expands
        self.sidebar.grid_columnconfigure(0, weight=1)
        
        # User section at top
        self.setup_user_section()
        
        # Navigation items
        self.setup_navigation()
        
        # Bottom section
        self.setup_bottom_section()
        
    def setup_user_section(self):
        """Setup the user profile section."""
        user_frame = tk.Frame(self.sidebar, bg=ModernStyle.BG_SIDEBAR)
        user_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 30))
        
        # User avatar (circle)
        avatar_frame = tk.Frame(user_frame, bg=ModernStyle.BG_CARD, 
                               width=50, height=50)
        avatar_frame.pack()
        avatar_frame.pack_propagate(False)
        
        # User initial
        user_label = tk.Label(avatar_frame, text="👤", 
                             font=("Segoe UI", 20),
                             bg=ModernStyle.BG_CARD,
                             fg=ModernStyle.TEXT_SECONDARY)
        user_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
    def setup_navigation(self):
        """Setup navigation menu items."""
        nav_items = [
            ("🌐", "Translation Manager", True),
            ("📁", "File Browser", False),
            ("⭐", "Favorites", False),
            ("📤", "Export Center", False)
        ]
        
        nav_frame = tk.Frame(self.sidebar, bg=ModernStyle.BG_SIDEBAR)
        nav_frame.grid(row=1, column=0, sticky="nsew", padx=10)
        
        for i, (icon, text, active) in enumerate(nav_items):
            self.create_nav_item(nav_frame, icon, text, active, i)
            
    def create_nav_item(self, parent, icon, text, active=False, row=0):
        """Create a navigation item."""
        bg_color = ModernStyle.ACCENT_CYAN if active else ModernStyle.BG_SIDEBAR
        text_color = ModernStyle.TEXT_WHITE
        
        item_frame = tk.Frame(parent, bg=bg_color, cursor="hand2")
        item_frame.grid(row=row, column=0, sticky="ew", pady=2)
        
        # Content frame
        content = tk.Frame(item_frame, bg=bg_color)
        content.pack(fill=tk.X, padx=15, pady=12)
        
        # Icon
        icon_label = tk.Label(content, text=icon, 
                             font=("Segoe UI", 14),
                             bg=bg_color, fg=text_color)
        icon_label.pack(side=tk.LEFT)
        
        # Text
        text_label = tk.Label(content, text=text,
                             font=ModernStyle.BODY_FONT,
                             bg=bg_color, fg=text_color)
        text_label.pack(side=tk.LEFT, padx=(15, 0))
        
    def setup_bottom_section(self):
        """Setup bottom section with settings."""
        bottom_frame = tk.Frame(self.sidebar, bg=ModernStyle.BG_SIDEBAR)
        bottom_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=20)
        
        # Settings
        self.create_nav_item(bottom_frame, "⚙️", "Settings", False, 0)
        # Sign out
        self.create_nav_item(bottom_frame, "🚪", "Sign Out", False, 1)
    
    @staticmethod
    def configure_style():
        """Configure modern UI styles with enhanced visual effects."""
        style = ttk.Style()
        
        # Use a modern theme as base
        style.theme_use('clam')
        
        # Configure default font for all tkinter widgets
        import tkinter as tk
        tk.font.nametofont("TkDefaultFont").configure(family="Segoe UI", size=11)
        tk.font.nametofont("TkTextFont").configure(family="Segoe UI", size=11)
        tk.font.nametofont("TkFixedFont").configure(family="Consolas", size=11)
        tk.font.nametofont("TkMenuFont").configure(family="Segoe UI", size=10)
        tk.font.nametofont("TkHeadingFont").configure(family="Segoe UI", size=14, weight="bold")
        tk.font.nametofont("TkCaptionFont").configure(family="Segoe UI", size=9)
        tk.font.nametofont("TkSmallCaptionFont").configure(family="Segoe UI", size=8)
        tk.font.nametofont("TkIconFont").configure(family="Segoe UI", size=11)
        tk.font.nametofont("TkTooltipFont").configure(family="Segoe UI", size=10)
        
        # Configure default ttk styles with modern fonts
        style.configure(".", font=ModernStyle.BODY_FONT)
        style.configure("TLabel", font=ModernStyle.BODY_FONT, background=ModernStyle.BG_CARD)
        style.configure("TFrame", background=ModernStyle.BG_CARD)
        style.configure("TEntry", font=ModernStyle.BODY_FONT, fieldbackground=ModernStyle.BG_CARD)
        style.configure("TCombobox", font=ModernStyle.BODY_FONT)
        style.configure("Treeview", font=ModernStyle.BODY_FONT, background=ModernStyle.BG_CARD)
        style.configure("Treeview.Heading", font=ModernStyle.SUBHEADER_FONT)
        
        # Modern Primary Button (enhanced)
        style.configure("ModernPrimary.TButton",
                       background=ModernStyle.PRIMARY_BLUE,
                       foreground=ModernStyle.TEXT_WHITE,
                       font=ModernStyle.BUTTON_FONT,
                       padding=(20, 12),
                       relief="flat",
                       borderwidth=0)
        
        style.map("ModernPrimary.TButton",
                 background=[('active', '#1d4ed8'),
                            ('pressed', '#1e40af')])
        
        # Modern Secondary Button
        style.configure("ModernSecondary.TButton",
                       background=ModernStyle.BG_CARD,
                       foreground=ModernStyle.PRIMARY_BLUE,
                       font=ModernStyle.BUTTON_FONT,
                       padding=(20, 12),
                       relief="solid",
                       borderwidth=1)
        
        style.map("ModernSecondary.TButton",
                 background=[('active', ModernStyle.BG_SECONDARY)],
                 relief=[('pressed', 'flat')])
        
        # Modern Success Button
        style.configure("ModernSuccess.TButton",
                       background=ModernStyle.ACCENT_GREEN,
                       foreground=ModernStyle.TEXT_WHITE,
                       font=ModernStyle.BUTTON_FONT,
                       padding=(20, 12),
                       relief="flat",
                       borderwidth=0)
        
        # Modern Purple Accent Button
        style.configure("ModernAccent.TButton",
                       background=ModernStyle.PRIMARY_PURPLE,
                       foreground=ModernStyle.TEXT_WHITE,
                       font=ModernStyle.BUTTON_FONT,
                       padding=(20, 12),
                       relief="flat",
                       borderwidth=0)
        
        # Configure Modern Frame styles to fix visual boxes
        style.configure("CopilotCard.TFrame",
                       background=ModernStyle.BG_CARD,
                       relief="flat",
                       borderwidth=0)
        
        # Configure Card Frame (for main.py compatibility)
        style.configure("Card.TFrame",
                       background=ModernStyle.BG_CARD,
                       relief="flat",
                       borderwidth=0)
        
        # Configure Clean Frame (no borders at all)
        style.configure("Clean.TFrame",
                       background=ModernStyle.BG_CARD,
                       relief="flat",
                       borderwidth=0)
        
        # Configure Light Background Frame
        style.configure("Light.TFrame",
                       background=ModernStyle.BG_LIGHT,
                       relief="flat",
                       borderwidth=0)
        
        # Configure Header Frame
        style.configure("CopilotHeader.TFrame",
                       background=ModernStyle.PRIMARY_BLUE,
                       relief="flat",
                       borderwidth=0)
        
        # Configure Labels
        style.configure("CopilotTitle.TLabel",
                       font=ModernStyle.HEADER_FONT,
                       foreground=ModernStyle.TEXT_WHITE,
                       background=ModernStyle.PRIMARY_BLUE)
        
        style.configure("CopilotSubtitle.TLabel",
                       font=ModernStyle.SUBHEADER_FONT,
                       foreground=ModernStyle.TEXT_PRIMARY,
                       background=ModernStyle.BG_CARD)
        
        style.configure("CopilotBody.TLabel",
                       font=ModernStyle.BODY_FONT,
                       foreground=ModernStyle.TEXT_SECONDARY,
                       background=ModernStyle.BG_CARD)
        
        style.configure("CopilotMuted.TLabel",
                       font=ModernStyle.SMALL_FONT,
                       foreground=ModernStyle.TEXT_MUTED,
                       background=ModernStyle.BG_CARD)
        
        # Configure Entry
        style.configure("Copilot.TEntry",
                       fieldbackground=ModernStyle.BG_CARD,
                       borderwidth=2,
                       relief="solid",
                       insertcolor=ModernStyle.PRIMARY_BLUE)
        
        style.map("Copilot.TEntry",
                 focuscolor=[('!focus', ModernStyle.BORDER_LIGHT),
                            ('focus', ModernStyle.BORDER_FOCUS)])
        
        # Configure Combobox
        style.configure("Copilot.TCombobox",
                       fieldbackground=ModernStyle.BG_CARD,
                       borderwidth=2,
                       relief="solid")
        
        # Configure LabelFrame
        style.configure("CopilotPanel.TLabelframe",
                       background=ModernStyle.BG_CARD,
                       borderwidth=2,
                       relief="solid",
                       lightcolor=ModernStyle.BORDER_LIGHT,
                       darkcolor=ModernStyle.BORDER_LIGHT)
        
        style.configure("CopilotPanel.TLabelframe.Label",
                       font=ModernStyle.SUBHEADER_FONT,
                       foreground=ModernStyle.PRIMARY_BLUE,
                       background=ModernStyle.BG_CARD)

class TranslationTable:
    """Advanced table widget for managing translations."""
    
    def __init__(self, parent, edit_callback: Callable[[str, str], None]):
        self.parent = parent
        self.edit_callback = edit_callback
        self.data = {}
        self.translations = {}
        self.item_keys = {}  # Store mapping from item_id to key
        self.tree = None  # Initialize tree as None first
        
        # Initialize modern styling
        ModernStyle.configure_style()
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the modern UI with sidebar navigation and enhanced design."""
        # Create main container with modern background gradient
        self.frame = tk.Frame(self.parent, bg=ModernStyle.BG_GRADIENT_START)
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        # Create horizontal layout: sidebar + main content
        self.create_layout()
        
    def create_layout(self):
        """Create the main layout with sidebar and content area."""
        # Configure main frame for grid layout
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=0)  # Sidebar - fixed width
        self.frame.grid_columnconfigure(1, weight=1)  # Content - expandable
        
        # Modern sidebar navigation
        self.sidebar = ModernSidebar(self.frame)
        
        # Main content area
        self.content_area = tk.Frame(self.frame, bg=ModernStyle.BG_GRADIENT_START)
        self.content_area.grid(row=0, column=1, sticky="nsew")
        
        # Configure main content area for responsive layout
        self.content_area.grid_rowconfigure(0, weight=0)  # Header - fixed
        self.content_area.grid_rowconfigure(1, weight=0)  # Categories - fixed
        self.content_area.grid_rowconfigure(2, weight=0)  # Controls - fixed
        self.content_area.grid_rowconfigure(3, weight=1)  # Table - expandable  
        self.content_area.grid_rowconfigure(4, weight=0)  # Footer - fixed
        self.content_area.grid_columnconfigure(0, weight=1)  # Full width
        
        # Setup content sections
        self.setup_modern_header()
        self.setup_category_section()
        self.setup_control_panels()
        self.setup_content_section()
        self.setup_footer()
        
    def setup_modern_header(self):
        """Setup modern header with search and pro badge."""
        header_frame = tk.Frame(self.content_area, bg=ModernStyle.BG_GRADIENT_START, height=80)
        header_frame.grid(row=0, column=0, sticky="ew", padx=30, pady=20)
        header_frame.grid_propagate(False)
        header_frame.grid_columnconfigure(1, weight=1)
        
        # Main title
        title_label = tk.Label(header_frame,
                              text="Translation Manager",
                              font=ModernStyle.HEADER_FONT,
                              fg=ModernStyle.TEXT_PRIMARY,
                              bg=ModernStyle.BG_GRADIENT_START)
        title_label.grid(row=0, column=0, sticky="w")
        
        # Search bar (center)
        self.setup_header_search(header_frame)
        
        # Pro badge (right)
        pro_frame = tk.Frame(header_frame, bg=ModernStyle.PRIMARY_BLUE)
        pro_frame.grid(row=0, column=2, sticky="e")
        
        pro_label = tk.Label(pro_frame,
                            text="Pro",
                            font=ModernStyle.BUTTON_FONT,
                            fg=ModernStyle.TEXT_WHITE,
                            bg=ModernStyle.PRIMARY_BLUE)
        pro_label.pack(padx=20, pady=10)
        
    def setup_header_search(self, parent):
        """Setup the header search bar."""
        search_frame = tk.Frame(parent, bg=ModernStyle.BG_CARD)
        search_frame.grid(row=0, column=1, sticky="ew", padx=50)
        search_frame.grid_columnconfigure(0, weight=1)
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.on_search_change)
        
        search_entry = tk.Entry(search_frame,
                               textvariable=self.search_var,
                               font=ModernStyle.BODY_FONT,
                               bg=ModernStyle.BG_CARD,
                               fg=ModernStyle.TEXT_SECONDARY,
                               relief=tk.FLAT,
                               bd=0)
        search_entry.grid(row=0, column=0, sticky="ew", padx=20, pady=12)
        search_entry.insert(0, "🔍 Search translations...")
        
        # Search styling
        def on_focus_in(event):
            if search_entry.get() == "🔍 Search translations...":
                search_entry.delete(0, tk.END)
                search_entry.config(fg=ModernStyle.TEXT_PRIMARY)
                
        def on_focus_out(event):
            if not search_entry.get():
                search_entry.insert(0, "🔍 Search translations...")
                search_entry.config(fg=ModernStyle.TEXT_SECONDARY)
                
        search_entry.bind("<FocusIn>", on_focus_in)
        search_entry.bind("<FocusOut>", on_focus_out)
        
    def setup_category_section(self):
        """Setup category cards section like the reference UI."""
        categories_frame = tk.Frame(self.content_area, bg=ModernStyle.BG_GRADIENT_START)
        categories_frame.grid(row=1, column=0, sticky="ew", padx=30, pady=(0, 20))
        
        # Section title
        title_frame = tk.Frame(categories_frame, bg=ModernStyle.BG_GRADIENT_START)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        categories_title = tk.Label(title_frame,
                                   text="Categories",
                                   font=ModernStyle.SUBHEADER_FONT,
                                   fg=ModernStyle.TEXT_PRIMARY,
                                   bg=ModernStyle.BG_GRADIENT_START)
        categories_title.pack(side=tk.LEFT)
        
        # Category cards container
        cards_frame = tk.Frame(categories_frame, bg=ModernStyle.BG_GRADIENT_START)
        cards_frame.pack(fill=tk.X)
        
        # Create category cards with colors like reference UI
        self.create_category_cards(cards_frame)
        
    def create_category_cards(self, parent):
        """Create colorful category cards."""
        categories = [
            ("📝", "Translations", ModernStyle.CATEGORY_PURPLE, self.get_translation_count()),
            ("📁", "Topics", ModernStyle.CATEGORY_TEAL, self.get_topic_count()),
            ("🎯", "Components", ModernStyle.CATEGORY_PINK, self.get_component_count()),
            ("✅", "Completed", ModernStyle.CATEGORY_BLUE, self.get_completed_count())
        ]
        
        for icon, title, color, count in categories:
            ModernCard.create_category_card(parent, title, icon, color, count)
            
    def get_translation_count(self):
        """Get total translation count."""
        return len(self.data) if self.data else 0
        
    def get_topic_count(self):
        """Get unique topic count."""
        if not self.data:
            return 0
        topics = set(entry.get('topic', 'Unknown') for entry in self.data.values())
        return len(topics)
        
    def get_component_count(self):
        """Get unique component count."""
        if not self.data:
            return 0
        components = set(entry.get('ui_component', 'Unknown') for entry in self.data.values())
        return len(components)
        
    def get_completed_count(self):
        """Get completed translations count."""
        if not self.data:
            return 0
        return len([k for k in self.data.keys() if self.translations.get(k, '')])
        
        # Header content
        header_content = tk.Frame(header_frame, bg=ModernStyle.PRIMARY_BLUE)
        header_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # Title with icon
        title_frame = tk.Frame(header_content, bg=ModernStyle.PRIMARY_BLUE)
        title_frame.pack(side=tk.LEFT)
        
        title_label = tk.Label(title_frame, 
                              text="🤖 Translation Manager", 
                              font=ModernStyle.HEADER_FONT,
                              fg=ModernStyle.TEXT_WHITE,
                              bg=ModernStyle.PRIMARY_BLUE)
        title_label.pack(side=tk.LEFT)
        
        subtitle_label = tk.Label(title_frame,
                                 text="Copilot Studio Localization Tool",
                                 font=ModernStyle.BODY_FONT,
                                 fg="#b3d7ff",  # Light blue
                                 bg=ModernStyle.PRIMARY_BLUE)
        subtitle_label.pack(side=tk.LEFT, padx=(15, 0))
        
        # Status indicator
        self.header_status = tk.Label(header_content,
                                     text="Ready",
                                     font=ModernStyle.BODY_FONT,
                                     fg=ModernStyle.TEXT_WHITE,
                                     bg=ModernStyle.PRIMARY_BLUE)
        self.header_status.pack(side=tk.RIGHT)
        
    def setup_control_panels(self):
        """Setup modern control panels with card design."""
        controls_container = tk.Frame(self.content_area, bg=ModernStyle.BG_GRADIENT_START)
        controls_container.grid(row=2, column=0, sticky="ew", padx=30, pady=(0, 20))
        controls_container.grid_columnconfigure(0, weight=1)
        
        # Create modern filters card - simplified approach
        self.setup_modern_filters(controls_container)
        
    def setup_modern_filters(self, parent):
        """Setup modern filter panel with card design."""
        # Modern filters card with enhanced styling
        filters_card = tk.Frame(parent, bg=ModernStyle.BG_CARD, relief=tk.FLAT, bd=0, highlightthickness=1, highlightcolor=ModernStyle.BORDER_LIGHT)
        filters_card.grid(row=0, column=0, sticky="ew", pady=10, ipady=10)
        filters_card.grid_columnconfigure((0, 1, 2), weight=1)  # Three filter columns
        
        # Add inner padding frame for better spacing
        inner_frame = tk.Frame(filters_card, bg=ModernStyle.BG_CARD)
        inner_frame.grid(row=0, column=0, columnspan=3, sticky="ew", padx=20, pady=15)
        inner_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Filters header
        header_frame = tk.Frame(inner_frame, bg=ModernStyle.BG_CARD)
        header_frame.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(0, 15))
        
        filters_title = tk.Label(header_frame,
                                text="🔍 Filters & Search",
                                font=ModernStyle.SUBHEADER_FONT,
                                fg=ModernStyle.TEXT_PRIMARY,
                                bg=ModernStyle.BG_CARD)
        filters_title.pack(side=tk.LEFT)
        
        # Filter controls in the inner frame
        self.setup_filter_controls(inner_frame)
        
    def setup_filter_controls(self, parent):
        """Setup modern filter dropdown controls."""
        filter_configs = [
            ("📁", "Topic", "topic", 1),
            ("🧩", "Component", "component", 2), 
            ("📊", "Status", "status", 3)
        ]
        
        for icon, title, filter_type, column in filter_configs:
            self.create_modern_filter(parent, icon, title, filter_type, column)
            
    def create_modern_filter(self, parent, icon, title, filter_type, column):
        """Create a modern filter control."""
        filter_frame = tk.Frame(parent, bg=ModernStyle.BG_CARD)
        filter_frame.grid(row=1, column=column-1, sticky="ew", padx=10, pady=(0, 15))
        filter_frame.grid_columnconfigure(0, weight=1)
        
        # Filter label
        filter_label = tk.Label(filter_frame,
                               text=f"{icon} {title}",
                               font=ModernStyle.BODY_FONT,
                               fg=ModernStyle.TEXT_SECONDARY,
                               bg=ModernStyle.BG_CARD)
        filter_label.grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        # Filter dropdown
        if filter_type == "topic":
            self.topic_filter = ttk.Combobox(filter_frame, 
                                           state="readonly", 
                                           font=ModernStyle.BODY_FONT,
                                           style="Modern.TCombobox")
            self.topic_filter.bind('<<ComboboxSelected>>', self.on_filter_change)
            self.topic_filter.grid(row=1, column=0, sticky="ew")
            
        elif filter_type == "component":
            self.component_filter = ttk.Combobox(filter_frame, 
                                               state="readonly", 
                                               font=ModernStyle.BODY_FONT,
                                               style="Modern.TCombobox")
            self.component_filter.bind('<<ComboboxSelected>>', self.on_filter_change)
            self.component_filter.grid(row=1, column=0, sticky="ew")
            
        elif filter_type == "status":
            self.status_filter = ttk.Combobox(filter_frame, 
                                            state="readonly", 
                                            font=ModernStyle.BODY_FONT,
                                            style="Modern.TCombobox")
            self.status_filter['values'] = ['All Status', 'Pending', 'Translated']
            self.status_filter.set('All Status')
            self.status_filter.bind('<<ComboboxSelected>>', self.on_filter_change)
            self.status_filter.grid(row=1, column=0, sticky="ew")
            
    def setup_content_section(self):
        """Setup the main content area with modern table."""
        content_container = tk.Frame(self.content_area, bg=ModernStyle.BG_GRADIENT_START)
        content_container.grid(row=3, column=0, sticky="nsew", padx=30, pady=(0, 20))
        content_container.grid_rowconfigure(1, weight=1)
        content_container.grid_columnconfigure(0, weight=1)
        
        # Content header
        self.setup_content_header(content_container)
        
        # Table in modern card
        self.setup_modern_table(content_container)
        
    def setup_content_header(self, parent):
        """Setup content area header with actions."""
        header_frame = tk.Frame(parent, bg=ModernStyle.BG_GRADIENT_START)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        header_frame.grid_columnconfigure(0, weight=1)
        
        # Left side - title and stats
        left_frame = tk.Frame(header_frame, bg=ModernStyle.BG_GRADIENT_START)
        left_frame.pack(side=tk.LEFT)
        
        title_label = tk.Label(left_frame,
                              text="💬 Translation Data",
                              font=ModernStyle.SUBHEADER_FONT,
                              fg=ModernStyle.TEXT_PRIMARY,
                              bg=ModernStyle.BG_GRADIENT_START)
        title_label.pack(side=tk.LEFT)
        
        # Right side - action buttons
        actions_frame = tk.Frame(header_frame, bg=ModernStyle.BG_GRADIENT_START)
        actions_frame.pack(side=tk.RIGHT)
        
        # Modern action buttons
        buttons = [
            ("🔥", "Add Files", ModernStyle.PRIMARY_BLUE),
            ("📥", "Select All", ModernStyle.BG_CARD),
            ("📤", "Export", ModernStyle.ACCENT_GREEN)
        ]
        
        for icon, text, color in buttons:
            btn_color = ModernStyle.TEXT_WHITE if color != ModernStyle.BG_CARD else ModernStyle.TEXT_PRIMARY
            
            btn = tk.Button(actions_frame,
                           text=f"{icon}",
                           font=("Segoe UI", 16),
                           bg=color,
                           fg=btn_color,
                           relief=tk.FLAT,
                           bd=0,
                           width=3,
                           height=1,
                           cursor="hand2")
            btn.pack(side=tk.RIGHT, padx=(10, 0))
            
    def setup_modern_table(self, parent):
        """Setup modern table with enhanced card design."""
        # Modern table card with enhanced styling
        table_card = tk.Frame(parent, bg=ModernStyle.BG_CARD, relief=tk.FLAT, bd=0, 
                             highlightthickness=1, highlightcolor=ModernStyle.BORDER_LIGHT)
        table_card.grid(row=1, column=0, sticky="nsew", padx=2, pady=2, ipady=5)
        
        # Configure table card for expansion
        table_card.grid_rowconfigure(0, weight=1)
        table_card.grid_columnconfigure(0, weight=1)
        
        # Table container with inner padding
        table_container = tk.Frame(table_card, bg=ModernStyle.BG_CARD)
        table_container.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        table_container.grid_rowconfigure(0, weight=1)
        table_container.grid_columnconfigure(0, weight=1)
        
        # Modern Treeview
        columns = ('original', 'translation', 'topic', 'component', 'status')
        self.tree = ttk.Treeview(table_container, columns=columns, show='headings')
        
        # Configure modern column headers
        headers = [
            ('original', '📝 Original Text'),
            ('translation', '🌐 Translation'),
            ('topic', '📁 Topic'),
            ('component', '🧩 Component'),
            ('status', '📊 Status')
        ]
        
        for col, header in headers:
            self.tree.heading(col, text=header, anchor=tk.W if col != 'status' else tk.CENTER)
            
        # Set responsive column widths
        self.tree.column('original', width=350, minwidth=200, stretch=True)
        self.tree.column('translation', width=350, minwidth=200, stretch=True)
        self.tree.column('topic', width=180, minwidth=100, stretch=True)
        self.tree.column('component', width=120, minwidth=80, stretch=True)
        self.tree.column('status', width=100, minwidth=80, stretch=False)
        
        # Modern scrollbars
        v_scrollbar = ttk.Scrollbar(table_container, orient=tk.VERTICAL, command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(table_container, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid positioning
        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # Configure row styling
        self.tree.tag_configure('translated', 
                               background=ModernStyle.STATUS_SUCCESS, 
                               foreground=ModernStyle.ACCENT_GREEN)
        self.tree.tag_configure('pending', 
                               background=ModernStyle.STATUS_WARNING, 
                               foreground=ModernStyle.ACCENT_ORANGE)
        self.tree.tag_configure('selected', 
                               background=ModernStyle.STATUS_INFO, 
                               foreground=ModernStyle.PRIMARY_BLUE)
        
        # Bind events
        self.tree.bind('<Double-1>', self.on_double_click)
        self.tree.bind('<Button-3>', self.show_context_menu)
        self.tree.bind('<Return>', self.on_double_click)
        
        # Modern context menu
        self.setup_context_menu()
        
    def setup_search_panel(self, parent):
        """Setup prominent search panel."""
        search_frame = tk.Frame(parent, bg=ModernStyle.BG_CARD, relief=tk.FLAT, bd=0)
        search_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        search_frame.grid_columnconfigure(0, weight=1)  # Responsive search panel
        
        # Search content
        search_content = tk.Frame(search_frame, bg=ModernStyle.BG_CARD)
        search_content.grid(row=0, column=0, sticky="ew", padx=25, pady=20)
        search_content.grid_columnconfigure(1, weight=1)  # Search field expandable
        
        # Search icon and label
        search_header = tk.Frame(search_content, bg=ModernStyle.BG_CARD)
        search_header.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        search_icon_label = tk.Label(search_header,
                                    text="🔍 Search & Filter",
                                    font=ModernStyle.SUBHEADER_FONT,
                                    fg=ModernStyle.PRIMARY_BLUE,
                                    bg=ModernStyle.BG_CARD)
        search_icon_label.pack(side=tk.LEFT)
        
        # Clear all button
        clear_all_btn = tk.Button(search_header,
                                 text="Clear All",
                                 font=ModernStyle.SMALL_FONT,
                                 fg=ModernStyle.PRIMARY_PURPLE,
                                 bg=ModernStyle.BG_CARD,
                                 relief=tk.FLAT,
                                 cursor="hand2",
                                 command=self.reset_filters)
        clear_all_btn.pack(side=tk.RIGHT)
        
        # Search input with modern styling - responsive
        search_input_frame = tk.Frame(search_content, bg=ModernStyle.BG_CARD)
        search_input_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        search_input_frame.grid_columnconfigure(0, weight=1)  # Entry expands
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.on_search_change)
        
        search_entry = tk.Entry(search_input_frame,
                               textvariable=self.search_var,
                               font=ModernStyle.BODY_FONT,
                               bg=ModernStyle.BG_SECONDARY,
                               fg=ModernStyle.TEXT_PRIMARY,
                               relief=tk.FLAT,
                               bd=0,
                               highlightthickness=2,
                               highlightbackground=ModernStyle.BORDER_LIGHT,
                               highlightcolor=ModernStyle.PRIMARY_BLUE)
        search_entry.grid(row=0, column=0, sticky="ew", ipady=8, ipadx=10)
        
        # Search button
        search_btn = tk.Button(search_input_frame,
                              text="🔍 Search",
                              font=ModernStyle.BUTTON_FONT,
                              bg=ModernStyle.PRIMARY_BLUE,
                              fg=ModernStyle.TEXT_WHITE,
                              relief=tk.FLAT,
                              padx=20,
                              cursor="hand2",
                              bd=0)
        search_btn.grid(row=0, column=1, padx=(10, 0), ipady=8)
        
    def setup_filter_panel(self, parent):
        """Setup filter panel with cards - responsive layout."""
        filter_frame = tk.Frame(parent, bg=ModernStyle.BG_LIGHT)
        filter_frame.grid(row=1, column=0, sticky="ew")
        filter_frame.grid_columnconfigure((0, 1, 2), weight=1)  # Equal weight for 3 columns
        
        # Filter cards - responsive grid
        self.setup_filter_card(filter_frame, "📁", "Topic", "topic", 0)
        self.setup_filter_card(filter_frame, "🧩", "Component", "component", 1)
        self.setup_filter_card(filter_frame, "📊", "Status", "status", 2)
        
    def setup_filter_card(self, parent, icon, title, filter_type, column):
        """Setup individual filter card with grid positioning."""
        card = tk.Frame(parent, bg=ModernStyle.BG_CARD, relief=tk.FLAT, bd=0)
        card.grid(row=0, column=column, sticky="ew", padx=(0, 15 if column < 2 else 0))
        card.grid_columnconfigure(0, weight=1)  # Card content expands
        
        # Card content
        card_content = tk.Frame(card, bg=ModernStyle.BG_CARD)
        card_content.grid(row=0, column=0, sticky="nsew", padx=20, pady=15)
        card_content.grid_columnconfigure(0, weight=1)  # Filter dropdown expands
        card.grid_rowconfigure(0, weight=1)
        card.grid_columnconfigure(0, weight=1)
        
        # Card header
        header_label = tk.Label(card_content,
                               text=f"{icon} {title}",
                               font=ModernStyle.SUBHEADER_FONT,
                               fg=ModernStyle.PRIMARY_PURPLE,
                               bg=ModernStyle.BG_CARD)
        header_label.grid(row=0, column=0, sticky="w", pady=(0, 8))
        
        # Filter dropdown
        if filter_type == "topic":
            self.topic_filter = ttk.Combobox(card_content, 
                                           state="readonly", 
                                           style="Copilot.TCombobox",
                                           font=ModernStyle.BODY_FONT)
            self.topic_filter.bind('<<ComboboxSelected>>', self.on_filter_change)
            self.topic_filter.grid(row=1, column=0, sticky="ew")
            
        elif filter_type == "component":
            self.component_filter = ttk.Combobox(card_content, 
                                               state="readonly", 
                                               style="Copilot.TCombobox",
                                               font=ModernStyle.BODY_FONT)
            self.component_filter.bind('<<ComboboxSelected>>', self.on_filter_change)
            self.component_filter.grid(row=1, column=0, sticky="ew")
            
        elif filter_type == "status":
            self.status_filter = ttk.Combobox(card_content, 
                                            state="readonly", 
                                            style="Copilot.TCombobox",
                                            font=ModernStyle.BODY_FONT)
            self.status_filter['values'] = ['All Status', 'Pending', 'Translated']
            self.status_filter.set('All Status')
            self.status_filter.bind('<<ComboboxSelected>>', self.on_filter_change)
            self.status_filter.grid(row=1, column=0, sticky="ew")
        
    def setup_content_area(self):
        """Setup the main content area with modern table - responsive."""
        content_frame = tk.Frame(self.frame, bg=ModernStyle.BG_LIGHT)
        content_frame.grid(row=2, column=0, sticky="nsew", padx=30, pady=(0, 20))
        
        # Make content area fully responsive
        content_frame.grid_rowconfigure(1, weight=1)  # Table area expands
        content_frame.grid_columnconfigure(0, weight=1)  # Full width
        
        # Content header
        content_header = tk.Frame(content_frame, bg=ModernStyle.BG_LIGHT)
        content_header.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        content_header.grid_columnconfigure(0, weight=1)  # Header responsive
        
        content_title = tk.Label(content_header,
                               text="💬 Translation Data",
                               font=ModernStyle.SUBHEADER_FONT,
                               fg=ModernStyle.TEXT_PRIMARY,
                               bg=ModernStyle.BG_LIGHT)
        content_title.pack(side=tk.LEFT)
        
        # Action buttons
        actions_frame = tk.Frame(content_header, bg=ModernStyle.BG_LIGHT)
        actions_frame.pack(side=tk.RIGHT)
        
        # Select all button
        select_all_btn = tk.Button(actions_frame,
                                  text="Select All",
                                  font=ModernStyle.SMALL_FONT,
                                  bg=ModernStyle.BG_CARD,
                                  fg=ModernStyle.PRIMARY_BLUE,
                                  relief=tk.FLAT,
                                  padx=15,
                                  cursor="hand2",
                                  command=self.select_all_items)
        select_all_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Export button
        export_btn = tk.Button(actions_frame,
                              text="📤 Export",
                              font=ModernStyle.BUTTON_FONT,
                              bg=ModernStyle.ACCENT_GREEN,
                              fg=ModernStyle.TEXT_WHITE,
                              relief=tk.FLAT,
                              padx=15,
                              cursor="hand2")
        export_btn.pack(side=tk.LEFT)
        
        # Table container with shadow effect - responsive
        table_container = tk.Frame(content_frame, bg=ModernStyle.BG_CARD, relief=tk.FLAT, bd=0)
        table_container.grid(row=1, column=0, sticky="nsew")
        
        # Make table container responsive
        table_container.grid_rowconfigure(0, weight=1)
        table_container.grid_columnconfigure(0, weight=1)
        
        # Table frame
        table_frame = tk.Frame(table_container, bg=ModernStyle.BG_CARD)
        table_frame.grid(row=0, column=0, sticky="nsew", padx=1, pady=1)
        
        # Make table frame responsive
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        # Modern Treeview with responsive columns
        columns = ('original', 'translation', 'topic', 'component', 'status')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings')
        
        # Configure modern column headers
        self.tree.heading('original', text='📝 Original Text', anchor=tk.W)
        self.tree.heading('translation', text='🌐 Translation', anchor=tk.W)
        self.tree.heading('topic', text='📁 Topic', anchor=tk.W)
        self.tree.heading('component', text='🧩 Component', anchor=tk.W)
        self.tree.heading('status', text='📊 Status', anchor=tk.CENTER)
        
        # Set responsive column widths
        self.tree.column('original', width=400, minwidth=200, stretch=True)
        self.tree.column('translation', width=400, minwidth=200, stretch=True)
        self.tree.column('topic', width=200, minwidth=100, stretch=True)
        self.tree.column('component', width=150, minwidth=80, stretch=True)
        self.tree.column('status', width=120, minwidth=80, stretch=False)
        
        # Modern scrollbars with grid positioning
        v_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid positioning for tree and scrollbars
        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # Grid layout
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
        
        # Configure vibrant row styling
        self.tree.tag_configure('translated', 
                               background=ModernStyle.STATUS_SUCCESS, 
                               foreground=ModernStyle.ACCENT_GREEN)
        self.tree.tag_configure('pending', 
                               background=ModernStyle.STATUS_WARNING, 
                               foreground=ModernStyle.ACCENT_ORANGE)
        self.tree.tag_configure('selected', 
                               background=ModernStyle.STATUS_INFO, 
                               foreground=ModernStyle.PRIMARY_BLUE)
        
        # Bind events
        self.tree.bind('<Double-1>', self.on_double_click)
        self.tree.bind('<Button-3>', self.show_context_menu)
        self.tree.bind('<Return>', self.on_double_click)
        
        # Modern context menu
        self.setup_context_menu()
        
    def setup_context_menu(self):
        """Setup modern context menu."""
        self.context_menu = tk.Menu(self.tree, tearoff=0, bg=ModernStyle.BG_CARD, 
                                   fg=ModernStyle.TEXT_PRIMARY, font=ModernStyle.BODY_FONT)
        
        self.context_menu.add_command(label="✏️ Edit Translation", command=self.edit_selected)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="📋 Copy Original", command=self.copy_original)
        self.context_menu.add_command(label="📋 Copy Translation", command=self.copy_translation)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="🗑️ Clear Translation", command=self.clear_selected)
        
    def setup_footer(self):
        """Setup footer with statistics - responsive."""
        footer_frame = tk.Frame(self.content_area, bg=ModernStyle.PRIMARY_BLUE, height=50)
        footer_frame.grid(row=4, column=0, sticky="ew")
        footer_frame.grid_propagate(False)
        footer_frame.grid_columnconfigure(0, weight=1)  # Responsive footer
        
        # Footer content
        footer_content = tk.Frame(footer_frame, bg=ModernStyle.PRIMARY_BLUE)
        footer_content.grid(row=0, column=0, sticky="ew", padx=30, pady=15)
        footer_content.grid_columnconfigure(0, weight=1)  # Stats area expands
        
        # Stats on the left
        self.stats_label = tk.Label(footer_content,
                                   text="🔍 Ready to load translation data...",
                                   font=ModernStyle.BODY_FONT,
                                   fg=ModernStyle.TEXT_WHITE,
                                   bg=ModernStyle.PRIMARY_BLUE)
        self.stats_label.pack(side=tk.LEFT)
        
        # Action buttons on the right
        actions_right = tk.Frame(footer_content, bg=ModernStyle.PRIMARY_BLUE)
        actions_right.pack(side=tk.RIGHT)
        
        # Translate button
        translate_btn = tk.Button(actions_right,
                                 text="🚀 Translate Selected",
                                 font=ModernStyle.BUTTON_FONT,
                                 bg=ModernStyle.ACCENT_CYAN,
                                 fg=ModernStyle.TEXT_WHITE,
                                 relief=tk.FLAT,
                                 padx=20,
                                 cursor="hand2")
        translate_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Validate button
        validate_btn = tk.Button(actions_right,
                               text="✅ Validate",
                               font=ModernStyle.BUTTON_FONT,
                               bg=ModernStyle.ACCENT_GREEN,
                               fg=ModernStyle.TEXT_WHITE,
                               relief=tk.FLAT,
                               padx=20,
                               cursor="hand2")
        validate_btn.pack(side=tk.RIGHT)
        
    def grid(self, **kwargs):
        """Grid the main frame."""
        self.frame.grid(**kwargs)
        
    def load_data(self, data: Dict[str, Dict]):
        """Load localization data into the table."""
        self.data = data
        self.translations = {}
        self.item_keys = {}  # Clear the key mapping
        
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Populate all filters
        topics = sorted(set(entry['topic'] for entry in data.values()))
        self.topic_filter['values'] = ['All Topics'] + topics
        self.topic_filter.set('All Topics')
        
        components = sorted(set(entry['ui_component'] for entry in data.values()))
        self.component_filter['values'] = ['All Components'] + components
        self.component_filter.set('All Components')
        
        # Update stats
        self.update_stats()
        
        # Add data to tree
        self.refresh_display()
        
    def refresh_display(self):
        """Refresh the table display based on current filters."""
        # Check if tree exists
        if not self.tree:
            return
            
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.item_keys.clear()  # Clear the key mapping
            
        # Apply filters
        filtered_data = self.apply_filters()
        
        # Add items to tree
        for key, entry in filtered_data.items():
            translation = self.translations.get(key, '')
            status = 'Translated' if translation else 'Pending'
            
            # Truncate long text for display
            original_display = self.truncate_text(entry['text'], 100)
            translation_display = self.truncate_text(translation, 100)
            
            item_id = self.tree.insert('', tk.END, values=(
                original_display,
                translation_display,
                entry['topic'],
                entry['ui_component'],
                status
            ))
            
            # Store the key for reference using item metadata
            self.item_keys[item_id] = key
            
            # Color code based on status
            if translation:
                self.tree.item(item_id, tags=('translated',))
            else:
                self.tree.item(item_id, tags=('pending',))
        
        # Update stats
        self.update_stats()
        
    def apply_filters(self) -> Dict[str, Dict]:
        """Apply search, topic, component, and status filters to the data."""
        filtered_data = self.data.copy()
        
        # Apply search filter
        search_term = self.search_var.get().lower()
        if search_term:
            filtered_data = {
                key: entry for key, entry in filtered_data.items()
                if (search_term in entry['text'].lower() or
                    search_term in entry['topic'].lower() or
                    search_term in entry['description'].lower() or
                    search_term in entry['ui_component'].lower())
            }
            
        # Apply topic filter
        topic_filter = self.topic_filter.get()
        if topic_filter and topic_filter != 'All Topics':
            filtered_data = {
                key: entry for key, entry in filtered_data.items()
                if entry['topic'] == topic_filter
            }
        
        # Apply component filter
        component_filter = self.component_filter.get()
        if component_filter and component_filter != 'All Components':
            filtered_data = {
                key: entry for key, entry in filtered_data.items()
                if entry['ui_component'] == component_filter
            }
        
        # Apply status filter
        status_filter = self.status_filter.get()
        if status_filter and status_filter != 'All Status':
            if status_filter == 'Translated':
                filtered_data = {
                    key: entry for key, entry in filtered_data.items()
                    if self.translations.get(key, '')
                }
            elif status_filter == 'Pending':
                filtered_data = {
                    key: entry for key, entry in filtered_data.items()
                    if not self.translations.get(key, '')
                }
            
        return filtered_data
    
    def select_all_items(self):
        """Select all visible items in the tree."""
        for item in self.tree.get_children():
            self.tree.selection_add(item)
            
    def clear_search(self):
        """Clear the search field."""
        self.search_var.set('')
        
    def reset_filters(self):
        """Reset all filters to default values."""
        self.search_var.set('')
        self.topic_filter.set('All Topics')
        self.component_filter.set('All Components')
        self.status_filter.set('All Status')
        self.refresh_display()
        
    def update_stats(self):
        """Update the vibrant statistics display."""
        if not self.data:
            self.stats_label.config(text="🔍 Ready to load translation data...")
            return
            
        total_entries = len(self.data)
        translated_count = len([k for k in self.data.keys() if self.translations.get(k, '')])
        pending_count = total_entries - translated_count
        
        filtered_data = self.apply_filters()
        filtered_count = len(filtered_data)
        
        # Calculate completion percentage
        completion_pct = int((translated_count / total_entries * 100)) if total_entries > 0 else 0
        
        if filtered_count != total_entries:
            stats_text = f"📊 Showing {filtered_count} of {total_entries} entries • ✅ {translated_count} translated ({completion_pct}%) • ⏳ {pending_count} pending"
        else:
            stats_text = f"📊 {total_entries} entries total • ✅ {translated_count} translated ({completion_pct}%) • ⏳ {pending_count} pending"
            
        self.stats_label.config(text=stats_text)
        
        # Update header status with completion info
        if hasattr(self, 'header_status'):
            if completion_pct == 100:
                self.header_status.config(text="🎉 Complete!", fg="#90EE90")  # Light green
            elif completion_pct > 50:
                self.header_status.config(text=f"⚡ {completion_pct}% Done", fg="#87CEEB")  # Sky blue
            else:
                self.header_status.config(text=f"🚀 {completion_pct}% Done", fg="#FFB6C1")  # Light pink
        
    def truncate_text(self, text: str, max_length: int) -> str:
        """Truncate text for display."""
        if len(text) <= max_length:
            return text
        return text[:max_length-3] + "..."
        
    def on_search_change(self, *args):
        """Handle search input changes."""
        self.refresh_display()
        
    def on_filter_change(self, event):
        """Handle filter changes."""
        self.refresh_display()
        self.update_stats()
        
    def on_double_click(self, event):
        """Handle double-click to edit translation."""
        self.edit_selected()
        
    def show_context_menu(self, event):
        """Handle right-click context menu."""
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)
            
    def edit_selected(self):
        """Edit the selected translation."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an item to edit")
            return
            
        item = selection[0]
        key = self.get_key_from_item(item)
        if not key:
            return
            
        original_text = self.data[key]['text']
        current_translation = self.translations.get(key, '')
        
        # Show edit dialog
        dialog = TranslationEditDialog(self.parent, original_text, current_translation, 
                                     self.data[key]['description'])
        new_translation = dialog.result
        
        if new_translation is not None:
            self.translations[key] = new_translation
            self.edit_callback(key, new_translation)
            self.refresh_display()
            
    def copy_original(self):
        """Copy original text to clipboard."""
        selection = self.tree.selection()
        if not selection:
            return
            
        item = selection[0]
        key = self.get_key_from_item(item)
        if key:
            self.parent.clipboard_clear()
            self.parent.clipboard_append(self.data[key]['text'])
            
    def copy_translation(self):
        """Copy translation to clipboard."""
        selection = self.tree.selection()
        if not selection:
            return
            
        item = selection[0]
        key = self.get_key_from_item(item)
        if key and key in self.translations:
            self.parent.clipboard_clear()
            self.parent.clipboard_append(self.translations[key])
            
    def clear_selected(self):
        """Clear the selected translation."""
        selection = self.tree.selection()
        if not selection:
            return
            
        item = selection[0]
        key = self.get_key_from_item(item)
        if key and key in self.translations:
            del self.translations[key]
            self.edit_callback(key, '')
            self.refresh_display()
            
    def get_key_from_item(self, item) -> Optional[str]:
        """Get the localization key from a tree item."""
        return self.item_keys.get(item)
        
    def update_translation(self, key: str, translation: str):
        """Update a translation programmatically."""
        self.translations[key] = translation
        self.refresh_display()
        self.update_stats()
        
    def get_selected_keys(self) -> List[str]:
        """Get keys of selected items."""
        selection = self.tree.selection()
        keys = []
        
        for item in selection:
            key = self.get_key_from_item(item)
            if key:
                keys.append(key)
                
        return keys
        
    def select_all(self):
        """Select all items in the table."""
        for item in self.tree.get_children():
            self.tree.selection_add(item)
            
    def clear_translations(self):
        """Clear all translations."""
        self.translations.clear()
        self.refresh_display()

class TranslationEditDialog:
    """Dialog for editing translations."""
    
    def __init__(self, parent, original_text: str, current_translation: str, description: str):
        self.result = None
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Edit Translation")
        self.dialog.geometry("800x600")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
        
        self.setup_ui(original_text, current_translation, description)
        
    def setup_ui(self, original_text: str, current_translation: str, description: str):
        """Setup the dialog UI."""
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Description
        ttk.Label(main_frame, text="Context:", font=('TkDefaultFont', 9, 'bold')).pack(anchor=tk.W)
        desc_label = ttk.Label(main_frame, text=description, wraplength=750)
        desc_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Original text
        ttk.Label(main_frame, text="Original Text:", font=('TkDefaultFont', 9, 'bold')).pack(anchor=tk.W)
        orig_frame = ttk.Frame(main_frame)
        orig_frame.pack(fill=tk.X, pady=(0, 10))
        
        orig_text = tk.Text(orig_frame, height=4, wrap=tk.WORD, state='disabled')
        orig_scroll = ttk.Scrollbar(orig_frame, orient=tk.VERTICAL, command=orig_text.yview)
        orig_text.configure(yscrollcommand=orig_scroll.set)
        
        orig_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        orig_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Insert original text
        orig_text.config(state='normal')
        orig_text.insert('1.0', original_text)
        orig_text.config(state='disabled')
        
        # Translation text
        ttk.Label(main_frame, text="Translation:", font=('TkDefaultFont', 9, 'bold')).pack(anchor=tk.W)
        trans_frame = ttk.Frame(main_frame)
        trans_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.trans_text = tk.Text(trans_frame, height=8, wrap=tk.WORD)
        trans_scroll = ttk.Scrollbar(trans_frame, orient=tk.VERTICAL, command=self.trans_text.yview)
        self.trans_text.configure(yscrollcommand=trans_scroll.set)
        
        self.trans_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        trans_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Insert current translation
        if current_translation:
            self.trans_text.insert('1.0', current_translation)
            
        # Focus on translation text
        self.trans_text.focus_set()
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(button_frame, text="Cancel", command=self.cancel).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(button_frame, text="Save", command=self.save).pack(side=tk.RIGHT)
        
        # Bind Enter to save
        self.dialog.bind('<Control-Return>', lambda e: self.save())
        
    def save(self):
        """Save the translation."""
        self.result = self.trans_text.get('1.0', tk.END).strip()
        self.dialog.destroy()
        
    def cancel(self):
        """Cancel the edit."""
        self.result = None
        self.dialog.destroy()

class ProgressDialog:
    """Progress dialog for long-running operations."""
    
    def __init__(self, parent, title: str, message: str):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("400x150")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 100, parent.winfo_rooty() + 100))
        
        # Make dialog non-resizable
        self.dialog.resizable(False, False)
        
        self.setup_ui(message)
        
    def setup_ui(self, message: str):
        """Setup the progress dialog UI."""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Message
        self.message_label = ttk.Label(main_frame, text=message)
        self.message_label.pack(pady=(0, 20))
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(main_frame, mode='determinate', length=300)
        self.progress_bar.pack(pady=(0, 10))
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="Initializing...")
        self.status_label.pack()
        
    def update_progress(self, value: int, maximum: int, status: str = ""):
        """Update the progress bar and status."""
        self.progress_bar['maximum'] = maximum
        self.progress_bar['value'] = value
        
        if status:
            self.status_label.config(text=status)
            
        self.dialog.update()
        
    def close(self):
        """Close the dialog."""
        self.dialog.destroy()

class StyleSelector:
    """Widget for selecting translation style."""
    
    def __init__(self, parent, style_var: tk.StringVar):
        self.parent = parent
        self.style_var = style_var
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the style selector UI."""
        self.frame = ttk.LabelFrame(self.parent, text="Translation Style", padding="5")
        
        styles = {
            'formal': 'Professional, formal tone suitable for business applications',
            'conversational': 'Natural, conversational tone for user interactions',
            'chatbot': 'Friendly, helpful tone optimized for chatbot interactions'
        }
        
        for i, (style, description) in enumerate(styles.items()):
            rb = ttk.Radiobutton(self.frame, text=style.capitalize(), 
                               variable=self.style_var, value=style)
            rb.grid(row=i, column=0, sticky=tk.W, pady=2)
            
            desc_label = ttk.Label(self.frame, text=description, font=('TkDefaultFont', 8))
            desc_label.grid(row=i, column=1, sticky=tk.W, padx=(10, 0), pady=2)
            
    def grid(self, **kwargs):
        """Grid the frame."""
        self.frame.grid(**kwargs)

# Test the components
if __name__ == "__main__":
    root = tk.Tk()
    root.title("UI Components Test")
    root.geometry("1000x700")
    
    # Test data
    test_data = {
        'key1': {
            'text': 'Vänligen ge feedback på svaret:',
            'topic': 'Conversation Start',
            'ui_component': 'Card',
            'description': 'Feedback request in card component'
        },
        'key2': {
            'text': 'Ser bra ut',
            'topic': 'Conversation Start', 
            'ui_component': 'Button',
            'description': 'Positive feedback button'
        }
    }
    
    def on_edit(key, translation):
        print(f"Edited {key}: {translation}")
        
    # Test translation table
    table = TranslationTable(root, on_edit)
    table.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)
    table.load_data(test_data)
    
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    
    root.mainloop()