import tkinter as tk
import math
import sys
import os
from tkinter import ttk
from tkinter.messagebox import showinfo
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass
from translations import translations

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # When running from source, use the directory where the script is located
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

# Contents:
# Various:
#    Visual acuity conversion (-->VAC)
#    Snu cylinder (-->SC)
#    Beregn minimum diameter (-->MD)
#    Sfærisk ekvivalens (-->SE)
# Vertex:
#    Vertex distance calculator (-->VDC)
#    Vertex chart (-->VCH)
# Decentration:
#    Beregn prisme av desentrering (-->CD)
#    Antall mm desentrering som gir 0.5 prismedioptrier (-->MA)
# Price for glasses: (-->GP)
# Price for contact lenses: (-->CLP)
# General:
#    Distance converter (-->DIST)
#    Weight converter (-->WT)
#    Volume converter (-->VOL)
#    Temperature converter (-->TC)

current_language = 'no'
text_widgets = {}

header_font = ('Arial', 14, 'bold')
medium_font = ('Arial', 13, 'bold')
bold_font = ('Arial', 12, 'bold')
font_12 = ('Arial', 12)
bold_11 = ('Arial', 11, 'bold')
small_font = ('Arial', 11)
mini_font = ('Arial', 10)

root = tk.Tk()
root.configure(bg="#f0f0f0")
root.title(translations[current_language]['title'])
root.geometry('950x950+50+50')
root.minsize(200, 200)

root.withdraw()

# All this code just to make the window scrollable...
main_frame = tk.Frame(root, bg="#f0f0f0")
main_frame.pack(fill='both', expand=1)
# Create canvas with both scrollbars
canvas = tk.Canvas(main_frame, bg="#f0f0f0")
canvas.grid(row=0, column=0, sticky='nsew')
# Vertical scrollbar
v_scrollbar = ttk.Scrollbar(main_frame, orient='vertical', command=canvas.yview)
v_scrollbar.grid(row=0, column=1, sticky='ns')
# Horizontal scrollbar
h_scrollbar = ttk.Scrollbar(main_frame, orient='horizontal', command=canvas.xview)
h_scrollbar.grid(row=1, column=0, sticky='ew')
# Configure grid weights
main_frame.grid_rowconfigure(0, weight=1)
main_frame.grid_columnconfigure(0, weight=1)
# Configure canvas scroll commands
canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
window = tk.Frame(canvas, bg="#f0f0f0")
def _on_scroll(event):
    # Unified scroll handler for both mouse wheel and touchpad
    if event.delta:
        # Windows mouse wheel and touchpad
        canvas.yview_scroll(int(-1*(event.delta/90)), 'units')
    elif event.num == 4:
        # Linux scroll up
        canvas.yview_scroll(-1, 'units')
    elif event.num == 5:
        # Linux scroll down
        canvas.yview_scroll(1, 'units')
    else:
        # Fallback
        canvas.yview_scroll(-1, 'units')
def _on_horizontal_scroll(event):
    # Horizontal scroll handler
    if event.delta:
        # Windows mouse wheel and touchpad
        canvas.xview_scroll(int(-1*(event.delta/90)), 'units')
    elif event.num == 4:
        # Linux scroll left
        canvas.xview_scroll(-1, 'units')
    elif event.num == 5:
        # Linux scroll right
        canvas.xview_scroll(1, 'units')
    else:
        # Fallback
        canvas.xview_scroll(-1, 'units')
# Bind scroll events for different platforms
canvas.bind('<MouseWheel>', _on_scroll)  # Windows vertical scroll
canvas.bind('<Shift-MouseWheel>', _on_horizontal_scroll)  # Windows horizontal scroll
canvas.bind('<Button-4>', _on_scroll)    # Linux scroll up
canvas.bind('<Button-5>', _on_scroll)    # Linux scroll down
# Additional touchpad support - try multiple event types
try:
    canvas.bind('<Control-MouseWheel>', _on_horizontal_scroll)  # Ctrl+scroll for horizontal
    canvas.bind('<Alt-MouseWheel>', _on_horizontal_scroll)      # Alt+scroll for horizontal
    # Some touchpads use these events
    canvas.bind('<Button-6>', lambda e: canvas.yview_scroll(-1, 'units'))
    canvas.bind('<Button-7>', lambda e: canvas.yview_scroll(1, 'units'))
    # Try binding to the root window as well
    root.bind('<MouseWheel>', _on_scroll)
    root.bind('<Shift-MouseWheel>', _on_horizontal_scroll)
    root.bind('<Control-MouseWheel>', _on_horizontal_scroll)
    root.bind('<Alt-MouseWheel>', _on_horizontal_scroll)
except:
    pass
    
canvas.create_window((0,0), window=window, anchor='nw')

# Main frames
nav_frame = tk.Frame(window, bg="#f0f0f0")
nav_frame.grid(row=1, column=0, sticky='ew', pady=(10, 0), padx=50)
#
DIVframe = tk.Frame(window, bg="#f0f0f0")
DIVframe.grid(row=2, column=0, sticky='nsew', padx=30)
#
VERTEXframe = tk.Frame(window, bg="#f0f0f0")
VERTEXframe.grid(row=2, column=0, sticky='nsew', padx=30)
#
DESENTRERINGframe = tk.Frame(window, bg="#f0f0f0")
DESENTRERINGframe.grid(row=2, column=0, sticky='nsew', padx=30)
#
GLASSESPRICEframe = tk.Frame(window, bg="#f0f0f0")
GLASSESPRICEframe.grid(row=2, column=0, sticky='nsew', padx=30)
#
CLPRICEframe = tk.Frame(window, bg="#f0f0f0")
CLPRICEframe.grid(row=2, column=0, sticky='nsew', padx=30)
#
GENERALframe = tk.Frame(window, bg="#f0f0f0")
GENERALframe.grid(row=2, column=0, sticky='nsew', padx=30)

def show_frame(frame_to_show):
    for frame in [DIVframe, VERTEXframe, DESENTRERINGframe, GLASSESPRICEframe, CLPRICEframe, GENERALframe]:
        frame.grid_remove()
    frame_to_show.grid(row=2, column=0, sticky='nsew', pady=10, padx=30)
    if disclaimer_visible:
        disclaimer_frame.grid(row=3, column=0, sticky='ew', pady=(50, 0), padx=50)
    # Update scrollbar after frame change
    canvas.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox('all'))

# Frame toggle buttons
div_button = ttk.Button(nav_frame, text=translations[current_language]['diverse'], command=lambda: show_frame(DIVframe), style='Nav.TButton', width=12)
div_button.grid(row=0, column=0, sticky='ew', pady=(30, 0), padx=25, ipadx=15, ipady=10, rowspan=1)
#
vertex_button = ttk.Button(nav_frame, text=translations[current_language]['vertex'], command=lambda: show_frame(VERTEXframe), style='Nav.TButton', width=12)
vertex_button.grid(row=0, column=1, sticky='ew', pady=(30, 0), padx=25, ipadx=15, ipady=10, rowspan=1)
#
desentrering_button = ttk.Button(nav_frame, text=translations[current_language]['desentrering'], command=lambda: show_frame(DESENTRERINGframe), style='Nav.TButton', width=12)
desentrering_button.grid(row=0, column=2, sticky='ew', pady=(30, 0), padx=25, ipadx=15, ipady=10, rowspan=1)
#
glasses_price_button = ttk.Button(nav_frame, text=translations[current_language]['glasses_price'], command=lambda: show_frame(GLASSESPRICEframe), style='Nav.TButton', width=12)
glasses_price_button.grid(row=1, column=0, sticky='ew', pady=(10, 0), padx=25, ipadx=15, ipady=10, rowspan=1)
#
cl_price_button = ttk.Button(nav_frame, text=translations[current_language]['cl_price'], command=lambda: show_frame(CLPRICEframe), style='Nav.TButton', width=12)
cl_price_button.grid(row=1, column=1, sticky='ew', pady=(10, 0), padx=25, ipadx=15, ipady=10, rowspan=1)
#
general_button = ttk.Button(nav_frame, text=translations[current_language]['general'], command=lambda: show_frame(GENERALframe), style='Nav.TButton', width=12)
general_button.grid(row=1, column=2, sticky='ew', pady=(10, 0), padx=25, ipadx=15, ipady=10, rowspan=1)
#
language_frame = tk.Frame(nav_frame, bg="#f0f0f0", height=100)
language_frame.grid(row=0, column=3, sticky='n', pady=13, padx=5, ipadx=5, ipady=5, rowspan=2)
# Language buttons in nav_frame
no_button = ttk.Button(language_frame, text="NO", command=lambda: change_language('no'), width=4)
en_button = ttk.Button(language_frame, text="EN", command=lambda: change_language('en'), width=4)
no_button.grid(row=0, column=0, padx=2, pady=(26, 0))
en_button.grid(row=1, column=0, padx=2, pady=2)

def change_language(language_code):
    global current_language
    current_language = language_code
    update_all_texts()
    # Update scrollbar after language change
    canvas.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox('all'))

def update_all_texts():      # update all text widgets when language changes
    global text_widgets
    lang = translations[current_language]
    # Update main window and navigation
    root.title(lang['title'])
    div_button.config(text=lang['diverse'])
    vertex_button.config(text=lang['vertex'])
    desentrering_button.config(text=lang['desentrering'])
    glasses_price_button.config(text=lang['glasses_price'])
    cl_price_button.config(text=lang['cl_price'])
    general_button.config(text=lang['general'])
    hide_disclaimer_button.config(text=lang['hide_disclaimer'])
    show_disclaimer_button.config(text=lang['show_disclaimer'])
    # Update main UI widgets using grouped approach
    widget_updates = [
        # SC section
        (SC_header, 'SC_header'), (SC_t1, 'sphere'), (SC_t2, 'cylinder'), (SC_t3, 'axis'), (SCknapp, 'calculate'), (SCretninglabel, 'direction'), (SCpluss_mot_minus, 'SC_plus_to_minus'), (SCminus_mot_pluss, 'SC_minus_to_plus'),
        # MD section
        (MD_header, 'MD_header'), (MD_bin_pd, 'bin_pd'), (MD_a_measure, 'a_measure'), (MD_bridge, 'bridge'), (MDknapp, 'calculate'), (MD_footer, 'MD_footer'),
        # SE section
        (SE_header, 'SE_header'), (SE_sphere, 'sphere'), (SE_cylinder, 'cylinder'), (SE_footer, 'SE_footer'), (SEknapp, 'calculate'),
        # DIST section
        (DIST_header, 'DIST_header'), (DIST_mm, 'mm'), (DIST_cm, 'cm'), (DIST_m, 'm'), (DIST_in, 'inches'), (DIST_ft, 'feet'), (DIST_ft_i, 'feet_and_inches'), (DIST_footer, 'DIST_footer'),
        # VDC section
        (VDC_header, 'VDC_header'), (VDC_sphere, 'sphere'), (VDC_cylinder, 'cylinder'), (VDC_axis, 'axis'), (VDC_mm, 'mm'), (VDC_knapp, 'calculate'), (VDC_footer1, 'VDC_footer1'), (VDC_footer2, 'VDC_footer2'),
        # VCH section
        (VCH_header, 'VCH_header'),
        (VCH_from_prescription, 'from_prescription'), (VCH_to_prescription, 'to_prescription'), (VCH_mm_amount, 'mm_amount'), (VCH_footer, 'VCH_footer'), (vchart_button, 'VCH_button'),
        # CD section
        (CD_header, 'CD_header'), (CD_sphere, 'sphere'), (CD_cylinder, 'cylinder'), (CD_mm_desentration, 'mm_decentration'), (CD_prisms, 'prisms'), (CD_footer1, 'CD_footer1'), (CD_footer2, 'CD_footer2'),
        # MA section
        (MA_header, 'MA_header'), (MA_sphere, 'sphere'), (MA_cylinder, 'cylinder'), (MAknapp, 'calculate'), (MA_footer, 'MA_footer')
    ]
    # Special cases with custom formatting
    SC_adjusted_correction.config(text=f'{lang["adjusted_correction"]}:')
    MD_frame.config(text=f'{lang["frame"]}:')
    MD_estimated_minimum_diameter.config(text=f'{lang["estimated_minimum_diameter"]}:')
    SE_spherical_equivalent.config(text=f'{lang["spherical_equivalent"]}:')
    VDC_adjusted_correction.config(text=f'{lang["adjusted_correction"]}:')
    VDC_equivalent.config(text=f'{lang["equivalent"]}:')
    MA_mm_amount.config(text=f'{lang["mm_amount"]}:')
    #MA_total.config(text=f'{lang["bin_mm_amount"]}:')
    # Update widgets using loop
    for widget, translation_key in widget_updates:
        widget.config(text=lang[translation_key])
    # Update disclaimer text
    text.config(state='normal')
    text.delete('1.0', 'end')
    text.insert('1.0', lang['disclaimer_text'])
    text.config(state='disabled')
    # Update text widgets made in functions using grouped approach
    widget_groups = {
        'invalid_input': ['SC_invalid_input', 'SC_invalid_input2', 'MD_invalid_input', 'SE_invalid_input', 'SE_invalid_input2', 'DIST_invalid_input',
                         'VDC_invalid_input', 'VDC_invalid_input2', 'VCH_invalid_input', 
                         'CD_error', 'MA_error', 'MA_error2'],
        'choose_direction': ['SC_choose_direction', 'SC_choose_direction2'],
        'SC_cyl_must_be_positive': ['SC_cyl_must_be_positive', 'SC_cyl_must_be_positive2'],
        'SC_cyl_must_be_negative': ['SC_cyl_must_be_negative', 'SC_cyl_must_be_negative2'],
        'minus': ['VCH_minus'],
        'number': ['VCH_number'],
        'plus': ['VCH_plus'],
        'prescription_outside_range': ['VCH_prescription_outside_range', 'VDC_outside_range', 'VDC_outside_range2'],
        'MA_null': ['MA_null', 'MA_null2', 'MA_bin_null']
    }
    for translation_key, widget_keys in widget_groups.items():
        for widget_key in widget_keys:
            try:
                text_widgets[widget_key].config(text=lang[translation_key])
            except:
                pass
    for GP_instance in GP_instances:
        GP_instance.update_texts()
    for CLP_instance in CLP_instances:
        CLP_instance.update_texts()
    visual_acuity_conversion.update_texts()
    weight_converter.update_texts()
    volume_converter.update_texts()
    temperature_converter.update_texts()

# Style for navigation buttons++
ttk.Style().configure('Nav.TButton', font=('Arial', 12, 'bold'))      
ttk.Style().configure('SmallNav.TButton', font=('Arial', 11, 'bold'))   

# Style for reset buttons++
style = ttk.Style()
style.configure('Bold.TButton', 
               font=('Arial', 10, 'bold'),
               background='#f0f0f0',
               foreground='#333333')

# Less contrast entry field++
ttk.Style().configure('Custom.TEntry', fieldbackground='#666666')

           

try:      # load icon and image
    root.iconbitmap(resource_path('logo.ico'))
except:
    pass
try:
    photo = tk.PhotoImage(file=resource_path('logo.png'))
    root.iconphoto(False, photo)
except:
    photo = None
if photo:    # load top-right picture
    image = ttk.Label(nav_frame, image=photo, padding=10)
    image.grid(row=0, column=5, sticky='ne', padx=(10, 0), pady=(10, 0), rowspan=2)

def filter_value(var):      # filter input values for commas, bad input
    value = var.get()
    if value.strip() == "":
        return 0.0
    if ',' in value:
        value = value.replace(',', '.')
    try:
        return float(value)
    except ValueError:
        return None

def filter_fraction(var):
    value = var.get()
    try:
        split_fraction = value.split('/')
        if len(split_fraction) != 2:
            return None
        if split_fraction[0].strip() == "" or split_fraction[1].strip() == "":
            return None
        if split_fraction[1].strip() == "0":
            return None
        return (float(split_fraction[0]), float(split_fraction[1]))
    except ValueError:
        return None
    return None

def update_scrollbar():
    canvas.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox('all'))

class CalculatorSection: # Parent class for calculator sections (-->CLASS)
    def __init__(self, parent, title_key, row):
        self.parent = parent
        self.title_key = title_key
        self.row = row
        self.frame = None
        self.values = []
        self.holders = []
        self.labels = []
        self.create_frame()
        self.create_header()
        self.create_reset_button()
#        self.create_content()
#        self.create_footer()
#        self.update_texts()

    def create_frame(self):
        self.frame = tk.Frame(self.parent, height=200, width=700, borderwidth=3, relief='groove', bg="#E9E9E9")
        self.frame.grid(row=self.row, column=0, sticky='nsew', pady=10, padx=30)

    def create_header(self):
        self.header = tk.Label(self.frame, text=f'{translations[current_language][self.title_key]}', font=header_font, bg="#E9E9E9")
        self.header.place(x=20, y=10)

    def update_texts(self):
        lang = translations[current_language]
        self.header.config(text=lang[self.title_key])
        try:
            if self.invalid_input:
                self.invalid_input.config(text=f'{translations[current_language]["invalid_input"]}')
        except:
            pass
        for label, type in self.labels:
            label.config(text=f'{lang[type]}')

    def create_reset_button(self):
        self.reset_button = ttk.Button(self.frame, text="C", command=self.reset, width=3, style='Bold.TButton')
        self.reset_button.place(x=652, y=8)

    def reset(self):
        for holder in self.holders:
            holder.set("")
        for value in self.values:
            value = 0
        try:
            if self.invalid_input:
                self.invalid_input.destroy()
        except:
            pass
    



#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Visual acuity conversion (-->VAC)

