from tkinter import *
import sqlite3
import random, math

LARGE_FONT = ("Verdana", 20)
NORM_FONT = ("Verdana", 16)
SMALL_FONT = ("Verdana", 10)

def tyre_sizes():    
    conn = sqlite3.connect('tyre.db')
    c = conn.cursor()    
    c.execute("SELECT * FROM steer")
    tyres = c.fetchall()
    conn.commit()

    sizes = ['None',]
    for tyre in range(len(tyres)):
        sizes.append(tyres[tyre][0])
    
    return tuple(sizes)

def tyre_prop(tyre_size, applic):
    conn = sqlite3.connect('tyre.db')
    c = conn.cursor()
    
    if applic == 'Steer':
        c.execute("SELECT * FROM steer WHERE size_name=:size", {'size': tyre_size})
        result = c.fetchall()

    if applic == 'Drive':
        c.execute("SELECT * FROM drive WHERE size_name=:size", {'size': tyre_size})
        result = c.fetchall()

    if applic == 'Roll':
        c.execute("SELECT * FROM roll WHERE size_name=:size", {'size': tyre_size})
        result = c.fetchall()
    
    conn.commit()    
    low = result[0][2]
    high = result[0][1]    
    
    return high, low
        

class Tyre_App():
    
    def __init__(self, master):        
        
        ## Vehicle Configuration
        self.config = 'None'
        self.m_mcode = 'None'
        self.quote = 'None'
        self.distance = 0
        
        self.axle_1_size = 'None'
        self.axle_2_size = 'None'
        self.axle_3_size = 'None'
        self.axle_4_size = 'None'
        self.axle_1_type = 'None'
        self.axle_2_type = 'None'
        self.axle_3_type = 'None'
        self.axle_4_type = 'None'

        self.calc_flag = False

        ## Initilize the session
        self.master = master
                
        # Configure the Window
        self.master.iconbitmap('coltique.ico')
        self.master.wm_title('Tyre Estimation v1.1')        
        self.master.update()

        ### Window pane
        # Initialize a paned window
        self.window = PanedWindow(self.master, width=900, height=600)
        self.window.pack(side = "top", fill = 'x')
        
        ### Canvas pane 
        # Initialize the Canvas
        self.pic_canvas = Canvas(self.window, bg='gray75')
        self.window.add(self.pic_canvas)

        # Canvas Labels
        self.canvas_label = Label(self.pic_canvas, text = 'Vehicle Configuration', font = LARGE_FONT, bg = 'gray75', fg='white')
        self.canvas_label.grid(row = 0, column = 0, columnspan = 10, pady = 20, padx = 20)

        self.canvas_sublabel = Label(self.pic_canvas, text = 'Wheel Positions', font = NORM_FONT, bg = 'gray75', fg='white')
        self.canvas_sublabel.grid(row = 2, column = 0, columnspan = 10, pady = 10, padx = 20)

        canvas_spacer = LabelFrame(self.pic_canvas, bg = 'gray75', height = 30)
        canvas_spacer.grid(row = 1, column = 0, columnspan = 10, padx = 20)

        ## Wheel position grid
        # Initialize with all positions
        # no tyres fitted - text = '', bg = 'white', fg = 'black', relief = 'sunken'
        # fitted - text = 'pos', bg = 'black', fg= 'white', relief = 'raised'
        
        ## Axle 1
        # Axle type
        self.axle1_label = Label(self.pic_canvas, text = 'None\nNone', justify = CENTER, bg = 'gray75', fg = 'white', bd = 5, width = 15)
        self.axle1_label.grid(row = 3, column = 3, columnspan = 4, padx = 5, pady = 10)     
        
        # grid 1
        self.g1_label = Label(self.pic_canvas, text = '', bg = 'white', fg = 'black', bd = 5, width = 3, relief = 'sunken')
        self.g1_label.grid(row = 3, column = 1, pady = 5, padx = 5)
        # grid 2
        self.g2_label = Label(self.pic_canvas, text = '', bg = 'white', fg = 'black', bd = 5, width = 3, relief = 'sunken')
        self.g2_label.grid(row = 3, column = 2, pady = 5, padx = 5)  
        # grid 3
        self.g3_label = Label(self.pic_canvas, text = '', bg = 'white', fg = 'black', bd = 5, width = 3, relief = 'sunken')
        self.g3_label.grid(row = 3, column = 7, pady = 5, padx = 5)
        # grid 4
        self.g4_label = Label(self.pic_canvas, text = '', bg = 'white', fg = 'black', bd = 5, width = 3, relief = 'sunken')
        self.g4_label.grid(row = 3, column = 8, pady = 5, padx = 5)

        ## Axle 2
        # Axle type
        self.axle2_label = Label(self.pic_canvas, text = 'None\nNone', justify = CENTER, bg = 'gray75', fg = 'white', bd = 5, width = 15)
        self.axle2_label.grid(row = 5, column = 3, columnspan = 4, padx = 5, pady = 10)      
        # grid 5
        self.g5_label = Label(self.pic_canvas, text = '', bg = 'white', fg = 'black', bd = 5, width = 3, relief = 'sunken')
        self.g5_label.grid(row = 5, column = 1, pady = 5, padx = 5)
        # grid 6
        self.g6_label = Label(self.pic_canvas, text = '', bg = 'white', fg = 'black', bd = 5, width = 3, relief = 'sunken')
        self.g6_label.grid(row = 5, column = 2, pady = 5, padx = 5)
        # grid 7
        self.g7_label = Label(self.pic_canvas, text = '', bg = 'white', fg = 'black', bd = 5, width = 3, relief = 'sunken')
        self.g7_label.grid(row = 5, column = 7, pady = 5, padx = 5)
        # grid 8
        self.g8_label = Label(self.pic_canvas, text = '', bg = 'white', fg = 'black', bd = 5, width = 3, relief = 'sunken')
        self.g8_label.grid(row = 5, column = 8, pady = 5, padx = 5)
        
        ## Axle 3
        # Axle type
        self.axle3_label = Label(self.pic_canvas, text = 'None\nNone', justify = CENTER, bg = 'gray75', fg = 'white', bd = 5, width = 15)
        self.axle3_label.grid(row = 7, column = 3, columnspan = 4, padx = 5, pady = 10)       
        # grid 9
        self.g9_label = Label(self.pic_canvas, text = '', bg = 'white', fg = 'black', bd = 5, width = 3, relief = 'sunken')
        self.g9_label.grid(row = 7, column = 1, pady = 5, padx = 5)
        # grid 10
        self.g10_label = Label(self.pic_canvas, text = '', bg = 'white', fg = 'black', bd = 5, width = 3, relief = 'sunken')
        self.g10_label.grid(row = 7, column = 2, pady = 5, padx = 5)
        # grid 11
        self.g11_label = Label(self.pic_canvas, text = '', bg = 'white', fg = 'black', bd = 5, width = 3, relief = 'sunken')
        self.g11_label.grid(row = 7, column = 7, pady = 5, padx = 5)
        # grid 12
        self.g12_label = Label(self.pic_canvas, text = '', bg = 'white', fg = 'black', bd = 5, width = 3, relief = 'sunken')
        self.g12_label.grid(row = 7, column = 8, pady = 5, padx = 5)

        ## Axle 4
        # Axle type
        self.axle4_label = Label(self.pic_canvas, text = 'None\nNone', justify = CENTER, bg = 'gray75', fg = 'white', bd = 5, width = 15)
        self.axle4_label.grid(row = 9, column = 3, columnspan = 4, padx = 5, pady = 10)        
        # grid 13
        self.g13_label = Label(self.pic_canvas, text = '', bg = 'white', fg = 'black', bd = 5, width = 3, relief = 'sunken')
        self.g13_label.grid(row = 9, column = 1, pady = 5, padx = 5)
        # grid 14
        self.g14_label = Label(self.pic_canvas, text = '', bg = 'white', fg = 'black', bd = 5, width = 3, relief = 'sunken')
        self.g14_label.grid(row = 9, column = 2, pady = 5, padx = 5)
        # grid 15
        self.g15_label = Label(self.pic_canvas, text = '', bg = 'white', fg = 'black', bd = 5, width = 3, relief = 'sunken')
        self.g15_label.grid(row = 9, column = 7, pady = 5, padx = 5)
        # grid 6
        self.g16_label = Label(self.pic_canvas, text = '', bg = 'white', fg = 'black', bd = 5, width = 3, relief = 'sunken')
        self.g16_label.grid(row = 9, column = 8, pady = 5, padx = 5)        
        
        
        ### Work pane
        self.work_frame = Frame(self.window, bg='white')
        self.window.add(self.work_frame)

        # Work pane Label
        self.work_label = Label(self.work_frame, text = 'Selection', font = LARGE_FONT, bg = 'white', fg='black')
        self.work_label.place(relx = 0.5, rely = 0.03, anchor = 'n')

        ## Configuration frame
        self.config_frame = LabelFrame(self.work_frame, height = 300, text = 'Update Vehicle', font = NORM_FONT, bg = 'white', bd = 5, relief = 'ridge') 
        self.config_frame.place(relx = 0, rely = 0.15, relwidth = 1)

        # Configuration Selector
        self.config_1 = Radiobutton(self.config_frame, bg='white', text = '6x4', value = 1, command=lambda: set_config(self,'6x4'))
        self.config_1.grid(row = 0, column = 0, sticky = 'w')
        self.config_2 = Radiobutton(self.config_frame, bg='white',text = '4x2', value = 2, command=lambda: set_config(self,'4x2'))
        self.config_2.grid(row = 1, column = 0, sticky = 'w')
        self.config_3 = Radiobutton(self.config_frame, bg='white',text = '8x4', value = 3, command=lambda: set_config(self,'8x4'))
        self.config_3.grid(row = 2, column = 0, sticky = 'w')
        self.config_4 = Radiobutton(self.config_frame, bg='white',text = '6x2', value = 4, command=lambda: set_config(self,'6x2'))
        self.config_4.grid(row = 3, column = 0, sticky = 'w')
        self.config_5 = Radiobutton(self.config_frame, bg='white',text = 'Tandem Dual', value = 5, command=lambda: set_config(self,'tandem dual'))
        self.config_5.grid(row = 4, column = 0, sticky = 'w')
        self.config_6 = Radiobutton(self.config_frame, bg='white',text = 'Tandem Single', value = 6, command=lambda: set_config(self,'tandem single'))
        self.config_6.grid(row = 5, column = 0, sticky = 'w')
        self.config_7 = Radiobutton(self.config_frame, bg='white',text = 'Tridem Dual', value = 7, command=lambda: set_config(self,'tridem dual'))
        self.config_7.grid(row = 6, column = 0, sticky = 'w')
        self.config_8 = Radiobutton(self.config_frame, bg='white',text = 'Tridem Single', value = 8, command=lambda: set_config(self,'tridem single'))
        self.config_8.grid(row = 7, column = 0, sticky = 'w')
        self.config_9 = Radiobutton(self.config_frame, bg='white',text = 'Quad Dual', value = 9, command=lambda: set_config(self,'quad dual'))
        self.config_9.grid(row = 8, column = 0, sticky = 'w')
        
        # distance entry
        distance_label = Label(self.config_frame, text = 'Contract Distance (km)', font = SMALL_FONT, bg = 'white')
        distance_label.grid(row = 1, column = 3, columnspan = 2)
        distance_entry = Entry(self.config_frame, bd = 2, relief = 'groove')
        distance_entry.grid(row = 1, column = 5)        

        # M&M Code entry
        MM_label = Label(self.config_frame, text = 'Mead & McGrouter Code', font = SMALL_FONT, bg = 'white')
        MM_label.grid(row = 2, column = 3, columnspan = 2)
        MM_entry = Entry(self.config_frame, bd = 2, relief = 'groove')
        MM_entry.grid(row = 2, column = 5)
        
        # Quote entry
        quote_label = Label(self.config_frame, text = 'Quote Number', font = SMALL_FONT, bg = 'white')
        quote_label.grid(row = 3, column = 3, columnspan = 2)
        quote_entry = Entry(self.config_frame, bd = 2, relief = 'groove')
        quote_entry.grid(row = 3, column = 5)

        # Tyre Sizes        
        sizes = tyre_sizes()
        axle_1_label = Label(self.config_frame, text = 'Tyre Size - Axle 1', font = SMALL_FONT, bg = 'white')
        axle_1_label.grid(row = 5, column = 3, columnspan = 2)
        axle1_size = Spinbox(self.config_frame, values = sizes, command = lambda: tyre_size(self))
        axle1_size.grid(row = 5, column = 5)        

        axle_2_label = Label(self.config_frame, text = 'Tyre Size - Axle 2', font = SMALL_FONT, bg = 'white')
        axle_2_label.grid(row = 6, column = 3, columnspan = 2)
        axle2_size = Spinbox(self.config_frame, values = sizes, command = lambda: tyre_size(self))
        axle2_size.grid(row = 6, column = 5)

        axle_3_label = Label(self.config_frame, text = 'Tyre Size - Axle 3', font = SMALL_FONT, bg = 'white')
        axle_3_label.grid(row = 7, column = 3, columnspan = 2)
        axle3_size = Spinbox(self.config_frame, values = sizes, command = lambda: tyre_size(self))
        axle3_size.grid(row = 7, column = 5)

        axle_4_label = Label(self.config_frame, text = 'Tyre Size - Axle 4', font = SMALL_FONT, bg = 'white')
        axle_4_label.grid(row = 8, column = 3, columnspan = 2)
        axle4_size = Spinbox(self.config_frame, values = sizes, command = lambda: tyre_size(self))
        axle4_size.grid(row = 8, column = 5)

        # update
        update_button = Button(self.config_frame, text = 'Update', font = NORM_FONT, bg = 'green', fg = 'white', width = 10, height = 2, bd = 2, command = lambda: update(self))
        update_button.grid(row = 1, column = 7, columnspan = 2, rowspan = 4)

        # calculate
        calc_button = Button(self.config_frame, text = 'Calculate', font = NORM_FONT, bg = 'gray', fg = 'black', state = DISABLED, width = 10, height = 1, bd = 2, command = lambda: calculate(self))
        calc_button.grid(row = 6, column = 7, columnspan = 2, rowspan = 3)

        ## Result frame
        self.result_frame = LabelFrame(self.work_frame, height = 200, text= 'Results', font = NORM_FONT, bg = 'snow2', fg = 'black', bd = 5, relief = 'ridge') 
        self.result_frame.place(relx = 0.02, rely = 0.60, relwidth = 0.96)      

        ### Status Bar
        config_status = 'Vehicle Configuration: ' + str(self.config)
        mead = 'M&M Code: ' + self.m_mcode
        quote = 'Quote: ' + self.quote
        status_bar_quote = Label(self.master, text=quote, font=SMALL_FONT, pady=5, bd=3, relief='sunken')        
        status_bar_quote.pack(side = 'left', expand = True, fill = 'x')
        status_bar_mead = Label(self.master, text=mead, font=SMALL_FONT, pady=5, bd=3, relief='sunken')        
        status_bar_mead.pack(side= 'left', expand = True, fill = 'x')
        status_bar_config = Label(self.master, text=config_status, font=SMALL_FONT, pady=5, bd=3, relief='sunken')        
        status_bar_config.pack(side = 'left', expand = True, fill = 'x')
       

        def set_config(self, new_config):
            self.config = new_config
            config_status = 'Vehicle Configuration: ' + self.config
            status_bar_config.config(text=config_status)
            
            clear_config(self)

            if self.config == '6x4':
                # [g1_label, g4_label, g9_label, g10_label, g11_label, g12_label, g13_label, g14_label, g15_label, g16_label]
                self.g1_label.config(text = 1, bg = 'black', fg= 'white', relief = 'raised')                
                self.g4_label.config(text = 2, bg = 'black', fg= 'white', relief = 'raised')
                self.g9_label.config(text = 3, bg = 'black', fg= 'white', relief = 'raised')
                self.g10_label.config(text = 4, bg = 'black', fg= 'white', relief = 'raised')
                self.g11_label.config(text = 5, bg = 'black', fg= 'white', relief = 'raised')
                self.g12_label.config(text = 6, bg = 'black', fg= 'white', relief = 'raised')
                self.g13_label.config(text = 7, bg = 'black', fg= 'white', relief = 'raised')
                self.g14_label.config(text = 8, bg = 'black', fg= 'white', relief = 'raised')
                self.g15_label.config(text = 9, bg = 'black', fg= 'white', relief = 'raised')
                self.g16_label.config(text = 10, bg = 'black', fg= 'white', relief = 'raised')
                
                self.axle_1_type = 'Steer'
                self.axle_2_type = ''
                self.axle_3_type = 'Drive'
                self.axle_4_type = 'Drive'
                
                self.axle_1_size = axle1_size.get()
                axle1_size.config(state = NORMAL)
                axle2_size.config(state = DISABLED)
                self.axle_2_size = ''
                self.axle_3_size = axle1_size.get()
                axle3_size.config(state = NORMAL)
                self.axle_4_size = axle1_size.get()
                axle4_size.config(state = NORMAL)

                axle__1 = self.axle_1_type + '\n' + self.axle_1_size
                axle__2 = self.axle_2_type + '\n' + self.axle_2_size
                axle__3 = self.axle_3_type + '\n' + self.axle_3_size
                axle__4 = self.axle_4_type + '\n' + self.axle_4_size

                self.axle1_label.config(text = axle__1)
                self.axle2_label.config(text = axle__2)
                self.axle3_label.config(text = axle__3)
                self.axle4_label.config(text = axle__4)

            elif self.config == '4x2':
                # [g1_label, g4_label, g9_label, g10_label, g11_label, g12_label]
                self.g1_label.config(text = 1, bg = 'black', fg= 'white', relief = 'raised')
                self.g4_label.config(text = 2, bg = 'black', fg= 'white', relief = 'raised')
                self.g9_label.config(text = 3, bg = 'black', fg= 'white', relief = 'raised')
                self.g10_label.config(text = 4, bg = 'black', fg= 'white', relief = 'raised')
                self.g11_label.config(text = 5, bg = 'black', fg= 'white', relief = 'raised')
                self.g12_label.config(text = 6, bg = 'black', fg= 'white', relief = 'raised')

                self.axle_1_type = 'Steer'
                self.axle_2_type = ''
                self.axle_3_type = 'Drive'
                self.axle_4_type = ''

                self.axle_1_size = axle1_size.get()
                axle1_size.config(state = NORMAL)
                axle2_size.config(state = DISABLED)
                self.axle_2_size = ''
                self.axle_3_size = axle3_size.get()
                axle3_size.config(state = NORMAL)
                axle4_size.config(state = DISABLED)
                self.axle_4_size = ''

                axle__1 = self.axle_1_type + '\n' + self.axle_1_size
                axle__2 = self.axle_2_type + '\n' + self.axle_2_size
                axle__3 = self.axle_3_type + '\n' + self.axle_3_size
                axle__4 = self.axle_4_type + '\n' + self.axle_4_size

                self.axle1_label.config(text = axle__1)
                self.axle2_label.config(text = axle__2)
                self.axle3_label.config(text = axle__3)
                self.axle4_label.config(text = axle__4)                

            elif self.config == '8x4':
                self.g1_label.config(text = 1, bg = 'black', fg= 'white', relief = 'raised')                
                self.g4_label.config(text = 2, bg = 'black', fg= 'white', relief = 'raised')
                self.g5_label.config(text = 3, bg = 'black', fg= 'white', relief = 'raised')
                self.g8_label.config(text = 4, bg = 'black', fg= 'white', relief = 'raised')
                self.g9_label.config(text = 5, bg = 'black', fg= 'white', relief = 'raised')
                self.g10_label.config(text = 6, bg = 'black', fg= 'white', relief = 'raised')
                self.g11_label.config(text = 7, bg = 'black', fg= 'white', relief = 'raised')
                self.g12_label.config(text = 8, bg = 'black', fg= 'white', relief = 'raised')
                self.g13_label.config(text = 9, bg = 'black', fg= 'white', relief = 'raised')
                self.g14_label.config(text = 10, bg = 'black', fg= 'white', relief = 'raised')
                self.g15_label.config(text = 11, bg = 'black', fg= 'white', relief = 'raised')
                self.g16_label.config(text = 12, bg = 'black', fg= 'white', relief = 'raised')

                self.axle_1_type = 'Steer'
                self.axle_2_type = 'Steer'
                self.axle_3_type = 'Drive'
                self.axle_4_type = 'Drive'

                self.axle_1_size = axle1_size.get()
                axle1_size.config(state = NORMAL)
                self.axle_2_size = axle2_size.get()
                axle2_size.config(state = NORMAL)
                self.axle_3_size = axle3_size.get()
                axle3_size.config(state = NORMAL)
                self.axle_4_size = axle4_size.get()
                axle4_size.config(state = NORMAL)

                axle__1 = self.axle_1_type + '\n' + self.axle_1_size
                axle__2 = self.axle_2_type + '\n' + self.axle_2_size
                axle__3 = self.axle_3_type + '\n' + self.axle_3_size
                axle__4 = self.axle_4_type + '\n' + self.axle_4_size

                self.axle1_label.config(text = axle__1)
                self.axle2_label.config(text = axle__2)
                self.axle3_label.config(text = axle__3)
                self.axle4_label.config(text = axle__4)  
                
            elif self.config == '6x2':
                self.g1_label.config(text = 1, bg = 'black', fg= 'white', relief = 'raised')                
                self.g4_label.config(text = 2, bg = 'black', fg= 'white', relief = 'raised')
                self.g9_label.config(text = 3, bg = 'black', fg= 'white', relief = 'raised')
                self.g10_label.config(text = 4, bg = 'black', fg= 'white', relief = 'raised')
                self.g11_label.config(text = 5, bg = 'black', fg= 'white', relief = 'raised')
                self.g12_label.config(text = 6, bg = 'black', fg= 'white', relief = 'raised')
                self.g13_label.config(text = 7, bg = 'black', fg= 'white', relief = 'raised')
                self.g14_label.config(text = 8, bg = 'black', fg= 'white', relief = 'raised')
                self.g15_label.config(text = 9, bg = 'black', fg= 'white', relief = 'raised')
                self.g16_label.config(text = 10, bg = 'black', fg= 'white', relief = 'raised')

                self.axle_1_type = 'Steer'
                self.axle_2_type = ''
                self.axle_3_type = 'Drive'
                self.axle_4_type = 'Roll'

                self.axle_1_size = axle1_size.get()
                axle1_size.config(state = NORMAL)
                axle2_size.config(state = DISABLED)
                self.axle_2_size = ''
                self.axle_3_size = axle3_size.get()
                axle3_size.config(state = NORMAL)
                self.axle_4_size = axle4_size.get()
                axle4_size.config(state = NORMAL)

                axle__1 = self.axle_1_type + '\n' + self.axle_1_size
                axle__2 = self.axle_2_type + '\n' + self.axle_2_size
                axle__3 = self.axle_3_type + '\n' + self.axle_3_size
                axle__4 = self.axle_4_type + '\n' + self.axle_4_size

                self.axle1_label.config(text = axle__1)
                self.axle2_label.config(text = axle__2)
                self.axle3_label.config(text = axle__3)
                self.axle4_label.config(text = axle__4)  

            elif self.config == 'tridem dual':
                self.g1_label.config(text = 1, bg = 'black', fg= 'white', relief = 'raised')                
                self.g2_label.config(text = 2, bg = 'black', fg= 'white', relief = 'raised')
                self.g3_label.config(text = 3, bg = 'black', fg= 'white', relief = 'raised')                
                self.g4_label.config(text = 4, bg = 'black', fg= 'white', relief = 'raised')                
                self.g5_label.config(text = 5, bg = 'black', fg= 'white', relief = 'raised')
                self.g6_label.config(text = 6, bg = 'black', fg= 'white', relief = 'raised')
                self.g7_label.config(text = 7, bg = 'black', fg= 'white', relief = 'raised')
                self.g8_label.config(text = 8, bg = 'black', fg= 'white', relief = 'raised')
                self.g9_label.config(text = 9, bg = 'black', fg= 'white', relief = 'raised')
                self.g10_label.config(text = 10, bg = 'black', fg= 'white', relief = 'raised')
                self.g11_label.config(text = 11, bg = 'black', fg= 'white', relief = 'raised')
                self.g12_label.config(text = 12, bg = 'black', fg= 'white', relief = 'raised')

                self.axle_1_type = 'Roll'
                self.axle_2_type = 'Roll'
                self.axle_3_type = 'Roll'
                self.axle_4_type = ''

                self.axle_1_size = axle1_size.get()
                axle1_size.config(state = NORMAL)
                self.axle_2_size = axle2_size.get()
                axle2_size.config(state = NORMAL)
                self.axle_3_size = axle3_size.get()
                axle3_size.config(state = NORMAL)
                axle4_size.config(state = DISABLED)
                self.axle_4_size = ''

                axle__1 = self.axle_1_type + '\n' + self.axle_1_size
                axle__2 = self.axle_2_type + '\n' + self.axle_2_size
                axle__3 = self.axle_3_type + '\n' + self.axle_3_size
                axle__4 = self.axle_4_type + '\n' + self.axle_4_size

                self.axle1_label.config(text = axle__1)
                self.axle2_label.config(text = axle__2)
                self.axle3_label.config(text = axle__3)
                self.axle4_label.config(text = axle__4) 

            elif self.config == 'tridem single':
                self.g1_label.config(text = 1, bg = 'black', fg= 'white', relief = 'raised')                
                self.g4_label.config(text = 2, bg = 'black', fg= 'white', relief = 'raised')
                self.g5_label.config(text = 3, bg = 'black', fg= 'white', relief = 'raised')
                self.g8_label.config(text = 4, bg = 'black', fg= 'white', relief = 'raised')
                self.g9_label.config(text = 5, bg = 'black', fg= 'white', relief = 'raised')
                self.g12_label.config(text = 6, bg = 'black', fg= 'white', relief = 'raised')

                self.axle_1_type = 'Roll'
                self.axle_2_type = 'Roll'
                self.axle_3_type = 'Roll'
                self.axle_4_type = ''

                self.axle_1_size = axle1_size.get()
                axle1_size.config(state = NORMAL)
                self.axle_2_size = axle2_size.get()
                axle2_size.config(state = NORMAL)
                self.axle_3_size = axle3_size.get()
                axle3_size.config(state = NORMAL)
                axle4_size.config(state = DISABLED)
                self.axle_4_size = ''

                axle__1 = self.axle_1_type + '\n' + self.axle_1_size
                axle__2 = self.axle_2_type + '\n' + self.axle_2_size
                axle__3 = self.axle_3_type + '\n' + self.axle_3_size
                axle__4 = self.axle_4_type + '\n' + self.axle_4_size

                self.axle1_label.config(text = axle__1)
                self.axle2_label.config(text = axle__2)
                self.axle3_label.config(text = axle__3)
                self.axle4_label.config(text = axle__4) 
        
            elif self.config == 'tandem dual':
                self.g1_label.config(text = 1, bg = 'black', fg= 'white', relief = 'raised')                
                self.g2_label.config(text = 2, bg = 'black', fg= 'white', relief = 'raised')
                self.g3_label.config(text = 3, bg = 'black', fg= 'white', relief = 'raised')
                self.g4_label.config(text = 4, bg = 'black', fg= 'white', relief = 'raised')
                self.g5_label.config(text = 5, bg = 'black', fg= 'white', relief = 'raised')
                self.g6_label.config(text = 6, bg = 'black', fg= 'white', relief = 'raised')
                self.g7_label.config(text = 7, bg = 'black', fg= 'white', relief = 'raised')
                self.g8_label.config(text = 8, bg = 'black', fg= 'white', relief = 'raised')

                self.axle_1_type = 'Roll'
                self.axle_2_type = 'Roll'
                self.axle_3_type = ''
                self.axle_4_type = ''

                self.axle_1_size = axle1_size.get()
                axle1_size.config(state = NORMAL)
                self.axle_2_size = axle2_size.get()
                axle2_size.config(state = NORMAL)
                axle3_size.config(state = DISABLED)
                self.axle_3_size = ''
                axle4_size.config(state = DISABLED)
                self.axle_4_size = ''

                axle__1 = self.axle_1_type + '\n' + self.axle_1_size
                axle__2 = self.axle_2_type + '\n' + self.axle_2_size
                axle__3 = self.axle_3_type + '\n' + self.axle_3_size
                axle__4 = self.axle_4_type + '\n' + self.axle_4_size

                self.axle1_label.config(text = axle__1)
                self.axle2_label.config(text = axle__2)
                self.axle3_label.config(text = axle__3)
                self.axle4_label.config(text = axle__4) 

            elif self.config == 'tandem single':
                self.g1_label.config(text = 1, bg = 'black', fg= 'white', relief = 'raised')                
                self.g4_label.config(text = 2, bg = 'black', fg= 'white', relief = 'raised')
                self.g5_label.config(text = 3, bg = 'black', fg= 'white', relief = 'raised')
                self.g8_label.config(text = 4, bg = 'black', fg= 'white', relief = 'raised')

                self.axle_1_type = 'Roll'
                self.axle_2_type = 'Roll'
                self.axle_3_type = ''
                self.axle_4_type = ''

                self.axle_1_size = axle1_size.get()
                axle1_size.config(state = NORMAL)
                self.axle_2_size = axle2_size.get()
                axle2_size.config(state = NORMAL)
                axle3_size.config(state = DISABLED)
                self.axle_3_size = ''
                axle4_size.config(state = DISABLED)
                self.axle_4_size = ''

                axle__1 = self.axle_1_type + '\n' + self.axle_1_size
                axle__2 = self.axle_2_type + '\n' + self.axle_2_size
                axle__3 = self.axle_3_type + '\n' + self.axle_3_size
                axle__4 = self.axle_4_type + '\n' + self.axle_4_size

                self.axle1_label.config(text = axle__1)
                self.axle2_label.config(text = axle__2)
                self.axle3_label.config(text = axle__3)
                self.axle4_label.config(text = axle__4) 

            elif self.config == 'quad dual':
                self.g1_label.config(text = 1, bg = 'black', fg= 'white', relief = 'raised')                
                self.g2_label.config(text = 2, bg = 'black', fg= 'white', relief = 'raised')
                self.g3_label.config(text = 3, bg = 'black', fg= 'white', relief = 'raised')
                self.g4_label.config(text = 4, bg = 'black', fg= 'white', relief = 'raised')
                self.g5_label.config(text = 5, bg = 'black', fg= 'white', relief = 'raised')
                self.g6_label.config(text = 6, bg = 'black', fg= 'white', relief = 'raised')
                self.g7_label.config(text = 7, bg = 'black', fg= 'white', relief = 'raised')
                self.g8_label.config(text = 8, bg = 'black', fg= 'white', relief = 'raised')
                self.g9_label.config(text = 9, bg = 'black', fg= 'white', relief = 'raised')
                self.g10_label.config(text = 10, bg = 'black', fg= 'white', relief = 'raised')
                self.g11_label.config(text = 11, bg = 'black', fg= 'white', relief = 'raised')
                self.g12_label.config(text = 12, bg = 'black', fg= 'white', relief = 'raised')
                self.g13_label.config(text = 13, bg = 'black', fg= 'white', relief = 'raised')
                self.g14_label.config(text = 14, bg = 'black', fg= 'white', relief = 'raised')
                self.g15_label.config(text = 15, bg = 'black', fg= 'white', relief = 'raised')
                self.g16_label.config(text = 16, bg = 'black', fg= 'white', relief = 'raised')

                self.axle_1_type = 'Roll'
                self.axle_2_type = 'Roll'
                self.axle_3_type = 'Roll'
                self.axle_4_type = 'Roll'

                self.axle_1_size = axle1_size.get()
                axle1_size.config(state = NORMAL)
                self.axle_2_size = axle2_size.get()
                axle2_size.config(state = NORMAL)
                self.axle_3_size = axle3_size.get()
                axle3_size.config(state = NORMAL)
                self.axle_4_size = axle4_size.get()
                axle4_size.config(state = NORMAL)

                axle__1 = self.axle_1_type + '\n' + self.axle_1_size
                axle__2 = self.axle_2_type + '\n' + self.axle_2_size
                axle__3 = self.axle_3_type + '\n' + self.axle_3_size
                axle__4 = self.axle_4_type + '\n' + self.axle_4_size

                self.axle1_label.config(text = axle__1)
                self.axle2_label.config(text = axle__2)
                self.axle3_label.config(text = axle__3)
                self.axle4_label.config(text = axle__4) 

        def clear_config(self):
            # [g1_label, g2_label, g3_label, g4_label, g5_label, g6_label, g7_label, g8_label, g9_label, g10_label, g11_label, g12_label, g13_label, g14_label, g15_label, g16_label]
            self.g1_label.config(text = '', bg = 'white', fg = 'black', relief = 'sunken')
            self.g2_label.config(text = '', bg = 'white', fg = 'black', relief = 'sunken')
            self.g3_label.config(text = '', bg = 'white', fg = 'black', relief = 'sunken')
            self.g4_label.config(text = '', bg = 'white', fg = 'black', relief = 'sunken')
            self.g5_label.config(text = '', bg = 'white', fg = 'black', relief = 'sunken')
            self.g6_label.config(text = '', bg = 'white', fg = 'black', relief = 'sunken')
            self.g7_label.config(text = '', bg = 'white', fg = 'black', relief = 'sunken')
            self.g8_label.config(text = '', bg = 'white', fg = 'black', relief = 'sunken')
            self.g9_label.config(text = '', bg = 'white', fg = 'black', relief = 'sunken')
            self.g10_label.config(text = '', bg = 'white', fg = 'black', relief = 'sunken')
            self.g11_label.config(text = '', bg = 'white', fg = 'black', relief = 'sunken')
            self.g12_label.config(text = '', bg = 'white', fg = 'black', relief = 'sunken')
            self.g13_label.config(text = '', bg = 'white', fg = 'black', relief = 'sunken')
            self.g14_label.config(text = '', bg = 'white', fg = 'black', relief = 'sunken')
            self.g15_label.config(text = '', bg = 'white', fg = 'black', relief = 'sunken')
            self.g16_label.config(text = '', bg = 'white', fg = 'black', relief = 'sunken')
        
            self.axle1_label.config(text = 'None\nNone')
            self.axle2_label.config(text = 'None\nNone')
            self.axle3_label.config(text = 'None\nNone')
            self.axle4_label.config(text = 'None\nNone')

        def update(self):            
            # Update the status Distance
            self.distance = int(float(distance_entry.get()))
            
            # Update the status MM Code
            if MM_entry.get() == '':
                self.m_mcode = 'None'
            else:
                self.m_mcode = MM_entry.get()
            
            mead = 'M&M Code: ' + self.m_mcode
            status_bar_mead.config(text = mead)
            
            # Update the status Quote Number
            if quote_entry.get() == '':
                self.quote = 'None'
            else:
                self.quote = quote_entry.get()

            quote = 'Quote: ' + self.quote
            status_bar_quote.config(text = quote)

            # Enable Calculate Button if all values are submitted
            if calc_test(self):
                calc_button.config(state = NORMAL, bg = 'green', fg = 'white')
                update_button.config(bg = 'gray', fg = 'black')

            try:
                result_clear(self)
            except:
                pass
            result_plot(self)

        def tyre_size(self):
            self.axle_1_size = axle1_size.get()
            self.axle_2_size = axle2_size.get()
            self.axle_3_size = axle3_size.get()
            self.axle_4_size = axle4_size.get()

            set_config(self, self.config)

        def calc_test(self):
            self.calc_flag = True
            
            if self.config == 'None':
                self.calc_flag = False

            if self.axle_1_size == 'None':
                self.calc_flag = False
              
            if self.axle_2_size == 'None':
                self.calc_flag = False
              
            if self.axle_3_size == 'None':
                self.calc_flag = False
              
            if self.axle_4_size == 'None':
                self.calc_flag = False

            if self.distance == 0:
                self.calc_flag = False
                        
            return self.calc_flag
        
        def calculate(self):
            ## update state of screen
            update_button.config(bg = 'green', fg = 'white')
            calc_button.config(state = DISABLED, bg = 'gray', fg = 'black')            
            result_clear(self)            
            result_plot(self)            
            
            ## Reset the tyre count
            self.steer_count = 0
            self.drive_count = 0
            self.roll_count = 0
            self.steer_count_least = 0
            self.drive_count_least = 0
            self.roll_count_least = 0
            self.tyre_quote = 0
            self.steer_quote = 0
            self.drive_quote = 0
            self.roll_quote = 0

            axle1pos = []
            axle2pos = []
            axle3pos = []
            axle4pos = []
            steer_pos = 0
            drive_pos = 0
            roll_pos = 0            
            
            ## Plot the configuration
            self.res_config_result.config(text = self.config)
            ## Plot the contract distance            
            dist = int(self.distance)
            dist_format = str('{:,}'.format(dist)) + ' km'
            self.res_distance_result.config(text = dist_format)

            ### Simualte Axle 1
            ## test if axle is active
            if self.axle_1_size != 'None' or self.axle_1_size != '':
                ## get active positions 
                axle1pos = []
                l1 = self.g1_label['text']
                l2 = self.g2_label['text']
                l3 = self.g3_label['text']
                l4 = self.g4_label['text']
                
                if type(l1) == int:
                    axle1pos.append(l1)
                if type(l2) == int:
                    axle1pos.append(l2)
                if type(l3) == int:
                    axle1pos.append(l3)
                if type(l4) == int:
                    axle1pos.append(l4)

                ### Update tyre type counts                
                if self.axle_1_type == 'Steer':
                        steer_pos += len(axle1pos)
                if self.axle_1_type == 'Drive':
                        drive_pos += len(axle1pos)
                if self.axle_1_type == 'Roll':
                        roll_pos += len(axle1pos)     
                
                ## run full distance simulation for every tyre position
                for tyre in axle1pos:
                    least = 10000
                    most = 0
                    ## trials of multiple vehicles
                    for vehicle in range(100):                    
                        completed_distance = 0
                        event = []
                        while completed_distance < self.distance:                            
                            thisTyre = sim_tyre(self, self.axle_1_size, self.axle_1_type)           
                            completed_distance += thisTyre
                            event.append(thisTyre)
                        if len(event) > most:
                            most = len(event)
                        if len(event) < least:
                            least = len(event)
                    
                    # Update the tyre counts
                    if self.axle_1_type == 'Steer':
                        self.steer_count += most
                        self.steer_count_least += least
                    if self.axle_1_type == 'Drive':
                        self.drive_count += most
                        self.drive_count_least += least
                    if self.axle_1_type == 'Roll':
                        self.roll_count += most
                        self.roll_count_least += least
                
            ### Calculate Axle 2
            ## test if axle is active
            if self.axle_2_size != 'None' or self.axle_2_size != '':
                ## get active positions 
                axle2pos = []
                l5 = self.g5_label['text']
                l6 = self.g6_label['text']
                l7 = self.g7_label['text']
                l8 = self.g8_label['text']
                
                if type(l5) == int:
                    axle2pos.append(l5)
                if type(l6) == int:
                    axle2pos.append(l6)
                if type(l7) == int:
                    axle2pos.append(l7)
                if type(l8) == int:
                    axle2pos.append(l8)

                ### Update tyre type counts                
                if self.axle_2_type == 'Steer':
                        steer_pos += len(axle2pos)
                if self.axle_2_type == 'Drive':
                        drive_pos += len(axle2pos)
                if self.axle_2_type == 'Roll':
                        roll_pos += len(axle2pos)

                ## run full distance simulation for every tyre position
                for tyre in axle2pos:
                    least = 10000
                    most = 0
                    ## trials of multiple vehicles
                    for vehicle in range(100):                    
                        completed_distance = 0
                        event = []
                        while completed_distance < self.distance:                            
                            thisTyre = sim_tyre(self, self.axle_2_size, self.axle_2_type)           
                            completed_distance += thisTyre
                            event.append(thisTyre)
                        if len(event) > most:
                            most = len(event)
                        if len(event) < least:
                            least = len(event)
                    
                    # Update the tyre counts
                    if self.axle_2_type == 'Steer':
                        self.steer_count += most
                        self.steer_count_least += least
                    if self.axle_2_type == 'Drive':
                        self.drive_count += most
                        self.drive_count_least += least
                    if self.axle_2_type == 'Roll':
                        self.roll_count += most
                        self.roll_count_least += least
            
            ### Calculate Axle 3
            ## test if axle is active
            if self.axle_3_size != 'None' or self.axle_3_size != '':
                ## get active positions 
                axle3pos = []
                l9 = self.g9_label['text']
                l10 = self.g10_label['text']
                l11 = self.g11_label['text']
                l12 = self.g12_label['text']
                
                if type(l9) == int:
                    axle3pos.append(l9)
                if type(l10) == int:
                    axle3pos.append(l10)
                if type(l11) == int:
                    axle3pos.append(l11)
                if type(l12) == int:
                    axle3pos.append(l12)

                ### Update tyre type counts                
                if self.axle_3_type == 'Steer':
                        steer_pos += len(axle3pos)
                if self.axle_3_type == 'Drive':
                        drive_pos += len(axle3pos)
                if self.axle_3_type == 'Roll':
                        roll_pos += len(axle3pos)
                
                ## run full distance simulation for every tyre position
                for tyre in axle3pos:
                    least = 10000
                    most = 0
                    ## trials of multiple vehicles
                    for vehicle in range(100):                    
                        completed_distance = 0
                        event = []
                        while completed_distance < self.distance:                            
                            thisTyre = sim_tyre(self, self.axle_3_size, self.axle_3_type)           
                            completed_distance += thisTyre
                            event.append(thisTyre)
                        if len(event) > most:
                            most = len(event)
                        if len(event) < least:
                            least = len(event)
                    
                    # Update the tyre counts
                    if self.axle_3_type == 'Steer':
                        self.steer_count += most
                        self.steer_count_least += least
                    if self.axle_3_type == 'Drive':
                        self.drive_count += most
                        self.drive_count_least += least
                    if self.axle_3_type == 'Roll':
                        self.roll_count += most
                        self.roll_count_least += least

            ### Calculate Axle 4
            ## test if axle is active
            if self.axle_4_size != 'None' or self.axle_4_size != '':
                ## get active positions 
                axle4pos = []
                l13 = self.g13_label['text']
                l14 = self.g14_label['text']
                l15 = self.g15_label['text']
                l16 = self.g16_label['text']
                
                if type(l13) == int:
                    axle4pos.append(l3)
                if type(l14) == int:
                    axle4pos.append(l14)
                if type(l15) == int:
                    axle4pos.append(l15)
                if type(l16) == int:
                    axle4pos.append(l16)

                ### Update tyre type counts                
                if self.axle_4_type == 'Steer':
                        steer_pos += len(axle4pos)
                if self.axle_4_type == 'Drive':
                        drive_pos += len(axle4pos)
                if self.axle_4_type == 'Roll':
                        roll_pos += len(axle4pos)
                
                ## run full distance simulation for every tyre position
                for tyre in axle4pos:
                    least = 10000
                    most = 0
                    ## trials of multiple vehicles
                    for vehicle in range(100):                    
                        completed_distance = 0
                        event = []
                        while completed_distance < self.distance:                            
                            thisTyre = sim_tyre(self, self.axle_4_size, self.axle_4_type)           
                            completed_distance += thisTyre
                            event.append(thisTyre)
                        if len(event) > most:
                            most = len(event)
                        if len(event) < least:
                            least = len(event)
                    
                    # Update the tyre counts
                    if self.axle_4_type == 'Steer':
                        self.steer_count += most
                        self.steer_count_least += least
                    if self.axle_4_type == 'Drive':
                        self.drive_count += most
                        self.drive_count_least += least
                    if self.axle_4_type == 'Roll':
                        self.roll_count += most
                        self.roll_count_least += least

            ### Update wheel position count
            self.wheel_count = len(axle1pos) + len(axle2pos) + len(axle3pos) + len(axle4pos)
            self.res_wpos_result.config(text = self.wheel_count)

            ### Update tyre type counts on screen
            self.res_fitsteer_result.config(text = steer_pos)
            self.res_fitdrive_result.config(text = drive_pos)
            self.res_fitroll_result.config(text = roll_pos)

            ### Update tyres used counts
            self.tyre_count = self.steer_count + self.drive_count + self.roll_count            
            self.res_totused_result.config(text = self.tyre_count)
            self.res_usedsteer_result.config(text = self.steer_count)
            self.res_useddrive_result.config(text = self.drive_count)
            self.res_usedroll_result.config(text = self.roll_count)

            ### Update least tyres used counts
            self.tyre_count_least = self.steer_count_least + self.drive_count_least + self.roll_count_least
            self.res_totworst_result.config(text = self.tyre_count_least)
            self.res_worststeer_result.config(text = self.steer_count_least)
            self.res_worstdrive_result.config(text = self.drive_count_least)
            self.res_worstroll_result.config(text = self.roll_count_least)

            ### Update 'Quote for' tyres
            self.steer_quote = self.steer_count - steer_pos
            self.drive_quote = self.drive_count - drive_pos
            self.roll_quote = self.roll_count - roll_pos
            self.tyre_quote = self.steer_quote + self.drive_quote + self.roll_quote
            
            self.res_quotebest_result.config(text = self.tyre_quote)
            self.res_quotesteer_result.config(text = self.steer_quote)
            self.res_quotedrive_result.config(text = self.drive_quote)
            self.res_quoteroll_result.config(text = self.roll_quote)              
             

        def sim_tyre(self, tyre_size, tyre_type):
            ### get the tyre high and low values
            high, low = tyre_prop(tyre_size, tyre_type)

            # calculate the expected life distribution
            stdDev = (high - low)/4
            # mean = (high - low)/2 + low
            mean = (high + low)/2
            # stdDev = math.sqrt((high - mean)**2+(low - mean)**2)


            return random.gauss(mean, stdDev)

        

        def result_plot(self):
            ## Labels with the following information Grid
            # Configuration -> Wheel Positions  = n Steer + n Drive + n Roll
            # Distance      -> Tyres Used       = n Steer + n Drive + n Roll

            res_config_label = Label(self.result_frame, text = 'Configuration', font = SMALL_FONT, bg = 'snow2')
            res_config_label.grid(row = 0, column = 0)
            self.res_config_result = Label(self.result_frame, text = 'x', font = SMALL_FONT, bg = 'snow2')
            self.res_config_result.grid(row = 1, column = 0)
            res_wpos_label = Label(self.result_frame, text = 'Wheel Positions', font = SMALL_FONT, bg = 'snow2')
            res_wpos_label.grid(row = 0, column = 1)
            self.res_wpos_result = Label(self.result_frame, text = 'x', font = SMALL_FONT, bg = 'snow2')
            self.res_wpos_result.grid(row = 1, column = 1)
            res_fitsteer_label = Label(self.result_frame, text = 'Steer Positions', font = SMALL_FONT, bg = 'snow2')
            res_fitsteer_label.grid(row = 0, column = 2)
            self.res_fitsteer_result = Label(self.result_frame, text = 'x', font = SMALL_FONT, bg = 'snow2')
            self.res_fitsteer_result.grid(row = 1, column = 2)
            res_fitdrive_label = Label(self.result_frame, text = 'Drive Positions', font = SMALL_FONT, bg = 'snow2')
            res_fitdrive_label.grid(row = 0, column = 3)
            self.res_fitdrive_result = Label(self.result_frame, text = 'x', font = SMALL_FONT, bg = 'snow2')
            self.res_fitdrive_result.grid(row = 1, column = 3)
            res_fitroll_label = Label(self.result_frame, text = 'Roll Positions', font = SMALL_FONT, bg = 'snow2')
            res_fitroll_label.grid(row = 0, column = 4)
            self.res_fitroll_result = Label(self.result_frame, text = 'x', font = SMALL_FONT, bg = 'snow2')
            self.res_fitroll_result.grid(row = 1, column = 4)
            
            res_space_top = LabelFrame(self.result_frame, height = 10)
            res_space_top.grid(row = 2, column = 0, columnspan = 5)            
            
            self.res_distance_result = Label(self.result_frame, text = 'x', font = SMALL_FONT, bg = 'snow2')
            self.res_distance_result.grid(row = 3, column = 0)
            res_distance_label = Label(self.result_frame, text = 'Most Tyres Used', font = SMALL_FONT, bg = 'snow2')
            res_distance_label.grid(row = 4, column = 0)            
            res_totused_label = Label(self.result_frame, text = 'Total Tyres', font = SMALL_FONT, bg = 'snow2')
            res_totused_label.grid(row = 3, column = 1)
            self.res_totused_result = Label(self.result_frame, text = 'x', font = SMALL_FONT, bg = 'snow2')
            self.res_totused_result.grid(row = 4, column = 1)
            res_usedsteer_label = Label(self.result_frame, text = 'Steer Tyres', font = SMALL_FONT, bg = 'snow2')
            res_usedsteer_label.grid(row = 3, column = 2)
            self.res_usedsteer_result = Label(self.result_frame, text = 'x', font = SMALL_FONT, bg = 'snow2')
            self.res_usedsteer_result.grid(row = 4, column = 2)
            res_useddrive_label = Label(self.result_frame, text = 'Drive Tyres', font = SMALL_FONT, bg = 'snow2')
            res_useddrive_label.grid(row = 3, column = 3)
            self.res_useddrive_result = Label(self.result_frame, text = 'x', font = SMALL_FONT, bg = 'snow2')
            self.res_useddrive_result.grid(row = 4, column = 3)
            res_usedroll_label = Label(self.result_frame, text = 'Roll Tyres', font = SMALL_FONT, bg = 'snow2')
            res_usedroll_label.grid(row = 3, column = 4)
            self.res_usedroll_result = Label(self.result_frame, text = 'x', font = SMALL_FONT, bg = 'snow2')
            self.res_usedroll_result.grid(row = 4, column = 4)

            res_space_mid = LabelFrame(self.result_frame, height = 10)
            res_space_mid.grid(row = 5, column = 0, columnspan = 5)
            
            res_worst_label = Label(self.result_frame, text = 'Least Tyres Used', font = SMALL_FONT, bg = 'snow2')
            res_worst_label.grid(row = 6, column = 0)
            self.res_totworst_result = Label(self.result_frame, text = 'x', font = SMALL_FONT, bg = 'snow2')
            self.res_totworst_result.grid(row = 6, column = 1)
            self.res_worststeer_result = Label(self.result_frame, text = 'x', font = SMALL_FONT, bg = 'snow2')
            self.res_worststeer_result.grid(row = 6, column = 2)
            self.res_worstdrive_result = Label(self.result_frame, text = 'x', font = SMALL_FONT, bg = 'snow2')
            self.res_worstdrive_result.grid(row = 6, column = 3)
            self.res_worstroll_result = Label(self.result_frame, text = 'x', font = SMALL_FONT, bg = 'snow2')
            self.res_worstroll_result.grid(row = 6, column = 4)            

            res_space_lower = LabelFrame(self.result_frame, height = 10)
            res_space_lower.grid(row = 7, column = 0, columnspan = 5)            

            res_quote_label = Label(self.result_frame, text = 'Quote for', font = SMALL_FONT, bg = 'snow2')
            res_quote_label.grid(row = 8, column = 0)
            self.res_quotebest_result = Label(self.result_frame, text = 'x', font = SMALL_FONT, bg = 'snow2')
            self.res_quotebest_result.grid(row = 8, column = 1)
            self.res_quotesteer_result = Label(self.result_frame, text = 'x', font = SMALL_FONT, bg = 'snow2')
            self.res_quotesteer_result.grid(row = 8, column = 2)
            self.res_quotedrive_result = Label(self.result_frame, text = 'x', font = SMALL_FONT, bg = 'snow2')
            self.res_quotedrive_result.grid(row = 8, column = 3)
            self.res_quoteroll_result = Label(self.result_frame, text = 'x', font = SMALL_FONT, bg = 'snow2')
            self.res_quoteroll_result.grid(row = 8, column = 4)


        def result_clear(self):
            self.res_config_result.grid_forget()          
            self.res_wpos_result.grid_forget()
            self.res_fitsteer_result.grid_forget()
            self.res_fitdrive_result.grid_forget()        
            self.res_fitroll_result.grid_forget()
            self.res_distance_result.grid_forget()
            self.res_totused_result.grid_forget()
            self.res_usedsteer_result.grid_forget()
            self.res_useddrive_result.grid_forget()
            self.res_usedroll_result.grid_forget()
            self.res_totworst_result.grid_forget()
            self.res_worststeer_result.grid_forget()
            self.res_worstdrive_result.grid_forget()
            self.res_worstroll_result.grid_forget()   
            self.res_quotebest_result.grid_forget()
            self.res_quotesteer_result.grid_forget()
            self.res_quotedrive_result.grid_forget()
            self.res_quoteroll_result.grid_forget()

            


root = Tk()
app = Tyre_App(root)
root.mainloop()






