## Horsepower and Torque calculator in Python

Information:  
This is just a evening project i made for myself to see differences in my tune revisions.  
The application is not 100% accurate and is meant to mostly get an idea of how your powergrah looks and somewhat close numbers of horsepower and torque.  
The example log is from my Audi with a 1.8t AWT engine.  

### Required for using the script

- CSV Editor (Excel, Libreoffice Calc or other)
- Logs from ME7Logger or similar
- Python Version 3.9.0

<details>
<summary>Needed Python Modules</summary>
<br>
pandas  <br>
matplotlib.pyplot  <br>
mplcursors  <br>
numpy  <br>
tkinter  
</details>

---

## How to Use

1. Start by getting your CSV log from your car
2. Open the log in a application that can manipulate CSV files
3. Remove each extra field other than RPM and Mass Airflow (Has to be in g/s, You can convert mg/stroke [here](#how-to-conver-mgstroke-to-gs))
4. Name the Mass Airflow Column to **```AirFlow```** and RPM column to **```RPM```**  
![Log_Example](https://github.com/user-attachments/assets/fe8338e1-06c4-4104-ba5d-7fdc80da17b7)
5. Delete all excess Metadata and "non csv" text
6. Look through your log and find the part where your pull starts and ends, Delete all other parts and save it (your csv should look similar to this)  
![ready_log](https://github.com/user-attachments/assets/0fa2d243-8d5a-499e-bdda-16e92f26902b)
7. Start the **```Horsepower_Calculator.pyw```**  
![Select file](https://github.com/user-attachments/assets/b3e17e49-885f-426f-8fcd-ead55aa0d630)
  - Click on **Select CSV File** and find your recently edited CSV
  - Select fuel type Gasoline or Diesel (If running on ethanol or a blend choose Gasoline)
  - Choose curve smoothing value, 5 Is recommended (Lower smoothing values are more accurate but can look worse)
![Smoothing_5](https://github.com/user-attachments/assets/0a7136ae-8bbf-4191-9744-e95da165a6a1)
![Smoothing_1](https://github.com/user-attachments/assets/b91c67e3-4a12-4489-aa59-0c6d15f77c8c)
8. Press **Calculate HP and Torque**


## Other features

1. Save Icon  
  - Pressing this will create a PNG image of your Power Graph
2. Slider button  
  - Brings up a menu to adjust the size of the graph inside of the applications window
3. Search icon  
  - Lets you use Left Click to Zoom in and Right Click to zoom out by selecting an area
4. Pan Button  
  - Lets you move the graph with Left Click and resize with Right Click by moving the mouse
5. Left and Right Arrow  
  - Lets you Undo and Redo changes you have done to the graph
6. Home Button
  - Resets your graph to the original view

---

### How to conver mg/stroke to g/s
![calculation](https://github.com/user-attachments/assets/a2fc979d-ffc6-4450-ae41-470df8a27df4)

##### Example:  
- mg/stroke  
- RPM = 777  
- Cylinders = 6

![calculation2](https://github.com/user-attachments/assets/6258c6c8-3492-4d92-bf0c-357e9aac48ce)  
![calculation3](https://github.com/user-attachments/assets/a5176802-3c85-4d87-9539-762af3d8c775)  