class VisualAcuityConversion(CalculatorSection):
    def __init__(self, parent, title_key, row):
        super().__init__(parent, title_key, row)
        self.snellen_decimal = 0
        self.snellen_decimal_holder = tk.StringVar()
        self.snellen_fraction_meter = 0
        self.snellen_fraction_meter_holder = tk.StringVar()
        self.snellen_fraction_foot = 0
        self.snellen_fraction_foot_holder = tk.StringVar()
        self.logmar = 0
        self.logmar_holder = tk.StringVar()
        self.values = [self.snellen_decimal, self.snellen_fraction_meter, self.snellen_fraction_foot, self.logmar]
        self.holders = [self.snellen_decimal_holder, self.snellen_fraction_meter_holder, self.snellen_fraction_foot_holder, self.logmar_holder]
        self.create_labels()
        self.create_entries()
        self.update_texts()

    def create_labels(self):
        self.snellen_decimal_label = tk.Label(self.frame, text=f'{translations[current_language]["Snellen decimal"]}', bg="#E9E9E9", font=small_font)
        self.snellen_decimal_label.place(x=35, y=65)
        self.labels.append((self.snellen_decimal_label, 'Snellen decimal'))
        self.snellen_fraction_meter_label = tk.Label(self.frame, text=f'{translations[current_language]["Snellen fraction meter"]}', bg="#E9E9E9", font=small_font)
        self.snellen_fraction_meter_label.place(x=185, y=65)
        self.labels.append((self.snellen_fraction_meter_label, 'Snellen fraction meter'))
        self.snellen_fraction_foot_label = tk.Label(self.frame, text=f'{translations[current_language]["Snellen fraction foot"]}', bg="#E9E9E9", font=small_font)
        self.snellen_fraction_foot_label.place(x=350, y=65)
        self.labels.append((self.snellen_fraction_foot_label, 'Snellen fraction foot'))
        self.logmar_label = tk.Label(self.frame, text=f'{translations[current_language]["LogMAR"]}', bg="#E9E9E9", font=small_font)
        self.logmar_label.place(x=538, y=65)
        self.labels.append((self.logmar_label, 'LogMAR'))
        self.footer = tk.Label(self.frame, text=f'{translations[current_language]["VAC_footer"]}', font=mini_font, bg="#E9E9E9")
        self.footer.place(x=220, y=165)
        self.labels.append((self.footer, 'VAC_footer'))

    def create_entries(self):
        self.snellen_decimal_entry = ttk.Entry(self.frame, textvariable=self.snellen_decimal_holder, justify='right', font=bold_font)
        self.snellen_decimal_entry.place(x=50, y=105, width=95)
        self.snellen_decimal_entry.bind('<Return>', lambda event: self.convert(self.snellen_decimal_holder, 'decimal'))
        self.snellen_fraction_meter_entry = ttk.Entry(self.frame, textvariable=self.snellen_fraction_meter_holder, justify='right', font=bold_font)
        self.snellen_fraction_meter_entry.place(x=210, y=105, width=95)
        self.snellen_fraction_meter_entry.bind('<Return>', lambda event: self.convert(self.snellen_fraction_meter_holder, 'fraction_meter'))
        self.snellen_fraction_foot_entry = ttk.Entry(self.frame, textvariable=self.snellen_fraction_foot_holder, justify='right', font=bold_font)
        self.snellen_fraction_foot_entry.place(x=370, y=105, width=95)
        self.snellen_fraction_foot_entry.bind('<Return>', lambda event: self.convert(self.snellen_fraction_foot_holder, 'fraction_foot'))
        self.logmar_entry = ttk.Entry(self.frame, textvariable=self.logmar_holder, justify='right', font=bold_font)
        self.logmar_entry.place(x=530, y=105, width=95)
        self.logmar_entry.bind('<Return>', lambda event: self.convert(self.logmar_holder, 'logmar'))

    def convert(self, input, type):
        try:
            if self.invalid_input:
                self.invalid_input.destroy()
        except:
            pass
        if type == 'decimal' or type == 'logmar':
            filtered_input = filter_value(input)
        else:
            filtered_input = filter_fraction(input)
        if filtered_input is None:
            self.invalid_input = tk.Label(self.frame, text=f'{translations[current_language]["invalid_input"]}', width=19, font=('Arial', 13, 'bold'), bg="#E9E9E9")
            self.invalid_input.place(x=400, y=30)
            return
        if type == 'decimal':
            snellen_decimal = filtered_input
        elif type == 'logmar':
            snellen_decimal = 10 ** (-1 * filtered_input)
        else:
            snellen_decimal = filtered_input[0] / filtered_input[1]
        self.snellen_decimal_holder.set(f'{round(snellen_decimal, 2)}')
        if type != 'fraction_meter':
            denominator_meter = 6 / snellen_decimal
            if denominator_meter % 1 == 0:
                self.snellen_fraction_meter_holder.set(f'6/{int(denominator_meter)}')
            else:
                self.snellen_fraction_meter_holder.set(f'6/{round(denominator_meter, 1)}')
        if type != 'fraction_foot':
            denominator_foot = 20 / snellen_decimal
            if denominator_foot % 1 == 0:
                self.snellen_fraction_foot_holder.set(f'20/{int(denominator_foot)}')
            else:
                self.snellen_fraction_foot_holder.set(f'20/{round(denominator_foot, 1)}')
        self.logmar_holder.set(f'{round(math.log10(1/snellen_decimal), 2)}')

visual_acuity_conversion = VisualAcuityConversion(DIVframe, "VAC_header", 0)
    

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Snu cylinder (-->SC)
SCframe = tk.Frame(DIVframe, height=200, width=700, borderwidth=3, relief='groove', bg="#E9E9E9")
#borderwidth=3, relief='groove'
SCframe.grid(row=1, column=0, sticky='nsew', pady=10, padx=30)

SC_header = tk.Label(SCframe, text=f'{translations[current_language]["SC_header"]}', font=header_font, bg="#E9E9E9")
SC_header.place(x=20, y=10)
SC_t1 = tk.Label(SCframe, text=f'{translations[current_language]["sphere"]}', bg="#E9E9E9", font=mini_font)
SC_t1.place(x=23, y=53)
SC_t2 = tk.Label(SCframe, text=f'{translations[current_language]["cylinder"]}', bg="#E9E9E9", font=mini_font)
SC_t2.place(x=88, y=53)
SC_t3 = tk.Label(SCframe, text=f'{translations[current_language]["axis"]}', bg="#E9E9E9", font=mini_font)
SC_t3.place(x=154, y=53)
SC_adjusted_correction = tk.Label(SCframe, text=f'{translations[current_language]["adjusted_correction"]}:', width=17, font=bold_font, bg="#E9E9E9")
SC_adjusted_correction.place(x=460, y=49)


SCsphere = 0
SCcylinder = 0
SCaxis = None
SCretning = tk.StringVar()
SCsphereholder = tk.StringVar()
SCcylinderholder = tk.StringVar()
SCaxisholder = tk.StringVar()
SCsphere_entry = ttk.Entry(SCframe, textvariable=SCsphereholder, justify='right')
SCsphere_entry.place(x=20, y=80, width=72)
SCcylinder_entry = ttk.Entry(SCframe, textvariable=SCcylinderholder, justify='right')
SCcylinder_entry.place(x=95, y=80, width=56)
SCaxis_entry = ttk.Entry(SCframe, textvariable=SCaxisholder, justify='right')
SCaxis_entry.place(x=154, y=80, width=48)

# Second set of StringVars
SCsphereholder2 = tk.StringVar()
SCcylinderholder2 = tk.StringVar()
SCaxisholder2 = tk.StringVar()

# Second set of Entry widgets
SCsphere_entry2 = ttk.Entry(SCframe, textvariable=SCsphereholder2, justify='right')
SCsphere_entry2.place(x=20, y=112, width=72)
SCcylinder_entry2 = ttk.Entry(SCframe, textvariable=SCcylinderholder2, justify='right')
SCcylinder_entry2.place(x=95, y=112, width=56)
SCaxis_entry2 = ttk.Entry(SCframe, textvariable=SCaxisholder2, justify='right')
SCaxis_entry2.place(x=154, y=112, width=48)

# Direction widget
SCretninglabel = tk.LabelFrame(SCframe, text=f'{translations[current_language]["direction"]}', width=240, height=90, bg="#E9E9E9", font=mini_font)
SCretninglabel.place(x=210, y=55)

# Create custom style for radiobuttons
style = ttk.Style()
style.configure('Custom.TRadiobutton', background="#E9E9E9", font=mini_font)

SCpluss_mot_minus = ttk.Radiobutton(SCretninglabel, text=f'{translations[current_language]["SC_plus_to_minus"]}', value='pluss_mot_minus', variable=SCretning, style='Custom.TRadiobutton')
SCpluss_mot_minus.place(x=0, y=4)
SCminus_mot_pluss = ttk.Radiobutton(SCretninglabel, text=f'{translations[current_language]["SC_minus_to_plus"]}', value='minus_mot_pluss', variable=SCretning, style='Custom.TRadiobutton')
SCminus_mot_pluss.place(x=0, y=35)

def snu_cylinder(sphereholder, cylinderholder, axisholder, y_result=80):
    global text_widgets
    sphere = filter_value(sphereholder)
    cylinder = filter_value(cylinderholder)
    axis = filter_value(axisholder)
    
    # Check if any value is None (invalid input)
    if sphere is None or cylinder is None or axis is None:
        if y_result == 108:
            text_widgets['SC_invalid_input2'] = tk.Label(SCframe, text=f'{translations[current_language]["invalid_input"]}', width=17, font=('Arial', 13, 'bold'), bg="#E9E9E9")
            text_widgets['SC_invalid_input2'].place(x=450, y=y_result)
            return
        text_widgets['SC_invalid_input'] = tk.Label(SCframe, text=f'{translations[current_language]["invalid_input"]}', width=17, font=('Arial', 13, 'bold'), bg="#E9E9E9")
        text_widgets['SC_invalid_input'].place(x=450, y=y_result)
        return
    
    maxis = (axis + 90) % 180
    if not SCretning.get():
        if y_result == 108:
            text_widgets['SC_choose_direction2'] = tk.Label(SCframe, text=f'{translations[current_language]["choose_direction"]}', width=17, font=('Arial', 13, 'bold'), bg="#E9E9E9")
            text_widgets['SC_choose_direction2'].place(x=450, y=y_result)
            return
        text_widgets['SC_choose_direction'] = tk.Label(SCframe, text=f'{translations[current_language]["choose_direction"]}', width=17, font=('Arial', 13, 'bold'), bg="#E9E9E9")
        text_widgets['SC_choose_direction'].place(x=450, y=y_result)
        return
    if not cylinder:
        result = f'{"+" if sphere >= 0 else ""}{sphere:.2f}'
        tk.Label(SCframe, text=result, width=17, font=('Arial', 13, 'bold'), bg="#E9E9E9").place(x=450, y=y_result)
        return
    if SCretning.get() == 'pluss_mot_minus' and cylinder < 0:
        if y_result == 108:
            text_widgets['SC_cyl_must_be_positive2'] = tk.Label(SCframe, text=f'{translations[current_language]["SC_cyl_must_be_positive"]}', width=17, font=('Arial', 13, 'bold'), bg="#E9E9E9")
            text_widgets['SC_cyl_must_be_positive2'].place(x=450, y=y_result)
            return
        text_widgets['SC_cyl_must_be_positive'] = tk.Label(SCframe, text=f'{translations[current_language]["SC_cyl_must_be_positive"]}', width=17, font=('Arial', 13, 'bold'), bg="#E9E9E9")
        text_widgets['SC_cyl_must_be_positive'].place(x=450, y=y_result)
        return
    if SCretning.get() == 'minus_mot_pluss' and cylinder > 0:
        if y_result == 108:
            text_widgets['SC_cyl_must_be_negative2'] = tk.Label(SCframe, text=f'{translations[current_language]["SC_cyl_must_be_negative"]}', width=17, font=('Arial', 13, 'bold'), bg="#E9E9E9")
            text_widgets['SC_cyl_must_be_negative2'].place(x=450, y=y_result)
            return
        text_widgets['SC_cyl_must_be_negative'] = tk.Label(SCframe, text=f'{translations[current_language]["SC_cyl_must_be_negative"]}', width=17, font=('Arial', 13, 'bold'), bg="#E9E9E9")
        text_widgets['SC_cyl_must_be_negative'].place(x=450, y=y_result)
        return
    msphere = sphere + cylinder
    mcylinder = -1 * cylinder
    tk.Label(SCframe, text=f'{"+" if msphere > 0 else ""}{msphere:.2f}/{"+" if mcylinder > 0 else ""}{mcylinder:.2f}x{int(maxis)}', width=17, font=('Arial', 13, 'bold'), bg="#E9E9E9").place(x=450, y=y_result)
    return

def run_both_snu_cylinder():
    snu_cylinder(SCsphereholder, SCcylinderholder, SCaxisholder, 76)
    snu_cylinder(SCsphereholder2, SCcylinderholder2, SCaxisholder2, 108)

SCknapp = ttk.Button(SCframe, text=translations[current_language]["calculate"], command=run_both_snu_cylinder, style='Nav.TButton')
SCknapp.place(x=50, y=150, height=37, width=150)

for entry in [SCsphere_entry, SCcylinder_entry, SCaxis_entry, SCsphere_entry2, SCcylinder_entry2, SCaxis_entry2]:
    entry.bind('<Return>', lambda event: run_both_snu_cylinder())

def reset_snu_cylinder():
    SCsphereholder.set("")
    SCcylinderholder.set("")
    SCaxisholder.set("")
    SCsphereholder2.set("")
    SCcylinderholder2.set("")
    SCaxisholder2.set("")
    tk.Label(SCframe, text="", width=19, font=('Arial', 13, 'bold'), bg="#E9E9E9").place(x=450, y=76)
    tk.Label(SCframe, text="", width=19, font=('Arial', 13, 'bold'), bg="#E9E9E9").place(x=450, y=108)

reset_snu_cylinder_knapp = ttk.Button(SCframe, text="C", command=reset_snu_cylinder, width=3, style='Bold.TButton')
reset_snu_cylinder_knapp.place(x=652, y=8)


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Minimum diameter (-->MD)
MDframe = tk.Frame(DIVframe, height=200, width=700, borderwidth=3, relief='groove', bg="#E9E9E9")
MDframe.grid(row=2, column=0, sticky='nsew', pady=10, padx=30)
MD_header = tk.Label(MDframe, text=f'{translations[current_language]["MD_header"]}', font=header_font, bg="#E9E9E9")
MD_header.place(x=20, y=10)
MD_bin_pd = tk.Label(MDframe, text=f'{translations[current_language]["bin_pd"]}', bg="#E9E9E9", font=small_font)
MD_bin_pd.place(x=30, y=55)
MD_frame = tk.Label(MDframe, text=f'{translations[current_language]["frame"]}:', bg="#E9E9E9", font=small_font)
MD_frame.place(x=117, y=55)
MD_a_measure = tk.Label(MDframe, text=f'{translations[current_language]["a_measure"]}', bg="#E9E9E9", font=small_font)
MD_a_measure.place(x=205, y=55)
MD_bridge = tk.Label(MDframe, text=f'{translations[current_language]["bridge"]}', bg="#E9E9E9", font=small_font)
MD_bridge.place(x=278, y=55)
MD_estimated_minimum_diameter = tk.Label(MDframe, text=f'{translations[current_language]["estimated_minimum_diameter"]}:', width=25, font=bold_font, bg="#E9E9E9")
MD_estimated_minimum_diameter.place(x=360, y=55)

MDpd = 0
MDbredde = 0
MDbro = 0
MDpdholder = tk.StringVar()
MDbreddeholder = tk.StringVar()
MDbroholder = tk.StringVar()

MDpd_entry = ttk.Entry(MDframe, textvariable=MDpdholder, justify='right', font=small_font)
MDpd_entry.place(x=40, y=87, width=48)
MDbredde_entry = ttk.Entry(MDframe, textvariable=MDbreddeholder, justify='right', font=small_font)
MDbredde_entry.place(x=205, y=87, width=60)
MDbro_entry = ttk.Entry(MDframe, textvariable=MDbroholder, justify='right', font=small_font)
MDbro_entry.place(x=280, y=87, width=48)

def minimum_diameter(pdholder, breddeholder, broholder):
    global text_widgets
    pd = filter_value(pdholder)
    bredde = filter_value(breddeholder)
    bro = filter_value(broholder)

    if pd is None or bredde is None or bro is None or pd < 0 or bredde < 0 or bro < 0:
        text_widgets['MD_invalid_input'] = tk.Label(MDframe, text=f'{translations[current_language]["invalid_input"]}', width=19, font=bold_font, bg="#E9E9E9")
        text_widgets['MD_invalid_input'].place(x=400, y=85)
        return
    result = f"{(bredde + bredde + bro + 4) - pd:.1f} mm"
    if result == "4.0 mm":
        return
    tk.Label(MDframe, text=result, width=19, font=bold_font, bg="#E9E9E9").place(x=400, y=85)
    return

MDknapp = ttk.Button(MDframe, text=translations[current_language]["calculate"], command=lambda: minimum_diameter(MDpdholder, MDbreddeholder, MDbroholder), style='Nav.TButton')
MDknapp.place(x=50, y=124, height=37, width=150)

for entry in [MDpd_entry, MDbredde_entry, MDbro_entry]:
    entry.bind('<Return>', lambda event: minimum_diameter(MDpdholder, MDbreddeholder, MDbroholder))

def reset_minimum_diameter():
    MDpdholder.set("")
    MDbreddeholder.set("")
    MDbroholder.set("")
    tk.Label(MDframe, text="", width=19, font=('Arial', 13, 'bold'), bg="#E9E9E9").place(x=400, y=90)

reset_minimum_diameter_knapp = ttk.Button(MDframe, text="C", command=reset_minimum_diameter, width=3, style='Bold.TButton')
reset_minimum_diameter_knapp.place(x=652, y=8)



MD_footer = tk.Label(MDframe, text=f'{translations[current_language]["MD_footer"]}', font=mini_font, bg="#E9E9E9")
MD_footer.place(x=8, y=165)





#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Sfærisk ekvivalent (-->SE)
SEframe = tk.Frame(DIVframe, height=200, width=700, borderwidth=3, relief='groove', bg="#E9E9E9")
SEframe.grid(row=3, column=0, sticky='nsew', pady=10, padx=30)
SE_header = tk.Label(SEframe, text=f'{translations[current_language]["SE_header"]}', font=header_font, bg="#E9E9E9")
SE_header.place(x=20, y=10)
SE_sphere = tk.Label(SEframe, text=f'{translations[current_language]["sphere"]}', bg="#E9E9E9", font=small_font)
SE_sphere.place(x=77, y=45)
SE_cylinder = tk.Label(SEframe, text=f'{translations[current_language]["cylinder"]}', bg="#E9E9E9", font=small_font)
SE_cylinder.place(x=165, y=45)
SE_spherical_equivalent = tk.Label(SEframe, text=f'{translations[current_language]["spherical_equivalent"]}:', bg="#E9E9E9", font=bold_font)
SE_spherical_equivalent.place(x=355, y=45)

SEsphere = 0
SEcylinder = 0
SEsphereholder = tk.StringVar()
SEcylinderholder = tk.StringVar()
SEsphere_entry = ttk.Entry(SEframe, textvariable=SEsphereholder, justify='right', font=bold_font)
SEsphere_entry.place(x=60, y=75, width=95)
SEcylinder_entry = ttk.Entry(SEframe, textvariable=SEcylinderholder, justify='right', font=bold_font)
SEcylinder_entry.place(x=165, y=75, width=75)

# Second set of StringVars
SEsphereholder2 = tk.StringVar()
SEcylinderholder2 = tk.StringVar()

# Second set of Entry widgets
SEsphere_entry2 = ttk.Entry(SEframe, textvariable=SEsphereholder2, justify='right', font=bold_font)
SEsphere_entry2.place(x=60, y=107, width=95)
SEcylinder_entry2 = ttk.Entry(SEframe, textvariable=SEcylinderholder2, justify='right', font=bold_font)
SEcylinder_entry2.place(x=165, y=107, width=75)

for entry in [SEsphere_entry, SEcylinder_entry, SEsphere_entry2, SEcylinder_entry2]:
    entry.bind('<Return>', lambda event: run_both_SE(SEsphereholder, SEcylinderholder, SEsphereholder2, SEcylinderholder2))

def SE(sphereholder, cylinderholder, y_result):
    global text_widgets
    sphere = filter_value(sphereholder)
    cylinder = filter_value(cylinderholder)
    if sphere is None or cylinder is None:
        if y_result == 107:
            text_widgets['SE_invalid_input2'] = tk.Label(SEframe, text=f'{translations[current_language]["invalid_input"]}', width=19, font=('Arial', 13, 'bold'), bg="#E9E9E9")
            text_widgets['SE_invalid_input2'].place(x=340, y=y_result)
            return
        text_widgets['SE_invalid_input'] = tk.Label(SEframe, text=f'{translations[current_language]["invalid_input"]}', width=19, font=('Arial', 13, 'bold'), bg="#E9E9E9")
        text_widgets['SE_invalid_input'].place(x=340, y=y_result)
        return
    if cylinder == 0:
        result = f"{"+" if sphere > 0 else ""}{float(sphere):.2f}"
        tk.Label(SEframe, text=result, width=20, font=('Arial', 13, 'bold'), bg="#E9E9E9").place(x=310, y=y_result)
        return
    result = f"{"+" if (sphere + (cylinder / 2)) > 0 else ""}{(sphere + (cylinder / 2)):.2f}"
    tk.Label(SEframe, text=result, width=20, font=('Arial', 13, 'bold'), bg="#E9E9E9").place(x=310, y=y_result)
    return

def run_both_SE(SEsphereholder, SEcylinderholder, SEsphereholder2, SEcylinderholder2):
    SE(SEsphereholder, SEcylinderholder, 75)
    SE(SEsphereholder2, SEcylinderholder2, 107)

