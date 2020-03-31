from tkinter import *
import country_spliter as cs
import time
from tkinter.font import Font
import matplotlib.pyplot as plt


class GUI(Tk):
    def __init__(self):
        super().__init__()
        self.title("SARS-COV-2 Suivi")
        self.geometry("500x450")
        self.resizable(width=False, height=False)
        create_gui_status_code = self.createGui()
        if create_gui_status_code == 0:
            self.mainLoop()
    def mainLoop(self):
        last_list_scale_value = 0
        last_searched_country_name = ""
        while True:
            time.sleep(1 / 60)
            try:
                self.update()
                list_scale_value = self.list_scale.get()
                searched_country_name = self.searched_country.get()
                #Check scale value
                if list_scale_value != last_list_scale_value:
                    self.createList(self.country_list, list_scale_value)
                last_list_scale_value = list_scale_value
                #Check search value
                if searched_country_name != last_searched_country_name:
                    self.createList(self.getCountryListFromString(searched_country_name), list_scale_value)
                last_searched_country_name = searched_country_name
            except TclError as e:
                break
    def createGui(self):
        # Do the creation
        self.initializeGui()
        self.setupGui()
        return 0
    def initializeGui(self):
        # Create and place majors elements
        self.control_frame = Frame(self, width = 500, height=100, bg="light blue")
        self.control_frame.place(x=0, y=0)
        self.country_list_frame = Frame(self, width = 500, height=350, bg="red")
        self.country_list_frame.place(x=0, y=100)
    def setupGui(self):
        # Complete all elements with data and place minors elements
        cs.STATUS #Status du chargement des donnnées
        self.country_list = cs.getCountryList()
        self.select_country = []
        self.int_vars = {}
        self.initializeScale(self.country_list)
        self.createControlFrame()
        self.createList(self.country_list, 0)
    def createControlFrame(self):
        bg_color = "light blue"
        custom_font = Font(family="Helveltica", size=14)
        self.searched_country = StringVar()
        Label(self.control_frame, text="Rechecher un pays:", font=custom_font, bg=bg_color).place(x=5, y=5)
        Entry(self.control_frame, textvariable=self.searched_country, font=custom_font).place(x=10, y=35)
        Button(self.control_frame, text="Tracer les courbes", font=custom_font, command=self.createCurves).place(x=280, y=31)
    def initializeScale(self, _country_list):
        self.list_scale = Scale(self, orient='vertical', from_=0, to=len(_country_list) - 5, length=345)
        self.list_scale.place(x=-23, y=100)
    def getCountryListFromString(self, _searched_text):
        new_country_list = []
        for country in self.country_list:
            if _searched_text.lower() in country.lower():
                new_country_list.append(country)
        return new_country_list
    def getSelectedCountries(self):
        select_countries = []
        for country in self.int_vars.keys():
            if self.int_vars[country].get() == 1:
                select_countries.append(country)
        return select_countries
    def createList(self, _country_list, _start_index):
        #Create new country list graphics
        for c in self.country_list_frame.winfo_children():
            c.destroy()
        custom_font = Font(family="Helveltica", size=14)
        bg_color = "light grey"
        def createLine(_country, _index):
            canvas = Canvas(self.country_list_frame, width=460, height=50, bg=bg_color, highlightthickness=0)
            y = 53 * _index + 3
            canvas.place(x=30, y=y)
            Label(canvas, text=_country, bg=bg_color, font=custom_font).place(x=0, y=10)
            if _country not in self.int_vars.keys():
                self.int_vars[_country] = IntVar()
            Checkbutton(canvas, text="Choisir ce pays", variable=self.int_vars[_country], bg=bg_color).place(x=340, y=12)
        def createErrorMessage():
            canvas = Canvas(self.country_list_frame, width=460, height=50, bg=bg_color, highlightthickness=0)
            canvas.place(x=30, y=3)
            Label(canvas, text="Le pays n'a pas pu être trouvé", bg=bg_color, font=custom_font).place(x=0, y=10)
        if len(_country_list) != 0:
            j = 0
            for i in range(_start_index, _start_index + 6):
                try:
                    createLine(_country_list[i], j)
                    j += 1
                except IndexError:
                    pass
        else:
            createErrorMessage()
    def createCurves(self):
        selected_country = self.getSelectedCountries()
        country_data = cs.getSpecifiedCountryData(selected_country)
        plt.plot([1, 2, 3, 4], [1, 4, 9, 16])
        plt.show()
        # No code after

gui = GUI()