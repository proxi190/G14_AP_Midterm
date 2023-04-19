import folium
import tkinter as tk
import customtkinter as ctk
import pyodbc
import folium.plugins
from folium import Icon
import webbrowser
from tkinter import ttk 
import geopandas as gpd
import pandas as pd
from tkinter import messagebox
from tkinter import *
import tkinter.ttk as ttk
import functools
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
fp = functools.partial



conn_str = ('DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};' 'DBQ=C:\\Users\\ASUS\\Documents\\BMS\\Database-Python-1-1.accdb;')
conn = pyodbc.connect(conn_str)


class DateOfBirthEntry(ttk.Entry):
    def __init__(self, master=None, **kw):
        # Call the constructor of the parent class
        super().__init__(master, **kw)

        # Set the validation command to the validate_date function
        self.configure(validate="key", validatecommand=(self.register(self.validate_date), '%P'))

    def validate_date(self, date_str):
        # Check that the date string has 10 characters and contains two '/' characters
        if len(date_str) != 10 or date_str.count('/') != 2:
            return False

        # Split the date string into day, month, and year components
        day, month, year = date_str.split('/')

        # Check that the day, month, and year components are valid integers
        try:
            day = int(day)
            month = int(month)
            year = int(year)
        except ValueError:
            return False

        # Check that the day, month, and year components are within valid ranges
        if not (1 <= day <= 31 and 1 <= month <= 12 and 1900 <= year <= 2100):
            return False

        # The date string is valid
        return True

class VerticalScrolledFrame(Frame):

    def __init__(self, parent, sidebar, *args, **kw, ):
        self.sidebar = sidebar
        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())


        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        def _bind_to_mousewheel(event):
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
        def _unbind_from_mousewheel(event):
            canvas.unbind_all("<MouseWheel>")

        Frame.__init__(self, parent, *args, **kw)

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = Scrollbar(self, orient=VERTICAL)
        if self.sidebar.show_scrollbar:
            vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        canvas = Canvas(self, bd=0, highlightthickness=0,
                           yscrollcommand=vscrollbar.set)
        self.canvas = canvas
        canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=NW)

        interior.bind('<Configure>', _configure_interior)
        canvas.bind('<Configure>', _configure_canvas)
        canvas.bind('<Enter>', _bind_to_mousewheel)
        canvas.bind('<Leave>', _unbind_from_mousewheel)


class Sidebar(VerticalScrolledFrame,ttk.Treeview):
    def __init__(self, parent, width=200, show_scrollbar=False):
        self.show_scrollbar = show_scrollbar
        super().__init__(parent, self)
        self.config(width=width)
        self.interior.config(bg="#FFFFFF")
        self.canvas.config(bg="#232323")
        self.pack_propagate(0)

        self.pack(expand=False, side=LEFT, fill=Y)

    def add_spacer(self, text):
        SideBarSpacer(self.interior, text)

    def add_button(self, text, command, icon=None):
        SideBarButton(self.interior, text, command, icon)


def Sprite(picture, res1, res2):
    im = Image.open(picture).convert("RGBA").resize((res1, res2), Image.BOX)
    pic = ImageTk.PhotoImage(im)
    cor = Image.open(picture)
    return pic

class SideBarSpacer(Canvas):
    def __init__(self, parent, text, *args, **kwargs):

        self.frame_color = "#232323"
        self.hover_border_color = "grey"

        Canvas.__init__(self, parent, width=199, height=35, bg=self.frame_color, highlightthickness=1, highlightbackground=self.frame_color, *args, **kwargs)
        self.pack()

        self.text = Label(self, text=text, bg=self.frame_color, font="Segoe 10 bold", fg="lightgrey")
        self.text.place(x=3, y=12)

    def hover(self, event=None):
        self.config(highlightbackground=self.hover_border_color)

    def unhover(self, event=None):
        self.config(highlightbackground=self.frame_color)

    def click(self, event=None):
        print()


class SideBarButton(Canvas):
    def __init__(self, parent, text, command, icon=None, tab=False, *args, **kwargs):

        self.frame_color = "#232323"
        self.hover_color = "#4D4c4c"
        self.hover_border_color = "grey"
        self.is_tab = tab

        self.selected = False

        self.command = command

        Canvas.__init__(self, parent, width=198, height=35, bg=self.frame_color, highlightthickness=1, highlightbackground=self.frame_color, *args, **kwargs)
        self.pack()

        if icon == None:
            pass
        else:
            self.icon = Sprite(icon, 20, 20)
            self.create_image(20, 20, image=self.icon)

        self.text = Label(self, text=text, font="Segoe 10", bg=self.frame_color, fg="lightgrey")
        self.text.place(x=40, y=10)

        self.bind('<Enter>', self.hover)
        self.bind('<Button-1>', self.click)
        if self.is_tab == False:
            self.bind('<ButtonRelease-1>', self.unclick)

        self.text.bind('<Enter>', self.hover)
        self.text.bind('<Button-1>', self.click)
        if self.is_tab == False:
            self.text.bind('<ButtonRelease-1>', self.unclick)

    
    def hover(self, event=None):
        if self.selected == False:
            self.bind('<Leave>', self.unhover)
            self.config(highlightbackground=self.hover_border_color, bg=self.hover_color)
            self.text.config(bg=self.hover_color)

    def unhover(self, event=None):
        self.config(highlightbackground=self.frame_color, bg=self.frame_color)
        self.text.config(bg=self.frame_color)

    def click(self, event=None):

        if self.is_tab:
            self.bind('<Leave>', str)

        self.selected = True

        self.config(bg=self.hover_border_color)
        self.text.config(bg=self.hover_border_color)

        self.command()

    def unclick(self, event=None):
        if not self.selected:
            self.config(bg=self.hover_color)
            self.text.config(bg=self.hover_color)
        else:
            self.config(bg=self.hover_border_color)
            self.text.config(bg=self.hover_border_color)

    def Selected(self):
        self.config(bg=self.hover_border_color)
        self.text.config(bg=self.hover_border_color)

    def Unselected(self):
        self.config(bg=self.frame_color)
        self.text.config(bg=self.frame_color)


