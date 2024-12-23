import customtkinter
import os
from PIL import Image
import irrigation
import requests
from geopy.geocoders import Nominatim
import yaml

with open('auth.yaml', 'r') as file:
    auth = yaml.safe_load(file)

stormglass_response = requests.get(
  'https://api.stormglass.io/v2/bio/point',
  params={
    'lat': 58.7984,
    'lng': 17.8081,
    'params': ','.join(['soilMoisture', 'soilTemperature'])
  },
  headers={
    'Authorization': auth['stormglass']['apiKey']
  }
)

stormglass_data = stormglass_response.json()

weatherapi_response = requests.get(
    'https://api.weatherapi.com/v1/forecast.json', 
    params={
        'key': auth['weatherapi']['apiKey'],
        'q': "Atlanta",
        'days': 10
    }
)

weatherapi_data = weatherapi_response.json()


average_temperatures = []
average_cloud_covers = []
average_precipitations = []

for day in weatherapi_data['forecast']['forecastday']:
    total_temp = 0
    total_cloud = 0
    total_precip = 0
    count = 0

    for hour in day['hour']:
        total_temp += hour['temp_c']
        total_cloud += hour['cloud']
        total_precip += hour['precip_in']
        count += 1

    avg_temp = round(total_temp / count)
    avg_cloud = round(total_cloud / count)
    avg_precip = round(total_precip / count)

    average_temperatures.append(avg_temp)
    average_cloud_covers.append(avg_cloud)
    average_precipitations.append(avg_precip)

    
import customtkinter
import os
from PIL import Image


class ScrollableWeatherFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, forecast_data, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")

        self.thermostat_icon = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "thermostat.png")),
            dark_image=Image.open(os.path.join(image_path, "thermostat.png")),
            size=(20, 20),
        )
        self.cloud_cover_icon = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "cloud.png")),
            dark_image=Image.open(os.path.join(image_path, "cloud.png")),
            size=(20, 20),
        )
        self.rain_icon = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "rain.png")),
            dark_image=Image.open(os.path.join(image_path, "rain.png")),
            size=(20, 20),
        )

        for index, forecast in enumerate(forecast_data):
            day_frame = customtkinter.CTkFrame(self, fg_color="transparent")
            day_frame.grid(row=index, column=0, padx=10, pady=(5, 0), sticky="w")

            day_text_label = customtkinter.CTkLabel(
                day_frame,
                text=f"{forecast['day']}",
                font=("Arial", 12)
            )
            day_text_label.pack(side="left", padx=5)

         
            temp_frame = customtkinter.CTkFrame(self, fg_color="transparent")
            temp_frame.grid(row=index, column=1, padx=10, pady=(5, 0), sticky="w")

            temp_icon_label = customtkinter.CTkLabel(
                temp_frame,
                text="",
                image=self.thermostat_icon
            )
            temp_icon_label.pack(side="left")

            temp_text_label = customtkinter.CTkLabel(
                temp_frame,
                text=f"Temp: {forecast['temp']}",
                font=("Arial", 10)
            )
            temp_text_label.pack(side="left", padx=5)

            cloud_frame = customtkinter.CTkFrame(self, fg_color="transparent")
            cloud_frame.grid(row=index, column=2, padx=10, pady=(5, 0), sticky="w")

            cloud_icon_label = customtkinter.CTkLabel(
                cloud_frame,
                text="",
                image=self.cloud_cover_icon
            )
            cloud_icon_label.pack(side="left")

            cloud_text_label = customtkinter.CTkLabel(
                cloud_frame,
                text=f"Cloud Cover: {forecast['cloud_cover']}",
                font=("Arial", 10)
            )
            cloud_text_label.pack(side="left", padx=5)

            precip_frame = customtkinter.CTkFrame(self, fg_color="transparent")
            precip_frame.grid(row=index, column=3, padx=10, pady=(5, 0), sticky="w")

            precip_icon_label = customtkinter.CTkLabel(
                precip_frame,
                text="",
                image=self.rain_icon
            )
            precip_icon_label.pack(side="left")

            precip_text_label = customtkinter.CTkLabel(
                precip_frame,
                text=f"Precip: {forecast['precip']}",
                font=("Arial", 10)
            )
            precip_text_label.pack(side="left", padx=5)