SEknapp = ttk.Button(SEframe, text=translations[current_language]["calculate"], command=lambda: run_both_SE(SEsphereholder, SEcylinderholder, SEsphereholder2, SEcylinderholder2), style='Nav.TButton')
SEknapp.place(x=70, y=151, height=37, width=150)

def reset_SE():
    global text_widgets
    # Destroy text widgets using grouped approach
    widget_keys = ['SE_invalid_input', 'SE_invalid_input2']
    for widget_key in widget_keys:
        try:
            if text_widgets[widget_key]:
                text_widgets[widget_key].destroy()
        except:
            pass
    # Clear input fields
    SEsphereholder.set("")
    SEcylinderholder.set("")
    SEsphereholder2.set("")
    SEcylinderholder2.set("")
    # Clear result labels
    tk.Label(SEframe, text="", width=19, font=('Arial', 13, 'bold'), bg="#E9E9E9").place(x=310, y=83)
    tk.Label(SEframe, text="", width=19, font=('Arial', 13, 'bold'), bg="#E9E9E9").place(x=310, y=115)

reset_SE_knapp = ttk.Button(SEframe, text="C", command=reset_SE, width=3, style='Bold.TButton')
reset_SE_knapp.place(x=652, y=8)


SE_footer = tk.Label(SEframe, text=f'{translations[current_language]["SE_footer"]}', font=mini_font, bg="#E9E9E9")
SE_footer.place(x=280, y=169)



#VERTEX-------------------------------------------------------------------------------------------
#VERTEX-------------------------------------------------------------------------------------------
#VERTEX-------------------------------------------------------------------------------------------
#VERTEX-------------------------------------------------------------------------------------------
#VERTEX-------------------------------------------------------------------------------------------
#VERTEX-------------------------------------------------------------------------------------------
#VERTEX-------------------------------------------------------------------------------------------
#VERTEX-------------------------------------------------------------------------------------------
#VERTEX-------------------------------------------------------------------------------------------
#VERTEX-------------------------------------------------------------------------------------------
#VERTEX-------------------------------------------------------------------------------------------
#VERTEX-------------------------------------------------------------------------------------------
#VERTEX-------------------------------------------------------------------------------------------
#VERTEX-------------------------------------------------------------------------------------------
#VERTEX-------------------------------------------------------------------------------------------
#VERTEX-------------------------------------------------------------------------------------------
#VERTEX-------------------------------------------------------------------------------------------
#VERTEX-------------------------------------------------------------------------------------------
#VERTEX-------------------------------------------------------------------------------------------
#VERTEX-------------------------------------------------------------------------------------------
#VERTEX-------------------------------------------------------------------------------------------
#VERTEX-------------------------------------------------------------------------------------------
#VERTEX-------------------------------------------------------------------------------------------
#VERTEX-------------------------------------------------------------------------------------------
#VERTEX-------------------------------------------------------------------------------------------
#VERTEX-------------------------------------------------------------------------------------------
#VERTEX-------------------------------------------------------------------------------------------
#VERTEX-------------------------------------------------------------------------------------------


# Vertex distance calculator (-->VDC)
vdistframe = tk.Frame(VERTEXframe, height=200, width=700, borderwidth=3, relief='groove', bg="#E9E9E9")
vdistframe.grid(row=0, column=0, sticky='nsew', pady=10, padx=30)

sphere = 0
cylinder = 0
axis = None
distance = 12
VDC_header = tk.Label(vdistframe, text=f'{translations[current_language]["VDC_header"]}', font=header_font, bg="#E9E9E9")
VDC_header.place(x=20, y=10)
VDC_sphere = tk.Label(vdistframe, text=f'{translations[current_language]["sphere"]}', font=small_font, bg="#E9E9E9")
VDC_sphere.place(x=23, y=53)
VDC_cylinder = tk.Label(vdistframe, text=f'{translations[current_language]["cylinder"]}', font=small_font, bg="#E9E9E9")
VDC_cylinder.place(x=110, y=53)
VDC_axis = tk.Label(vdistframe, text=f'{translations[current_language]["axis"]}', font=small_font, bg="#E9E9E9")
VDC_axis.place(x=197, y=53)
VDC_mm = tk.Label(vdistframe, text=f'{translations[current_language]["mm"]}', font=small_font, bg="#E9E9E9")
VDC_mm.place(x=263, y=53)
VDC_adjusted_correction = tk.Label(vdistframe, text=f'{translations[current_language]["adjusted_correction"]}:', width=16, font=bold_font, bg="#E9E9E9")
VDC_adjusted_correction.place(x=310, y=49)
VDC_equivalent = tk.Label(vdistframe, text=f'{translations[current_language]["equivalent"]}:', width=14, font=bold_font, bg="#E9E9E9")
VDC_equivalent.place(x=520, y=49)

sphereholder = tk.StringVar()
cylinderholder = tk.StringVar()
axisholder = tk.StringVar()
distanceholder = tk.StringVar()
distanceholder.set("12")
sphere_entry = ttk.Entry(vdistframe, textvariable=sphereholder, justify='right')
sphere_entry.place(x=20, y=84, width=95)
cylinder_entry = ttk.Entry(vdistframe, textvariable=cylinderholder, justify='right')
cylinder_entry.place(x=120, y=84, width=75)
axis_entry = ttk.Entry(vdistframe, textvariable=axisholder, justify='right')
axis_entry.place(x=200, y=84, width=45)
distance_entry = ttk.Entry(vdistframe, textvariable=distanceholder, justify='right')
distance_entry.place(x=260, y=84, width=45)

# Second set of StringVars
sphereholder2 = tk.StringVar()
cylinderholder2 = tk.StringVar()
axisholder2 = tk.StringVar()
distanceholder2 = tk.StringVar()
distanceholder2.set("12")

# Second set of Entry widgets
sphere_entry2 = ttk.Entry(vdistframe, textvariable=sphereholder2, justify='right')
sphere_entry2.place(x=20, y=115, width=95)
cylinder_entry2 = ttk.Entry(vdistframe, textvariable=cylinderholder2, justify='right')
cylinder_entry2.place(x=120, y=115, width=75)
axis_entry2 = ttk.Entry(vdistframe, textvariable=axisholder2, justify='right')
axis_entry2.place(x=200, y=115, width=45)
distance_entry2 = ttk.Entry(vdistframe, textvariable=distanceholder2, justify='right')
distance_entry2.place(x=260, y=115, width=45)

def vertex_correction_generic(sphereholder, cylinderholder, axisholder, distanceholder, y_result):
    global text_widgets
    if y_result == 81:
        try:
            if text_widgets['VDC_invalid_input']:
                text_widgets['VDC_invalid_input'].destroy()
        except:
            pass
    elif y_result == 112:
        try:
            if text_widgets['VDC_invalid_input2']:
                text_widgets['VDC_invalid_input2'].destroy()
        except:
            pass
    sphere = filter_value(sphereholder)
    cylinder = filter_value(cylinderholder)
    axis = filter_value(axisholder)
    distance = filter_value(distanceholder)
    for var_name, var_value in [('Sfære', sphere), ('Cylinder', cylinder), ('Akse', axis), ('Avstand', distance)]:
        if var_value is None:
            if y_result == 112:
                text_widgets['VDC_invalid_input2'] = tk.Label(vdistframe, text=f'{translations[current_language]["invalid_input"]}', width=18, font=('Arial', 13, 'bold'), bg="#E9E9E9")
                text_widgets['VDC_invalid_input2'].place(x=310, y=y_result)
                return
            text_widgets['VDC_invalid_input'] = tk.Label(vdistframe, text=f'{translations[current_language]["invalid_input"]}', width=18, font=('Arial', 13, 'bold'), bg="#E9E9E9")
            text_widgets['VDC_invalid_input'].place(x=310, y=y_result)
            return
    distance = distance / 1000
    if sphere == 0:
        vertex_sphere = 0.00
    else:
        vertex_sphere = 1 / (1 / sphere - distance)
    sterkeste_snitt = sphere + cylinder
    if sterkeste_snitt == 0:
        vertex_sterkeste_snitt = 0.00
    else:    
        vertex_sterkeste_snitt = 1 / (1 / sterkeste_snitt - distance)
    vertex_cylinder = vertex_sterkeste_snitt - vertex_sphere
    if vertex_cylinder == 0:
        result = f'{"+" if vertex_sphere >= 0 else ""}{vertex_sphere:.2f}'
        spherical_equivalent = f'{"+" if vertex_sphere >= 0 else ""}{vertex_sphere:.2f}'
    else:
        result = f'{"+" if vertex_sphere > 0 else ""}{vertex_sphere:.2f}/{"+" if vertex_cylinder > 0 else ""}{vertex_cylinder:.2f}x{int(axis)}'
        spherical_equivalent = f'{"+" if (vertex_sphere + (vertex_cylinder / 2)) >= 0 else ""}{(vertex_sphere + (vertex_cylinder / 2)):.2f}'
    outside_range = False
    if sphere > 0 and vertex_sphere < 0:
        outside_range = True
    if sphere < 0 and vertex_sphere > 0:
        outside_range = True
    if cylinder > 0 and vertex_cylinder < 0:
        outside_range = True
    if cylinder < 0 and vertex_cylinder > 0:
        outside_range = True
    if outside_range:
        if y_result == 112:
            text_widgets['VDC_outside_range2'] = tk.Label(vdistframe, text=f'{translations[current_language]["prescription_outside_range"]}', width=20, font=('Arial', 13, 'bold'), bg="#E9E9E9")
            text_widgets['VDC_outside_range2'].place(x=310, y=y_result)
            return
        text_widgets['VDC_outside_range'] = tk.Label(vdistframe, text=f'{translations[current_language]["prescription_outside_range"]}', width=20, font=('Arial', 13, 'bold'), bg="#E9E9E9")
        text_widgets['VDC_outside_range'].place(x=310, y=y_result)
        return
    tk.Label(vdistframe, text=result, width=20, font=('Arial', 13, 'bold'), bg="#E9E9E9").place(x=310, y=y_result)
    tk.Label(vdistframe, text=spherical_equivalent, width=11, font=('Arial', 13, 'bold'), bg="#E9E9E9").place(x=520, y=y_result)

def run_both_vertex_corrections():
    vertex_correction_generic(sphereholder, cylinderholder, axisholder, distanceholder, 81)
    vertex_correction_generic(sphereholder2, cylinderholder2, axisholder2, distanceholder2, 112)

VDC_knapp = ttk.Button(vdistframe, text=translations[current_language]["calculate"], command=run_both_vertex_corrections, style='Nav.TButton')
VDC_knapp.place(x=485, y=153, height=37, width=150)

for entry in [sphere_entry, cylinder_entry, axis_entry, distance_entry, sphere_entry2, cylinder_entry2, axis_entry2, distance_entry2]:
    entry.bind('<Return>', lambda event: run_both_vertex_corrections())

def reset_vertex_corrections():
    sphereholder.set("")
    cylinderholder.set("")
    axisholder.set("")
    distanceholder.set("12")
    sphereholder2.set("")
    cylinderholder2.set("")
    axisholder2.set("")
    distanceholder2.set("12")
    tk.Label(vdistframe, text="", width=20, font=('Arial', 13, 'bold'), bg="#E9E9E9").place(x=310, y=85)
    tk.Label(vdistframe, text="", width=18, font=('Arial', 13, 'bold'), bg="#E9E9E9").place(x=430, y=85)
    tk.Label(vdistframe, text="", width=20, font=('Arial', 13, 'bold'), bg="#E9E9E9").place(x=310, y=115)
    tk.Label(vdistframe, text="", width=18, font=('Arial', 13, 'bold'), bg="#E9E9E9").place(x=430, y=115)

reset_vertex_knapp = ttk.Button(vdistframe, text="C", command=reset_vertex_corrections, width=3, style='Bold.TButton')
reset_vertex_knapp.place(x=652, y=8)


VDC_footer1 = tk.Label(vdistframe, text=f'{translations[current_language]["VDC_footer1"]}', font=mini_font, bg="#E9E9E9")
VDC_footer1.place(x=8, y=147)
VDC_footer2 = tk.Label(vdistframe, text=f'{translations[current_language]["VDC_footer2"]}', font=mini_font, bg="#E9E9E9")
VDC_footer2.place(x=8, y=169)

#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------

# Vertex distance chart (-->VCH)
vchartframe = tk.Frame(VERTEXframe, height=200, width=700, borderwidth=3, relief='groove', bg="#E9E9E9")
vchartframe.grid(row=1, column=0, sticky='nsew', pady=10, padx=30)

VCH_header = tk.Label(vchartframe, text=f'{translations[current_language]["VCH_header"]}', font=header_font, bg="#E9E9E9")
VCH_header.place(x=20, y=10)
VCH_from_prescription = tk.Label(vchartframe, text=f'{translations[current_language]["from_prescription"]}', bg="#E9E9E9", font=bold_font)
VCH_from_prescription.place(x=90, y=60)
VCH_to_prescription = tk.Label(vchartframe, text=f'{translations[current_language]["to_prescription"]}', bg="#E9E9E9", font=bold_font)
VCH_to_prescription.place(x=280, y=60)
VCH_mm_amount = tk.Label(vchartframe, text=f'{translations[current_language]["mm_amount"]}', bg="#E9E9E9", font=bold_font)
VCH_mm_amount.place(x=373, y=60)

vchart_from_holder = tk.StringVar()
vchart_to_holder = tk.StringVar()
vchart_antallmm_holder = tk.StringVar()
vchart_antallmm_holder.set("12")

vchart_from_entry = ttk.Entry(vchartframe, textvariable=vchart_from_holder, justify='right', font=bold_font)
vchart_from_entry.place(x=60, y=92, width=110)
vchart_to_entry = ttk.Entry(vchartframe, textvariable=vchart_to_holder, justify='right', font=bold_font)
vchart_to_entry.place(x=245, y=92, width=110)
vchart_antallmm_entry = ttk.Entry(vchartframe, textvariable=vchart_antallmm_holder, justify='right', font=bold_font)
vchart_antallmm_entry.place(x=400, y=92, width=45)

def vertex_distance_chart(vchart_from_holder, vchart_to_holder, vchart_antallmm_holder):
    global vchart
    global text_widgets
    try:
        text_widgets['VCH_invalid_input'].destroy()
    except:
        pass
    try:
        if vchart:
            vchart.destroy()
    except:
        pass
    from_value = filter_value(vchart_from_holder)
    to_value = filter_value(vchart_to_holder)
    distance_factor = filter_value(vchart_antallmm_holder) / 1000
    if from_value is None or to_value is None or distance_factor is None or from_value < 0 or to_value < 0:
        text_widgets['VCH_invalid_input'] = tk.Label(vchartframe, text=f'{translations[current_language]["invalid_input"]}', width=30, font=('Arial', 13, 'bold'), bg="#E9E9E9")
        text_widgets['VCH_invalid_input'].place(x=20, y=130)
        return

    vchart = tk.Frame(VERTEXframe, width=700, height=1000, bg="#E9E9E9", borderwidth=3, relief='groove',)
    vchart.grid(row=3, column=0, sticky='nsew', pady=1, padx=30)
    # Configure only the fourth column to expand, keeping existing positioning
    vchart.grid_columnconfigure(3, weight=1)
    text_widgets['VCH_minus'] = tk.Label(vchart, text=f'{translations[current_language]["minus"]}', bg="#E9E9E9", font=bold_font)
    text_widgets['VCH_minus'].grid(row=0, column=0, sticky='n', padx=(120, 0))
    text_widgets['VCH_number'] = tk.Label(vchart, text=f'{translations[current_language]["number"]}', bg="#E9E9E9", font=bold_font)
    text_widgets['VCH_number'].grid(row=0, column=1, sticky='n', padx=(120, 0))
    text_widgets['VCH_plus'] = tk.Label(vchart, text=f'{translations[current_language]["plus"]}', bg="#E9E9E9", font=bold_font)
    text_widgets['VCH_plus'].grid(row=0, column=2, sticky='n', padx=(120, 0))
    gridrow=1
    for i in range(int(math.floor(from_value)), int(math.ceil(to_value))):
        for j in [i, i+0.25, i+0.5, i+0.75]:
            if j == 0:
                minus_value = 0
                original_value = 0
                plus_value = 0
            else:
                original_value = 1 / (1 / j)
                
                # Check for division by zero or very small numbers in minus_value calculation
                minus_denominator = (1 / j + distance_factor)
                if abs(minus_denominator) < 1e-10:  # Very small number, treat as zero
                    minus_value = float('-inf') if minus_denominator > 0 else float('inf')
                else:
                    minus_value = -1 * (1 / minus_denominator)
                
                # Check for division by zero or very small numbers in plus_value calculation
                plus_denominator = (1 / j - distance_factor)
                if abs(plus_denominator) < 1e-10:  # Very small number, treat as zero
                    plus_value = float('inf') if plus_denominator > 0 else float('-inf')
                else:
                    plus_value = 1 / plus_denominator
            
            # Check threshold
            if plus_value < 0 or minus_value > 0:
                text_widgets['VCH_prescription_outside_range'] = tk.Label(vchart, text=f'{translations[current_language]["prescription_outside_range"]}', bg="#E9E9E9", font=font_12)
                text_widgets['VCH_prescription_outside_range'].grid(row=gridrow, column=0, sticky='e', columnspan=3)
                # Force canvas to update and properly calculate scroll region
                canvas.update_idletasks()
                canvas.update()
                canvas.configure(scrollregion=canvas.bbox('all'))
                return
            
            # Handle infinite values in display
            minus_display = f'{minus_value:.2f}' if abs(minus_value) != float('inf') else '∞' if minus_value > 0 else '-∞'
            original_display = f'{original_value:.2f}' if abs(original_value) != float('inf') else '∞' if original_value > 0 else '-∞'
            plus_display = f'+{plus_value:.2f}' if abs(plus_value) != float('inf') else '+∞' if plus_value > 0 else '-∞'
            
            tk.Label(vchart, text=minus_display, bg="#E9E9E9", font=font_12).grid(row=gridrow, column=0, sticky='e')
            tk.Label(vchart, text=original_display, bg="#E9E9E9", font=font_12).grid(row=gridrow, column=1, sticky='e')
            tk.Label(vchart, text=plus_display, bg="#E9E9E9", font=font_12).grid(row=gridrow, column=2, sticky='e')

            # Add separator line between rows
            separator = tk.Frame(vchart, height=1, bg="#CCCCCC")
            separator.grid(row=gridrow+1, column=0, columnspan=4, sticky='ew')
            gridrow += 2
            if j == math.ceil(to_value) - 0.25:
                j += 0.25
                original_value = 1 / (1 / j)
                
                # Check for division by zero or very small numbers in minus_value calculation
                minus_denominator = (1 / j + distance_factor)
                if abs(minus_denominator) < 1e-10:  # Very small number, treat as zero
                    minus_value = float('-inf') if minus_denominator > 0 else float('inf')
                else:
                    minus_value = -1 * (1 / minus_denominator)
                
                # Check for division by zero or very small numbers in plus_value calculation
                plus_denominator = (1 / j - distance_factor)
                if abs(plus_denominator) < 1e-10:  # Very small number, treat as zero
                    plus_value = float('inf') if plus_denominator > 0 else float('-inf')
                else:
                    plus_value = 1 / plus_denominator
                
                # Check threshold for the final value too
                if plus_value < 0 or minus_value > 0:
                    tk.Label(vchart, text=f'Styrke utenfor rekkevidde', bg="#E9E9E9", font=font_12).grid(row=gridrow, column=0, sticky='e', columnspan=3)
                    # Force canvas to update and properly calculate scroll region
                    canvas.update_idletasks()
                    canvas.update()
                    canvas.configure(scrollregion=canvas.bbox('all'))
                    return
                
                # Handle infinite values in display for special case
                minus_display = f'{minus_value:.2f}' if abs(minus_value) != float('inf') else '∞' if minus_value > 0 else '-∞'
                original_display = f'{original_value:.2f}' if abs(original_value) != float('inf') else '∞' if original_value > 0 else '-∞'
                plus_display = f'+{plus_value:.2f}' if abs(plus_value) != float('inf') else '+∞' if plus_value > 0 else '-∞'
                
                tk.Label(vchart, text=minus_display, bg="#E9E9E9", font=font_12).grid(row=gridrow, column=0, sticky='e')
                tk.Label(vchart, text=original_display, bg="#E9E9E9", font=font_12).grid(row=gridrow, column=1, sticky='e')
                tk.Label(vchart, text=plus_display, bg="#E9E9E9", font=font_12).grid(row=gridrow, column=2, sticky='e')

                # Add separator line between rows
                separator = tk.Frame(vchart, height=1, bg="#CCCCCC")
                separator.grid(row=gridrow+1, column=0, columnspan=4, sticky='ew')
    canvas.update_idletasks()  # Make sure all widgets are positioned
    canvas.configure(scrollregion=canvas.bbox('all'))