class MapApplication:
    def __init__(self):
        self.map = folium.Map(location=[21.0278, 105.8342],tiles='Stamen Terrain', zoom_start=10)
        self.add_markers_from_database()
        self.map.add_child(folium.LatLngPopup())
        self.map.add_child(folium.plugins.MousePosition())
        self.map.add_child(folium.plugins.Fullscreen())

    def add_markers_from_database(self):
        # Fetch the locations from the database
        connection = pyodbc.connect(conn_str)
        cursor = connection.cursor()

        #Query value 
        location_query = "SELECT unit_type, unit_name, Latitude, Longtitude,status,total_troops,troops_standby,training_level,commander_name,commander_dob,commander_rank FROM units"
        cursor.execute(location_query)#This line is to execute the location_query strings

        #Fetch from query value and store in locations; for example locations[0] will hold unit_type 
        #location[1] = unit_name 
        #location[2] = latitude and location[3] = longtitude , etc
        #Change the query vvalue to change information store.
        locations = cursor.fetchall() #This line is todo what i just said 
    

        # Add markers to the map and set the popup to the unit_name
        #Loop through every locations in database

        for location in locations:
            #Set color Red for enemy marker and green for ally marker 
            #If you want to change color, You can change it in the ''
            color = 'red' if location[0].lower() == 'ally' else 'green'
            icon = 'star sign' if location[0].lower() == 'ally' else 'plus sign'

            icon = folium.Icon(color=color,icon = icon)

            #marker properties and function (pop-up and mouse hover)
            marker = folium.Marker(location=[location[2], location[3]], tooltip=f"Unit Name: <strong>{location[1]}</strong><br>Status: <strong>{location[4]}</strong><br>Total troop: <strong>{location[5]}</strong><br>Troop standby: <strong>{location[6]}</strong><br>Traing level: <strong>{location[7]}</strong>"
                                   ,popup = f'Commander: <strong>{location[8]}</strong><br>DoB: <strong>{location[9]}</strong> <br>Rank:<strong>{location[10]}</strong>' #This line is Pop-up but i havent finished this yet 
                                   ,icon=icon
                                   ,Max_width = 2000
                                   ,radius_corner = 0)

            #This line does nothing but i too lazy to remove it 
            marker.add_child(folium.ClickForMarker(popup="Add Marker Here"))
            #Place the marker on the map
            self.map.add_child(marker)

        self.cursor = cursor
        self.connection = connection
        self.map.save("BMS.html")


    #'Run' method to automatically save and run the map so you dont have to manually open it and run
    def run(self):
        webbrowser.open("BMS.html")

#Create login class
class LoginApplication:
    #You know what i does 
    def __init__(self):
        #THis line is for connecting database to the script
        #You have to give a right path otherwise it will not run 
        self.connection = pyodbc.connect(conn_str) #Replace your path here 
        self.cursor = self.connection.cursor()
        #Login GUI properties 
        #You create an blue print of your LOGIN GUI 
        self.root=Tk()
        self.root.title('Login')
        self.root.geometry('925x500+300+20')
        self.root.configure(bg="#fff")
        self.root.resizable(False,False)


        Label(self.root,bg= "#FFFFFF").place(x=50,y=50)
        self.frame=Frame (self.root, width=350, height=350,bg="white")
        self.frame.place (x=480,y=70)


        self.heading=Label(self.frame, text= 'Sign in',fg= '#232323',bg= 'white' ,font=( 'Microsoft YaHei UI Light' ,23, 'bold'))
        self.heading.place(x=100,y=5)

        def on_enter(e):
           self.user.delete(0,'end')

        def on_leave(e):
           name = self.user.get()
           if name=='':
              self.user.insert(0,'Username')
 
        self.user = Entry(self.frame, width=25, fg= 'black',border=0,bg="white",font=('Microsoft YaHei UI Light',11))
        self.user.place(x=30,y=80)
        self.user.insert(0,'Username')
        Frame(self.frame, width=295,height=2, bg='black').place(x=25,y=107)
        self.user.bind('<FocusIn>',on_enter)
        self.user.bind('<FocusOut>',on_leave)

        def on_enter_password(e):
            self.password.delete(0,'end')
            self.password.config(show='*')
    

        def on_leave_password(e):
            name = self.password.get()
            if name=='':
                self.password.config(show='')
                self.password.insert(0,'Password')
            else:
                self.password.config(show='*')


        self.password = Entry(self.frame, width=25, fg= 'black' ,border=0, bg="white",font=('Microsoft YaHei UI Light',11))
        self.password.place(x=30,y=150)
        self.password.insert(0,'Password')
        Frame (self.frame, width=295, height=2, bg='black').place(x=25,y=177)
        self.password.bind('<FocusIn>',on_enter_password)
        self.password.bind('<FocusOut>',on_leave_password)


        Button (self.frame ,width = 39, pady = 8,text= 'Sign in',bg = '#232323',fg = 'white',border =0,command = self.login).place(x=35,y=205)

        self.root.bind("<Return>", lambda event: self.login())
        #Run the windown that include the login GUI 
        self.root.mainloop()


    #login method for login valid
    
    def login(self):
        username = self.user.get()
        password = self.password.get()

        # Perform login validation here
        query = f"SELECT * FROM user_database WHERE Username='{username}' AND Password='{password}'"
        self.cursor.execute(query)
        print('Querying') #Check if it run properly
        

        # Fetch the results
        result = self.cursor.fetchone()
        print('Done') #check if it run properly
        self.root.destroy() #Close the login window
        

        # If login is successful, switch to map view
        if result:
            role = result[3]
            app = SettingPage(role)
            
            

        # Otherwise, display an error message
        else:
            self.message = messagebox.askretrycancel("Fail", "Try again?")
            app = LoginApplication()
            

