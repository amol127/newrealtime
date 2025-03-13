import wmi
import customtkinter

class InnerFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="#191919")
        self.percentage_label = customtkinter.CTkLabel(self, text="", font=("Arial", 16), fg_color="white")
        self.percentage_label.place(x=10, y=10)

    def update_battery_percentage(self, percentage):
        self.percentage_label.configure(text=f"Battery Percentage: {percentage}%")

class MyFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="#000000")

        self.inner_frames = []
        for i in range(8):
            inner_frame = InnerFrame(self)
            inner_frame.grid(row=i//4, column=i%4, padx=20, pady=10, sticky="nsew")
            self.inner_frames.append(inner_frame)

        self.monitor_battery()

    def monitor_battery(self):
        c = wmi.WMI()
        batteries = c.Win32_Battery()
        
        for i, battery in enumerate(batteries):
            if i < len(self.inner_frames) and "external" in battery.DeviceID.lower():
                percentage = battery.EstimatedChargeRemaining
                self.inner_frames[i].update_battery_percentage(percentage)
    
        self.after(1000, self.monitor_battery)

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        self.geometry(f"{screen_width}x{screen_height}+0+0")
        self.overrideredirect(True)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.my_frame = MyFrame(self)
        self.my_frame.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")


app = App()
app.mainloop()