vchart_button = ttk.Button(vchartframe, text=f"{translations[current_language]["VCH_button"]}", style='Nav.TButton', command=lambda: vertex_distance_chart(vchart_from_holder, vchart_to_holder, vchart_antallmm_holder))
vchart_button.place(x=500, y=70, height=50, width=150)



for entry in [vchart_from_entry, vchart_to_entry, vchart_antallmm_entry]:
    entry.bind('<Return>', lambda event: vertex_distance_chart(vchart_from_holder, vchart_to_holder, vchart_antallmm_holder))

VCH_footer = tk.Label(vchartframe, text=f'{translations[current_language]["VCH_footer"]}', font=mini_font, bg="#E9E9E9")
VCH_footer.place(x=8, y=165)


def reset_vchart():
    global vchart
    vchart_from_holder.set("")
    vchart_to_holder.set("")
    vchart_antallmm_holder.set("12")
    try:
        vchart.destroy()
    except:
        pass
    canvas.update_idletasks()  # Make sure all widgets are positioned
    canvas.configure(scrollregion=canvas.bbox('all'))
    try:
        text_widgets['VCH_invalid_input'].destroy()
    except:
        pass

reset_vchart_button = ttk.Button(vchartframe, text="C", command=reset_vchart, width=3, style='Bold.TButton')
reset_vchart_button.place(x=652, y=8)


#DECENTRATION-------------------------------------------------------------------------------------------
#DECENTRATION-------------------------------------------------------------------------------------------
#DECENTRATION-------------------------------------------------------------------------------------------
#DECENTRATION-------------------------------------------------------------------------------------------
#DECENTRATION-------------------------------------------------------------------------------------------
#DECENTRATION-------------------------------------------------------------------------------------------
#DECENTRATION-------------------------------------------------------------------------------------------
#DECENTRATION-------------------------------------------------------------------------------------------
#DECENTRATION-------------------------------------------------------------------------------------------
#DECENTRATION-------------------------------------------------------------------------------------------
#DECENTRATION-------------------------------------------------------------------------------------------
#DECENTRATION-------------------------------------------------------------------------------------------
#DECENTRATION-------------------------------------------------------------------------------------------
#DECENTRATION-------------------------------------------------------------------------------------------
#DECENTRATION-------------------------------------------------------------------------------------------
#DECENTRATION-------------------------------------------------------------------------------------------
#DECENTRATION-------------------------------------------------------------------------------------------
#DECENTRATION-------------------------------------------------------------------------------------------
#DECENTRATION-------------------------------------------------------------------------------------------
#DECENTRATION-------------------------------------------------------------------------------------------
#DECENTRATION-------------------------------------------------------------------------------------------
#DECENTRATION-------------------------------------------------------------------------------------------
#DECENTRATION-------------------------------------------------------------------------------------------
#DECENTRATION-------------------------------------------------------------------------------------------
#DECENTRATION-------------------------------------------------------------------------------------------
#DECENTRATION-------------------------------------------------------------------------------------------
#DECENTRATION-------------------------------------------------------------------------------------------
#DECENTRATION-------------------------------------------------------------------------------------------
#DECENTRATION-------------------------------------------------------------------------------------------
#DECENTRATION-------------------------------------------------------------------------------------------
#DECENTRATION-------------------------------------------------------------------------------------------
#DECENTRATION-------------------------------------------------------------------------------------------


# Calculate decentration (-->CD)
CDframe = tk.Frame(DESENTRERINGframe, height=200, width=700, borderwidth=3, relief='groove', bg="#E9E9E9")
#borderwidth=3, relief='groove'
CDframe.grid(row=0, column=0, sticky='nsew', pady=10, padx=30)

CD_header = tk.Label(CDframe, text=f'{translations[current_language]["CD_header"]}', font=header_font, bg="#E9E9E9")
CD_header.place(x=20, y=10)
CD_sphere = tk.Label(CDframe, text=f'{translations[current_language]["sphere"]}', bg="#E9E9E9", font=small_font)
CD_sphere.place(x=80, y=53)
CD_cylinder = tk.Label(CDframe, text=f'{translations[current_language]["cylinder"]}', bg="#E9E9E9", font=small_font)
CD_cylinder.place(x=165, y=53)
CD_mm_desentration = tk.Label(CDframe, text=f'{translations[current_language]["mm_decentration"]}', bg="#E9E9E9", font=small_font)
CD_mm_desentration.place(x=260, y=53)
CD_prisms = tk.Label(CDframe, text=f'{translations[current_language]["prisms"]}', bg="#E9E9E9", font=small_font)
CD_prisms.place(x=440, y=53)

CDsphere = 0
CDcylinder = 0
CDsphereholder = tk.StringVar()
CDcylinderholder = tk.StringVar()
CDmmholder = tk.StringVar()
CDprismholder = tk.StringVar()
CDsphere_entry = ttk.Entry(CDframe, textvariable=CDsphereholder, justify='right', font=bold_font)
CDsphere_entry.place(x=60, y=80, width=95)
CDcylinder_entry = ttk.Entry(CDframe, textvariable=CDcylinderholder, justify='right', font=bold_font)
CDcylinder_entry.place(x=165, y=80, width=75)
CDmm_entry = ttk.Entry(CDframe, textvariable=CDmmholder, justify='right', font=bold_font)
CDmm_entry.place(x=300, y=80, width=55)
CDmm_entry.bind('<Return>', lambda event: CD(CDsphereholder, CDcylinderholder, "mm", CDmmholder, CDprismholder))
CDprism_entry = ttk.Entry(CDframe, textvariable=CDprismholder, justify='right', font=bold_font)
CDprism_entry.place(x=430, y=80, width=85)
CDprism_entry.bind('<Return>', lambda event: CD(CDsphereholder, CDcylinderholder, "prism", CDmmholder, CDprismholder))

# Second set of StringVars
CDsphereholder2 = tk.StringVar()
CDcylinderholder2 = tk.StringVar()
CDmmholder2 = tk.StringVar()
CDprismholder2 = tk.StringVar()

# Second set of Entry widgets
CDsphere_entry2 = ttk.Entry(CDframe, textvariable=CDsphereholder2, justify='right', font=bold_font)
CDsphere_entry2.place(x=60, y=112, width=95)
CDcylinder_entry2 = ttk.Entry(CDframe, textvariable=CDcylinderholder2, justify='right', font=bold_font)
CDcylinder_entry2.place(x=165, y=112, width=75)
CDmm_entry2 = ttk.Entry(CDframe, textvariable=CDmmholder2, justify='right', font=bold_font)
CDmm_entry2.place(x=300, y=112, width=55)
CDmm_entry2.bind('<Return>', lambda event: CD(CDsphereholder2, CDcylinderholder2, "mm", CDmmholder2, CDprismholder2))
CDprism_entry2 = ttk.Entry(CDframe, textvariable=CDprismholder2, justify='right', font=bold_font)
CDprism_entry2.place(x=430, y=112, width=85)
CDprism_entry2.bind('<Return>', lambda event: CD(CDsphereholder2, CDcylinderholder2, "prism", CDmmholder2, CDprismholder2))

def CD(CDsphereholder, CDcylinderholder, type, CDmmholder, CDprismholder):
    global CDerror
    global text_widgets
    try:
        if text_widgets['CD_error']:
            text_widgets['CD_error'].destroy()
    except:
        pass
    sphere = filter_value(CDsphereholder)
    cylinder = filter_value(CDcylinderholder)
    if sphere is None or cylinder is None:
        text_widgets['CD_error'] = tk.Label(CDframe, text=f'{translations[current_language]["invalid_input"]}', width=12, font=('Arial', 13, 'bold'), bg="#E9E9E9")
        text_widgets['CD_error'].place(x=520, y=92)
        return
    if type == "mm":
        mm = filter_value(CDmmholder)
        if mm is None:
            text_widgets['CD_error'] = tk.Label(CDframe, text=f'{translations[current_language]["invalid_input"]}', width=12, font=('Arial', 13, 'bold'), bg="#E9E9E9")
            text_widgets['CD_error'].place(x=520, y=92)
            return
        spherical_equivalent = sphere + (cylinder / 2)
        prism = mm / 10 * spherical_equivalent
        CDprismholder.set(round(prism, 1))
    elif type == "prism":
        prism = filter_value(CDprismholder)
        if prism is None:
            text_widgets['CD_error'] = tk.Label(CDframe, text=f'{translations[current_language]["invalid_input"]}', width=12, font=('Arial', 13, 'bold'), bg="#E9E9E9")
            text_widgets['CD_error'].place(x=520, y=92)
            return
        spherical_equivalent = sphere + (cylinder / 2)
        mm = prism / spherical_equivalent * 10
        CDmmholder.set(round(mm, 1))

def reset_CD():
    global text_widgets
    try:
        if text_widgets['CD_error']:
            text_widgets['CD_error'].destroy()
    except:
        pass
    CDsphereholder.set("")
    CDcylinderholder.set("")
    CDmmholder.set("")
    CDprismholder.set("")
    CDsphereholder2.set("")
    CDcylinderholder2.set("")
    CDmmholder2.set("")
    CDprismholder2.set("")

CD_footer1 = tk.Label(CDframe, text=f'{translations[current_language]["CD_footer1"]}', font=mini_font, bg="#E9E9E9")
CD_footer1.place(x=30, y=147)
CD_footer2 = tk.Label(CDframe, text=f'{translations[current_language]["CD_footer2"]}', font=mini_font, bg="#E9E9E9")
CD_footer2.place(x=70, y=169)

reset_CD_knapp = ttk.Button(CDframe, text="C", command=reset_CD, width=3, style='Bold.TButton')
reset_CD_knapp.place(x=652, y=8)



#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------


# Maks avvik (-->MA)
MAframe = tk.Frame(DESENTRERINGframe, height=200, width=700, borderwidth=3, relief='groove', bg="#E9E9E9")
#borderwidth=3, relief='groove'
MAframe.grid(row=1, column=0, sticky='nsew', pady=10, padx=30)

MA_header = tk.Label(MAframe, text=f'{translations[current_language]["MA_header"]}', font=header_font, bg="#E9E9E9")
MA_header.place(x=20, y=10)
MA_sphere = tk.Label(MAframe, text=f'{translations[current_language]["sphere"]}', bg="#E9E9E9", font=small_font)
MA_sphere.place(x=75, y=48)
MA_cylinder = tk.Label(MAframe, text=f'{translations[current_language]["cylinder"]}', bg="#E9E9E9", font=small_font)
MA_cylinder.place(x=163, y=48)
MA_mm_amount = tk.Label(MAframe, text=f'{translations[current_language]["mm_amount"]}:', width=15, font=('Arial', 13, 'bold'), bg="#E9E9E9")
MA_mm_amount.place(x=270, y=44)
#MA_total = tk.Label(MAframe, text=f'{translations[current_language]["bin_mm_amount"]}:', bg="#E9E9E9", font=bold_font)
#MA_total.place(x=500, y=60)

MAsphere = 0
MAcylinder = 0
MAsphereholder = tk.StringVar()
MAcylinderholder = tk.StringVar()
MAsphere_entry = ttk.Entry(MAframe, textvariable=MAsphereholder, justify='right', font=bold_font)
MAsphere_entry.place(x=60, y=75, width=95)
MAcylinder_entry = ttk.Entry(MAframe, textvariable=MAcylinderholder, justify='right', font=bold_font)
MAcylinder_entry.place(x=165, y=75, width=70)

# Second set of StringVars
MAsphereholder2 = tk.StringVar()
MAcylinderholder2 = tk.StringVar()

# Second set of Entry widgets
MAsphere_entry2 = ttk.Entry(MAframe, textvariable=MAsphereholder2, justify='right', font=bold_font)
MAsphere_entry2.place(x=60, y=109, width=95)
MAcylinder_entry2 = ttk.Entry(MAframe, textvariable=MAcylinderholder2, justify='right', font=bold_font)
MAcylinder_entry2.place(x=165, y=109, width=70)

def maks_avvik(sphereholder, cylinderholder, y_result=80):
    global text_widgets
    sphere = filter_value(sphereholder)
    cylinder = filter_value(cylinderholder)
    if sphere is None or cylinder is None:
        if y_result == 105:
            text_widgets['MA_error2'] = tk.Label(MAframe, text=f'{translations[current_language]["invalid_input"]}', width=19, font=('Arial', 13, 'bold'), bg="#E9E9E9")
            text_widgets['MA_error2'].place(x=240, y=y_result)
            return
        text_widgets['MA_error'] = tk.Label(MAframe, text=f'{translations[current_language]["invalid_input"]}', width=19, font=('Arial', 13, 'bold'), bg="#E9E9E9")
        text_widgets['MA_error'].place(x=240, y=y_result)
        return
    spherical_equivalent = sphere + (cylinder / 2)
    if spherical_equivalent == 0:
        if y_result == 105:
            text_widgets['MA_null2'] = tk.Label(MAframe, text=f'{translations[current_language]["MA_null"]}', width=19, font=('Arial', 13, 'bold'), bg="#E9E9E9")
            text_widgets['MA_null2'].place(x=240, y=y_result)
            return 0
        text_widgets['MA_null'] = tk.Label(MAframe, text=f'{translations[current_language]["MA_null"]}', width=19, font=('Arial', 13, 'bold'), bg="#E9E9E9")
        text_widgets['MA_null'].place(x=240, y=y_result)
        return 0
    max_movement = (0.5 / spherical_equivalent) * 10
    if max_movement < 0:
        max_movement *= -1
    result = f'{max_movement:.2f}'
    tk.Label(MAframe, text=result, width=19, font=('Arial', 13, 'bold'), bg="#E9E9E9").place(x=240, y=y_result)
    return max_movement

def run_both_maks_avvik():
    max_movement1 = maks_avvik(MAsphereholder, MAcylinderholder, 71)
    max_movement2 = maks_avvik(MAsphereholder2, MAcylinderholder2, 105)
    if max_movement1 is None or max_movement2 is None:
        return
#    if max_movement1 + max_movement2 == 0:
#        text_widgets['MA_bin_null'] = tk.Label(MAframe, text=f'{translations[current_language]["MA_null"]}', width=19, font=('Arial', 13, 'bold'), bg="#E9E9E9")
#        text_widgets['MA_bin_null'].place(x=470, y=87)
#        return
#    tk.Label(MAframe, text=f'{max_movement1 + max_movement2:.2f}', width=19, font=('Arial', 13, 'bold'), bg="#E9E9E9").place(x=470, y=87)     # Faulty logic, kept in case I find an improment

MAknapp = ttk.Button(MAframe, text=translations[current_language]['calculate'], command=run_both_maks_avvik, style='Nav.TButton')
MAknapp.place(x=80, y=145, height=45, width=150)

for entry in [MAsphere_entry, MAcylinder_entry, MAsphere_entry2, MAcylinder_entry2]:
    entry.bind('<Return>', lambda event: run_both_maks_avvik())

def reset_maks_avvik():
    global text_widgets
    # Destroy text widgets using grouped approach
    widget_keys = ['MA_error', 'MA_error2', 'MA_null', 'MA_null2', 'MA_bin_null']
    for widget_key in widget_keys:
        try:
            if text_widgets[widget_key]:
                text_widgets[widget_key].destroy()
        except:
            pass
    # Clear input fields
    MAsphereholder.set("")
    MAcylinderholder.set("")
    MAsphereholder2.set("")
    MAcylinderholder2.set("")
    # Clear result labels
    tk.Label(MAframe, text="", width=19, font=('Arial', 13, 'bold'), bg="#E9E9E9").place(x=240, y=71)
    tk.Label(MAframe, text="", width=19, font=('Arial', 13, 'bold'), bg="#E9E9E9").place(x=240, y=105)
#    tk.Label(MAframe, text="", width=19, font=('Arial', 13, 'bold'), bg="#E9E9E9").place(x=440, y=87)

reset_maks_avvik_knapp = ttk.Button(MAframe, text="C", command=reset_maks_avvik, width=3, style='Bold.TButton')
reset_maks_avvik_knapp.place(x=652, y=8)

MA_footer = tk.Label(MAframe, text=f'{translations[current_language]["MA_footer"]}', font=mini_font, bg="#E9E9E9")
MA_footer.place(x=280, y=169)


#GLASSESPRICE-------------------------------------------------------------------------------------------
#GLASSESPRICE-------------------------------------------------------------------------------------------
#GLASSESPRICE-------------------------------------------------------------------------------------------
#GLASSESPRICE-------------------------------------------------------------------------------------------
#GLASSESPRICE-------------------------------------------------------------------------------------------
#GLASSESPRICE-------------------------------------------------------------------------------------------
#GLASSESPRICE-------------------------------------------------------------------------------------------
#GLASSESPRICE-------------------------------------------------------------------------------------------
#GLASSESPRICE-------------------------------------------------------------------------------------------
#GLASSESPRICE-------------------------------------------------------------------------------------------
#GLASSESPRICE-------------------------------------------------------------------------------------------
#GLASSESPRICE-------------------------------------------------------------------------------------------
#GLASSESPRICE-------------------------------------------------------------------------------------------
#GLASSESPRICE-------------------------------------------------------------------------------------------
#GLASSESPRICE-------------------------------------------------------------------------------------------
#GLASSESPRICE-------------------------------------------------------------------------------------------
#GLASSESPRICE-------------------------------------------------------------------------------------------
#GLASSESPRICE-------------------------------------------------------------------------------------------
#GLASSESPRICE-------------------------------------------------------------------------------------------
#GLASSESPRICE-------------------------------------------------------------------------------------------
#GLASSESPRICE-------------------------------------------------------------------------------------------
#GLASSESPRICE-------------------------------------------------------------------------------------------
#GLASSESPRICE-------------------------------------------------------------------------------------------
#GLASSESPRICE-------------------------------------------------------------------------------------------
#GLASSESPRICE-------------------------------------------------------------------------------------------
#GLASSESPRICE-------------------------------------------------------------------------------------------
#GLASSESPRICE-------------------------------------------------------------------------------------------
#GLASSESPRICE-------------------------------------------------------------------------------------------
#GLASSESPRICE-------------------------------------------------------------------------------------------
#GLASSESPRICE-------------------------------------------------------------------------------------------
#GLASSESPRICE-------------------------------------------------------------------------------------------
#GLASSESPRICE-------------------------------------------------------------------------------------------
#GLASSESPRICE-------------------------------------------------------------------------------------------
#GLASSESPRICE-------------------------------------------------------------------------------------------
#GLASSESPRICE-------------------------------------------------------------------------------------------
#GLASSESPRICE-------------------------------------------------------------------------------------------
#GLASSESPRICE-------------------------------------------------------------------------------------------
#GLASSESPRICE-------------------------------------------------------------------------------------------
#GLASSESPRICE-------------------------------------------------------------------------------------------
#GLASSESPRICE-------------------------------------------------------------------------------------------
#GLASSESPRICE-------------------------------------------------------------------------------------------
#GLASSESPRICE-------------------------------------------------------------------------------------------