forecast_data = []
for i in range(len(average_temperatures)):
    day_data = {
        "day": f"Day {i + 1}",
        "temp": f"{average_temperatures[i]}°C",
        "cloud_cover": f"{average_cloud_covers[i]}%",
        "precip": f"{average_precipitations[i]} in"
    }
    forecast_data.append(day_data)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("AgroAssistant")
        self.geometry("900x600") 

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.landing_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.landing_frame.grid(row=0, column=0, sticky="nsew")

        self.landing_frame.grid_rowconfigure(0, weight=1)
        self.landing_frame.grid_rowconfigure(1, weight=0)
        self.landing_frame.grid_columnconfigure(0, weight=1)

        self.landing_title_label = customtkinter.CTkLabel(
            self.landing_frame,
            text="Welcome to AgroAssistant",
            font=("Arial", 30, "bold")
        )
        self.landing_title_label.grid(row=0, column=0, padx=20, pady=(50, 20), sticky="n")

        self.landing_description_label = customtkinter.CTkLabel(
            self.landing_frame,
            text=(
                "AgroAssistant is your one-stop application for monitoring and managing\n"
                "soil conditions, irrigation schedules, and weather forecasts.\n\n"
                "Whether you're a home gardener or a commercial farmer, AgroAssistant\n"
                "provides the tools you need to make data-driven decisions."
            ),
            font=("Arial", 15),
            justify="center"
        )
        self.landing_description_label.grid(row=1, column=0, padx=20, pady=20, sticky="n")

        self.get_started_button = customtkinter.CTkButton(
            self.landing_frame,
            text="Get Started",
            command=self.show_main_app,
            fg_color="#239B56",
            text_color="white"
        )
        self.get_started_button.grid(row=2, column=0, pady=40, sticky="n")

        self.master_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.master_frame.grid_columnconfigure(0, weight=0) 
        self.master_frame.grid_columnconfigure(1, weight=1)  
        self.master_frame.grid_rowconfigure(0, weight=1)

        self.navigation_frame = customtkinter.CTkFrame(self.master_frame, width=200, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="ns")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20))
        self.irrigation_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "chat_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "chat_light.png")), size=(20, 20))
        self.add_user_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "add_user_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "add_user_light.png")), size=(20, 20))

        self.navigation_frame_label = customtkinter.CTkLabel(
            self.navigation_frame,
            text="  AgroAssistant",
            font=customtkinter.CTkFont(size=15, weight="bold")
        )
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Dashboard",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.home_image,
            anchor="w",
            command=self.home_button_event
        )
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.irrigation_button = customtkinter.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Irrigation",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.irrigation_image,
            anchor="w",
            command=self.irrigation_button_event
        )
        self.irrigation_button.grid(row=2, column=0, sticky="ew")

        self.frame_3_button = customtkinter.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Frame 3",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.add_user_image,
            anchor="w",
            command=self.frame_3_button_event
        )
        self.frame_3_button.grid(row=3, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(
            self.navigation_frame,
            values=["Light", "Dark", "System"],
            command=self.change_appearance_mode_event
        )
        self.appearance_mode_menu.grid(row=5, column=0, padx=20, pady=20, sticky="s")

        self.home_frame = customtkinter.CTkFrame(self.master_frame, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)
        self.home_frame.grid_columnconfigure(1, weight=1)

        self.dashboard_title = customtkinter.CTkLabel(self.home_frame, text="Dashboard", font=("Arial", 25))
        self.dashboard_title.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        soil_moisture = 0.5 #stormglass_data['hours'][0]['soilMoisture']['noaa']
        self.moisture_bar_label = customtkinter.CTkLabel(
            self.home_frame,
            text=f"Soil Moisture Level: ({soil_moisture} m\u00b3/m\u00b3)",
            font=("Arial", 14)
        )
        self.moisture_bar_label.grid(row=1, column=0, padx=20, sticky="w")

        if soil_moisture < 0.4:
            self.moisture_bar = customtkinter.CTkProgressBar(self.home_frame, orientation="horizontal", progress_color=("red", "red"))
        elif soil_moisture <= 0.7:
            self.moisture_bar = customtkinter.CTkProgressBar(self.home_frame, orientation="horizontal", progress_color=("green", "green"))
        else:
            self.moisture_bar = customtkinter.CTkProgressBar(self.home_frame, orientation="horizontal", progress_color=("blue", "blue"))
        self.moisture_bar.grid(row=2, column=0, padx=20, pady=10, sticky="w")
        self.moisture_bar.set(soil_moisture)

        # Example: Soil Temperature
        soil_temperature = 10 #stormglass_data['hours'][1]['soilTemperature']['noaa']
        self.soil_temperature_bar_label = customtkinter.CTkLabel(
            self.home_frame,
            text=f"Soil Temperature Level: ({soil_temperature}°C)",
            font=("Arial", 14)
        )
        self.soil_temperature_bar_label.grid(row=3, column=0, padx=20, pady=10, sticky="w")

        if soil_temperature < 0:
            self.soil_temperature_bar = customtkinter.CTkProgressBar(
                self.home_frame, orientation="horizontal", progress_color=("blue", "blue")
            )
            self.soil_temperature_bar.set(0.1)
        elif soil_temperature > 40:
            self.soil_temperature_bar = customtkinter.CTkProgressBar(
                self.home_frame, orientation="horizontal", progress_color=("red", "red")
            )
            self.soil_temperature_bar.set(1)
        elif soil_temperature / 40 < 0.375:
            self.soil_temperature_bar = customtkinter.CTkProgressBar(
                self.home_frame, orientation="horizontal", progress_color=("blue", "blue")
            )
            self.soil_temperature_bar.set(soil_temperature / 40)
        elif 0.375 <= soil_temperature / 40 <= 0.55:
            self.soil_temperature_bar = customtkinter.CTkProgressBar(
                self.home_frame, orientation="horizontal", progress_color=("green", "green")
            )
            self.soil_temperature_bar.set(soil_temperature / 40)
        else:
            self.soil_temperature_bar = customtkinter.CTkProgressBar(
                self.home_frame, orientation="horizontal", progress_color=("red", "red")
            )
            self.soil_temperature_bar.set(soil_temperature / 40)
        self.soil_temperature_bar.grid(row=4, column=0, padx=20, pady=10, sticky="w")

        # Weather Forecast
        weather_frame = ScrollableWeatherFrame(
            master=self.home_frame,
            forecast_data=[
                {
                    "day": f"Day {i+1}",
                    "temp": f"{average_temperatures[i]}°C",
                    "cloud_cover": f"{average_cloud_covers[i]}%",
                    "precip": f"{average_precipitations[i]} in"
                }
                for i in range(len(average_temperatures))
            ],
            width=650,
            height=150,
            corner_radius=10,
            fg_color="transparent",
        )
        weather_frame.grid(row=5, column=0, padx=20, pady=10, sticky="ew", columnspan=2)

        self.irrigation_frame = irrigation.IrrigationManagementScreen(self.master_frame)

        self.third_frame = customtkinter.CTkFrame(self.master_frame, corner_radius=0, fg_color="transparent")
        third_label = customtkinter.CTkLabel(self.third_frame, text="Frame 3", font=("Arial", 25))
        third_label.pack(padx=20, pady=20)


    def show_main_app(self):
        self.landing_frame.grid_forget()     
        self.master_frame.grid(row=0, column=0, sticky="nsew") 
        self.select_frame_by_name("home")

    def select_frame_by_name(self, name):
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.irrigation_button.configure(fg_color=("gray75", "gray25") if name == "irrigation" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")

        self.home_frame.grid_forget()
        self.irrigation_frame.grid_forget()
        self.third_frame.grid_forget()

        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        elif name == "irrigation":
            self.irrigation_frame.grid(row=0, column=1, sticky="nsew")
        elif name == "frame_3":
            self.third_frame.grid(row=0, column=1, sticky="nsew")

    def home_button_event(self):
        self.select_frame_by_name("home")

    def irrigation_button_event(self):
        self.select_frame_by_name("irrigation")

    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)


if __name__ == "__main__":
    app = App()
    app.mainloop()