#-----------------------------------------------PAGE VIEW FROM HERE-----------------------------------------------------


class Page(Frame):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)



class Homepage(Page):
    def __init__(self,master,role,**kw):
        super().__init__(master,**kw)
        self.role = role
        self.Frame_content().pack(fill=BOTH,expand = True)

    def Frame_content(self):
        # Create a frame for the content
        self.frame_content = LabelFrame(self, text='Welcome User')

        # Create a label for the content
        self.label_content = Label(self.frame_content, text=f'Welcome to BMS. You are logged in as {self.role.upper()}', font=20)
        self.label_content.grid(row=0, column=0, columnspan=3, pady=20, padx=20)

        conn = pyodbc.connect(conn_str)

        # Retrieve counts from database
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM units")
        total_units = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM units WHERE unit_type = 'Ally'")
        ally_units = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM units WHERE unit_type = 'Enemy'")
        enemy_units = cursor.fetchone()[0]

        # Create rectangle

        self.allies = Canvas(self.frame_content, width=300, height=100)
        self.allies.create_rectangle(10, 10, 190, 90)
        self.total_allies_title = Label(self.allies, text="Total Allies", font=("Helvetica", 14,"bold"))
        self.total_allies_title.place(x=100,y=25 ,anchor="center")
        self.total_allies_count = Label(self.allies,text=str(ally_units), font=("Helvetica",24,"bold"))
        self.total_allies_count.place(x=100,y=65 ,anchor="center")
        self.allies.grid(row=2,column=1, sticky='ns')
        
        # Add pie chart for allies
        cursor.execute("SELECT status, COUNT(*) FROM units WHERE unit_type = 'Ally' GROUP BY status")
        data = cursor.fetchall()
        
        fig_allies = Figure(figsize=(4, 4))
        ax_allies = fig_allies.add_subplot(111)
        
        labels_allies = [row[0] for row in data]
        sizes_allies = [row[1] for row in data]
        
        plt.rcParams['text.color'] = 'white'
        plt.rcParams['font.weight'] = 'bold'

        colors = ['#9BD770','#66B032','#375F1B','#1B3409']
        ax_allies.pie(sizes_allies, labels=labels_allies, autopct='%.1f%%', colors=colors)
        
        chart_allies = FigureCanvasTkAgg(fig_allies,master=self.frame_content)
        chart_allies.get_tk_widget().config(width=400, height=300)
        chart_allies.draw()
        chart_allies.get_tk_widget().grid(row=3,column=1)

        self.enemies = Canvas(self.frame_content,width=300,height=100)
        self.enemies.create_rectangle(10 ,10 ,190 ,90)
        self.total_enemies_title = Label(self.enemies,text="Total Enemies", font=("Helvetica",14,"bold"))
        self.total_enemies_title.place(x=100,y=25 ,anchor="center")
        self.total_enemies_count = Label(self.enemies,text=str(enemy_units), font=("Helvetica",24,"bold"))
        self.total_enemies_count.place(x=100,y=65 ,anchor="center")
        self.enemies.grid(row=2,column=6, sticky='ns')

        # Add pie chart for enemies
        cursor.execute("SELECT status, COUNT(*) FROM units WHERE unit_type = 'Enemy' GROUP BY status")
        data = cursor.fetchall()
        
        fig_enemies = Figure(figsize=(4, 4))
        ax_enemies = fig_enemies.add_subplot(111)
        
        labels_enemies = [row[0] for row in data]
        sizes_enemies = [row[1] for row in data]
        
        ax_enemies.pie(sizes_enemies, labels=labels_enemies, autopct='%.1f%%', colors=colors)

        chart_enemies = FigureCanvasTkAgg(fig_enemies,master=self.frame_content)
        chart_enemies.get_tk_widget().config(width=400, height=300)
        chart_enemies.draw()
        chart_enemies.get_tk_widget().grid(row=3,column=6)
        

        fig_allies.set_facecolor('#232323')
        ax_allies.set_title('Ally Chart', color='white')
        ax_allies.set_axis_off()        
        fig_enemies.set_facecolor('#232323')
        ax_enemies.set_axis_off()
        ax_enemies.set_title('Enemy Chart', color='white')
        return self.frame_content
    
    def refresh_data(self):
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM units WHERE unit_type = 'Ally'")
        ally_units = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM units WHERE unit_type = 'Enemy'")
        enemy_units = cursor.fetchone()[0]
        self.total_allies_count.config(text=str(ally_units))
        self.total_enemies_count.config(text=str(enemy_units))


