import customtkinter
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
import random  # Mock data generator for example
import app

class IrrigationManagementScreen(customtkinter.CTkScrollableFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        #self.configure(fg_color="white")
        
        # Title Label
        self.title_label = customtkinter.CTkLabel(self, text="Irrigation Management Screen", font=("Arial", 20, "bold"))
        self.title_label.pack(pady=10)

        # Real-time soil moisture display
        self.create_soil_moisture_graph()

        # Scheduling Section
        self.schedule_section = customtkinter.CTkFrame(self, corner_radius=8)
        self.schedule_section.pack(pady=20, padx=20, fill="x")
        schedule_label = customtkinter.CTkLabel(self.schedule_section, text="Irrigation Scheduling", font=("Arial", 16))
        schedule_label.pack(pady=5)
        customtkinter.CTkButton(self.schedule_section, text="Add New Schedule", command=self.add_schedule).pack(pady=10)

        # Historical Data Section
        self.history_section = customtkinter.CTkFrame(self, corner_radius=8)
        self.history_section.pack(pady=20, padx=20, fill="x")
        history_label = customtkinter.CTkLabel(self.history_section, text="Historical Irrigation Data", font=("Arial", 16))
        history_label.pack(pady=5)
        customtkinter.CTkButton(self.history_section, text="View History", command=self.view_history).pack(pady=10)

        # New Irrigation Section Title
        self.irrigation_section = customtkinter.CTkFrame(self, corner_radius=8)
        self.irrigation_section.pack(pady=20, padx=20, fill="x")
        self.irrigation_section_title = customtkinter.CTkLabel(self.irrigation_section, text="New Irrigation", font=("Arial", 18, "bold"))
        

        # Input for Crop Type
        self.crop_type_label = customtkinter.CTkLabel(self.irrigation_section, text="Crop Type:", font=("Arial", 14)).pack(pady=10)
        self.crop_type_entry = customtkinter.CTkEntry(self.irrigation_section, placeholder_text="Enter crop type").pack(pady=10)
        

        # Input for Water Amount
        self.water_amount_label = customtkinter.CTkLabel(self.irrigation_section, text="Water Amount (L):", font=("Arial", 14)).pack(pady=10)
        self.water_amount_entry = customtkinter.CTkEntry(self.irrigation_section, placeholder_text="Enter water amount").pack(pady=10)
        

        # Input for Irrigation Date
        self.irrigation_date_label = customtkinter.CTkLabel(self.irrigation_section, text="Irrigation Date:", font=("Arial", 14)).pack(pady=10)
        self.irrigation_date_entry = customtkinter.CTkEntry(self.irrigation_section, placeholder_text="Enter date (YYYY-MM-DD)").pack(pady=10)
        

        # Submit Button
        self.submit_button = customtkinter.CTkButton(
            self.irrigation_section,
            text="Submit",
            command=self.submit_irrigation_data
        ).pack(pady=10)
        
    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def submit_irrigation_data(self):
        crop_type = self.crop_type_entry.get()
        water_amount = self.water_amount_entry.get()
        irrigation_date = self.irrigation_date_entry.get()

        if not crop_type or not water_amount or not irrigation_date:
            customtkinter.CTkMessagebox.show_error("Error", "Please fill in all fields.")
            return

        try:
            water_amount = float(water_amount)
        except ValueError:
            customtkinter.CTkMessagebox.show_error("Error", "Water amount must be a number.")
            return

        print(f"Submitted Data - Crop: {crop_type}, Water: {water_amount}L, Date: {irrigation_date}")
        customtkinter.CTkMessagebox.show_info("Success", "Irrigation data submitted successfully!")

        # Clear input fields
        self.crop_type_entry.delete(0, "end")
        self.water_amount_entry.delete(0, "end")
        self.irrigation_date_entry.delete(0, "end")

    def create_soil_moisture_graph(self):
        # Create a matplotlib figure
        fig = Figure(figsize=(5, 3), dpi=100)
        self.ax = fig.add_subplot(111)
        self.ax.set_title("Soil Moisture Levels (Real-Time)")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Moisture (m3/m3)")
        
        # Mock data
        times = [datetime.now().strftime("%H:%M:%S") for _ in range(10)]
        moisture_levels = [random.uniform(0.1, 0.3) for _ in range(10)]
        
        # Plot the data
        self.ax.plot(times, moisture_levels, label="Soil Moisture", color="blue", marker="o")
        self.ax.legend()
        
        # Embed the plot in the Tkinter UI
        canvas = FigureCanvasTkAgg(fig, self)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(pady=20)

    def add_schedule(self):
        print("Add new irrigation schedule")

    def view_history(self):
        print("View historical irrigation data")
