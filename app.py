import customtkinter
from tkinter import ttk
import os
from PIL import Image

# 5-Day Weather Forecast using CTkScrollableFrame
class ScrollableWeatherFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, forecast_data, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)

        # Add weather details
        for index, forecast in enumerate(forecast_data):
            day_label = customtkinter.CTkLabel(self, text=f"{forecast['day']}", font=("Arial", 12))
            day_label.grid(row=index, column=0, padx=10, pady=(5, 0), sticky="w")

            temp_label = customtkinter.CTkLabel(self, text=f"Temp: {forecast['temp']}", font=("Arial", 10))
            temp_label.grid(row=index, column=1, padx=10, pady=(5, 0), sticky="w")

            cloud_label = customtkinter.CTkLabel(self, text=f"Cloud Cover: {forecast['cloud_cover']}", font=("Arial", 10))
            cloud_label.grid(row=index, column=2, padx=10, pady=(5, 0), sticky="w")

            precip_label = customtkinter.CTkLabel(self, text=f"Precip: {forecast['precip']}", font=("Arial", 10))
            precip_label.grid(row=index, column=3, padx=10, pady=(5, 0), sticky="w")


# Example Forecast Data
forecast_data = [
    {"day": "Day 1", "temp": "20°C", "cloud_cover": "25%", "precip": "5%"},
    {"day": "Day 2", "temp": "22°C", "cloud_cover": "50%", "precip": "10%"},
    {"day": "Day 3", "temp": "18°C", "cloud_cover": "10%", "precip": "0%"},
    {"day": "Day 4", "temp": "21°C", "cloud_cover": "30%", "precip": "15%"},
    {"day": "Day 5", "temp": "19°C", "cloud_cover": "40%", "precip": "20%"},
    {"day": "Day 6", "temp": "20°C", "cloud_cover": "25%", "precip": "5%"},
    {"day": "Day 7", "temp": "22°C", "cloud_cover": "50%", "precip": "10%"},
    {"day": "Day 8", "temp": "18°C", "cloud_cover": "10%", "precip": "0%"},
    {"day": "Day 9", "temp": "21°C", "cloud_cover": "30%", "precip": "15%"},
    {"day": "Day 10", "temp": "19°C", "cloud_cover": "40%", "precip": "20%"}\
]





class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("AgroAssistant")
        self.geometry("700x450")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")), size=(26, 26))
        self.large_test_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "large_test_image.png")), size=(500, 150))
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")), size=(20, 20))
        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20))
        self.chat_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "chat_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "chat_light.png")), size=(20, 20))
        self.add_user_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "add_user_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "add_user_light.png")), size=(20, 20))

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  AgroAssistant", image=self.logo_image,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Dashboard",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Frame 2",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.chat_image, anchor="w", command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        self.frame_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Frame 3",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.add_user_image, anchor="w", command=self.frame_3_button_event)
        self.frame_3_button.grid(row=3, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)
        self.home_frame.grid_columnconfigure(1, weight=1)  

        # Title 
        self.dashboard_title = customtkinter.CTkLabel(self.home_frame, text="Dashboard", font=("Arial", 25))
        self.dashboard_title.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        # Soil Moisture Level Progress Bar
        self.moisture_bar_label = customtkinter.CTkLabel(self.home_frame, text="Soil Moisture Level:", font=("Arial", 14))
        self.moisture_bar_label.grid(row=1, column=0, padx=20, sticky="w")

        soil_moisture = 0.9

        if soil_moisture < 0.4:
            self.moisture_bar = customtkinter.CTkProgressBar(self.home_frame, orientation="horizontal", progress_color=("red", "red"))
            self.moisture_bar.grid(row=2, column=0, padx=20, pady=10, sticky="w")
        elif soil_moisture > 0.4 and soil_moisture <= 0.7:
            self.moisture_bar = customtkinter.CTkProgressBar(self.home_frame, orientation="horizontal", progress_color=("green", "green"))
            self.moisture_bar.grid(row=2, column=0, padx=20, pady=10, sticky="w")
        else:
            self.moisture_bar = customtkinter.CTkProgressBar(self.home_frame, orientation="horizontal", progress_color=("blue", "blue"))
            self.moisture_bar.grid(row=2, column=0, padx=20, pady=10, sticky="w")

        self.moisture_bar.set(soil_moisture)

        # Soil Temperature Level Progress Bar
        self.soil_temperature_bar_label = customtkinter.CTkLabel(self.home_frame, text="Soil Temperature Level:", font=("Arial", 14))
        self.soil_temperature_bar_label.grid(row=3, column=0, padx=20, pady=10, sticky="w")

        soil_temperature = 18

        if soil_temperature/40 < 0.375:
            self.soil_temperature_bar = customtkinter.CTkProgressBar(self.home_frame, orientation="horizontal", progress_color=("blue", "blue"))
            self.soil_temperature_bar.grid(row=4, column=0, padx=20, pady=10, sticky="w")
        elif soil_temperature/40 >= 0.375 and soil_moisture/40 <= 0.55:
            self.soil_temperature_bar = customtkinter.CTkProgressBar(self.home_frame, orientation="horizontal", progress_color=("green", "green"))
            self.soil_temperature_bar.grid(row=4, column=0, padx=20, pady=10, sticky="w")
        else:
            self.soil_temperature_bar = customtkinter.CTkProgressBar(self.home_frame, orientation="horizontal", progress_color=("red", "red"))
            self.soil_temperature_bar.grid(row=4, column=0, padx=20, pady=10, sticky="w")

        self.soil_temperature_bar.set(soil_temperature/40)

        #5-Day weather forecast
        weather_frame = ScrollableWeatherFrame(
            master=self.home_frame,
            forecast_data=forecast_data,
            width=650,
            height=150,
            corner_radius=10,
            fg_color="transparent",
        )
        weather_frame.grid(row=5, column=0, padx=20, pady=10, sticky="ew")






        # create second frame
        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # create third frame
        self.third_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # select default frame
        self.select_frame_by_name("home")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()
        if name == "frame_3":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")

    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)


if __name__ == "__main__":
    app = App()
    app.mainloop()