class SearchForm(Page):
    def __init__(self, master, table_name, column_names, primary_key, **kw):
        super().__init__(master, **kw)
        self.table_name = table_name
        self.column_names = column_names
        self.primary_key = primary_key
        self.Frame_content().pack(fill=BOTH, expand=True)
        self.tree_units.bind('<<TreeviewSelect>>', lambda event: self.gets_unit())

    def deleteIns(self):
        self.searchbar.delete(0, END)

    def CombineMethod(self):
        self.deleteIns()
        self.search()

    def delete(self):
        # Connect to the database
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Delete data from the table where the primary key column matches the value entered by the user
        value = self.entries['unit_id'].get()
        cursor.execute(f"DELETE FROM {self.table_name} WHERE {self.primary_key} = ?", value)

        # Commit changes and close the database connection
        conn.commit()
        conn.close()

        # Display a message to the user
        messagebox.showinfo(title="Delete", message="Data deleted successfully")

    def update(self):
        # Connect to the database
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        
        # Build the SET and WHERE clauses of the UPDATE statement based on the values entered by the user
        set_clauses = [] 
        values = []
        primary_key_value = self.entries['unit_id'].get()
        values.append(primary_key_value)
        for column_name, entry in self.entries.items():
            if column_name != self.primary_key:
                if column_name in ('Longtitude', 'Latitude'):
                    value = entry.get()
                    value = value.replace('.', ',')
                else:
                    value = entry.get()
                if value:
                    set_clauses.append(f"{column_name} = ?")
                    values.append(value)

        set_str = ", ".join(set_clauses)

        # Execute the UPDATE statement
        cursor.execute(f"UPDATE {self.table_name} SET {set_str} WHERE {self.primary_key} = ?", *values[1:], values[0])

        # Commit changes and close the database connection
        conn.commit()
        conn.close()

        messagebox.showinfo(title="Update", message="Data updated successfully")

    def search(self):
        # Connect to the database
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Build the WHERE clause of the SELECT statement based on the values entered by the user
        where_clauses = []
        values = []
        for column_name, entry in self.entries.items():
            value = entry.get()
            if value:
                if '>' in value:
                    where_clauses.append(f"{column_name} > ?")
                    values.append(value.split('>')[1])
                elif '<' in value:
                    where_clauses.append(f"{column_name} < ?")
                    values.append(value.split('<')[1])
                elif 'to' in value:
                    value = value.split('to')
                    where_clauses.append(f"{column_name} BETWEEN ? AND ?")
                    values.append(value[0])
                    values.append(value[1])
                elif column_name == 'unit_name':
                    where_clauses.append(f"{column_name} LIKE ?")
                    values.append(f"%{value}%")
                else:
                    where_clauses.append(f"{column_name} = ?")
                    values.append(value)

        where_str = " AND ".join(where_clauses)

        # Execute the SELECT statement and fetch the results
        cursor.execute(f"SELECT * FROM {self.table_name} WHERE {where_str}", values)
        rows = cursor.fetchall()

        # Display the results in a treeview
        self.tree_units.delete(*self.tree_units.get_children())
        for row in rows:
            self.tree_units.insert('', 'end', values=[str(value) for value in row])

    def gets_unit(self):
        # Check if an item is selected
        if self.tree_units.selection():
            # Get the selected item
            selected_item = self.tree_units.selection()[0]

            # Get the values of the selected item
            values = self.tree_units.item(selected_item, 'values')

            # Fill the entries in the form with the values of the selected item
            for column_name, value in zip(self.column_names, values):
                if column_name in self.entries:
                    self.entries[column_name].delete(0, END)
                    self.entries[column_name].insert(0, value)


    def refresh_entries(self):
        for entry in self.entries.values():
            entry.delete(0, END)

    def Frame_content(self):

        self.conn = pyodbc.connect(conn_str)
        # Create a cursor object and execute a SELECT statement
        self.cursor = self.conn.cursor()
        self.cursor.execute('SELECT * FROM Units')
        self.frameContent = LabelFrame(self)

        # Create labels and entry fields for each column in the table
        self.searchbarf = LabelFrame(self.frameContent,text='Result Table',highlightthickness = 5)
        self.searchbarf.pack(fill='x',expand=True,anchor='n')
    

        #Create a scroolframe attach to the top conner an fill the 'x' axis
        self.scroolframe = ctk.CTkScrollableFrame(self.searchbarf)
        self.scroolframe.pack(side='top',fill='both',expand=True,anchor='n')

        self.searchbar = Entry(self.searchbarf)
        self.searchbar.pack(fill='x',pady=5)
          
        self.searchubttn = Button(self.searchbarf,text='Search',bg = '#232323',fg = 'white',border =0,command=self.CombineMethod)
        self.searchubttn.pack(fill='x',pady = 5)

        self.deleteubttn = Button(self.searchbarf,text='Delete',bg = '#232323',fg = 'white',border =0,command=self.delete)
        self.deleteubttn.pack(fill='x',pady=5)

        self.updatebttn = Button(self.searchbarf,text='Update',bg='#232323',fg='white',border=0, command=self.update)
        self.updatebttn.pack(fill='x',pady=5)

        self.refresh_button = Button(self.searchbarf, text='Refresh Entries', bg='#232323', fg='white', border=0, command=self.refresh_entries)
        self.refresh_button.pack(fill='x', pady=5)


        self.tree_units = ttk.Treeview(self.scroolframe)
        self.tree_units.pack(fill='both',expand=True,anchor='n')


        self.hscroll = ttk.Scrollbar(self.scroolframe,orient='horizontal',command=self.tree_units.xview)
        self.hscroll.pack(side='bottom',fill='x')

        # Set up the columns and headings based on the cursor description
        columns = [column[0] for column in self.cursor.description]
        self.tree_units['columns'] = columns
        self.tree_units['show'] = 'headings'
        for column in columns:
            self.tree_units.heading(column, text=column)
            self.tree_units.column(column, width=100) 

        self.overall_info = LabelFrame(self.frameContent,text='Search result',highlightthickness = 5)

        #Place the frame right under the previous frame 
        self.overall_info.pack(fill='both',expand=True,anchor='n')

        self.unit_name = Label(self.overall_info,text='Unit name')
        self.unit_name.grid(row=0,column=0)

        self.unit_type = Label(self.overall_info,text='Unit type')
        self.unit_type.grid(row=0,column=1)

        self.unit_status = Label(self.overall_info,text='Unit status')
        self.unit_status.grid(row=0,column=2)

        self.unit_id = Label(self.overall_info,text = 'Unit ID')
        self.unit_id.grid(row = 0,column = 3)

        self.Total_troop = Label(self.overall_info,text = 'Total Troop')
        self.Total_troop.grid(row = 2,column = 0)

        self.Troop_combat = Label(self.overall_info,text = 'Troop combat')
        self.Troop_combat.grid(row = 2,column = 1)

        self.Troop_standby = Label(self.overall_info,text = 'Troop Standby')
        self.Troop_standby.grid(row = 2,column = 2)

        self.Training_level = Label(self.overall_info,text = 'Training level')
        self.Training_level.grid(row = 2,column = 3)

        self.Arm_unit = Label(self.overall_info,text = 'Armament Unit')
        self.Arm_unit.grid(row = 4,column = 0)

        self.area_id = Label(self.overall_info,text = 'Area ID')
        self.area_id.grid(row = 4,column = 1)
                              
        self.lg = Label(self.overall_info,text = 'Longitude')
        self.lg.grid(row = 4,column = 2)

        self.att = Label(self.overall_info,text = 'Lattitude')
        self.att.grid(row = 4,column = 3)

        for widget in self.overall_info.winfo_children():
            widget.grid_configure(padx=15, pady=5)

        #Start the connection
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute("SELECT area_id FROM battlefield_areas")
        self.area_id = [row[0] for row in cursor.fetchall()]
        # Close the database connection
        conn.close()

        self.entries = {} 
        for column_name in self.column_names:
            if column_name == 'unit_id':
                entry = Entry(self.overall_info)
                entry.grid(row=1, column=3)
                self.entries[column_name] = entry
            if column_name == 'unit_name':
                entry = Entry(self.overall_info)
                entry.grid(row=1, column=0)
                self.entries[column_name] = entry
            elif column_name == 'status':
                cbb = ttk.Combobox(self.overall_info,values=["In combat", "Standing by", "Wounded"])
                cbb.grid(row=1, column=2)
                self.entries[column_name] = cbb
            elif column_name == 'total_troops':
                entry = Entry(self.overall_info)
                entry.grid(row=3, column=0)
                self.entries[column_name] = entry
            elif column_name == 'troops_combat':
                entry = Entry(self.overall_info)
                entry.grid(row=3, column=1)
                self.entries[column_name] = entry
            elif column_name == 'troops_standby':
                entry = Entry(self.overall_info)
                entry.grid(row=3, column=2)
                self.entries[column_name] = entry
            elif column_name == 'training_level':
                combobox = ttk.Combobox(self.overall_info, values=["Basic", "Advanced", "Special"])
                combobox.grid(row=3, column=3)
                self.entries[column_name] = combobox
            elif column_name == 'armament_units':
                entry = Entry(self.overall_info)
                entry.grid(row=5, column=0)
                self.entries[column_name] = entry
            elif column_name == 'area_id':
                combobox = ttk.Combobox(self.overall_info, values=self.area_id)
                combobox.grid(row=5, column=1)
                self.entries[column_name] = combobox
            elif column_name == 'Longtitude':
                entry = Entry(self.overall_info)
                entry.grid(row=5, column=2)
                self.entries[column_name] = entry
            elif column_name == 'Latitude':
                entry = Entry(self.overall_info)
                entry.grid(row=5, column=3)
                self.entries[column_name] = entry
            elif column_name == 'unit_type':
                combobox = ttk.Combobox(self.overall_info, values=["Ally","Enemy"])
                combobox.grid(row=1, column=1)
                self.entries[column_name] = combobox

        for widget in self.overall_info.winfo_children():
            widget.grid_configure(padx=15, pady=5)
        
        return self.frameContent
    