# Glasses price (-->GP)

GPcounter = 0
GP_instances = []
total_all_instances_checkboxes = []

total_all_instances = tk.Frame(GLASSESPRICEframe, height=310, width=120)
total_all_instances.grid(row=0, column=1, sticky='nsew', pady=10, padx=5, rowspan=999) # Large rowspan to cover whatever amount of frames the user adds

total_all_instances_header = tk.Label(total_all_instances, text=f'{translations[current_language]["total_all_instances_header"]}', font=medium_font, bg="#F0F0F0")
total_all_instances_header.place(x=1, y=10)
total_all_instances_before_discount_header = tk.Label(total_all_instances, text=f'{translations[current_language]["before_discount"]}', font=small_font, bg="#F0F0F0")
total_all_instances_before_discount_header.place(x=1, y=40)
total_all_instances_sum = tk.Label(total_all_instances, text=f'0.00', width=10, font=('Arial', 13, 'bold'), bg="#E9E9E9")
total_all_instances_sum.place(x=1, y=70)
total_all_instances_discount_header = tk.Label(total_all_instances, text=f'{translations[current_language]["discount"]}', font=small_font, bg="#F0F0F0")
total_all_instances_discount_header.place(x=1, y=110)
total_all_instances_discount = tk.Label(total_all_instances, text=f'0.00', width=10, font=('Arial', 13, 'bold'), bg="#E9E9E9")
total_all_instances_discount.place(x=1, y=140)
total_all_instances_after_discount_header = tk.Label(total_all_instances, text=f'{translations[current_language]["after_discount"]}', font=small_font, bg="#F0F0F0")
total_all_instances_after_discount_header.place(x=1, y=180)
total_all_instances_after_discount = tk.Label(total_all_instances, text=f'0.00', width=10, font=('Arial', 13, 'bold'), bg="#E9E9E9")
total_all_instances_after_discount.place(x=1, y=210)

total_all_instances_labelframe = ttk.LabelFrame(total_all_instances, text=f'{translations[current_language]["include"]}', width=110, height=100)
total_all_instances_labelframe.place(x=1, y=260)

def print_total_all_instances():
    global total_all_instances_sum
    global total_all_instances_discount
    global total_all_instances_after_discount
    total_before_discount = 0
    total_discount = 0
    total_after_discount = 0
    for gp in GP_instances:
        if gp.checkbox_var.get():
            total_before_discount += gp.total_number_before_discount
            total_discount += gp.total_discount_number
            total_after_discount += gp.total_number_after_discount
    total_all_instances_sum.config(text=f'{total_before_discount:.2f}')
    total_all_instances_discount.config(text=f'{total_discount:.2f}')
    total_all_instances_after_discount.config(text=f'{total_after_discount:.2f}')

class GPframe:
    def __init__(self, parent, row_number):
        if parent == CLPRICEframe:
            self.mainframe = 'CLP'
        elif parent == GLASSESPRICEframe:
            self.mainframe = 'GP'
        self.id = f'gp_{row_number}'
        self.frame = tk.Frame(parent, height=310, width=700, borderwidth=3, relief='groove', bg="#E9E9E9")
        self.frame.grid(row=row_number, column=0, sticky='nsew', pady=10, padx=(30, 10))
        self.entries = []
        self.vars = []
        self.total_number_before_discount = 0
        self.total_discount_number = 0
        self.total_number_after_discount = 0
        self.discount_type = tk.StringVar()
        self.discount_type.set('price')
        self.sum_after_discount_labels = []
        self.checkbox_var = tk.BooleanVar()
        for i in range(8):
            self.sum_after_discount_labels.append(None)
        self.sums_before_discount_for_calculation = [0.0] * 8
        self.discounts_for_calculation = [0.0] * 8
        self.sums_after_discount_for_calculation = [0.0] * 8
        self.invalid_labels = set()
        self.user_modified_cells = set()
        self.header = tk.Label(self.frame, text=f'{translations[current_language]["GP_header"]}', font=header_font, bg="#E9E9E9")
        self.header.place(x=20, y=10)
        self.header_counter = tk.Label(self.frame, text=f'#{row_number}:', bg="#E9E9E9", font=header_font)
        self.header_counter.place(x=350, y=10)
        self.price = tk.Label(self.frame, text=f'{translations[current_language]["price"]}', bg="#E9E9E9", font=small_font)
        self.price.place(x=205, y=43)
        self.discount = tk.Label(self.frame, text=f'{translations[current_language]["discount"]}', bg="#E9E9E9", font=small_font)
        self.discount.place(x=290, y=43)
        self.after_discount = tk.Label(self.frame, text=f'{translations[current_language]["after_discount"]}', font=small_font, bg="#E9E9E9")
        self.after_discount.place(x=380, y=43)
        self.enter_description_field_var = tk.StringVar()
        self.enter_description_field = tk.Entry(self.frame, font=medium_font, bg='#F9F9F9', textvariable=self.enter_description_field_var)
        self.enter_description_field.place(x=400, y=12, width=245)
        self.lower_right_before_discount = tk.Label(self.frame, text=f'{translations[current_language]["sum"]}', font=small_font, bg="#E9E9E9")
        self.lower_right_before_discount.place(x=508, y=175)
        self.lower_right_before_discount_number = tk.Label(self.frame, text=f'0.00', font=small_font, bg="#E9E9E9")
        self.lower_right_before_discount_number.place(x=580, y=175, width=100)
        self.lower_right_discount = tk.Label(self.frame, text=f'{translations[current_language]["discount"]}', font=small_font, bg="#E9E9E9")
        self.lower_right_discount.place(x=505, y=205)
        self.lower_right_discount_number = tk.Label(self.frame, text=f'0.00', font=small_font, bg="#E9E9E9")
        self.lower_right_discount_number.place(x=580, y=205, width=100)
        self.total = tk.Label(self.frame, text=f'{translations[current_language]["total"]}', font=medium_font, bg="#E9E9E9")
        self.total.place(x=505, y=235)
        self.total_number = tk.Label(self.frame, text=f'0.00', font=('Arial', 13, 'bold'), bg="#E9E9E9")
        self.total_number.place(x=575, y=235, width=110)
        self.reset_button = ttk.Button(self.frame, text="C", command=self.reset, width=3, style='Bold.TButton')
        self.reset_button.place(x=652, y=8)
        if self.id != 'gp_1':
            self.remove_frame_button = ttk.Button(self.frame, text="X", command=self.remove_frame, width=3, style='Bold.TButton')
            self.remove_frame_button.place(x=652, y=37)

        self.create_discount_type_widget()
        self.discount_type.trace('w', self.on_discount_type_change)
        self.make_grid()

    def remove_frame(self):
        global CLP_instances, CLPtotal_all_instances_checkboxes, CLPtotal_all_instances, CLPtotal_all_instances_labelframe, CLPtotal_all_instances_header, CLPtotal_all_instances_before_discount_header, CLPtotal_all_instances_sum, CLPtotal_all_instances_discount_header, CLPtotal_all_instances_discount, CLPtotal_all_instances_after_discount_header, CLPtotal_all_instances_after_discount, update_scrollbar
        global GP_instances, total_all_instances_checkboxes, total_all_instances, total_all_instances_labelframe, total_all_instances_header, total_all_instances_before_discount_header, total_all_instances_sum, total_all_instances_discount_header, total_all_instances_discount, total_all_instances_after_discount_header, total_all_instances_after_discount
        self.frame.destroy()
        if self.mainframe == 'CLP':
            CLP_instances.remove(self)
            self.checkbox.destroy()
            CLPtotal_all_instances_checkboxes.remove(self.checkbox)
            CLPtotal_all_instances.config(height=300 + (len(CLP_instances)) * 27)
            CLPtotal_all_instances_labelframe.config(height=70 + (len(CLP_instances) - 1) * 27)
            for checkbox in CLPtotal_all_instances_checkboxes:
                checkbox.place(x=1, y=1 + (CLPtotal_all_instances_checkboxes.index(checkbox)) * 27)
            print_CLPtotal_all_instances()
        elif self.mainframe == 'GP':
            GP_instances.remove(self)
            self.checkbox.destroy()
            total_all_instances_checkboxes.remove(self.checkbox)
            total_all_instances.config(height=300 + (len(GP_instances)) * 27)
            total_all_instances_labelframe.config(height=70 + (len(GP_instances) - 1) * 27)
            for checkbox in total_all_instances_checkboxes:
                checkbox.place(x=1, y=1 + (total_all_instances_checkboxes.index(checkbox)) * 27)
            print_total_all_instances()
        update_scrollbar()

    def create_discount_type_widget(self): # Radio buttons for price or percent discount
        self.discount_type_label = tk.LabelFrame(self.frame, text=f'{translations[current_language]["discount"]}', width=130, height=55, bg="#E9E9E9", font=mini_font)
        self.discount_type_label.place(x=520, y=80)
        self.DTLstyle = ttk.Style()
        self.DTLstyle.configure('Custom.TRadiobutton', background="#E9E9E9", font=mini_font)
        self.radio_percent = ttk.Radiobutton(self.discount_type_label, text='%', value='percent', variable=self.discount_type, style='Custom.TRadiobutton')
        self.radio_percent.place(x=0, y=4)
        self.radio_amount = ttk.Radiobutton(self.discount_type_label, text=f'{translations[current_language]["price"]}', value='price', variable=self.discount_type, style='Custom.TRadiobutton')
        self.radio_amount.place(x=50, y=4)

    def make_grid(self): # Grid for the entries
        self.entry_grid = tk.Frame(self.frame, bg="#E9E9E9", width=420, height=216)
        self.entry_grid.place(x=20, y=71)
        for row in range(8):
            row_entries = []
            row_vars = []
            for col in range(3):
                var = tk.StringVar()
                justify = 'left' if col == 0 else 'right'
                width = 183 if col == 0 else 87
                if col == 0:
                    x = 0
                elif col == 1:
                    x = 183
                elif col == 2:
                    x = 270
                entry = ttk.Entry(self.entry_grid, justify=justify, font=small_font, textvariable=var)
                entry.place(x=x, y=row * 27, width=width, height=27)
                
                # Set initial values before binding trace of whether the description is user-modified
                if col == 0 and row < 5:  # Only for description cells
                    var.set(translations[current_language][["frame", "right_lens", "left_lens", "adjustment", "clinical"][row]])
                elif col == 0 and row >= 5:  # Set '+' for the three lowest cells
                    var.set('+')
                
                # Bind trace after setting initial value of whether the description is user-modified
                if col == 0:
                    var.trace('w', lambda *args, r=row, c=col: self.on_description_change(r, c))

                if col in [1, 2]:
                #    entry.bind('<KeyRelease>', lambda event, r=row: self.on_entry_change(r))
                    var.trace('w', lambda *args, r=row: self.on_entry_change(r))
                # Bind arrow keys for navigation
                entry.bind('<KeyPress>', lambda event, r=row, c=col: self.on_key_press(event, r, c))
                row_entries.append(entry)
                row_vars.append(var)
            self.entries.append(row_entries)
            self.vars.append(row_vars)
        for row in range(8):
            try:
                price_var = self.vars[row][1]
                discount_var = self.vars[row][2]
                discount_type = self.discount_type.get()
                self.calculate_sum_after_discount(price_var, discount_var, discount_type, row)
            except Exception as e:
                print(f"Error recalculating row {row}: {e}")

    def on_key_press(self, event, row, col): # Handle arrow key navigation between cells
        try:
            # Get current row and column
            current_row = row
            current_col = col
            
            # Calculate new position based on key pressed
            if event.keysym == 'Up':
                new_row = max(0, current_row - 1)
                new_col = current_col
            elif event.keysym == 'Down':
                new_row = min(7, current_row + 1)  # 8 rows (0-7)
                new_col = current_col
            elif event.keysym == 'Left':
                new_row = current_row
                new_col = max(0, current_col - 1)
            elif event.keysym == 'Right':
                new_row = current_row
                new_col = min(2, current_col + 1)  # 3 columns (0-2)
            else:
                return  # Not an arrow key
            
            # Focus the new cell
            if new_row != current_row or new_col != current_col:
                self.entries[new_row][new_col].focus_set()
                # Select all text in the new cell
                self.entries[new_row][new_col].select_range(0, tk.END)
            
        except Exception as e:
            print(f"Error in keyboard navigation: {e}")

    def on_entry_change(self, row): # Make calculations happen when writing sums in cells
        try:
            price_var = self.vars[row][1]
            discount_var = self.vars[row][2]
            discount_type = self.discount_type.get()
            self.calculate_sum_after_discount(price_var, discount_var, discount_type, row)
            self.calculate_total()
            if self.mainframe == 'CLP':
                print_CLPtotal_all_instances()
            elif self.mainframe == 'GP':
                print_total_all_instances()
        except Exception as e:
            print(f"Error in on_entry_change: {e}")
            import traceback
            traceback.print_exc()

    def on_discount_type_change(self, *args): # Make calculations happen when changing discount type
        for row in range(8):
            try:
                price_var = self.vars[row][1]
                discount_var = self.vars[row][2]
                discount_type = self.discount_type.get()
                self.calculate_sum_after_discount(price_var, discount_var, discount_type, row)
            except Exception as e:
                print(f"Error recalculating row {row}: {e}")
        self.calculate_total()
        if self.mainframe == 'CLP':
            print_CLPtotal_all_instances()
        elif self.mainframe == 'GP':
            print_total_all_instances()

    def on_description_change(self, row, col): # Make sure the descriptions aren't overwritten by translations when changed by user
        # Only mark as user-modified if not updating programmatically
        if not hasattr(self, '_updating_programmatically') or not self._updating_programmatically:
            self.user_modified_cells.add((row, col))

    def calculate_sum_after_discount(self, price, discount, discount_type, row): # Calculate the current row
        sum_discount = 0
        price = filter_value(price)
        discount = filter_value(discount)
        
        if price is None or discount is None:
            sum_discount = f'{translations[current_language]["invalid_input"]}'
            self.invalid_labels.add(row)
            self.sums_before_discount_for_calculation[row] = 0
            self.discounts_for_calculation[row] = 0
            self.sums_after_discount_for_calculation[row] = 0
            if self.sum_after_discount_labels[row] is not None:
                self.sum_after_discount_labels[row].destroy()
            self.sum_after_discount_labels[row] = tk.Label(self.frame, text=sum_discount, width=11, font=('Arial', 13, 'bold'), bg="#E9E9E9")
            self.sum_after_discount_labels[row].place(x=380, y=row * 27 + 63)
            return  # Exit early for invalid input
        self.invalid_labels.discard(row)
        if discount_type == 'percent':
            sum_discount = round(price * (1 - discount / 100), 2)
        else:
            if discount < 0:
                discount *= -1
            sum_discount = round(price - discount, 2)
        self.sums_before_discount_for_calculation[row] = price
        self.discounts_for_calculation[row] = price - sum_discount
        self.sums_after_discount_for_calculation[row] = sum_discount

        if self.sum_after_discount_labels[row] is not None:
            self.sum_after_discount_labels[row].destroy()
        self.sum_after_discount_labels[row] = tk.Label(self.frame, text=sum_discount, width=9, font=('Arial', 13, 'bold'), bg="#E9E9E9")
        self.sum_after_discount_labels[row].place(x=380, y=row * 27 + 63)
    
    def calculate_total(self): # Calculate total before discount, total discount and total after discount
        self.total_number_before_discount = sum(self.sums_before_discount_for_calculation)
        self.lower_right_before_discount_number.config(text=f'{self.total_number_before_discount:.2f}')
        self.total_discount_number = sum(self.discounts_for_calculation)
        self.lower_right_discount_number.config(text=f'{self.total_discount_number:.2f}')
        self.total_number_after_discount = sum(self.sums_after_discount_for_calculation)
        self.total_number.config(text=f'{self.total_number_after_discount:.2f}')

    def update_texts(self):  # Run by the update_all_texts function connected to language buttons
        global GPadd_GP_button, GPPadd_CL_button, GPreset_all_button, total_all_instances_header, total_all_instances_before_discount_header, total_all_instances_discount_header, total_all_instances_after_discount_header, total_all_instances_labelframe
        lang = translations[current_language]
        self.header.config(text=lang["GP_header"])
        self.price.config(text=lang["price"])
        self.discount.config(text=lang["discount"])
        self.after_discount.config(text=lang["after_discount"])
        self.lower_right_before_discount.config(text=lang["sum"])
        self.lower_right_discount.config(text=lang["discount"])
        self.total.config(text=lang["total"])
        self.discount_type_label.config(text=lang["discount"])
        self.radio_amount.config(text=lang["price"])
        GPadd_GP_button.config(text=lang["add_GP"])
        GPPadd_CL_button.config(text=lang["add_CL"])
        GPreset_all_button.config(text=lang["reset_all"])
        total_all_instances_header.config(text=lang["total_all_instances_header"])
        total_all_instances_before_discount_header.config(text=lang["before_discount"])
        total_all_instances_discount_header.config(text=lang["discount"])
        total_all_instances_after_discount_header.config(text=lang["after_discount"])
        total_all_instances_labelframe.config(text=lang["include"])

        default_descriptions = [lang["frame"], lang["right_lens"], lang["left_lens"], lang["adjustment"], lang["clinical"], '+', '+', '+']
        
        # Set flag to prevent trace from marking cells as user-modified
        self._updating_programmatically = True
        
        for row in range(8):
            if (row, 0) not in self.user_modified_cells:
                self.vars[row][0].set(default_descriptions[row])
        
        # Clear the flag
        self._updating_programmatically = False

        for row in self.invalid_labels:
            if self.sum_after_discount_labels[row] is not None:
                self.sum_after_discount_labels[row].config(text=lang["invalid_input"])

    def reset(self):
        self.enter_description_field_var.set("")
        for row in range(8):
            self.vars[row][1].set("")
            self.vars[row][2].set("")
            self.calculate_sum_after_discount(self.vars[row][1], self.vars[row][2], self.discount_type.get(), row)
        self.calculate_total()
        self.user_modified_cells = set()
        if self.mainframe == 'CLP':
            print_CLPtotal_all_instances()
        elif self.mainframe == 'GP':
            print_total_all_instances()
        self.update_texts()



def create_GPframe(): # Create a new calculator box
    global GPcounter
    GPcounter += 1
    new_GP = GPframe(GLASSESPRICEframe, GPcounter)
    GP_instances.append(new_GP)
    GPcalculator_button_nav_frame.grid(row=(GPcounter + 1), column=0, sticky='nsew', pady=10, padx=30) # Moves lower NAV buttons down
    new_GP.checkbox_var = tk.BooleanVar()
    new_GP.checkbox_var.set(True)
    new_GP.checkbox = tk.Checkbutton(total_all_instances_labelframe, text=f'#{GPcounter}', variable=new_GP.checkbox_var, font=header_font)
    total_all_instances_checkboxes.append(new_GP.checkbox)
    new_GP.checkbox.place(x=1, y=1 + (len(GP_instances) - 1) * 27)
    new_GP.checkbox.bind('<ButtonRelease-1>', lambda event: print_total_all_instances())
    new_GP.checkbox_var.trace('w', lambda *args: print_total_all_instances())
    total_all_instances.config(height=300 + (len(GP_instances)) * 27)
    total_all_instances_labelframe.config(height=70 + (len(GP_instances) - 1) * 27)
    update_scrollbar()
    return new_GP

def find_gp_instance(id):
    for gp in GP_instances:
        if gp.id == id:
            return gp
    return None

