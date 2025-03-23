from tkinter import ttk
import tkinter as tk

class ThemeManager:
    # Modern color scheme
    COLORS = {
        'primary': '#2196F3',      # Blue
        'primary_dark': '#1976D2',  # Darker Blue for hover
        'primary_light': '#64B5F6', # Lighter Blue for active
        'secondary': '#FFC107',    # Amber
        'success': '#4CAF50',      # Green
        'success_dark': '#388E3C',  # Darker Green
        'danger': '#F44336',       # Red
        'danger_dark': '#D32F2F',  # Darker Red
        'warning': '#FF9800',      # Orange
        'info': '#00BCD4',         # Cyan
        'light': '#F5F5F5',        # Light Gray
        'dark': '#212121',         # Dark Gray
        'white': '#FFFFFF',
        'black': '#000000',
        'background': '#FAFAFA',
        'surface': '#FFFFFF',
        'button_text': '#2C3E50',  # Dark blue-gray for button text
        'button_hover': '#34495E',  # Darker blue-gray for hover
        'tab_active': '#1E88E5',   # Slightly darker blue for active tab
        'tab_inactive': '#E3F2FD', # Very light blue for inactive tabs
        'tab_hover': '#90CAF9',    # Light blue for hover state
    }

    # Process colors with good contrast
    PROCESS_COLORS = [
        '#2196F3',  # Blue
        '#4CAF50',  # Green
        '#F44336',  # Red
        '#9C27B0',  # Purple
        '#FF9800',  # Orange
        '#00BCD4',  # Cyan
        '#795548',  # Brown
        '#607D8B',  # Blue Gray
    ]

    @staticmethod
    def setup_theme():
        style = ttk.Style()
        
        # Configure main theme
        style.configure('.',
            background=ThemeManager.COLORS['background'],
            foreground=ThemeManager.COLORS['dark'],
            font=('Segoe UI', 10)
        )

        # Configure Notebook (tabs)
        style.configure('TNotebook',
            background=ThemeManager.COLORS['background'],
            tabmargins=[2, 5, 2, 0]
        )
        
        # Configure Notebook tabs with modern styling
        style.configure('TNotebook.Tab',
            padding=[15, 8],
            background=ThemeManager.COLORS['tab_inactive'],
            foreground=ThemeManager.COLORS['dark'],
            font=('Segoe UI', 10, 'bold'),
            borderwidth=1,
            relief='solid'
        )
        
        # Map different states for the tabs
        style.map('TNotebook.Tab',
            background=[
                ('selected', ThemeManager.COLORS['tab_active']),
                ('active', ThemeManager.COLORS['tab_hover'])
            ],
            foreground=[
                ('selected', ThemeManager.COLORS['white']),
                ('active', ThemeManager.COLORS['dark'])
            ],
            borderwidth=[
                ('selected', 0)
            ],
            relief=[
                ('selected', 'solid')
            ],
            padding=[
                ('selected', [15, 8])
            ]
        )

        # Configure Frames with slight shadow effect
        style.configure('TFrame',
            background=ThemeManager.COLORS['surface'],
            relief='solid',
            borderwidth=0
        )
        
        # Configure Labels
        style.configure('TLabel',
            background=ThemeManager.COLORS['surface'],
            foreground=ThemeManager.COLORS['dark'],
            font=('Segoe UI', 10)
        )
        
        # Configure Statistics Labels
        style.configure('Stats.TLabel',
            font=('Segoe UI', 11, 'bold'),
            foreground=ThemeManager.COLORS['dark'],
            padding=[10, 5]
        )

        # Configure Buttons with modern styling
        style.configure('TButton',
            background=ThemeManager.COLORS['surface'],
            foreground=ThemeManager.COLORS['button_text'],
            padding=[15, 8],
            font=('Segoe UI', 10, 'bold'),
            borderwidth=0,
            relief='flat'
        )
        
        # Button hover and pressed states
        style.map('TButton',
            background=[
                ('active', ThemeManager.COLORS['primary_light']),
                ('pressed', ThemeManager.COLORS['primary_dark'])
            ],
            foreground=[
                ('active', ThemeManager.COLORS['button_text']),
                ('pressed', ThemeManager.COLORS['white'])
            ],
            relief=[
                ('pressed', 'sunken'),
                ('!pressed', 'flat')
            ]
        )

        # Configure special button styles
        # Primary button
        style.configure('Primary.TButton',
            background=ThemeManager.COLORS['primary'],
            foreground=ThemeManager.COLORS['white']
        )
        style.map('Primary.TButton',
            background=[
                ('active', ThemeManager.COLORS['primary_dark']),
                ('pressed', ThemeManager.COLORS['primary_light'])
            ],
            foreground=[('pressed', ThemeManager.COLORS['white'])]
        )

        # Success button
        style.configure('Success.TButton',
            background=ThemeManager.COLORS['success'],
            foreground=ThemeManager.COLORS['white']
        )
        style.map('Success.TButton',
            background=[
                ('active', ThemeManager.COLORS['success_dark']),
                ('pressed', ThemeManager.COLORS['success'])
            ]
        )

        # Danger button
        style.configure('Danger.TButton',
            background=ThemeManager.COLORS['danger'],
            foreground=ThemeManager.COLORS['white']
        )
        style.map('Danger.TButton',
            background=[
                ('active', ThemeManager.COLORS['danger_dark']),
                ('pressed', ThemeManager.COLORS['danger'])
            ]
        )

        # Configure LabelFrames with subtle border
        style.configure('TLabelframe',
            background=ThemeManager.COLORS['surface'],
            font=('Segoe UI', 10, 'bold'),
            borderwidth=1,
            relief='solid'
        )
        style.configure('TLabelframe.Label',
            background=ThemeManager.COLORS['surface'],
            foreground=ThemeManager.COLORS['dark'],
            font=('Segoe UI', 11, 'bold')
        )

        # Configure Radiobuttons
        style.configure('TRadiobutton',
            background=ThemeManager.COLORS['surface'],
            foreground=ThemeManager.COLORS['dark'],
            font=('Segoe UI', 10)
        )
        style.map('TRadiobutton',
            background=[('active', ThemeManager.COLORS['light'])],
            foreground=[('active', ThemeManager.COLORS['dark'])]
        )

        # Configure Scale (slider) with modern look
        style.configure('TScale',
            background=ThemeManager.COLORS['surface'],
            troughcolor=ThemeManager.COLORS['primary_light'],
            sliderlength=20,
            sliderrelief='flat'
        )

    @staticmethod
    def get_process_color(index):
        return ThemeManager.PROCESS_COLORS[index % len(ThemeManager.PROCESS_COLORS)]