class Datapage(Page):
    def __init__(self, master,cursor, **kw):
        super().__init__(master, **kw)
        self.cursor = cursor    
        self.Frame_content().pack(fill=BOTH, expand=True)

    def Frame_content(self):
        self.frameContent = Frame(self)
        notebook = ttk.Notebook(self.frameContent)

        # Create a table for the Units tab
        tab1 = Frame(notebook)
        self.tree_units = ttk.Treeview(tab1)
        self.tree_units.pack(fill=BOTH, expand=True)

        #create a horizontal scrollbar associated with the treeview 
        self.tree_units_scroll = ttk.Scrollbar(tab1, orient=HORIZONTAL, command=self.tree_units.xview)
        self.tree_units_scroll.pack(side=BOTTOM, fill=X)
        self.tree_units.bind('<Left>', lambda event: self.tree_units.xview_scroll(-5, 'units'))
        self.tree_units.bind('<Right>', lambda event: self.tree_units.xview_scroll(5, 'units'))
        
        # Set up the connection string
        conn = pyodbc.connect(conn_str)

        # Create a cursor object and execute a SELECT statement
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Units')

        # Set up the columns and headings based on the cursor description
        columns = [column[0] for column in cursor.description]
        self.tree_units['columns'] = columns
        self.tree_units['show'] = 'headings'
        for column in columns:
            self.tree_units.heading(column, text=column)
            self.tree_units.column(column, width=100)

        # Fetch the results
        rows = cursor.fetchall()

        # Close the cursor and connection
        cursor.close()
        conn.close()

        # Add the data to the Treeview
        for row in rows:
            self.tree_units.insert('', 'end', values=[str(value) for value in row])

        notebook.add(tab1, text='Units')

        # Create a table for the Areas tab
        tab2 = Frame(notebook)
        self.tree_areas = ttk.Treeview(tab2)
        self.tree_areas.pack(fill=BOTH, expand=True)

        # Set up the connection string
        conn = pyodbc.connect(conn_str)

        # Create a cursor object and execute a SELECT statement
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM battlefield_areas')

        # Set up the columns and headings based on the cursor description
        columns = [column[0] for column in cursor.description]
        self.tree_areas['columns'] = columns
        self.tree_areas['show'] = 'headings'
        for column in columns:
            self.tree_areas.heading(column, text=column)
            self.tree_areas.column(column, width=100)

        # Fetch the results
        rows = cursor.fetchall()

        # Close the cursor and connection
        cursor.close()
        conn.close()

        # Add the data to the Treeview
        for row in rows:
            self.tree_areas.insert('', 'end', values=[str(value) for value in row])

        notebook.add(tab2, text='Areas')

        notebook.pack(fill=BOTH, expand=True) 

        return self.frameContent
    

    def refresh_data(self):
        # Clear the Treeviews
        self.tree_units.delete(*self.tree_units.get_children())
        self.tree_areas.delete(*self.tree_areas.get_children())

        # Refresh the data in the Treeviews
        self.cursor.execute('SELECT * FROM Units')
        rows = self.cursor.fetchall()
        for row in rows:
            self.tree_units.insert('', 'end', values=[str(value) for value in row])

        self.cursor.execute('SELECT * FROM battlefield_areas')
        rows = self.cursor.fetchall()
        for row in rows:
            self.tree_areas.insert('', 'end', values=[str(value) for value in row])


