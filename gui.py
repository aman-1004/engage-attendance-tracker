import tkinter as tk
import tkinter.filedialog as filedialog
from attendance import *
from datetime import datetime
import shutil
import threading 
from helper.record import *
from export import recordsAvailable, export, exportDir

window = tk.Tk()
window.title("Attendance Tracker")
# window.geometry('720x560')

imageFolder = os.path.join(Path(exportDir).parent, 'Images')
print(imageFolder)

def attend(dtime, time_int, meal, toPost):
    toPost=[]
    start(dtime, time_int , meal.lower(), toPost)
    print('final post is' , toPost)

    updateRecord(datetime.now(), toPost)
    # printRecord(months[datetime.now().month-1], datetime.now().year)
    printRecord("May", '2022')
    print("Detection Done")

def start_event_handler(): 
    print('Start Event Handler')
    meal = str(default_drop_down.get())
    time_int = 30 
    try:
        time_int = int(time_interval_field.get())
    except ValueError:
        time_interval_field.config(text="Enter a integer value")

    toPost = []
    print(meal, time_int)
    thread=threading.Thread(target=attend, args=(datetime.now(), time_int , meal.lower(), toPost,))
    thread.start()

def open_export_window():
    export_window = tk.Toplevel(window)
    export_window.title('Export')
    records_available = recordsAvailable()
    print('records available', records_available)
    default_value = tk.StringVar(export_window)
    default_value.set(records_available[0])
    select_record = tk.OptionMenu(export_window, default_value, *records_available)

    def browse(): 
        export_window.withdraw()
        filedir = filedialog.askdirectory(initialdir=exportDir)    
        record = default_value.get()
        # print(filedir)
        export(record, filedir)
        export_window.destroy()

    button = tk.Button(export_window, text="Browse where to save file", command=browse)
    select_record.pack() 
    button.pack()

def open_register_user_window():
    register_window = tk.Toplevel(window)
    register_window.title('Register User') 
    entry_label = tk.Label(register_window, text="*Enter Entry Number:")
    entry_widget = tk.Entry(register_window)
    def browse_image():
        register_window.withdraw()
        imagePath = filedialog.askopenfilename()
        print(imagePath)
        entryNumber = None
        entryNumber = entry_widget.get()
        image_ext=os.path.splitext(imagePath)[1]
        print(image_ext)
        if entryNumber and image_ext in ['.jpg', '.jpeg', '.png']:
            print('saving images..')
            shutil.copy(imagePath, os.path.join(imageFolder, entryNumber+image_ext))
        else: 
            print("Not saving. Either entry number is missing or image has wrong extension (only .jpg, .jpeg, .png are valid)")
        register_window.destroy() 


    button = tk.Button(register_window, text="Browse image", command=browse_image)
    entry_label.pack()
    entry_widget.pack()
    button.pack()



main_frame = tk.Frame(master=window, relief=tk.RAISED, borderwidth=5)
start_button = tk.Button(master=main_frame, text="Start Attendance Tracking", command=start_event_handler)
meal_options = ["Breakfast", "Lunch", "Dinner"]
default_drop_down = tk.StringVar(window)
default_drop_down.set(meal_options[0])
drop_down_meal = tk.OptionMenu(main_frame, default_drop_down , *meal_options)
time_interval_field = tk.Entry(main_frame, text="Enter time interval in seconds")
time_label = tk.Label(main_frame, text="Enter time interval in seconds (Default: 30)")

drop_down_meal.pack()
time_label.pack()
time_interval_field.pack()
start_button.pack(side=tk.TOP, fill=tk.BOTH, expand=1)



helper_frame = tk.Frame(master=window)
register_button = tk.Button(master=helper_frame, text="Register User", command=open_register_user_window)
register_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
export_button = tk.Button(master=helper_frame, text="Export as CSV", command=open_export_window)
export_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

helper_frame.grid(row=2, column=1, sticky="news")
main_frame.grid(row=1, column=1, sticky="news")

window.mainloop()
