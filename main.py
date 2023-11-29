import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import json
from tkinter import messagebox
from operator import itemgetter


class HospitalManagementSystem:
    def __init__(self, root):
        # Initialize the GUI and load existing appointments from a file
        self.root = root
        self.root.title("City Hospital Appointment")
        self.root.geometry("600x400")
        self.root.configure(bg="lightblue")

        self.appointments = []
        self.load_appointments_from_file()

        style = ttk.Style()
        style.configure("TFrame", background="#f0f0f0")
        style.configure("TLabel", background="#f0f0f0", font=("Times New Roman", 12))
        style.configure("TButton", font=("Times New Roman", 12))

        self.frame = ttk.Frame(root)
        self.frame.pack(pady=20)

        self.label = ttk.Label(
            self.frame,
            text="Welcome to Mental Health Consulting",
            font=("Times New Roman", 16),
            background="#f0f0f0",
        )
        self.label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        ttk.Label(self.frame, text="Name:").grid(
            row=1, column=0, padx=10, pady=5, sticky="w"
        )
        ttk.Label(self.frame, text="Age:").grid(
            row=2, column=0, padx=10, pady=5, sticky="w"
        )
        ttk.Label(self.frame, text="Gender:").grid(
            row=3, column=0, padx=10, pady=5, sticky="w"
        )
        ttk.Label(self.frame, text="Select Date:").grid(
            row=4, column=0, padx=10, pady=5, sticky="w"
        )
        ttk.Label(self.frame, text="Select Time:").grid(
            row=5, column=0, padx=10, pady=5, sticky="w"
        )
        ttk.Label(self.frame, text="Select Doctor:").grid(
            row=6, column=0, padx=10, pady=5, sticky="w"
        )
        ttk.Label(self.frame, text="Phone Number:").grid(
            row=7, column=0, padx=10, pady=5, sticky="w"
        )

        self.name_entry = ttk.Entry(self.frame)
        self.name_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        self.age_entry = ttk.Entry(self.frame)
        self.age_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        self.gender_options = ["Male", "Female", "Other"]
        self.selected_gender = tk.StringVar()
        self.gender_dropdown = ttk.Combobox(
            self.frame, textvariable=self.selected_gender, values=self.gender_options
        )
        self.gender_dropdown.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        self.date_entry = DateEntry(
            self.frame,
            width=12,
            background="darkblue",
            foreground="white",
            font=("Times New Roman", 10),
        )
        self.date_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        self.time_options = [
            "08:00 AM",
            "09:00 AM",
            "10:00 AM",
            "11:00 AM",
            "12:00 PM",
            "01:00 PM",
            "02:00 PM",
            "03:00 PM",
            "04:00 PM",
            "05:00 PM",
            "06:00 PM",
        ]
        self.selected_time = tk.StringVar()
        self.time_dropdown = ttk.Combobox(
            self.frame, textvariable=self.selected_time, values=self.time_options
        )
        self.time_dropdown.grid(row=5, column=1, padx=10, pady=5, sticky="w")

        self.doctor_options = ["Dr. Smith", "Dr. Johnson", "Dr. Williams", "Dr. Brown"]
        self.selected_doctor = tk.StringVar()
        self.doctor_dropdown = ttk.Combobox(
            self.frame, textvariable=self.selected_doctor, values=self.doctor_options
        )
        self.doctor_dropdown.grid(row=6, column=1, padx=10, pady=5, sticky="w")

        self.phone_entry = ttk.Entry(self.frame)
        self.phone_entry.grid(row=7, column=1, padx=10, pady=5, sticky="w")

        self.make_appointment_button = ttk.Button(
            self.frame,
            text="Make Appointment",
            command=self.make_appointment,
            style="TButton",
        )
        self.make_appointment_button.grid(row=8, column=0, columnspan=2, pady=10)

        style.configure(
            "TButton",
            background="green",
            foreground="green",
            font=("Times New Roman", 12),
        )

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def make_appointment(self):
        # Collect information from the input fields and attempt to make an appointment
        name = self.name_entry.get()
        age = self.age_entry.get()
        gender = self.selected_gender.get()
        date = self.date_entry.get()
        time = self.selected_time.get()
        doctor = self.selected_doctor.get()
        phone_number = self.phone_entry.get()

        if name and age and gender and date and time and doctor and phone_number:
            appointment_info = {
                "Name": name,
                "Age": age,
                "Gender": gender,
                "Date": date,
                "Time": time,
                "Doctor": doctor,
                "Phone": phone_number,
            }

            # Check for appointment conflicts before adding the new appointment
            conflict_message = self.check_appointment_conflict(appointment_info)
            if conflict_message:
                messagebox.showerror("Error", conflict_message)
                return

            # Add the new appointment to the list, save to file, and clear input fields
            self.appointments.append(appointment_info)
            self.appointments = sorted(self.appointments, key=itemgetter("Date"))
            self.save_appointments_to_file()
            self.clear_entry_fields()

    def check_appointment_conflict(self, new_appointment):
        # Check for conflicts with existing appointments
        for existing_appointment in self.appointments:
            if (
                existing_appointment["Date"] == new_appointment["Date"]
                and existing_appointment["Time"] == new_appointment["Time"]
                and existing_appointment["Doctor"] == new_appointment["Doctor"]
            ):
                return f"Appointment conflict! The selected date, time, and doctor are already booked."

        return None

    def save_appointments_to_file(self):
        # Save the list of appointments to a JSON file
        try:
            with open("appointments.json", mode="w") as file:
                json.dump(self.appointments, file, indent=2)
        except Exception as e:
            messagebox.showerror("Error", f"Error saving appointment data: {e}")

    def load_appointments_from_file(self):
        # Load existing appointments from a JSON file
        try:
            with open("appointments.json", mode="r") as file:
                self.appointments = json.load(file)
        except FileNotFoundError:
            # If the file doesn't exist, create it and save an empty list
            self.save_appointments_to_file()
        except Exception as e:
            messagebox.showerror("Error", f"Error loading appointment data: {e}")

    def clear_entry_fields(self):
        # Clear all input fields after making an appointment
        self.name_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)
        self.gender_dropdown.set("")
        self.date_entry.delete(0, tk.END)
        self.selected_time.set("")
        self.doctor_dropdown.set("")
        self.phone_entry.delete(0, tk.END)

    def on_close(self):
        # Save appointments to file before closing the application
        self.save_appointments_to_file()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = HospitalManagementSystem(root)
    root.mainloop()
