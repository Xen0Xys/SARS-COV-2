from tkinter import *
import country_spliter as cs
import time
from tkinter.font import Font


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
        while True:
            time.sleep(1 / 60)
            try:
                self.update()
                list_scale_value = self.list_scale.get()
                if list_scale_value != last_list_scale_value:
                    self.updateList(list_scale_value)
                last_list_scale_value = list_scale_value
            except TclError as e:
                break
    def createGui(self):
        # Do the creation
        self.initializeGui()
        self.setupGui()
        return 0
    def initializeGui(self):
        # Create and place majors elements
        self.search_frame = Frame(self, width = 500, height=100, bg="blue")
        self.search_frame.place(x=0, y=0)
        self.country_list_frame = Frame(self, width = 500, height=350, bg="red")
        self.country_list_frame.place(x=0, y=100)
        
    def setupGui(self):
        # Complete all elements with data and place minors elements
        cs.STATUS #Status du chargement des donnnées
        self.country_list = cs.getCountryList()
        self.select_country = []
        self.int_vars = {}
        self.initializeScale(self.country_list)
        self.createList(self.country_list, 0)
    def initializeScale(self, _country_list):
        self.list_scale = Scale(self, orient='vertical', from_=0, to=len(_country_list) - 5, length=345)
        self.list_scale.place(x=-23, y=100)
    def updateList(self, index):
        for c in self.country_list_frame.winfo_children():
            c.destroy()
        self.createList(self.country_list, index)
    def getSelectedCountries(self):
        select_countries = []
        for country in self.int_vars.keys():
            if self.int_vars[country].get() == 1:
                select_countries.append(country)
        return select_countries
    def createList(self, _country_list, _start_index):
        custom_font = Font(family="Helveltica", size=14)
        def createLine(_country, _index):
            canvas = Canvas(self.country_list_frame, width=460, height=50, bg="light grey", highlightthickness=0)
            y = 53 * _index + 3
            canvas.place(x=30, y=y)
            Label(canvas, text=_country, bg="light grey", font=custom_font).place(x=0, y=10)
            if _country not in self.int_vars.keys():
                self.int_vars[_country] = IntVar()
            Checkbutton(canvas, text="Select country", variable=self.int_vars[_country]).place(x=358, y=12)
        j = 0
        for i in range(_start_index, _start_index + 6):
            try:
                createLine(_country_list[i], j)
                j += 1
            except IndexError:
                pass

gui = GUI()