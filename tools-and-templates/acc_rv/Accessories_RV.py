from tkinter import Tk, Frame, BOTH, RIGHT, LEFT, RAISED, X, Checkbutton, BooleanVar, END
from tkinter.ttk import Button, Label, Entry

def crane_rv(price, age):
    """
    inputs
    price - int = purchase price of the crane
    age - int = age of crane at end of contract

    return
    residual - int = residual value in curreny
    """
    if age > 10:
        return 0
    
    rv_dict = {
        1 : 0.5,
        2 : 0.45,
        3 : 0.41,
        4 : 0.36,
        5 : 0.33,
        6 : 0.30,
        7 : 0.27,
        8 : 0.24,
        9 : 0.22,
        10: 0.19
        }

    rv = rv_dict[age]
    residual = int(price * rv)

    return residual

def trailer_rv(price, age):
    """
    inputs
    price - int = purchase price of the trailer
    age - int = age of trailer at end of contract

    return
    residual - int = residual value in curreny
    """
    if age > 10:
        return 0

    rv_dict = {
        1 : 0.75,
        2 : 0.67,
        3 : 0.59,
        4 : 0.52,
        5 : 0.46,
        6 : 0.40,
        7 : 0.35,
        8 : 0.31,
        9 : 0.27,
        10: 0.23
        }

    rv = rv_dict[age]
    residual = int(price * rv)

    return residual


def forklift_rv(price, hours):
    """
    inputs
    price - int = purchase price of the forklift
    hours - int = hours completed by the forklift at end of contract

    return
    residual - int = residual value in curreny
    """
    if hours > 9000:
        return 0

    expected_life = 10000
    remaining_life = expected_life - hours
    
    rv = (remaining_life / expected_life) - 0.1 

    residual = int(price * rv)

    return residual



