import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox
from tkinter import ttk
import pandas as pd
import json
import glob
import os


dataset_path = "input/playbooks.csv"
path_api_results = "API_Results/"
api_calls = glob.glob(os.path.join(path_api_results, '*.json'))
techniques_path = "output/techniques.txt"

results_path = "Output/Categories_output.txt"

if os.path.exists(results_path):
    print("File exists")
else:
    with open("output/Categories_output.txt", "w") as setup:
        setup.write("")

df = pd.read_csv(dataset_path)
df.head()
defend_options = []

with open(techniques_path, "r") as search_setup:
    for line in search_setup:
        line.strip()
        defend_options.append(line[:-1])
print(defend_options)

# Define the main application
class SimpleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Decision Support System")
        self.root.geometry("1280x1080")
        self.root.counter = 1
        self.choices = []
        # Define the font for the text display
        self.display_font = tkfont.Font(family="Helvetica", size=16)
        # ---------------------------------
        # ---- FRAME Nr. 1 Control Panel
        # ---------------------------------
        self.control_frame = tk.Frame(root)
        self.control_frame.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

        # Create the Back BUtton
        self.button_back = tk.Button(self.control_frame, text="Back", command=self.load_last_playbook, width=20,
                                     height=3)
        self.button_back.grid(row=0, column=0, sticky="w", padx=(5, 20))


        self.label_jumper = tk.Label(self.control_frame, text="Select a Playbook:")
        self.label_jumper.grid(row=0, column=1, sticky="n", pady=(5, 0))
        # Create a StringVar to hold the current value of the dropdown
        self.customized_playbooks = []
        self.setup_dropdown()
        # Create the Combobox (dropdown menu)
        self.combobox = ttk.Combobox(self.control_frame, values=self.customized_playbooks)
        self.combobox.set("Jump to a specific Playbook")  # Set the default value
        self.combobox.grid(row=1, column=1, sticky="n", pady=5)
        self.combobox.bind("<<ComboboxSelected>>", self.change_to_pb)

        # Create the third button to load the next playbook
        self.button_next = tk.Button(self.control_frame, text="Next", command=self.load_next_playbook, width=20,
                                     height=3)
        self.button_next.grid(row=0, column=2, sticky="e", padx=(20, 5))

        # Adjust column weights to distribute space
        self.control_frame.columnconfigure(0, weight=1)
        self.control_frame.columnconfigure(1, weight=1)
        self.control_frame.columnconfigure(2, weight=1)

        # ---------------------------------
        # ---- FRAME Nr. 2 Playbook Display
        # ---------------------------------
        self.text_frame = tk.Frame(root)
        self.text_frame.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
        # Create a text display area using a Text widget in read-only mode
        self.text_display = tk.Text(self.text_frame, font=self.display_font, bg="white", relief="sunken", padx=10, pady=10, wrap=tk.WORD)
        self.text_display.pack(fill=tk.BOTH, expand=True)



        # Initial Text display
        # Hier wir das erste playbook geladen
        self.root.counter = self.set_counter()
        print(self.root.counter)
        self.display_playbook(f"p{self.root.counter}")
        self.root.counter +=1

        self.text_display.config(state=tk.DISABLED)  # Set to read-only

        self.text_display.tag_configure("bold", font=tkfont.Font(family="Helvetica", size=16, weight="bold"))

        # ---------------------------------
        # ---- FRAME Nr. 3 Select Buttons
        # ---------------------------------
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=10)

        # Create the first button to display a message
        self.button_t1 = tk.Button(self.button_frame, text="T1", command=self.add_t1, width=35, height=2)
        self.button_t1.pack(side=tk.LEFT, padx=5)

        self.button_t2 = tk.Button(self.button_frame, text="T2", command=self.add_t2, width=35, height=2)
        self.button_t2.pack(side=tk.LEFT, padx=5)

        self.button_t3 = tk.Button(self.button_frame, text="T3", command=self.add_t3, width=35, height=2)
        self.button_t3.pack(side=tk.LEFT, padx=5)

        self.button_t4 = tk.Button(self.button_frame, text="T4", command=self.add_t4, width=35, height=2)
        self.button_t4.pack(side=tk.LEFT, padx=5)

        # Create the second button to clear the text display
       # self.button_clear = tk.Button(self.button_frame, text="Clear", command=self.clear_text, width=40, height=2)
       # self.button_clear.pack(side=tk.LEFT, padx=5)

        # ---------------------------------
        # ---- FRAME Nr. 4 Down select
        # ---------------------------------
        self.choices_frame = tk.Frame(root)
        self.choices_frame.pack(side=tk.LEFT, padx=10, pady=2, fill=tk.Y, expand=True)
        self.search_frame = tk.Frame(root)
        self.search_frame.pack(side=tk.LEFT,padx=10, pady=2, fill=tk.Y, expand=True)
        self.custom_frame = tk.Frame(root)
        self.custom_frame.pack(side=tk.LEFT,padx=10, pady=2, fill=tk.Y, expand=True)
        self.button_control_frame = tk.Frame(root)
        self.button_control_frame.pack(side=tk.LEFT, padx=10, pady=2, fill=tk.Y, expand=True)

        # Display the current Choices
        self.choice_label = tk.Label(self.choices_frame, text="Current Choices: ")
        self.choice_label.grid(row=0, column=0, sticky="w", padx=5, pady=0)

        self.text_display_status = tk.Text(self.choices_frame, font=("Arial", 12), bg="white", relief="sunken",
                                           padx=10, pady=10, wrap=tk.WORD, width=20, height=5)
        self.text_display_status.grid(row=1, column=0, sticky="w", padx=5, pady=0)
        self.text_display_status.config(state=tk.DISABLED)  # Set to read-only

        # Creation of the middle Elements with the search bar and suggestion widgets
        self.search_label = tk.Label(self.search_frame, text="Search: ")
        self.search_label.grid(row=0, column=1, sticky="w", padx=5, pady=0)
        self.search_var = tk.StringVar()
        self.search_bar = tk.Entry(self.search_frame, textvariable=self.search_var)
        self.search_bar.grid(row=1, column=1, sticky="w", padx=5, pady=0)
        self.suggestion_listbox = tk.Listbox(self.search_frame)
        self.suggestion_listbox.grid(row=2, column=1, sticky="w", padx=5, pady=10)
        self.search_bar.bind('<KeyRelease>', self.update_suggestions)
        self.suggestion_listbox.bind('<<ListboxSelect>>', self.on_suggestion_select)

        # Widgets for the right Elements with the custom add - Create the button
        self.button_custom = tk.Button(self.custom_frame, text="Add Custom", command=self.add_custom, width=20,
                                       height=1)
        self.button_custom.grid(row=0, column=2, sticky="w", padx=5, pady=0)
        self.text_display_custom = tk.Text(self.custom_frame, font=self.display_font, bg="white", relief="sunken",
                                           padx=5, pady=5, wrap=tk.WORD, width=20, height=5)
        self.text_display_custom.grid(row=1, column=2, sticky="w", padx=5, pady=0)

        # Custom Text insert
        self.button_briefing = tk.Button(self.button_control_frame, text="Briefing", command=self.show_briefing, width=20,
                                         height=3)
        self.button_briefing.grid(row=0, column=3, sticky="w", padx=5, pady=0)

        # Create the Save Button
        self.button_save = tk.Button(self.button_control_frame, text="Save", command=self.save_into_file, width=20, height=3)
        self.button_save.grid(row=1, column=3, sticky="w", padx=5, pady=0)

        self.button_remove = tk.Button(self.choices_frame, text="Remove", command=self.remove_last_choice, width=20,
                                       height=1)
        self.button_remove.grid(row=2, column=0, sticky="n", padx=5, pady=0)



        #self.selector_playbook = tk.StringVar()
        #self.selector_playbook.set(self.customized_playbooks[0])  # Set the default value

        # Create the OptionMenu (dropdown menu)
        #self.dropdown_menu = tk.OptionMenu(self.button_frame_next, self.selector_playbook, *self.customized_playbooks)
       # self.dropdown_menu.pack(side=tk.LEFT, pady=20)

       # self.selector_playbook.trace_add("write", self.change_to_pb)

    def update_dropdown(self):
        self.setup_dropdown()
        self.combobox['values'] = self.customized_playbooks

    def change_to_pb(self, *args):
        selected_value = self.combobox.get()
        selected_value = selected_value[1:]
        print(f"Sleected Option{selected_value}")
        self.root.counter = int(selected_value)
        self.display_playbook(f"p{self.root.counter}")
        self.root.counter += 1

    def setup_dropdown(self):
        self.customized_playbooks = []
        with open("output/Categories_output.txt", "r") as c:
            for line in c:
                current_playbook = line.split(" ")
                current_number = current_playbook[0]
                self.customized_playbooks.append(current_number)

    def show_briefing(self):
        message = '''
How it works - Follow the steps:

Open up MITRE D3FEND on you second screen, then classify based on your expert knowledge.

1. Read the Information:
- Read the Name and the Description of the Playbooks
- Read the Playbook Steps and identify potential Techniques

 2. Read the DEFEND Techniques provided by OpenAI:
- Pick the correctly classified DEFEND techniques

 3. Add additional DEFEND Techniques:
- Add additional DEFEND Techniques, using the Search Bar
IMPORTANT: Always add the Bold Main-Technique for Equivalency purposes

 4. Add Custom Categories:
If no DEFEND Technique provides a suitable Category
--> Add a Custom Technique
The Technique should describe the playbooks purpose
e.g. ManagementInstruction'''

        popup = tk.Toplevel(self.root)
        popup.title("Popup")
        popup.geometry("720x480")

        # Add a label to the popup
        message_label = tk.Label(popup, text=message)
        message_label.pack(pady=20)

        # Add a button to close the popup
        close_button = tk.Button(popup, text="Close", command=popup.destroy)
        close_button.pack(pady=10)

        # Set the popup to be non-blocking and allow interaction with the main window
        popup.transient(self.root)  # Keep the popup on top of the main window
        popup.grab_set()  # Set focus to the popup window
        popup.grab_release()
        self.root.wait_window(popup)  # Wait for the popup window to close

    def remove_last_choice(self):
        print("Removed last item")
        print(self.choices)
        self.choices = self.choices[0:-1]
        print(self.choices)
        self.text_display_status.config(state=tk.NORMAL)
        content = self.text_display_status.get("1.0", tk.END).strip()
        # Find the position of the last line
        last_line_start = content.rfind("\n")
        if last_line_start == -1:
            # If there is no newline, it means there is only one line
            last_line_start = 0

        # Delete the last line
        self.text_display_status.delete(f"1.0 + {last_line_start} chars", tk.END)

        # Set the text display back to read-only mode
        self.text_display_status.config(state=tk.DISABLED)

    def on_suggestion_select(self, event):
        selected_index = self.suggestion_listbox.curselection()
        if selected_index:
            selected_text = self.suggestion_listbox.get(selected_index)
            self.add_from_list(selected_text)


    def update_suggestions(self, event=None):
        search_term = self.search_var.get().lower()
        self.suggestion_listbox.delete(0, tk.END)

        for item in defend_options:
            if search_term in item.lower():
                self.suggestion_listbox.insert(tk.END, item)



    def set_counter(self):
        with open("output/Categories_output.txt", "r") as initial:
            lines = initial.readlines()  # Read all lines at once

        if not lines:  # Check if the file is empty
            return 1

        for i in range(len(lines) - 1):
            # Just iterate until the second to last line
            current_line = lines[i]
            next_line = lines[i + 1]

            if next_line:
                continue

        # Handle the last line
        last_line = lines[-1]
        splitted = last_line.split(" ")
        return int(splitted[0][1:])

    def add_from_list(self, technique):
        self.choices.append(technique.strip())
        value = technique.strip()
        self.text_display_status.config(state=tk.NORMAL)
        self.text_display_status.insert(tk.END, f"{value}\n")
        self.text_display_status.config(state=tk.DISABLED)

    def add_custom(self):
        print(f"Added Custom Technique to the file")
        print(self.text_display_custom.get(1.0, tk.END).strip())
        content = self.text_display_custom.get(1.0, tk.END).strip()
        self.choices.append(f"c:{content}")
        print(self.choices)
        value = self.text_display_custom.get(1.0, tk.END).strip()
        self.text_display_status.config(state=tk.NORMAL)
        self.text_display_status.insert(tk.END, f"c:{value} \n")
        self.text_display_status.config(state=tk.DISABLED)
    def add_t1(self):
        if "99" in self.choice_1:
            print(f"No Choice was provided, so nothing can be chosen")
        else:
            if self.choice_1["1"] in defend_options:
                print(f"Added T1 to the choices")
                self.choices.append(self.choice_1["1"])
                print(self.choices)
                value = self.choice_1["1"]
                self.text_display_status.config(state=tk.NORMAL)
                self.text_display_status.insert(tk.END, f"{value} \n")
                self.text_display_status.config(state=tk.DISABLED)
            else:
                print("Could not add to choices, please provide a more specific technique")
                messagebox.showinfo("Information", "Could not add to choices, please provide a more specific technique")
    def add_t2(self):
        if "99" in self.choice_2:
            print(f"No Choice was provided, so nothing can be chosen")
        else:
            if self.choice_2["2"] in defend_options:
                print(f"Added T2 to the file")
                self.choices.append(self.choice_2["2"])
                print(self.choices)
                value = self.choice_2["2"]
                self.text_display_status.config(state=tk.NORMAL)
                self.text_display_status.insert(tk.END, f"{value} \n")
                self.text_display_status.config(state=tk.DISABLED)
            else:
                print("Could not add to choices, please provide a more specific technique")
                messagebox.showinfo("Information", "Could not add to choices, please provide a more specific technique")
    def add_t3(self):
        if "99" in self.choice_3:
            print(f"No Choice was provided, so nothing can be chosen")
        else:
            if self.choice_3["3"] in defend_options:
                print(f"Added T3 to the file")
                self.choices.append(self.choice_3["3"])
                print(self.choices)
                value = self.choice_3["3"]
                self.text_display_status.config(state=tk.NORMAL)
                self.text_display_status.insert(tk.END, f"{value} \n")
                self.text_display_status.config(state=tk.DISABLED)
            else:
                print("Could not add to choices, please provide a more specific technique")
                messagebox.showinfo("Information", "Could not add to choices, please provide a more specific technique")
    def add_t4(self):
        if "99" in self.choice_4:
            print(f"No Choice was provided, so nothing can be chosen")
        else:
            if self.choice_4["4"] in defend_options:
                print(f"Added T4 to the file")
                self.choices.append(self.choice_4["4"])
                print(self.choices)
                value = self.choice_4["4"]
                self.text_display_status.config(state=tk.NORMAL)
                self.text_display_status.insert(tk.END, f"{value} \n")
                self.text_display_status.config(state=tk.DISABLED)
            else:
                print("Could not add to choices, please provide a more specific technique")
                messagebox.showinfo("Information", "Could not add to choices, please provide a more specific technique")

    def display_choices(self, number):
        self.text_display.insert(tk.END, f"D3FEND Techniques by OpenAI: \n", "bold")
       # print(number)
        for call in api_calls:
            file_name = os.path.basename(call)[0:-5]
           #  print(file_name)
            with open(call, 'r') as f:
                content = f.read()
                content_json = json.loads(content)
                if number in content_json:
                  #  print(content_json[number])
                  if len(content_json[number]) > 0:
                    try:
                        self.choice_1 = content_json[number][0]
                        self.text_display.insert(tk.END, f"{content_json[number][0]} \n")
                    except:
                        self.choice_1 = "NaN"
                        self.text_display.insert(tk.END, "NaN\n")
                    try:
                        self.choice_2 = content_json[number][1]
                        self.text_display.insert(tk.END, f"{content_json[number][1]} \n")
                    except:
                        self.choice_2 = "NaN"
                        self.text_display.insert(tk.END, "NaN\n")
                    try:
                        self.choice_3 = content_json[number][2]
                        self.text_display.insert(tk.END, f"{content_json[number][2]}\n")
                    except:
                        self.choice_3 = "NaN"
                        self.text_display.insert(tk.END, "NaN\n")
                    try:
                        self.choice_4 = content_json[number][3]
                        self.text_display.insert(tk.END, f"{content_json[number][3]}\n")
                    except:
                        self.choice_4 = "NaN"
                        self.text_display.insert(tk.END, "NaN\n")
                  else:
                    self.choice_1 = {'99': 'No Choice provided'}
                    self.choice_2 = {'99': 'No Choice provided'}
                    self.choice_3 = {'99': 'No Choice provided'}
                    self.choice_4 = {'99': 'No Choice provided'}
    def display_playbook(self, number):
        self.choices = []
        self.text_display.config(state=tk.NORMAL)
        self.text_display.delete(1.0, tk.END)
        # index,id,vendor,playbook_name,playbook_description,tags,steps,actuator,step_types,step_names
        for index, row in df.iterrows():
            if row.id == number:
                self.playbook_id = row.id
                self.playbook_name = row.playbook_name
                self.description = row.playbook_description
                self.vendor = row.vendor
                self.steps = row.steps
                self.step_names = row.step_names
                break

        self.text_display.insert(tk.END, f"Name ({self.playbook_id}): \n", "bold")
        self.text_display.insert(tk.END, f"{self.playbook_name} \n\n", )
        self.text_display.insert(tk.END, f"Description: \n", "bold")
        self.text_display.insert(tk.END, f"{self.description}\n\n")
        self.text_display.insert(tk.END,
                                 f"------------------------------------------------------------------------------------ \n",
                                 "bold")
        self.display_choices(number)
        self.text_display.insert(tk.END, f"------------------------------------------------------------------------------------ \n", "bold")

        self.text_display.insert(tk.END, f"Vendor:\n", "bold")
        self.text_display.insert(tk.END, f"{self.vendor}\n\n")
        self.text_display.insert(tk.END, f"Playbook Steps:\n", "bold")
        i = 1
        step_list = self.step_names.split(",")
        for step in step_list:
            self.text_display.insert(tk.END, f"{i}: {step}\n")
            i += 1

    def show_message(self):
        # Enable text widget to modify its content
        self.text_display.config(state=tk.NORMAL)
        self.text_display.insert(tk.END, "Hello, this is a simple message!\n")
        self.text_display.config(state=tk.DISABLED)

    def clear_text(self):
        # Enable text widget to modify its content
        self.text_display.config(state=tk.NORMAL)
        self.text_display.delete(1.0, tk.END)
        self.text_display.config(state=tk.DISABLED)

    def save_into_file(self):
        output_path = "output/Categories_output.txt"
        line_insert = self.playbook_id + " " + self.playbook_name + ", Mapped Techniques: " + str(self.choices) + "\n"
        index_replace = None
        with open("output/Categories_output.txt", "r") as f:
            lines = f.readlines()

        for index, line in enumerate(lines):
            if self.playbook_id in line.split(" ")[0]:
                index_replace = index

        if index_replace is not None:
            lines[index_replace] = line_insert
            with open(output_path, "w")as replacer:
                replacer.writelines(lines)
                print(f"Choices for {self.playbook_id} were replaced ")
        else:
            lines.append(line_insert)
            with open(output_path, "w")as appender:
                appender.writelines(lines)
                print(f"Choices for {self.playbook_id} was appended to file")
        self.update_dropdown()
        #f.write(line_insert)



    def load_last_playbook(self):
        self.root.counter -= 2
        print(self.root.counter)
        self.load_next_playbook()

    def load_next_playbook(self):
        # self.save_into_file()
        # Enable text widget to modify its content
        self.display_playbook(f"p{self.root.counter}")
        self.root.counter += 1

        self.text_display_status.config(state=tk.NORMAL)
        self.text_display_status.delete(1.0, tk.END)
        self.text_display_status.config(state=tk.DISABLED)



# Create the main window
root = tk.Tk()

# Create an instance of the application
app = SimpleApp(root)

# Run the application
root.mainloop()