class Add_Entry(Page):
    def __init__(self, master,table_name,column_names,primary_key,**kw):
        super().__init__(master, **kw)
        self.table_name = table_name
        self.column_names = column_names
        self.primary_key = primary_key
    
        self.Frame_content().pack(fill=BOTH, expand=True)

    def Frame_content(self):
        self.frameContent = ctk.CTkScrollableFrame(self)
        self.frameContent.columnconfigure(0, weight=1)
        #self.frameContent.rowconfigure(0, weight=1)
        #self.frameContent.rowconfigure(1, weight=0)
        
        #Create a frame for each entry field 
        self.commander_info = LabelFrame(self.frameContent,text = 'Commander Infomation',highlightthickness=5)
        self.commander_info.grid(row = 1,column =0,sticky='news',padx = 10,pady =10)
        #self.commander_info.columnconfigure(0,weight=1)
        self.commander_info.rowconfigure(0,weight=1)
        self.commander_info.rowconfigure(1,weight=1)

        self.unit_info = LabelFrame(self.frameContent,text = 'Unit Infomation',highlightthickness=5)
        self.unit_info.grid(row=0,column=0,sticky = 'nsew')
        #self.unit_info.columnconfigure(0,weight=1)
        self.unit_info.rowconfigure(0,weight=1)
        self.unit_info.rowconfigure(1,weight=1)
        self.unit_type = Label(self.unit_info,text ='Unit type')
        self.unit_type.grid(row = 0,column = 2)

        self.unit_name = Label(self.unit_info,text = 'Unit name')
        self.unit_name.grid(row = 0,column =0)

        self.unit_status = Label(self.unit_info,text = 'Unit status')
        self.unit_status.grid(row = 0,column = 1)

        self.Total_troop = Label(self.unit_info,text = 'Total Troop')
        self.Total_troop.grid(row = 2,column = 0)

        self.Troop_combat = Label(self.unit_info,text = 'Troop combat')
        self.Troop_combat.grid(row = 2,column = 1)

        self.Troop_standby = Label(self.unit_info,text = 'Troop Standby')
        self.Troop_standby.grid(row = 2,column = 2)

        self.Training_level = Label(self.unit_info,text = 'Training level')
        self.Training_level.grid(row = 4,column = 0)

        self.Arm_unit = Label(self.unit_info,text = 'Armament Unit')
        self.Arm_unit.grid(row = 4,column = 1)

        self.area_id = Label(self.unit_info,text = 'Area ID')
        self.area_id.grid(row = 6,column = 2)
                              
        self.lg = Label(self.unit_info,text = 'Longitude')
        self.lg.grid(row = 6,column = 0)

        self.att = Label(self.unit_info,text = 'Lattitude')
        self.att.grid(row = 6,column = 1)


        #Start the connection
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute("SELECT area_id FROM battlefield_areas")
        self.area_id = [row[0] for row in cursor.fetchall()]
        # Close the database connection
        conn.close()

        #Unit entry field 
        self.entries = {}
        for column_name in self.column_names:
            if column_name == 'unit_name':
                entry = Entry(self.unit_info)
                entry.grid(row=1, column=0)
                self.entries[column_name] = entry
            elif column_name == 'status':
                cbb = ttk.Combobox(self.unit_info,values=["In combat", "Standing by", "Wounded"])
                cbb.grid(row=1, column=1)
                self.entries[column_name] = cbb
            elif column_name == 'total_troops':
                entry = Entry(self.unit_info)
                entry.grid(row=3, column=0)
                self.entries[column_name] = entry
            elif column_name == 'troops_combat':
                entry = Entry(self.unit_info)
                entry.grid(row=3, column=1)
                self.entries[column_name] = entry
            elif column_name == 'troops_standby':
                entry = Entry(self.unit_info)
                entry.grid(row=3, column=2)
                self.entries[column_name] = entry
            elif column_name == 'training_level':
                combobox = ttk.Combobox(self.unit_info, values=["Basic", "Advanced", "Special"])
                combobox.grid(row=5, column=0)
                self.entries[column_name] = combobox
            elif column_name == 'armament_units':
                entry = Entry(self.unit_info)
                entry.grid(row=5, column=1)
                self.entries[column_name] = entry
            elif column_name == 'area_id':
                combobox = ttk.Combobox(self.unit_info, values=self.area_id)
                combobox.grid(row=7, column=2)
                self.entries[column_name] = combobox
            elif column_name == 'Longtitude':
                entry = Entry(self.unit_info)
                entry.grid(row=7, column=0)
                self.entries[column_name] = entry
            elif column_name == 'Latitude':
                entry = Entry(self.unit_info)
                entry.grid(row=7, column=1)
                self.entries[column_name] = entry
            elif column_name == 'unit_type':
                combobox = ttk.Combobox(self.unit_info, values=["Ally","Enemy"])
                combobox.grid(row=1, column=2)
                self.entries[column_name] = combobox
            
       
        def submit():
            # Connect to the Database-Python-1-1.accdb database
            conn = pyodbc.connect(conn_str)
            cursor = conn.cursor()
            
            # Insert data from the entry fields into the table (excluding the primary key column)
            columns_str = ", ".join([column_name for column_name in self.column_names if column_name != self.primary_key])
            placeholders_str = ", ".join("?" * len(self.entries))
            values = [entry.get() for entry in self.entries.values()]
            cursor.execute(f"INSERT INTO {self.table_name} ({columns_str}) VALUES ({placeholders_str})", values)
            
            # Commit changes and close the database connection
            conn.commit()
            conn.close()

            print('Done')

  
        for Widget in self.unit_info.winfo_children():
            Widget.grid_configure(padx=10,pady=5)

        #Commander label frame for commander entry field
        

        self.commander_name = Label(self.commander_info,text='Full Name')
        self.commander_name.grid(row=0,column=0)
        self.name = Entry(self.commander_info)
        self.name.grid(row=1, column=0)
        
        
        self.commander_dob = Label(self.commander_info,text='Date Of Birth')
        self.commander_dob.grid(row=0,column=1)
        self.dob = Entry(self.commander_info)
        self.dob.grid(row=1, column=1)

        self.commander_rank = Label(self.commander_info,text='Rank')
        self.commander_rank.grid(row=0,column=2)
        self.rank = ttk.Combobox(self.commander_info,values=['Major','Captain','Lieutenant'])
        self.rank.grid(row=1,column=2)

        self.entries['commander_name'] = self.name
        self.entries['commander_dob'] = self.dob
        self.entries['commander_rank'] = self.rank

    
        #Functioning button (Add,Update,Delete,Search)
        self.functionbttn = LabelFrame(self.frameContent,text='Option')
        self.functionbttn.grid(row=2,column=0,sticky='news',padx = 10,pady =10)
        self.functionbttn.grid_rowconfigure(0,weight=1)
        self.functionbttn.grid_rowconfigure(1,weight=1)

        self.Add = Button(self.functionbttn,text='Add to database',width=20,height =5,bg = '#232323',fg = 'white',border =0,command = submit)
        self.Add.grid(row=0,column=0,padx=10,pady=5)


        for Widget in self.commander_info.winfo_children():
            Widget.grid_configure(padx=10,pady=5,sticky = 'nsew')

    
        return self.frameContent
        
    