def create_CLframe_for_GP():
    global GPcounter
    GPcounter += 1
    new_CLP = CLPframe(GLASSESPRICEframe, GPcounter)
    GP_instances.append(new_CLP)
    GPcalculator_button_nav_frame.grid(row=(GPcounter + 1), column=0, sticky='nsew', pady=10, padx=30) # Moves lower NAV buttons down
    new_CLP.checkbox_var = tk.BooleanVar()
    new_CLP.checkbox_var.set(True)
    new_CLP.checkbox = tk.Checkbutton(total_all_instances_labelframe, text=f'#{GPcounter}', variable=new_CLP.checkbox_var, font=header_font)
    total_all_instances_checkboxes.append(new_CLP.checkbox)
    new_CLP.checkbox.place(x=1, y=1 + (len(GP_instances) - 1) * 27)
    new_CLP.checkbox.bind('<ButtonRelease-1>', lambda event: print_total_all_instances())
    new_CLP.checkbox_var.trace('w', lambda *args: print_total_all_instances())
    total_all_instances.config(height=300 + (len(GP_instances)) * 27)
    total_all_instances_labelframe.config(height=70 + (len(GP_instances) - 1) * 27)
    update_scrollbar()
    return new_CLP

GPcalculator_button_nav_frame = tk.Frame(GLASSESPRICEframe, bg="#F0F0F0")
GPcalculator_button_nav_frame.grid(row=(GPcounter + 1), column=0, sticky='nsew', pady=1, padx=30)

def GPreset_all():
    global GP_instances
    global GPcounter
    global GPcalculator_button_nav_frame
    frames_to_remove = GP_instances.copy()
    for gp in frames_to_remove:
        gp.remove_frame()
    GPcounter = 0
    GP_instances = []
    create_GPframe()
    GPcalculator_button_nav_frame.grid(row=(GPcounter + 1), column=0, sticky='nsew', pady=10, padx=30)

GPadd_GP_button = ttk.Button(GPcalculator_button_nav_frame, text=translations[current_language]["add_GP"], command=create_GPframe, width=12, style='SmallNav.TButton')
GPadd_GP_button.grid(row=0, column=0, sticky='nsew', pady=10, padx=30, ipadx=7, ipady=2)

GPPadd_CL_button = ttk.Button(GPcalculator_button_nav_frame, text=translations[current_language]["add_CL"], command=create_CLframe_for_GP, width=12, style='SmallNav.TButton')
GPPadd_CL_button.grid(row=0, column=1, sticky='nsew', pady=10, padx=30, ipadx=7, ipady=2)

GPreset_all_button = ttk.Button(GPcalculator_button_nav_frame, text=translations[current_language]["reset_all"], command=GPreset_all, width=12, style='SmallNav.TButton')
GPreset_all_button.grid(row=0, column=2, sticky='nsew', pady=10, padx=30, ipadx=7, ipady=2)


#CLPRICE-------------------------------------------------------------------------------------------------
#CLPRICE-------------------------------------------------------------------------------------------------
#CLPRICE-------------------------------------------------------------------------------------------------
#CLPRICE-------------------------------------------------------------------------------------------------
#CLPRICE-------------------------------------------------------------------------------------------------
#CLPRICE-------------------------------------------------------------------------------------------------
#CLPRICE-------------------------------------------------------------------------------------------------


# Price for contact lenses (-->CLP)

CLPcounter = 0
CLP_instances = []
CLPtotal_all_instances_checkboxes = []

CLPtotal_all_instances = tk.Frame(CLPRICEframe, height=310, width=120)
CLPtotal_all_instances.grid(row=0, column=1, sticky='nsew', pady=10, padx=5, rowspan=999) # Large rowspan to cover whatever amount of frames the user adds

CLPtotal_all_instances_header = tk.Label(CLPtotal_all_instances, text=f'{translations[current_language]["total_all_instances_header"]}', font=medium_font, bg="#F0F0F0")
CLPtotal_all_instances_header.place(x=1, y=10)
CLPtotal_all_instances_before_discount_header = tk.Label(CLPtotal_all_instances, text=f'{translations[current_language]["before_discount"]}', font=small_font, bg="#F0F0F0")
CLPtotal_all_instances_before_discount_header.place(x=1, y=40)
CLPtotal_all_instances_sum = tk.Label(CLPtotal_all_instances, text=f'0.00', width=10, font=('Arial', 13, 'bold'), bg="#E9E9E9")
CLPtotal_all_instances_sum.place(x=1, y=70)
CLPtotal_all_instances_discount_header = tk.Label(CLPtotal_all_instances, text=f'{translations[current_language]["discount"]}', font=small_font, bg="#F0F0F0")
CLPtotal_all_instances_discount_header.place(x=1, y=110)
CLPtotal_all_instances_discount = tk.Label(CLPtotal_all_instances, text=f'0.00', width=10, font=('Arial', 13, 'bold'), bg="#E9E9E9")
CLPtotal_all_instances_discount.place(x=1, y=140)
CLPtotal_all_instances_after_discount_header = tk.Label(CLPtotal_all_instances, text=f'{translations[current_language]["after_discount"]}', font=small_font, bg="#F0F0F0")
CLPtotal_all_instances_after_discount_header.place(x=1, y=180)
CLPtotal_all_instances_after_discount = tk.Label(CLPtotal_all_instances, text=f'0.00', width=10, font=('Arial', 13, 'bold'), bg="#E9E9E9")
CLPtotal_all_instances_after_discount.place(x=1, y=210)

CLPtotal_all_instances_labelframe = ttk.LabelFrame(CLPtotal_all_instances, text=f'{translations[current_language]["include"]}', width=110, height=100)
CLPtotal_all_instances_labelframe.place(x=1, y=260)

def print_CLPtotal_all_instances():
    global CLPtotal_all_instances_sum
    global CLPtotal_all_instances_discount
    global CLPtotal_all_instances_after_discount
    total_before_discount = 0
    total_discount = 0
    total_after_discount = 0
    for gp in CLP_instances:
        if gp.checkbox_var.get():
            total_before_discount += gp.total_number_before_discount
            total_discount += gp.total_discount_number
            total_after_discount += gp.total_number_after_discount
    CLPtotal_all_instances_sum.config(text=f'{total_before_discount:.2f}')
    CLPtotal_all_instances_discount.config(text=f'{total_discount:.2f}')
    CLPtotal_all_instances_after_discount.config(text=f'{total_after_discount:.2f}')

class CLPframe:
    def __init__(self, parent, row_number):
        if parent == CLPRICEframe:
            self.mainframe = 'CLP'
        elif parent == GLASSESPRICEframe:
            self.mainframe = 'GP'
        self.id = f'clp_{row_number}'
        self.frame = tk.Frame(parent, height=310, width=700, borderwidth=3, relief='groove', bg="#E9E9E9")
        self.frame.grid(row=row_number, column=0, sticky='nsew', pady=10, padx=(30, 10))
        self.entries = []
        self.vars = []
        self.total_number_before_discount = 0
        self.total_discount_number = 0
        self.total_number_after_discount = 0
        self.discount_type = tk.StringVar()
        self.discount_type.set('price')
        self.sum_after_discount_labels = []
        self.checkbox_var = tk.BooleanVar()
        for i in range(5):
            self.sum_after_discount_labels.append(None)
        self.sums_before_discount_for_calculation = [0.0] * 5
        self.discounts_for_calculation = [0.0] * 5
        self.sums_after_discount_for_calculation = [0.0] * 5
        self.invalid_labels = set()
        self.user_modified_cells = set()
        self.header = tk.Label(self.frame, text=f'{translations[current_language]["CLP_header"]}', font=header_font, bg="#E9E9E9")
        self.header.place(x=20, y=10)
        self.header_counter = tk.Label(self.frame, text=f'#{row_number}:', bg="#E9E9E9", font=header_font)
        self.header_counter.place(x=350, y=10)
        self.price = tk.Label(self.frame, text=f'{translations[current_language]["price"]}', bg="#E9E9E9", font=small_font)
        self.price.place(x=345, y=46)
        self.qty = tk.Label(self.frame, text=f'{translations[current_language]["qty"]}', bg="#E9E9E9", font=small_font)
        self.qty.place(x=420, y=46)
        self.discount = tk.Label(self.frame, text=f'{translations[current_language]["discount"]}', bg="#E9E9E9", font=small_font)
        self.discount.place(x=465, y=46)
        self.after_discount = tk.Label(self.frame, text=f'{translations[current_language]["after_discount"]}', font=small_font, bg="#E9E9E9")
        self.after_discount.place(x=553, y=46)
        self.enter_description_field_var = tk.StringVar()
        self.enter_description_field = tk.Entry(self.frame, font=medium_font, bg='#F9F9F9', textvariable=self.enter_description_field_var)
        self.enter_description_field.place(x=400, y=12, width=245)
        self.lower_right_before_discount = tk.Label(self.frame, text=f'{translations[current_language]["sum"]}', font=small_font, bg="#E9E9E9")
        self.lower_right_before_discount.place(x=491, y=215)
        self.lower_right_before_discount_number = tk.Label(self.frame, text=f'0.00', font=small_font, bg="#E9E9E9")
        self.lower_right_before_discount_number.place(x=563, y=215, width=100)
        self.lower_right_discount = tk.Label(self.frame, text=f'{translations[current_language]["discount"]}', font=small_font, bg="#E9E9E9")
        self.lower_right_discount.place(x=488, y=240)
        self.lower_right_discount_number = tk.Label(self.frame, text=f'0.00', font=small_font, bg="#E9E9E9")
        self.lower_right_discount_number.place(x=563, y=240, width=100)
        self.total = tk.Label(self.frame, text=f'{translations[current_language]["total"]}', font=medium_font, bg="#E9E9E9")
        self.total.place(x=488, y=265)
        self.total_number = tk.Label(self.frame, text=f'0.00', font=('Arial', 13, 'bold'), bg="#E9E9E9")
        self.total_number.place(x=558, y=265, width=110)
        self.reset_button = ttk.Button(self.frame, text="C", command=self.reset, width=3, style='Bold.TButton')
        self.reset_button.place(x=652, y=8)
        if self.id != 'clp_1':
            self.remove_frame_button = ttk.Button(self.frame, text="X", command=self.remove_frame, width=3, style='Bold.TButton')
            self.remove_frame_button.place(x=652, y=37)

        self.create_discount_type_widget()
        self.discount_type.trace('w', self.on_discount_type_change)
        self.make_grid()

    def remove_frame(self):
        global CLP_instances, CLPtotal_all_instances_checkboxes, CLPtotal_all_instances, CLPtotal_all_instances_labelframe, CLPtotal_all_instances_header, CLPtotal_all_instances_before_discount_header, CLPtotal_all_instances_sum, CLPtotal_all_instances_discount_header, CLPtotal_all_instances_discount, CLPtotal_all_instances_after_discount_header, CLPtotal_all_instances_after_discount, update_scrollbar
        global GP_instances, total_all_instances_checkboxes, total_all_instances, total_all_instances_labelframe, total_all_instances_header, total_all_instances_before_discount_header, total_all_instances_sum, total_all_instances_discount_header, total_all_instances_discount, total_all_instances_after_discount_header, total_all_instances_after_discount
        self.frame.destroy()
        if self.mainframe == 'CLP':
            CLP_instances.remove(self)
            self.checkbox.destroy()
            CLPtotal_all_instances_checkboxes.remove(self.checkbox)
            CLPtotal_all_instances.config(height=300 + (len(CLP_instances)) * 27)
            CLPtotal_all_instances_labelframe.config(height=70 + (len(CLP_instances) - 1) * 27)
            for checkbox in CLPtotal_all_instances_checkboxes:
                checkbox.place(x=1, y=1 + (CLPtotal_all_instances_checkboxes.index(checkbox)) * 27)
            print_CLPtotal_all_instances()
        elif self.mainframe == 'GP':
            GP_instances.remove(self)
            self.checkbox.destroy()
            total_all_instances_checkboxes.remove(self.checkbox)
            total_all_instances.config(height=300 + (len(GP_instances)) * 27)
            total_all_instances_labelframe.config(height=70 + (len(GP_instances) - 1) * 27)
            for checkbox in total_all_instances_checkboxes:
                checkbox.place(x=1, y=1 + (total_all_instances_checkboxes.index(checkbox)) * 27)
            print_total_all_instances()
        update_scrollbar()

    def create_discount_type_widget(self): # Radio buttons for price or percent discount
        self.discount_type_label = tk.LabelFrame(self.frame, text=f'{translations[current_language]["discount"]}', width=130, height=55, bg="#E9E9E9", font=mini_font)
        self.discount_type_label.place(x=40, y=220)
        self.DTLstyle = ttk.Style()
        self.DTLstyle.configure('Custom.TRadiobutton', background="#E9E9E9", font=mini_font)
        self.radio_percent = ttk.Radiobutton(self.discount_type_label, text='%', value='percent', variable=self.discount_type, style='Custom.TRadiobutton')
        self.radio_percent.place(x=0, y=4)
        self.radio_amount = ttk.Radiobutton(self.discount_type_label, text=f'{translations[current_language]["price"]}', value='price', variable=self.discount_type, style='Custom.TRadiobutton')
        self.radio_amount.place(x=50, y=4)

    def make_grid(self): # Grid for the entries
        self.entry_grid = tk.Frame(self.frame, bg="#E9E9E9", width=620, height=135)
        self.entry_grid.place(x=20, y=73)
        for row in range(5):
            row_entries = []
            row_vars = []
            for col in range(4):
                var = tk.StringVar()
                justify = 'left' if col == 0 else 'right'
                if col == 0:
                    width = 327
                    x = 0
                elif col == 1:
                    width = 70
                    x = 327
                elif col == 2:
                    width = 47
                    x = 397
                elif col == 3:
                    width = 70
                    x = 444
                entry = ttk.Entry(self.entry_grid, justify=justify, font=small_font, textvariable=var)
                entry.place(x=x, y=row * 27, width=width, height=27)
                
                # Set initial values BEFORE binding trace
                if col == 0 and row < 3:  # Only for description cells
                    var.set(translations[current_language][["rcolon", "lcolon", "clinical"][row]])
                elif col == 0 and row >= 3:  # Set '+' for the two lowest cells
                    var.set('+')
                
                # Bind trace AFTER setting initial value
                if col == 0:
                    var.trace('w', lambda *args, r=row, c=col: self.on_description_change(r, c))

                if col in [1, 2, 3]:
                #    entry.bind('<KeyRelease>', lambda event, r=row: self.on_entry_change(r))
                    var.trace('w', lambda *args, r=row: self.on_entry_change(r))
                # Bind arrow keys for navigation
                entry.bind('<KeyPress>', lambda event, r=row, c=col: self.on_key_press(event, r, c))
                row_entries.append(entry)
                row_vars.append(var)
            self.entries.append(row_entries)
            self.vars.append(row_vars)
        for row in range(5):
            try:
                price_var = self.vars[row][1]
                qty_var = self.vars[row][2]
                discount_var = self.vars[row][3]
                discount_type = self.discount_type.get()
                self.calculate_sum_after_discount(price_var, qty_var, discount_var, discount_type, row)
            except Exception as e:
                print(f"Error recalculating row {row}: {e}")

    def on_key_press(self, event, row, col): # Handle arrow key navigation between cells
        try:
            # Get current row and column
            current_row = row
            current_col = col
            
            # Calculate new position based on key pressed
            if event.keysym == 'Up':
                new_row = max(0, current_row - 1)
                new_col = current_col
            elif event.keysym == 'Down':
                new_row = min(4, current_row + 1)  # 5 rows (0-4)
                new_col = current_col
            elif event.keysym == 'Left':
                new_row = current_row
                new_col = max(0, current_col - 1)
            elif event.keysym == 'Right':
                new_row = current_row
                new_col = min(3, current_col + 1)  # 4 columns (0-3)
            else:
                return  # Not an arrow key
            
            # Focus the new cell
            if new_row != current_row or new_col != current_col:
                self.entries[new_row][new_col].focus_set()
                # Select all text in the new cell
                self.entries[new_row][new_col].select_range(0, tk.END)
            
        except Exception as e:
            print(f"Error in keyboard navigation: {e}")

    def on_entry_change(self, row): # Make calculations happen when writing sums in cells
        try:
            price_var = self.vars[row][1]
            qty_var = self.vars[row][2]
            discount_var = self.vars[row][3]
            discount_type = self.discount_type.get()
            self.calculate_sum_after_discount(price_var, qty_var, discount_var, discount_type, row)
            self.calculate_total()
            if self.mainframe == 'CLP':
                print_CLPtotal_all_instances()
            elif self.mainframe == 'GP':
                print_total_all_instances()
        except Exception as e:
            print(f"Error in on_entry_change: {e}")
            import traceback
            traceback.print_exc()

    def on_discount_type_change(self, *args): # Make calculations happen when changing discount type
        for row in range(5):
            try:
                price_var = self.vars[row][1]
                qty_var = self.vars[row][2]
                discount_var = self.vars[row][3]
                discount_type = self.discount_type.get()
                self.calculate_sum_after_discount(price_var, qty_var, discount_var, discount_type, row)
            except Exception as e:
                print(f"Error recalculating row {row}: {e}")
        self.calculate_total()
        if self.mainframe == 'CLP':
            print_CLPtotal_all_instances()
        elif self.mainframe == 'GP':
            print_total_all_instances()

    def on_description_change(self, row, col): # Make sure the descriptions aren't overwritten by translations when changed by user
        # Only mark as user-modified if not updating programmatically
        if not hasattr(self, '_updating_programmatically') or not self._updating_programmatically:
            self.user_modified_cells.add((row, col))

    def calculate_sum_after_discount(self, price, qty, discount, discount_type, row): # Calculate the current row
        sum_discount = 0
        price = filter_value(price)
        discount = filter_value(discount)
        qty = filter_value(qty)
        
        if price is None or qty is None or discount is None:
            sum_discount = f'{translations[current_language]["invalid_input"]}'
            self.invalid_labels.add(row)
            self.sums_before_discount_for_calculation[row] = 0
            self.discounts_for_calculation[row] = 0
            self.sums_after_discount_for_calculation[row] = 0
            if self.sum_after_discount_labels[row] is not None:
                self.sum_after_discount_labels[row].destroy()
            self.sum_after_discount_labels[row] = tk.Label(self.frame, text=sum_discount, width=10, font=('Arial', 13, 'bold'), bg="#E9E9E9")
            self.sum_after_discount_labels[row].place(x=540, y=row * 27 + 70)
            return  # Exit early for invalid input
        self.invalid_labels.discard(row)
        if discount_type == 'percent':
            sum_discount = round(price * qty * (1 - discount / 100), 2)
        else:
            if discount < 0:
                discount *= -1
            sum_discount = round((price * qty) - discount, 2)
        self.sums_before_discount_for_calculation[row] = price * qty
        self.discounts_for_calculation[row] = (price * qty) - sum_discount
        self.sums_after_discount_for_calculation[row] = sum_discount

        if self.sum_after_discount_labels[row] is not None:
            self.sum_after_discount_labels[row].destroy()
        self.sum_after_discount_labels[row] = tk.Label(self.frame, text=sum_discount, width=9, font=('Arial', 13, 'bold'), bg="#E9E9E9")
        self.sum_after_discount_labels[row].place(x=550, y=row * 27 + 70)
    
    def calculate_total(self): # Calculate total before discount, total discount and total after discount
        self.total_number_before_discount = sum(self.sums_before_discount_for_calculation)
        self.lower_right_before_discount_number.config(text=f'{self.total_number_before_discount:.2f}')
        self.total_discount_number = sum(self.discounts_for_calculation)
        self.lower_right_discount_number.config(text=f'{self.total_discount_number:.2f}')
        self.total_number_after_discount = sum(self.sums_after_discount_for_calculation)
        self.total_number.config(text=f'{self.total_number_after_discount:.2f}')

    def update_texts(self):  # Run by the update_all_texts function connected to language buttons
        global CLPadd_CLP_button
        global CLPadd_GP_button
        global CLPreset_all_button
        global CLPtotal_all_instances_header
        global CLPtotal_all_instances_before_discount_header
        global CLPtotal_all_instances_discount_header
        global CLPtotal_all_instances_after_discount_header
        global CLPtotal_all_instances_labelframe
        lang = translations[current_language]
        self.header.config(text=lang["CLP_header"])
        self.price.config(text=lang["price"])
        self.qty.config(text=lang["qty"])
        self.discount.config(text=lang["discount"])
        self.after_discount.config(text=lang["after_discount"])
        self.lower_right_before_discount.config(text=lang["sum"])
        self.lower_right_discount.config(text=lang["discount"])
        self.total.config(text=lang["total"])
        self.discount_type_label.config(text=lang["discount"])
        self.radio_amount.config(text=lang["price"])
        CLPadd_GP_button.config(text=lang["add_GP"])
        CLPadd_CLP_button.config(text=lang["add_CL"])
        CLPreset_all_button.config(text=lang["reset_all"])
        CLPtotal_all_instances_header.config(text=lang["total_all_instances_header"])
        CLPtotal_all_instances_before_discount_header.config(text=lang["before_discount"])
        CLPtotal_all_instances_discount_header.config(text=lang["discount"])
        CLPtotal_all_instances_after_discount_header.config(text=lang["after_discount"])
        CLPtotal_all_instances_labelframe.config(text=lang["include"])

        default_descriptions = [lang["rcolon"], lang["lcolon"], lang["clinical"], '+', '+']
        
        # Set flag to prevent trace from marking cells as user-modified
        self._updating_programmatically = True
        
        for row in range(5):
            if (row, 0) not in self.user_modified_cells:
                self.vars[row][0].set(default_descriptions[row])
        
        # Clear the flag
        self._updating_programmatically = False

        for row in self.invalid_labels:
            if self.sum_after_discount_labels[row] is not None:
                self.sum_after_discount_labels[row].config(text=lang["invalid_input"])

    def reset(self):
        self.enter_description_field_var.set("")
        for row in range(5):
            self.vars[row][1].set("")
            self.vars[row][2].set("")
            self.vars[row][3].set("")
            self.calculate_sum_after_discount(self.vars[row][1], self.vars[row][2], self.vars[row][3], self.discount_type.get(), row)
        self.calculate_total()
        self.user_modified_cells = set()
        if self.mainframe == 'CLP':
            print_CLPtotal_all_instances()
        elif self.mainframe == 'GP':
            print_total_all_instances()
        self.update_texts()