class RVCalculator(Frame):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Generate the window
        self.master.title("RV Calculator")
        self.pack(fill=BOTH, expand=True)

        # Crane Variables
        self.crane = BooleanVar()
        self.crane_price = 0
        self.crane_age = 0
        self.crane_rv = 0        

        # Crane Frame                
        ## Generate the frame
        frame1 = Frame(self, relief=RAISED, borderwidth=5)
        frame1.pack(fill=X)

        ## The select button        
        craneCheckButton = Checkbutton(frame1, text="Crane", variable = self.crane, command = self.update)
        craneCheckButton.deselect()
        craneCheckButton.grid(column=0, row=0 ,padx=5, pady=5)

        ## Price Entry
        lbl1 = Label(frame1, text="Price (New)", width=10)
        lbl1.grid(column=1, row=0, padx=5, pady=5)

        self.crane_price_request = Entry(frame1)
        self.crane_price_request.insert(0, self.crane_price)
        self.crane_price_request.grid(column=2, row=0, padx=5, pady=5)

        ## Age Entry
        lbl2 = Label(frame1, text="Age (Years)", width=10)
        lbl2.grid(column=1, row=1, padx=5, pady=5)

        self.crane_age_request = Entry(frame1)
        self.crane_age_request.insert(END, self.crane_age)
        self.crane_age_request.grid(column=2, row=1, padx=5, pady=5)

        ## RV Output
        craneRV = Label(frame1, text="RV (Rand)", width=10)
        craneRV.grid(column=3, row=2, padx=5, pady=5)

        self.craneResult = Label(frame1, text="0")
        self.craneResult.grid(column=4, row=2, padx=5, pady=5)

        # Trailer
        ## Trailer Variables
        self.trailer = BooleanVar()
        self.trailer_price = 0
        self.trailer_age = 0
        self.trailer_rv = 0
        
        # Trailer Frame                
        ## Generate the frame
        frame2 = Frame(self, relief=RAISED, borderwidth=5)
        frame2.pack(fill=X)

        ## The select button        
        trailerCheckButton = Checkbutton(frame2, text="Trailer", variable = self.trailer, command = self.update)
        trailerCheckButton.deselect()
        trailerCheckButton.grid(column=0, row=0 ,padx=5, pady=5)

        ## Price Entry
        lbl3 = Label(frame2, text="Price (New)", width=10)
        lbl3.grid(column=1, row=0, padx=5, pady=5)

        self.trailer_price_request = Entry(frame2)
        self.trailer_price_request.insert(0, self.trailer_price)
        self.trailer_price_request.grid(column=2, row=0, padx=5, pady=5)

        ## Age Entry
        lbl4 = Label(frame2, text="Age (Years)", width=10)
        lbl4.grid(column=1, row=1, padx=5, pady=5)

        self.trailer_age_request = Entry(frame2)
        self.trailer_age_request.insert(END, self.trailer_age)
        self.trailer_age_request.grid(column=2, row=1, padx=5, pady=5)

        ## RV Output
        trailerRV = Label(frame2, text="RV (Rand)", width=10)
        trailerRV.grid(column=3, row=2, padx=5, pady=5)

        self.trailerResult = Label(frame2, text="0")
        self.trailerResult.grid(column=4, row=2, padx=5, pady=5)
        
                
        # Forklift
        ## Forklift Variables
        self.forklift = BooleanVar()
        self.forklift_price = 0
        self.forklift_age = 0
        self.forklift_rv = 0
        
        # Forklift Frame                
        ## Generate the frame
        frame3 = Frame(self, relief=RAISED, borderwidth=5)
        frame3.pack(fill=X)

        ## The select button        
        forkliftCheckButton = Checkbutton(frame3, text="Forklift", variable = self.forklift, command = self.update)
        forkliftCheckButton.deselect()
        forkliftCheckButton.grid(column=0, row=0 ,padx=5, pady=5)

        ## Price Entry
        lbl5 = Label(frame3, text="Price (New)", width=10)
        lbl5.grid(column=1, row=0, padx=5, pady=5)

        self.forklift_price_request = Entry(frame3)
        self.forklift_price_request.insert(0, self.forklift_price)
        self.forklift_price_request.grid(column=2, row=0, padx=5, pady=5)

        ## Age Entry
        lbl6 = Label(frame3, text="Age (Hours)", width=10)
        lbl6.grid(column=1, row=1, padx=5, pady=5)

        self.forklift_age_request = Entry(frame3)
        self.forklift_age_request.insert(END, self.forklift_age)
        self.forklift_age_request.grid(column=2, row=1, padx=5, pady=5)

        ## RV Output
        forkliftRV = Label(frame3, text="RV (Rand)", width=10)
        forkliftRV.grid(column=3, row=2, padx=5, pady=5)

        self.forkliftResult = Label(frame3, text="0")
        self.forkliftResult.grid(column=4, row=2, padx=5, pady=5)

        # Buttons        
        calcButton = Button(self, text="Calculate", command=self.calculate)
        calcButton.pack(side=LEFT, padx=10, pady=20)

        quitButton = Button(self, text="Quit", command=self.quit)
        quitButton.pack(side=RIGHT, padx=10, pady=20)

    
    def update(self):

        # Crane
        if self.crane.get() == True:        
            if int(self.crane_price_request.get()) > 0:
                self.crane_price = int(self.crane_price_request.get())
            else:
                self.crane_price_request.delete(0, END)
                self.crane_price_request.insert(END, "Please enter price")            
        
            if int(self.crane_age_request.get()) > 0:
                self.crane_age = int(self.crane_age_request.get())
            else:
                self.crane_age_request.delete(0, END)
                self.crane_age_request.insert(END, "Please enter age")  
        
        else:
            self.crane_price_request.delete(0, END)
            self.crane_price_request.insert(END, 0)

            self.crane_age_request.delete(0, END)
            self.crane_age_request.insert(END, 0)

        # Trailer
        if self.trailer.get() == True:        
            if int(self.trailer_price_request.get()) > 0:
                self.trailer_price = int(self.trailer_price_request.get())
            else:
                self.trailer_price_request.delete(0, END)
                self.trailer_price_request.insert(END, "Please enter price")            
        
            if int(self.trailer_age_request.get()) > 0:
                self.trailer_age = int(self.trailer_age_request.get())
            else:
                self.trailer_age_request.delete(0, END)
                self.trailer_age_request.insert(END, "Please enter age")  
        
        else:
            self.trailer_price_request.delete(0, END)
            self.trailer_price_request.insert(END, 0)

            self.trailer_age_request.delete(0, END)
            self.trailer_age_request.insert(END, 0)

        # Forklift
        if self.forklift.get() == True:        
            if int(self.forklift_price_request.get()) > 0:
                self.forklift_price = int(self.forklift_price_request.get())
            else:
                self.forklift_price_request.delete(0, END)
                self.forklift_price_request.insert(END, "Please enter price")            
        
            if int(self.forklift_age_request.get()) > 0:
                self.forklift_age = int(self.forklift_age_request.get())
            else:
                self.forklift_age_request.delete(0, END)
                self.forklift_age_request.insert(END, "Please enter age")  
        
        else:
            self.forklift_price_request.delete(0, END)
            self.forklift_price_request.insert(END, 0)

            self.forklift_age_request.delete(0, END)
            self.forklift_age_request.insert(END, 0)



    def calculate(self): 

        # Crane
        if self.crane.get() == True:
            try:  
                self.crane_price = int(self.crane_price_request.get())
                self.crane_age = int(self.crane_age_request.get())

                if int(self.crane_price) > 0 and int(self.crane_age) > 0:                    
                    # self.craneResult['text'] = str(crane_rv(self.crane_price, self.crane_age))
                    self.craneResult['text'] = f"{crane_rv(self.crane_price, self.crane_age):,}"
            
            except ValueError:
                self.craneResult['text'] = 0
        
        # Trailer
        if self.trailer.get() == True:
            try:  
                self.trailer_price = int(self.trailer_price_request.get())
                self.trailer_age = int(self.trailer_age_request.get())

                if int(self.trailer_price) > 0 and int(self.trailer_age) > 0:                    
                    self.trailerResult['text'] = f"{trailer_rv(self.trailer_price, self.trailer_age):,}"
            
            except ValueError:
                self.trailerResult['text'] = 0
        
        # Forklift
        if self.forklift.get() == True:
            try:  
                self.forklift_price = int(self.forklift_price_request.get())
                self.forklift_age = int(self.forklift_age_request.get())

                if int(self.forklift_price) > 0 and int(self.forklift_age) > 0:                    
                    self.forkliftResult['text'] = f"{forklift_rv(self.forklift_price, self.forklift_age):,}"
            
            except ValueError:
                self.forkliftResult['text'] = 0



def main():

    root = Tk()
    ex = RVCalculator()
    root.geometry("500x400+300+300")
    root.mainloop()

if __name__ == '__main__':
    main()
