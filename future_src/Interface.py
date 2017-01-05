from tkinter import *
import src.Controller
from src.Test import DEBUG
import time # time.sleep()

class Interface(Frame):

    def __init__(self, window):
        if DEBUG :
            print("->Class Interface : __init__")
        Frame.__init__(self, window, width=300, height=50)
        self.pack(fill=BOTH)

        if DEBUG :
            print("Class Interface : __init__ : creat label")
        # create label
        self.lbl_roll = Label(self, text="Roll : " ).grid(row=0)
        self.lbl_pitch = Label(self, text="Pitch : " ).grid(row=1)
        self.lbl_yaw = Label(self, text="Yaw : ").grid(row=0, column=4)
        self.lbl_thrust = Label(self, text="Thrust : ", fg="blue").grid(row=1, column=4)
        if DEBUG :
            print("Class Interface : __init__ : create label value")
        # create label value
        self.lbl_roll_value = Label(self, text="Roll Value").grid(row=0, column=1)
        self.lbl_pitch_value = Label(self, text="Pitch Value").grid(row=1, column=1)
        self.lbl_yaw_value = Label(self, text="Yaw Value").grid(row=0, column=5)
        self.lbl_thrust_value = Label(self, text="Thrust Value", fg="red").grid(row=1, column=5)

        # change label_value
        # lbl_row_value["text"] = "value"
        if DEBUG :
            print("Class Interface : __init__ : create buttons")
        # create buttons
        self.btn_update = Button(self, text="Update", command=window.update).grid(row=2, column=5)
        self.btn_quit = Button(self, text="Quit", command=window.quit).grid(row=2, column=4)

        if DEBUG :
            print("Class Interface : __init__ : layout")
        # Layout
        #self.canvas = Frame(window, width=300, height=50, borderwidth=1)
        #self.canvas.pack(fill=BOTH)

        if DEBUG:
            print("Class Interface : __init__ : Bind Buttons")
        # Bind Direction Keys
        window.bind('<Left>', self.leftKey)
        window.bind('<Right>', self.rightKey)
        window.bind('<Up>', self.upKey)
        window.bind('<Down>', self.downKey)
        window.bind('<h>', self.thrustUpKey)
        window.bind("<l>", self.thrustDownKey)
        window.bind('<a>', self.leftKey)
        window.bind('<d>', self.rightKey)
        window.bind('<w>', self.upKey)
        window.bind('<s>', self.downKey)
        window.bind('<e>', self.yawRKey)
        window.bind('<q>', self.yawLKey)
        #Emergency Shutdown
        window.bind('<0>', self.zeroKey)



    @staticmethod
    def thrustUpKey(event):
        if DEBUG :
            print("thrustUp key pressed")
        #change label value here or in Main?
        thrust_increment = 500
        src.Controller.Controller._setThrustValue(500)
        #Interface.lbl_thrust_value["texte"] = "test"

    @staticmethod
    def thrustDownKey(event):
        if DEBUG :
            print("thrustDown key pressed")
        thrust_increment = -500
        src.Controller.Controller._setThrustValue(-500)

    @staticmethod
    def upKey(event):
        if DEBUG :
            print("Up key pressed")
        pitch_increment = 5
        src.Controller.Controller._setPitchValue(5)

    @staticmethod
    def downKey(event):
        if DEBUG :
            print("Down key pressed")
        pitch_increment = -5
        src.Controller.Controller._setPitchValue(-5)

    @staticmethod
    def leftKey(event):
        if DEBUG :
            print("Left key pressed")
        roll_increment = -5
        src.Controller.Controller._setRollValue(-5)


    @staticmethod
    def rightKey(event):
        if DEBUG :
            print("Right key pressed")
        roll_increment = 5
        src.Controller.Controller._setRollValue(5)

    @staticmethod
    def yawRKey(event):
        if DEBUG :
            print("Yaw Right key pressed")
        yaw_increment = 22
        src.Controller.Controller._setYawValue(22)

    @staticmethod
    def yawLKey(event):
        if DEBUG :
            print("Yaw Left key pressed")
        yaw_increment = -22
        src.Controller.Controller._setYawValue(-22)

    @staticmethod
    def zeroKey(event):
        if DEBUG:
            print("Zero key pressed")
        src.Controller.Controller._setThrustValue(-60000)

        '''
        #adding labels replaced by .grid
        if DEBUG :
            print("Class Interface : __init__ : add labels to window")
        # add label to window
        self.lbl_row.pack()
        self.lbl_pitch.pack(side="left")
        self.lbl_yaw.pack(side="left")
        self.lbl_thrust.pack(side="left")

        if DEBUG :
            print("Class Interface : __init__ : add labels value to windows")
        # add label value to window
        self.lbl_row_value.pack(side="right")
        self.lbl_pitch_value.pack(side="right")
        self.lbl_yaw_value.pack(side="right")
        self.lbl_thrust_value.pack(side="right")

        if DEBUG :
            print("Class Interface : __init__ : add buttons to window")
        # add button to window
        self.btn_update.pack(side="left")
        self.btn_quit.pack(side="right")'''


#test Interface
def main():
    window = Tk()
    window.title("Controls Value")
    interface = Interface(window)
    interface.mainloop()

if __name__ == '__main__':
    main()