def create_CLPframe_for_CLP(): # Create a new calculator box
    global CLPcounter
    CLPcounter += 1
    new_CLP = CLPframe(CLPRICEframe, CLPcounter)
    CLP_instances.append(new_CLP)
    CLPcalculator_button_nav_frame.grid(row=(CLPcounter + 1), column=0, sticky='nsew', pady=10, padx=30) # Moves lower NAV buttons down
    new_CLP.checkbox_var = tk.BooleanVar()
    new_CLP.checkbox_var.set(True)
    new_CLP.checkbox = tk.Checkbutton(CLPtotal_all_instances_labelframe, text=f'#{CLPcounter}', variable=new_CLP.checkbox_var, font=header_font)
    CLPtotal_all_instances_checkboxes.append(new_CLP.checkbox)
    new_CLP.checkbox.place(x=1, y=1 + (len(CLP_instances) - 1) * 27)
    new_CLP.checkbox.bind('<ButtonRelease-1>', lambda event: print_CLPtotal_all_instances())
    new_CLP.checkbox_var.trace('w', lambda *args: print_CLPtotal_all_instances())
    CLPtotal_all_instances.config(height=300 + (len(CLP_instances)) * 27)
    CLPtotal_all_instances_labelframe.config(height=70 + (len(CLP_instances) - 1) * 27)
    update_scrollbar()
    return new_CLP

def create_GP_frame_for_CLP():
    global CLPcounter
    CLPcounter += 1
    new_GP = GPframe(CLPRICEframe, CLPcounter)
    CLP_instances.append(new_GP)
    CLPcalculator_button_nav_frame.grid(row=(CLPcounter + 1), column=0, sticky='nsew', pady=10, padx=30) # Moves lower NAV buttons down
    new_GP.checkbox_var = tk.BooleanVar()
    new_GP.checkbox_var.set(True)
    new_GP.checkbox = tk.Checkbutton(CLPtotal_all_instances_labelframe, text=f'#{CLPcounter}', variable=new_GP.checkbox_var, font=header_font)
    CLPtotal_all_instances_checkboxes.append(new_GP.checkbox)
    new_GP.checkbox.place(x=1, y=1 + (len(CLP_instances) - 1) * 27)
    new_GP.checkbox.bind('<ButtonRelease-1>', lambda event: print_CLPtotal_all_instances())
    new_GP.checkbox_var.trace('w', lambda *args: print_CLPtotal_all_instances())
    CLPtotal_all_instances.config(height=300 + (len(CLP_instances)) * 27)
    CLPtotal_all_instances_labelframe.config(height=70 + (len(CLP_instances) - 1) * 27)
    update_scrollbar()
    return new_GP

def find_clp_instance(id):
    for clp in CLP_instances:
        if clp.id == id:
            return clp
    return None


CLPcalculator_button_nav_frame = tk.Frame(CLPRICEframe, bg="#F0F0F0")
CLPcalculator_button_nav_frame.grid(row=(CLPcounter + 1), column=0, sticky='nsew', pady=1, padx=30)

def CLPreset_all():
    global CLP_instances
    global CLPcounter
    global CLPcalculator_button_nav_frame
    frames_to_remove = CLP_instances.copy()
    for clp in frames_to_remove:
        clp.remove_frame()
    CLPcounter = 0
    CLP_instances = []
    create_CLPframe_for_CLP()
    CLPcalculator_button_nav_frame.grid(row=(CLPcounter + 1), column=0, sticky='nsew', pady=10, padx=30)

CLPadd_CLP_button = ttk.Button(CLPcalculator_button_nav_frame, text=translations[current_language]["add_CL"], command=create_CLPframe_for_CLP, width=12, style='SmallNav.TButton')
CLPadd_CLP_button.grid(row=0, column=0, sticky='nsew', pady=10, padx=30, ipadx=7, ipady=2)

CLPadd_GP_button = ttk.Button(CLPcalculator_button_nav_frame, text=translations[current_language]["add_GP"], command=create_GP_frame_for_CLP, width=12, style='SmallNav.TButton')
CLPadd_GP_button.grid(row=0, column=1, sticky='nsew', pady=10, padx=30, ipadx=7, ipady=2)

CLPreset_all_button = ttk.Button(CLPcalculator_button_nav_frame, text=translations[current_language]["reset_all"], command=CLPreset_all, width=12, style='SmallNav.TButton')
CLPreset_all_button.grid(row=0, column=2, sticky='nsew', pady=10, padx=30, ipadx=7, ipady=2)



# Initiate glasses price and contact lens price frames-------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------


create_GPframe()
create_CLPframe_for_CLP()


# GENERALframe-------------------------------------------------------------------------------------------------------
# GENERALframe-------------------------------------------------------------------------------------------------------
# GENERALframe-------------------------------------------------------------------------------------------------------
# GENERALframe-------------------------------------------------------------------------------------------------------
# GENERALframe-------------------------------------------------------------------------------------------------------
# GENERALframe-------------------------------------------------------------------------------------------------------
# GENERALframe-------------------------------------------------------------------------------------------------------
# GENERALframe-------------------------------------------------------------------------------------------------------
# GENERALframe-------------------------------------------------------------------------------------------------------
# GENERALframe-------------------------------------------------------------------------------------------------------
# GENERALframe-------------------------------------------------------------------------------------------------------
# GENERALframe-------------------------------------------------------------------------------------------------------
# GENERALframe-------------------------------------------------------------------------------------------------------
# GENERALframe-------------------------------------------------------------------------------------------------------
# GENERALframe-------------------------------------------------------------------------------------------------------
# GENERALframe-------------------------------------------------------------------------------------------------------
# GENERALframe-------------------------------------------------------------------------------------------------------
# GENERALframe-------------------------------------------------------------------------------------------------------
# GENERALframe-------------------------------------------------------------------------------------------------------
# GENERALframe-------------------------------------------------------------------------------------------------------
# GENERALframe-------------------------------------------------------------------------------------------------------
# GENERALframe-------------------------------------------------------------------------------------------------------
# GENERALframe-------------------------------------------------------------------------------------------------------
# GENERALframe-------------------------------------------------------------------------------------------------------


# Distance converter (-->DIST)

#class DistanceConverter(CalculatorSection):
#    def __init__(self, parent):
#        super().__init__(parent, "DIST_header")
#        self.create_entries()
#        self.create_labels()

#    def create_content(self):
#        pass

#    def create_entries(self):
#        pass

#    def update_texts(self):
#        super().update_texts()
#        lang = translations[current_language]
#        self.header.config(text=lang[self.title_key])
#        self.m.config(text=lang["m"])
#        self.cm.config(text=lang["cm"])
#        self.mm.config(text=lang["mm"])
#        self.ft.config(text=lang["feet"])
#        self.in.config(text=lang["inches"])
#        self.ft_i.config(text=lang["feet_and_inches"])

#    def get_row(self):
#        return 4


DISTframe = tk.Frame(GENERALframe, height=200, width=700, borderwidth=3, relief='groove', bg="#E9E9E9")
DISTframe.grid(row=0, column=0, sticky='nsew', pady=10, padx=30)
DIST_header = tk.Label(DISTframe, text=f'{translations[current_language]["DIST_header"]}', font=header_font, bg="#E9E9E9")
DIST_header.place(x=20, y=10)
DIST_m = tk.Label(DISTframe, text=f'{translations[current_language]["m"]}', bg="#E9E9E9", font=font_12)
DIST_m.place(x=30, y=75)
DIST_cm = tk.Label(DISTframe, text=f'{translations[current_language]["cm"]}', bg="#E9E9E9", font=font_12)
DIST_cm.place(x=165, y=75)
DIST_mm = tk.Label(DISTframe, text=f'{translations[current_language]["mm"]}', bg="#E9E9E9", font=font_12)
DIST_mm.place(x=300, y=75)
DIST_ft = tk.Label(DISTframe, text=f'{translations[current_language]["feet"]}', bg="#E9E9E9", font=font_12)
DIST_ft.place(x=435, y=25)
DIST_in = tk.Label(DISTframe, text=f'{translations[current_language]["inches"]}', bg="#E9E9E9", font=font_12)
DIST_in.place(x=535, y=25)

DISTm = 0
DISTcm = 0
DISTmm = 0
DISTft = 0
DISTin = 0
DISTmholder = tk.StringVar()
DISTcmholder = tk.StringVar()
DISTmmholder = tk.StringVar()
DISTftholder = tk.StringVar()
DISTinholder = tk.StringVar()

DISTm_entry = ttk.Entry(DISTframe, textvariable=DISTmholder, justify='right', font=bold_font)
DISTm_entry.place(x=20, y=105, width=100)
DISTm_entry.bind('<Return>', lambda event: distance_converter(DISTmholder, 'm'))
DISTcm_entry = ttk.Entry(DISTframe, textvariable=DISTcmholder, justify='right', font=bold_font)
DISTcm_entry.place(x=155, y=105, width=100)
DISTcm_entry.bind('<Return>', lambda event: distance_converter(DISTcmholder, 'cm'))
DISTmm_entry = ttk.Entry(DISTframe, textvariable=DISTmmholder, justify='right', font=bold_font)
DISTmm_entry.place(x=290, y=105, width=100)
DISTmm_entry.bind('<Return>', lambda event: distance_converter(DISTmmholder, 'mm'))
DISTft_entry = ttk.Entry(DISTframe, textvariable=DISTftholder, justify='right', font=bold_font)
DISTft_entry.place(x=425, y=55, width=95)
DISTft_entry.bind('<Return>', lambda event: distance_converter(DISTftholder, 'feet'))
DISTin_entry = ttk.Entry(DISTframe, textvariable=DISTinholder, justify='right', font=bold_font)
DISTin_entry.place(x=530, y=55, width=95)
DISTin_entry.bind('<Return>', lambda event: distance_converter(DISTinholder, 'inches'))

# Feet and inches box
DIST_ft_i_frame = tk.Frame(DISTframe, height=70, width=200, borderwidth=1, relief='groove', bg="#E6E6E6")
DIST_ft_i_frame.place(x=420, y=100)
DIST_ft_i = tk.Label(DIST_ft_i_frame, text=f'{translations[current_language]["feet_and_inches"]}', bg="#E6E6E6", font=font_12)
DIST_ft_i.place(x=28, y=3)
DIST_ft_i_feet = 0
DIST_ft_i_feetholder = tk.StringVar()
DIST_ft_i_feet_entry = ttk.Entry(DIST_ft_i_frame, textvariable=DIST_ft_i_feetholder, justify='right', font=bold_font)
DIST_ft_i_feet_entry.place(x=5, y=32, width=85)
DIST_ft_i_feet_entry.bind('<Return>', lambda event: distance_converter((DIST_ft_i_feetholder, DIST_ft_i_inchesholder), 'feet_and_inches'))
DIST_ftmark = tk.Label(DIST_ft_i_frame, text="'", bg="#E6E6E6", font=bold_font)
DIST_ftmark.place(x=88, y=32)
DIST_ft_i_inches = 0
DIST_ft_i_inchesholder = tk.StringVar()
DIST_ft_i_inches_entry = ttk.Entry(DIST_ft_i_frame, textvariable=DIST_ft_i_inchesholder, justify='right', font=bold_font)
DIST_ft_i_inches_entry.place(x=100, y=32, width=85)
DIST_ft_i_inches_entry.bind('<Return>', lambda event: distance_converter((DIST_ft_i_feetholder, DIST_ft_i_inchesholder), 'feet_and_inches'))
DIST_inmark = tk.Label(DIST_ft_i_frame, text="''", bg="#E6E6E6", font=bold_font)
DIST_inmark.place(x=182, y=32)


def distance_converter(input, type):
    global text_widgets
    try:
        if text_widgets['DIST_invalid_input']:
            text_widgets['DIST_invalid_input'].destroy()
    except:
        pass
    if type == 'mm':
        mm = filter_value(input)
        if mm is None:
            text_widgets['DIST_invalid_input'] = tk.Label(DISTframe, text=f'{translations[current_language]["invalid_input"]}', width=10, font=('CArial', 13, 'bold'), bg="#E9E9E9")
            text_widgets['DIST_invalid_input'].place(x=270, y=145)
            return
        m = mm / 1000
        DISTcmholder.set(f'{m*100:.2f}')
        DISTmholder.set(f'{m:.3f}')
        DISTinholder.set(f'{m*39.37:.2f}')
        DISTftholder.set(f'{m*39.37/12:.2f}')
        DIST_ft_i_feetholder.set(f'{int(m*39.37//12)}')
        DIST_ft_i_inchesholder.set(f'{(m*39.37%12):.2f}')
    elif type == 'cm':
        cm = filter_value(input)
        if cm is None:
            text_widgets['DIST_invalid_input'] = tk.Label(DISTframe, text=f'{translations[current_language]["invalid_input"]}', width=10, font=('Arial', 13, 'bold'), bg="#E9E9E9")
            text_widgets['DIST_invalid_input'].place(x=270, y=145)
            return
        m = cm / 100
        DISTmmholder.set(f'{m*1000:.1f}')
        DISTmholder.set(f'{m:.3f}')
        DISTinholder.set(f'{m*39.37:.2f}')
        DISTftholder.set(f'{m*39.37/12:.2f}')
        DIST_ft_i_feetholder.set(f'{int(m*39.37//12)}')
        DIST_ft_i_inchesholder.set(f'{(m*39.37%12):.2f}')
    elif type == 'm':
        m = filter_value(input)
        if m is None:
            text_widgets['DIST_invalid_input'] = tk.Label(DISTframe, text=f'{translations[current_language]["invalid_input"]}', width=10, font=('Arial', 13, 'bold'), bg="#E9E9E9")
            text_widgets['DIST_invalid_input'].place(x=270, y=145)
            return
        DISTmmholder.set(f'{m*1000:.1f}')
        DISTcmholder.set(f'{m*100:.2f}')
        DISTinholder.set(f'{m*39.37:.2f}')
        DISTftholder.set(f'{m*39.37/12:.2f}')
        DIST_ft_i_feetholder.set(f'{int(m*39.37//12)}')
        DIST_ft_i_inchesholder.set(f'{(m*39.37%12):.2f}')
    elif type == 'inches':
        inches = filter_value(input)
        if inches is None:
            text_widgets['DIST_invalid_input'] = tk.Label(DISTframe, text=f'{translations[current_language]["invalid_input"]}', width=10, font=('Arial', 13, 'bold'), bg="#E9E9E9")
            text_widgets['DIST_invalid_input'].place(x=270, y=145)
            return
        DISTmmholder.set(f'{inches*25.4:.1f}')
        DISTcmholder.set(f'{inches*2.54:.2f}')
        DISTmholder.set(f'{inches*0.0254:.3f}')
        DISTftholder.set(f'{inches/12:.2f}')
        DIST_ft_i_feetholder.set(f'{int(inches//12)}')
        DIST_ft_i_inchesholder.set(f'{(inches%12):.2f}')
    elif type == 'feet':
        feet = filter_value(input)
        if feet is None:
            text_widgets['DIST_invalid_input'] = tk.Label(DISTframe, text=f'{translations[current_language]["invalid_input"]}', width=10, font=('Arial', 13, 'bold'), bg="#E9E9E9")
            text_widgets['DIST_invalid_input'].place(x=270, y=145)
            return
        inches = feet * 12
        DISTmmholder.set(f'{feet*304.8:.1f}')
        DISTcmholder.set(f'{feet*30.48:.2f}')
        DISTmholder.set(f'{feet*0.3048:.3f}')
        DISTinholder.set(f'{inches:.2f}')
        DIST_ft_i_feetholder.set(f'{int(inches//12)}')
        DIST_ft_i_inchesholder.set(f'{(inches%12):.2f}')
    elif type == 'feet_and_inches':
        feet = filter_value(input[0])
        inches = filter_value(input[1])
        if feet is None or inches is None:
            text_widgets['DIST_invalid_input'] = tk.Label(DISTframe, text=f'{translations[current_language]["invalid_input"]}', width=10, font=('Arial', 13, 'bold'), bg="#E9E9E9")
            text_widgets['DIST_invalid_input'].place(x=270, y=145)
            return
        inches = feet * 12 + inches
        DISTmmholder.set(f'{inches*25.4:.1f}')
        DISTcmholder.set(f'{inches*2.54:.2f}')
        DISTmholder.set(f'{inches*0.0254:.3f}')
        DISTinholder.set(f'{inches:.2f}')
        DISTftholder.set(f'{inches/12:.2f}')
        DIST_ft_i_feetholder.set(f'{int(inches//12)}')
        DIST_ft_i_inchesholder.set(f'{(inches%12):.2f}')

DIST_footer = tk.Label(DISTframe, text=f'{translations[current_language]["DIST_footer"]}', font=mini_font, bg="#E9E9E9")
DIST_footer.place(x=40, y=160)

def reset_DIST():
    global text_widgets
    try:
        if text_widgets['DIST_invalid_input']:
            text_widgets['DIST_invalid_input'].destroy()
    except:
        pass
    DISTmmholder.set("")
    DISTcmholder.set("")
    DISTmholder.set("")
    DISTinholder.set("")
    DISTftholder.set("")
    DIST_ft_i_feetholder.set("")
    DIST_ft_i_inchesholder.set("")

reset_DIST_knapp = ttk.Button(DISTframe, text="C", command=reset_DIST, width=3, style='Bold.TButton')
reset_DIST_knapp.place(x=652, y=8)


#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------

# Weight converter (-->WT)

