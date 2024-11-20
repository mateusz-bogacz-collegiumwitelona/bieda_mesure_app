import csv
from tkinter import *
from tkinter import ttk
from datetime import datetime
import os

from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class FrameOption:
    def __init__(self, root):
        self.root = root
        self.frm = ttk.Frame(self.root, padding=10)
        self.frm.grid()

    def SetTitle(self, title):
        self.root.title(title)


class MainFrame(FrameOption):
    def __init__(self, root):
        super().__init__(root)
        self.SetTitle("Bieda Ciśnienie")
        self.CreateButton()

    def CreateButton(self):
        ttk.Label(self.frm, text="Bieda Ciśnienie").grid(column=0, row=0, columnspan=3)

        ttk.Button(self.frm, text="Dodaj ciśnienie", command=self.OpenAddMeasure).grid(column=0, row=1)
        ttk.Button(self.frm, text="Wczytaj ciśnienie", command=self.OpenGetMeasure).grid(column=1, row=1)
        ttk.Button(self.frm, text="Zamknij", command=self.root.destroy).grid(column=2, row=1)

    def OpenAddMeasure(self):
        add_window = Toplevel(self.root)
        AddMeasure(add_window)

    def OpenGetMeasure(self):
        get_window = Toplevel(self.root)
        GetMeasure(get_window)


class AddMeasure(FrameOption):
    def __init__(self, root):
        super().__init__(root)
        self.SetTitle("Dodaj pomiar")
        self._systolic = None
        self._diatolic = None
        self._pulse = None
        self.GetInFrame()
        self.CreateButton()

    def CreateButton(self):
        ttk.Button(self.frm, text="Zapisz", command=self.saveToFile).grid(column=0, row=3)
        ttk.Button(self.frm, text="Zamknij", command=self.root.destroy).grid(column=1, row=3)

    def GetInFrame(self):
        self._systolic = ttk.Entry(self.frm)
        self._systolic.grid(column=1, row=0)
        ttk.Label(self.frm, text="Górne").grid(column=0, row=0)

        self._diatolic = ttk.Entry(self.frm)
        self._diatolic.grid(column=1, row=1)
        ttk.Label(self.frm, text="Dolne").grid(column=0, row=1)

        self._pulse = ttk.Entry(self.frm)
        self._pulse.grid(column=1, row=2)
        ttk.Label(self.frm, text="Puls").grid(column=0, row=2)

    def saveToFile(self):
        systolic = self._systolic.get()
        diastolic = self._diatolic.get()
        pulse = self._pulse.get()
        datetime_str = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

        with open("measure.csv", "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            if os.path.getsize("measure.csv") == 0:
                writer.writerow(["Date", "Systolic", "Diastolic", "Pulse"])
            writer.writerow([datetime_str, systolic, diastolic, pulse])

        self._systolic.delete(0, END)
        self._diatolic.delete(0, END)
        self._pulse.delete(0, END)


class GetMeasure(FrameOption):

    def __init__(self, root):
        super().__init__(root)
        self.SetTitle("Lista pomiarów")
        self.GetInFrame()
        self.CreateButton()
        self.createPlot()

    def CreateButton(self):
        ttk.Button(self.frm, text="Zamknij", command=self.root.destroy).grid(column=1, row=5)

    def GetInFrame(self):
        self.tree = ttk.Treeview(self.frm, columns=("Date", "Systolic", "Diastolic", "Pulse"), show="headings")
        self.tree.heading("Date", text="Data")
        self.tree.heading("Systolic", text="Górne")
        self.tree.heading("Diastolic", text="Dolne")
        self.tree.heading("Pulse", text="Puls")
        self.tree.grid(column=0, row=0, columnspan=3)

        self.loadData()

    def loadData(self):
        file_path = "./measure.csv"
        if not os.path.exists(file_path):
            return

        with open(file_path, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                self.tree.insert("", END, values=(row[0], row[1], row[2], row[3]))

    def createPlot(self):
        file_path = "./measure.csv"
        if not os.path.exists(file_path):
            ttk.Label(self.frm, text="Brak danych").grid(column=0, row=3)
            return

        dates = []
        systolics = []
        diastolics = []

        with open(file_path, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                dates.append(row[0])
                systolics.append(int(row[1]))
                diastolics.append(int(row[2]))

        figure = plt.figure(figsize=(8, 6), dpi=100)
        ax = figure.add_subplot(111)
        ax.plot(dates, systolics, label="Ciśnienie Skurczowe")
        ax.plot(dates, diastolics, label="Ciśnienie Rozkurczowe")
        ax.set_xlabel("")
        ax.xaxis.set_tick_params(labelbottom=False)
        ax.set_ylabel("Ciśnienie [mmHg]")
        ax.legend()
        ax.grid(True)
        figure.autofmt_xdate()

        plot_frame = ttk.Frame(self.frm)
        plot_frame.grid(column=0, row=4, columnspan=3, sticky='nw')

        canvas = FigureCanvasTkAgg(figure, plot_frame)
        canvas.get_tk_widget().grid(row=0, column=0, sticky='nsew')

        plot_frame.columnconfigure(0, weight=1)
        plot_frame.rowconfigure(0, weight=1)

        canvas.draw()


if __name__ == "__main__":
    root = Tk()
    app = MainFrame(root)
    root.mainloop()
