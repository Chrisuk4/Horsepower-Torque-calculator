import pandas as pd
import matplotlib.pyplot as plt
import mplcursors
import numpy as np  # Importing NumPy for type checking
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Function to calculate HP using the specified method
def calculate_hp(air_flow_gs, coefficient):
    return air_flow_gs / coefficient

# Function to calculate Torque using the HP value and convert to Nm
def calculate_torque(hp, rpm):
    return (hp * 5252) / rpm * 1.35582  # Convert lb-ft to Nm

# Function to apply a moving average for smoothing
def moving_average(data, window_size):
    return data.rolling(window=window_size, center=True).mean()

# Function to read CSV, calculate HP and Torque, smooth the data, and plot the graph
def plot_hp_torque_graph(csv_file, coefficient, window_size=5):
    # Read CSV with appropriate encoding
    try:
        data = pd.read_csv(csv_file, encoding='utf-8')  # Try UTF-8 first
    except UnicodeDecodeError:
        data = pd.read_csv(csv_file, encoding='Windows-1252')  # Fallback to Windows-1252 (ANSI)

    # Ensure the CSV has 'RPM' and 'AirFlow' columns
    if 'RPM' not in data.columns or 'AirFlow' not in data.columns:
        raise ValueError("CSV file must contain 'RPM' and 'AirFlow' columns")
    
    # Calculate HP and Torque
    data['HP'] = data['AirFlow'].apply(lambda x: calculate_hp(x, coefficient))
    data['Torque'] = data.apply(lambda row: calculate_torque(row['HP'], row['RPM']), axis=1)
    
    # Apply smoothing (moving average)
    data['HP_Smoothed'] = moving_average(data['HP'], window_size)
    data['Torque_Smoothed'] = moving_average(data['Torque'], window_size)
    
    # Find max values
    max_hp = data['HP_Smoothed'].max()
    max_torque = data['Torque_Smoothed'].max()
    max_hp_rpm = data['RPM'][data['HP_Smoothed'].idxmax()]
    max_torque_rpm = data['RPM'][data['Torque_Smoothed'].idxmax()]

    # Plot the smoothed HP and Torque graph
    plt.figure(figsize=(12, 6))
    hp_line, = plt.plot(data['RPM'], data['HP_Smoothed'], label='Horsepower (HP)', color='b')
    torque_line, = plt.plot(data['RPM'], data['Torque_Smoothed'], label='Torque (Nm)', color='r')
    
    # Annotate the max values
    plt.scatter(max_hp_rpm, max_hp, color='blue')
    plt.text(max_hp_rpm, max_hp, f'Max HP: {max_hp:.2f}', color='blue', fontsize=10, ha='left')
    
    plt.scatter(max_torque_rpm, max_torque, color='red')
    plt.text(max_torque_rpm, max_torque, f'Max Torque NM: {max_torque:.2f}', color='red', fontsize=10, ha='left')

    plt.title('Power Graph')
    plt.xlabel('RPM')
    plt.ylabel('Values')
    plt.legend()
    plt.grid(True)

    # Enable hover functionality with simplified annotation
    cursor = mplcursors.cursor([hp_line, torque_line], hover=True)

    @cursor.connect("add")
    def on_add(sel):
        index = sel.index
        if isinstance(index, (int, np.integer)):  # Ensure the index is an integer
            rpm_value = data["RPM"].iloc[index]
            if sel.artist == hp_line:
                value = data["HP_Smoothed"].iloc[index]
                sel.annotation.set_text(f'HP: {value:.1f}')
            elif sel.artist == torque_line:
                value = data["Torque_Smoothed"].iloc[index]
                sel.annotation.set_text(f'Torque: {value:.1f} Nm')

    plt.show()

# Function to handle file selection
def select_file():
    filename = filedialog.askopenfilename(title="Select CSV File", filetypes=[("CSV files", "*.csv")])
    if filename:
        file_label.config(text=filename)  # Update label to show selected file

# Function to start the plotting process
def start_plotting():
    csv_file = file_label.cget("text")  # Get the selected file path
    fuel_type = fuel_type_var.get()  # Get selected fuel type
    window_size = smoothing_entry.get()  # Get smoothing value

    # Validate window size input
    try:
        window_size = int(window_size)
        if window_size < 1:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid positive integer for smoothing.")
        return

    # Set coefficient based on fuel type
    if fuel_type == "diesel":
        coefficient = 0.85
    elif fuel_type == "gasoline":
        coefficient = 0.75
    else:
        messagebox.showerror("Error", "Invalid fuel type selected.")
        return

    try:
        plot_hp_torque_graph(csv_file, coefficient, window_size=window_size)  # Use user-defined window size
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Create the main window
root = tk.Tk()
root.title("Horsepower Calculator")

# Create and place widgets
file_label = tk.Label(root, text="No file selected", wraplength=400)
file_label.pack(pady=10)

select_button = tk.Button(root, text="Select CSV File", command=select_file)
select_button.pack(pady=10)

fuel_type_var = tk.StringVar(value="gasoline")  # Default value
fuel_frame = tk.LabelFrame(root, text="Select Fuel Type")
fuel_frame.pack(pady=10)

gasoline_radio = tk.Radiobutton(fuel_frame, text="Gasoline", variable=fuel_type_var, value="gasoline")
gasoline_radio.pack(side=tk.LEFT, padx=10)

diesel_radio = tk.Radiobutton(fuel_frame, text="Diesel", variable=fuel_type_var, value="diesel")
diesel_radio.pack(side=tk.LEFT, padx=10)

smoothing_frame = tk.LabelFrame(root, text="Curve smoothing (May decrease max HP/TQ value)")
smoothing_frame.pack(pady=10)

smoothing_entry = tk.Entry(smoothing_frame, width=10)
smoothing_entry.insert(0, "5")  # Default smoothing value
smoothing_entry.pack(pady=5)

start_button = tk.Button(root, text="Calculate HP and Torque", command=start_plotting)
start_button.pack(pady=20)

# Start the GUI loop
root.mainloop()