class WeightConverter(CalculatorSection):
    def __init__(self, parent, title_key, row):
        super().__init__(parent, title_key, row)
        self.kg = 0
        self.g = 0
        self.pounds = 0
        self.ounces = 0
        self.values = [self.kg, self.g, self.pounds, self.ounces]
        self.kg_holder = tk.StringVar()
        self.grams_holder = tk.StringVar()
        self.pounds_holder = tk.StringVar()
        self.ounces_holder = tk.StringVar()
        self.holders = [self.kg_holder, self.grams_holder, self.pounds_holder, self.ounces_holder]
        self.invalid_input = None
        self.create_labels()
        self.create_entries()
        self.update_texts()

    def create_entries(self):
        self.kg_entry = ttk.Entry(self.frame, textvariable=self.kg_holder, justify='right', font=bold_font)
        self.kg_entry.place(x=50, y=100, width=120)
        self.kg_entry.bind('<Return>', lambda event: self.weight_converter(self.kg_holder, 'kg'))
        self.grams_entry = ttk.Entry(self.frame, textvariable=self.grams_holder, justify='right', font=bold_font)
        self.grams_entry.place(x=200, y=100, width=120)
        self.grams_entry.bind('<Return>', lambda event: self.weight_converter(self.grams_holder, 'grams'))
        self.pounds_entry = ttk.Entry(self.frame, textvariable=self.pounds_holder, justify='right', font=bold_font)
        self.pounds_entry.place(x=350, y=100, width=120)
        self.pounds_entry.bind('<Return>', lambda event: self.weight_converter(self.pounds_holder, 'pounds'))
        self.ounces_entry = ttk.Entry(self.frame, textvariable=self.ounces_holder, justify='right', font=bold_font)
        self.ounces_entry.place(x=500, y=100, width=120)
        self.ounces_entry.bind('<Return>', lambda event: self.weight_converter(self.ounces_holder, 'ounces'))

    def create_labels(self):
        self.kg_label = tk.Label(self.frame, text=f'Kg', bg="#E9E9E9", font=font_12)
        self.kg_label.place(x=70, y=65)
        self.grams_label = tk.Label(self.frame, text=f'{translations[current_language]["grams"]}', bg="#E9E9E9", font=font_12)
        self.grams_label.place(x=220, y=65)
        self.labels.append((self.grams_label, 'grams'))
        self.pounds_label = tk.Label(self.frame, text=f'{translations[current_language]["pounds"]}', bg="#E9E9E9", font=font_12)
        self.pounds_label.place(x=370, y=65)
        self.labels.append((self.pounds_label, 'pounds'))
        self.ounces_label = tk.Label(self.frame, text=f'{translations[current_language]["ounces"]}', bg="#E9E9E9", font=font_12)
        self.ounces_label.place(x=520, y=65)
        self.labels.append((self.ounces_label, 'ounces'))
        self.footer = tk.Label(self.frame, text=f'{translations[current_language]["WT_footer"]}', font=mini_font, bg="#E9E9E9")
        self.footer.place(x=240, y=160)
        self.labels.append((self.footer, 'WT_footer'))

    def weight_converter(self, input, type):
        try:
            if self.invalid_input:
                self.invalid_input.destroy()
        except:
            pass
        filtered_value = filter_value(input)
        if filtered_value is None:
            self.invalid_input = tk.Label(self.frame, text=f'{translations[current_language]["invalid_input"]}', width=10, font=('Arial', 13, 'bold'), bg="#E9E9E9")
            self.invalid_input.place(x=370, y=25)
            return
        if type == 'kg':
            self.kg = filtered_value
        elif type == 'grams':
            self.kg = filtered_value / 1000
        elif type == 'pounds':
            self.kg = filtered_value * 0.453592
        elif type == 'ounces':
            self.kg = filtered_value * 0.0283495
        self.kg_holder.set(f'{self.kg:.4f}')
        self.grams_holder.set(f'{self.kg*1000:.2f}')
        self.pounds_holder.set(f'{self.kg*2.20462:.3f}')
        self.ounces_holder.set(f'{self.kg*35.274:.2f}')

weight_converter = WeightConverter(GENERALframe, "WT_header", 1)

#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------

# Volume converter (-->VOL)

class VolumeConverter(CalculatorSection):
    def __init__(self, parent, title_key, row):
        super().__init__(parent, title_key, row)
        self.liters = 0
        self.milliliters = 0
        self.cubic_meters = 0
        self.cubic_centimeters = 0
        self.cubic_feet = 0
        self.gallons = 0
        self.pints = 0
        self.cups = 0
        self.tablespoons = 0
        self.teaspoons = 0
        self.values = [self.liters, self.milliliters, self.cubic_meters, self.cubic_centimeters, self.cubic_feet, self.gallons, self.pints, self.cups, self.tablespoons, self.teaspoons]
        self.liters_holder = tk.StringVar()
        self.milliliters_holder = tk.StringVar()
        self.cubic_meters_holder = tk.StringVar()
        self.cubic_centimeters_holder = tk.StringVar()
        self.cubic_feet_holder = tk.StringVar()
        self.gallons_holder = tk.StringVar()
        self.pints_holder = tk.StringVar()
        self.cups_holder = tk.StringVar()
        self.tablespoons_holder = tk.StringVar()
        self.teaspoons_holder = tk.StringVar()
        self.holders = [self.liters_holder, self.milliliters_holder, self.cubic_meters_holder, self.cubic_centimeters_holder, self.cubic_feet_holder, self.gallons_holder, self.pints_holder, self.cups_holder, self.tablespoons_holder, self.teaspoons_holder]
        self.invalid_input = None
        self.create_labels()
        self.create_entries()
        self.update_texts()

    def create_labels(self):
        self.liters_label = tk.Label(self.frame, text=f'{translations[current_language]["liters"]}', bg="#E9E9E9", font=small_font)
        self.liters_label.place(x=350, y=6)
        self.labels.append((self.liters_label, 'liters'))
        self.milliliters_label = tk.Label(self.frame, text=f'{translations[current_language]["milliliters"]}', bg="#E9E9E9", font=small_font)
        self.milliliters_label.place(x=500, y=6)
        self.labels.append((self.milliliters_label, 'milliliters'))
        self.cubic_meters_label = tk.Label(self.frame, text=f'{translations[current_language]["cubic_meters"]}', bg="#E9E9E9", font=small_font)
        self.cubic_meters_label.place(x=50, y=56)
        self.labels.append((self.cubic_meters_label, 'cubic_meters'))
        self.cubic_centimeters_label = tk.Label(self.frame, text=f'{translations[current_language]["cubic_centimeters"]}', bg="#E9E9E9", font=small_font)
        self.cubic_centimeters_label.place(x=200, y=56)
        self.labels.append((self.cubic_centimeters_label, 'cubic_centimeters'))
        self.cubic_feet_label = tk.Label(self.frame, text=f'{translations[current_language]["cubic_feet"]}', bg="#E9E9E9", font=small_font)
        self.cubic_feet_label.place(x=350, y=56)
        self.labels.append((self.cubic_feet_label, 'cubic_feet'))
        self.gallons_label = tk.Label(self.frame, text=f'{translations[current_language]["gallons"]}', bg="#E9E9E9", font=small_font)
        self.gallons_label.place(x=500, y=56)
        self.labels.append((self.gallons_label, 'gallons'))
        self.pints_label = tk.Label(self.frame, text=f'{translations[current_language]["pints"]}', bg="#E9E9E9", font=small_font)
        self.pints_label.place(x=50, y=106)
        self.labels.append((self.pints_label, 'pints'))
        self.cups_label = tk.Label(self.frame, text=f'{translations[current_language]["cups"]}', bg="#E9E9E9", font=small_font)
        self.cups_label.place(x=200, y=106)
        self.labels.append((self.cups_label, 'cups'))
        self.tablespoons_label = tk.Label(self.frame, text=f'{translations[current_language]["tablespoons"]}', bg="#E9E9E9", font=small_font)
        self.tablespoons_label.place(x=350, y=106)
        self.labels.append((self.tablespoons_label, 'tablespoons'))
        self.teaspoons_label = tk.Label(self.frame, text=f'{translations[current_language]["teaspoons"]}', bg="#E9E9E9", font=small_font)
        self.teaspoons_label.place(x=500, y=106)
        self.labels.append((self.teaspoons_label, 'teaspoons'))
        self.footer = tk.Label(self.frame, text=f'{translations[current_language]["VOL_footer"]}', font=mini_font, bg="#E9E9E9")
        self.footer.place(x=240, y=165)
        self.labels.append((self.footer, 'VOL_footer'))

    def create_entries(self):
        self.liters_entry = ttk.Entry(self.frame, textvariable=self.liters_holder, justify='right', font=bold_11)
        self.liters_entry.place(x=350, y=30, width=140)
        self.liters_entry.bind('<Return>', lambda event: self.volume_converter(self.liters_holder, 'liters'))
        self.milliliters_entry = ttk.Entry(self.frame, textvariable=self.milliliters_holder, justify='right', font=bold_11)
        self.milliliters_entry.place(x=500, y=30, width=140)
        self.milliliters_entry.bind('<Return>', lambda event: self.volume_converter(self.milliliters_holder, 'milliliters'))
        self.cubic_meters_entry = ttk.Entry(self.frame, textvariable=self.cubic_meters_holder, justify='right', font=bold_11)
        self.cubic_meters_entry.place(x=50, y=80, width=140)
        self.cubic_meters_entry.bind('<Return>', lambda event: self.volume_converter(self.cubic_meters_holder, 'cubic_meters'))
        self.cubic_centimeters_entry = ttk.Entry(self.frame, textvariable=self.cubic_centimeters_holder, justify='right', font=bold_11)
        self.cubic_centimeters_entry.place(x=200, y=80, width=140)
        self.cubic_centimeters_entry.bind('<Return>', lambda event: self.volume_converter(self.cubic_centimeters_holder, 'cubic_centimeters'))
        self.cubic_feet_entry = ttk.Entry(self.frame, textvariable=self.cubic_feet_holder, justify='right', font=bold_11)
        self.cubic_feet_entry.place(x=350, y=80, width=140)
        self.cubic_feet_entry.bind('<Return>', lambda event: self.volume_converter(self.cubic_feet_holder, 'cubic_feet'))
        self.gallons_entry = ttk.Entry(self.frame, textvariable=self.gallons_holder, justify='right', font=bold_11)
        self.gallons_entry.place(x=500, y=80, width=140)
        self.gallons_entry.bind('<Return>', lambda event: self.volume_converter(self.gallons_holder, 'gallons'))
        self.pints_entry = ttk.Entry(self.frame, textvariable=self.pints_holder, justify='right', font=bold_11)
        self.pints_entry.place(x=50, y=130, width=140)
        self.pints_entry.bind('<Return>', lambda event: self.volume_converter(self.pints_holder, 'pints'))
        self.cups_entry = ttk.Entry(self.frame, textvariable=self.cups_holder, justify='right', font=bold_11)
        self.cups_entry.place(x=200, y=130, width=140)
        self.cups_entry.bind('<Return>', lambda event: self.volume_converter(self.cups_holder, 'cups'))
        self.tablespoons_entry = ttk.Entry(self.frame, textvariable=self.tablespoons_holder, justify='right', font=bold_11)
        self.tablespoons_entry.place(x=350, y=130, width=140)
        self.tablespoons_entry.bind('<Return>', lambda event: self.volume_converter(self.tablespoons_holder, 'tablespoons'))
        self.teaspoons_entry = ttk.Entry(self.frame, textvariable=self.teaspoons_holder, justify='right', font=bold_11)
        self.teaspoons_entry.place(x=500, y=130, width=140)
        self.teaspoons_entry.bind('<Return>', lambda event: self.volume_converter(self.teaspoons_holder, 'teaspoons'))

    def volume_converter(self, input, type):
        try:
            if self.invalid_input:
                self.invalid_input.destroy()
        except:
            pass
        filtered_value = filter_value(input)
        if filtered_value is None:
            self.invalid_input = tk.Label(self.frame, text=f'{translations[current_language]["invalid_input"]}', width=10, font=('Arial', 13, 'bold'), bg="#E9E9E9")
            self.invalid_input.place(x=30, y=160)
            return
        if type == 'liters':
            self.liters = filtered_value
        elif type == 'milliliters':
            self.liters = filtered_value / 1000
        elif type == 'cubic_meters':
            self.liters = filtered_value * 1000
        elif type == 'cubic_centimeters':
            self.liters = filtered_value / 1000
        elif type == 'cubic_feet':
            self.liters = filtered_value * 28.3168
        elif type == 'gallons':
            self.liters = filtered_value * 3.78541
        elif type == 'pints':
            self.liters = filtered_value * 0.473176
        elif type == 'cups':
            self.liters = filtered_value * 0.236588
        elif type == 'tablespoons':
            self.liters = filtered_value * 0.0147868
        elif type == 'teaspoons':
            self.liters = filtered_value * 0.00492892
        self.liters_holder.set(f'{self.liters:.1f}' if self.liters > 28 else f'{self.liters:.4f}')
        self.milliliters_holder.set(f'{self.liters*1000:.1f}')
        self.cubic_meters_holder.set(f'{self.liters*0.001:.4f}' if self.liters > 28 else f'{self.liters*0.001:.5f}')
        self.cubic_centimeters_holder.set(f'{self.liters*1000:.1f}')
        self.cubic_feet_holder.set(f'{self.liters*0.03531467:.1f}' if self.liters > 28 else f'{self.liters*0.03531467:.4f}')
        self.gallons_holder.set(f'{self.liters*0.26417205:.1f}' if self.liters > 28 else f'{self.liters*0.26417205:.3f}')
        self.pints_holder.set(f'{self.liters*2.113376421:.2f}')
        self.cups_holder.set(f'{self.liters*4.226752843:.2f}')
        self.tablespoons_holder.set(f'{self.liters*67.6280454:.2f}')
        self.teaspoons_holder.set(f'{self.liters*202.884136:.1f}')

volume_converter = VolumeConverter(GENERALframe, "VOL_header", 2)

#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------

# Temperature converter (-->TC)

class TemperatureConverter(CalculatorSection):
    def __init__(self, parent, title_key, row):
        super().__init__(parent, title_key, row)
        self.celsius = 0
        self.fahrenheit = 0
        self.kelvin = 0
        self.values = [self.celsius, self.fahrenheit, self.kelvin]
        self.celsius_holder = tk.StringVar()
        self.fahrenheit_holder = tk.StringVar()
        self.kelvin_holder = tk.StringVar()
        self.holders = [self.celsius_holder, self.fahrenheit_holder, self.kelvin_holder]
        self.create_labels()
        self.create_entries()
        self.update_texts()

    def create_labels(self):
        self.celsius_label = tk.Label(self.frame, text=f'Celsius', bg="#E9E9E9", font=font_12)
        self.celsius_label.place(x=70, y=65)
        self.fahrenheit_label = tk.Label(self.frame, text=f'Fahrenheit', bg="#E9E9E9", font=font_12)
        self.fahrenheit_label.place(x=270, y=65)
        self.kelvin_label = tk.Label(self.frame, text=f'Kelvin', bg="#E9E9E9", font=font_12)
        self.kelvin_label.place(x=470, y=65)
        self.footer = tk.Label(self.frame, text=f'{translations[current_language]["TC_footer"]}', font=mini_font, bg="#E9E9E9")
        self.footer.place(x=240, y=160)
        self.labels.append((self.footer, 'TC_footer'))

    def create_entries(self):
        self.celsius_entry = ttk.Entry(self.frame, textvariable=self.celsius_holder, justify='right', font=bold_font)
        self.celsius_entry.place(x=50, y=100, width=150)
        self.celsius_entry.bind('<Return>', lambda event: self.temperature_converter(self.celsius_holder, 'celsius'))
        self.fahrenheit_entry = ttk.Entry(self.frame, textvariable=self.fahrenheit_holder, justify='right', font=bold_font)
        self.fahrenheit_entry.place(x=250, y=100, width=150)
        self.fahrenheit_entry.bind('<Return>', lambda event: self.temperature_converter(self.fahrenheit_holder, 'fahrenheit'))
        self.kelvin_entry = ttk.Entry(self.frame, textvariable=self.kelvin_holder, justify='right', font=bold_font)
        self.kelvin_entry.place(x=450, y=100, width=150)
        self.kelvin_entry.bind('<Return>', lambda event: self.temperature_converter(self.kelvin_holder, 'kelvin'))

    def temperature_converter(self, input, type):
        try:
            if self.invalid_input:
                self.invalid_input.destroy()
        except:
            pass
        filtered_value = filter_value(input)
        if filtered_value is None:
            self.invalid_input = tk.Label(self.frame, text=f'{translations[current_language]["invalid_input"]}', width=10, font=('Arial', 13, 'bold'), bg="#E9E9E9")
            self.invalid_input.place(x=370, y=25)
            return
        if type == 'celsius':
            self.celsius = filtered_value
        elif type == 'fahrenheit':
            self.celsius = (filtered_value - 32) * 5/9
        elif type == 'kelvin':
            self.celsius = filtered_value - 273.15
        self.celsius_holder.set(f'{self.celsius:.1f}')
        self.fahrenheit_holder.set(f'{self.celsius*9/5+32:.1f}')
        self.kelvin_holder.set(f'{self.celsius+273.15:.1f}')

temperature_converter = TemperatureConverter(GENERALframe, "TC_header", 3)

#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------

disclaimer_visible = True

disclaimer_frame = tk.Frame(window, bg="#f0f0f0", height=290)

text = tk.Text(disclaimer_frame, height=30, width=190, font=mini_font, bg="#f0f0f0", 
               relief='flat', borderwidth=0, wrap='none', cursor='xterm')
text.place(x=3, y=20)
text.insert('1.0', translations[current_language]['disclaimer_text'])
text.config(state='disabled')

def hide_disclaimer():
    global disclaimer_visible
    disclaimer_visible = False
    disclaimer_frame.grid_remove()
    hide_disclaimer_button.grid_remove()
    show_disclaimer_button.grid(row=3, column=0, sticky='ne', pady=5, padx=200, ipadx=15, ipady=2)
    # Update scrollbar after disclaimer change
    canvas.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox('all'))

def show_disclaimer():
    global disclaimer_visible
    disclaimer_visible = True
    disclaimer_frame.grid(row=3, column=0, sticky='ew', pady=(50, 0), padx=50)
    hide_disclaimer_button.grid(row=3, column=0, sticky='ne', pady=5, padx=200, ipadx=15, ipady=2)
    show_disclaimer_button.grid_remove()
    # Update scrollbar after disclaimer change
    canvas.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox('all'))

style = ttk.Style()
style.configure('Mild.TButton', 
               font=('Arial', 10),
               background='#f0f0f0',            # Light background
               foreground='#333333') 

hide_disclaimer_button = ttk.Button(window, text=translations[current_language]['hide_disclaimer'], command=hide_disclaimer, width=10, style='Mild.TButton')
hide_disclaimer_button.grid(row=3, column=0, sticky='ne', pady=5, padx=200, ipadx=15, ipady=2)

show_disclaimer_button = ttk.Button(window, text=translations[current_language]['show_disclaimer'], command=show_disclaimer, width=10, style='Mild.TButton')




show_frame(DIVframe)


root.deiconify()
root.update()
root.mainloop()



# Fiks:
# - temperatur
# - variabelnavn
# - restrukturer
#   - hele greia med klasser
#   - endre VA og meter til å filtrere alt inn til én enhet, og så dele ut for kortere kode




# Mulige tillegg:
# cct
# forskjell mellom bildestørrelse
# aggressive briller - under "bonus"?
#    Legg til 1
#    Du har holdt ut X aggressive briller-vitser. Bra jobba!


# Character width * ~11.875 = pixel width


# Install command:
# python -m PyInstaller --onefile --windowed --add-data "translations.py;." --add-data "translations_no.py;." --add-data "translations_en.py;." --add-data "logo.ico;." --add-data "logo.png;." optolator.py