class User_setting(Page):
    def __init__(self, master,role, **kw):
        super().__init__(master, **kw)
        self.role = role 
        self.Frame_content().pack(fill=BOTH, expand=True)
        
        

    def Frame_content(self):
        self.frameContent = LabelFrame(self,text= 'User infomation')
        self.user_info = Frame(self.frameContent)
        self.user_info.grid(row=0,column=0,sticky='news',padx = 10,pady =10)

        self.username = Label(self.user_info,text='Username')
        self.username.grid(row=0,column=0)

        self.username_entry = Entry(self.user_info)
        self.username_entry.grid(row=1,column=0)
        self.username_entry.insert(0,'Admin')

        self.password = Label(self.user_info,text='Password')
        self.password.grid(row=0,column=1)

        self.password_entry = Entry(self.user_info)
        self.password_entry.grid(row=1,column=1)
        self.password_entry.insert(0,'************')

        self.role = Label(self.user_info,text='Role')
        self.role.grid(row=0,column=2)
        self.role = Entry(self.user_info)
        self.role.grid(row=1,column=2)
        self.role.insert(0,f'{self.role}')

        for Widget in self.user_info.winfo_children():
            Widget.grid_configure(padx=20,pady=10,sticky = 'nsew')


        return self.frameContent


class SettingPage(Tk):
    def __init__(self,role) -> None:
        super().__init__()
        self.geometry('1000x500+300+30')
        self.title('BMS')
        self.role = role
        self.conn = pyodbc.connect(conn_str)
        self.cursor = self.conn.cursor()
        
        sidebar = Sidebar(self)
        
        sidebar.add_spacer(text='Homepage')
        sidebar.add_button(text="Home",command=self.show_frame4,icon="C:\\Users\\ASUS\\Documents\\BMS\\png\\Home.png")
        sidebar.add_spacer(text='Database Configuration')
        sidebar.add_button(text="Database", command=self.show_frame1,icon="C:\\Users\\ASUS\\Documents\\BMS\\png\\Data.png") 
        sidebar.add_button(text="Map",command=self.switchmap,icon="C:\\Users\\ASUS\\Documents\\BMS\\png\\Map.png")

        if self.role == 'Admin':
            sidebar.add_button(text="Add Unit", command=self.show_frame2,icon="C:\\Users\\ASUS\\Documents\\BMS\\png\\Add.png")
            sidebar.add_button(text="Edit Unit", command=self.show_frame3,icon="C:\\Users\\ASUS\\Documents\\BMS\\png\\Edit.png")
       
        sidebar.add_spacer(text='User Configuration')
        sidebar.add_button(text="Logout",command=self.logout,icon="C:\\Users\\ASUS\\Documents\\BMS\\png\\Logout.png")
        self.frames = {}

        frame1 = Datapage(self,self.cursor)
        frame1.pack_propagate(0)
        self.frames["frame1"] = frame1

        self.cursor.execute("SELECT * FROM units")
        column_names = [column[0] for column in self.cursor.description]
        frame2 = Add_Entry(self,'units',column_names,'unit_id')
        frame2.pack_propagate(0)
        self.frames["frame2"] = frame2

        frame3 = SearchForm(self,'units',column_names,'unit_id')
        frame3.pack_propagate(0)
        self.frames["frame3"] = frame3    

        frame4 = Homepage(self,role)
        frame4.pack_propagate(0)
        self.frames["frame4"] = frame4

        self.show_frame4()

    def show_frame1(self):
        self.frames["frame1"].refresh_data()
        self.frames["frame1"].pack(side="right", fill="both", expand=True)
        self.frames["frame2"].pack_forget()
        self.frames["frame3"].pack_forget()
        self.frames["frame4"].pack_forget()

    def show_frame2(self):
        self.frames["frame2"].pack(side="right", fill="both", expand=True)
        self.frames["frame4"].pack_forget()
        self.frames["frame1"].pack_forget()
        self.frames["frame3"].pack_forget()

    def show_frame3(self):
        self.frames["frame3"].pack(side="right", fill="both", expand=True)
        self.frames["frame1"].pack_forget()
        self.frames["frame2"].pack_forget()
        self.frames["frame4"].pack_forget()

    def show_frame4(self):
        self.frames["frame4"].refresh_data()
        self.frames["frame4"].pack(side="right", fill="both", expand=True)
        self.frames["frame1"].pack_forget()
        self.frames["frame2"].pack_forget()
        self.frames["frame3"].pack_forget()

    def logout(self):
        self.destroy()
        print('Logout succesfully')
        app = LoginApplication()

    def switchmap(self):
        map = MapApplication()
        webbrowser.open("BMS.html")
        

if __name__ == '__main__':
    app = LoginApplication()
#This is the end--------------------------------------------------------------------------------------------