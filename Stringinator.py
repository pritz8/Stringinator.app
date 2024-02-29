import os
import pickle
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from theme import Theme


def browse_file():
    filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if filename:
        entry_input_file.delete(0, tk.END)
        entry_input_file.insert(0, filename)


def generate_commands():
    input_file = entry_input_file.get()
    command_type = command_var.get()
    game_type = game_var.get()

    if not input_file:
        messagebox.showerror("Error", "Please select an input file.")
        return

    # Create the output folder if it does not exist
    output_folder = "Output"
    os.makedirs(output_folder, exist_ok=True)

    # Create the _String folder if it does not exist
    string_folder = os.path.join(output_folder, "_String")
    os.makedirs(string_folder, exist_ok=True)

    languages = [
        "ENGLISH",
        "DANISH",
        "DUTCH",
        "FINNISH",
        "FRENCH",
        "GERMAN",
        "ITALIAN",
        "MEXICAN",
        "POLISH",
        "SPANISH",
        "SWEDISH",
    ]

    with open(input_file, "r") as file:
        data = file.readlines()

    with open(os.path.join(output_folder, "String.end"), "w") as string_end_file:
        for lang in languages:
            string_end_file.write("// String\n\n")
            if game_type == "Most Wanted":
                string_end_file.write(
                    f"if file_exists absolute LANGUAGES\\{lang}.bin\n"
                )
            elif game_type == "Carbon":
                string_end_file.write(
                    f"if file_exists absolute LANGUAGES\\{lang}_FRONTEND.bin\n"
                )
            string_end_file.write("do\n")
            string_end_file.write(f"append _String\\{lang}.end\n")
            string_end_file.write("else\n")
            string_end_file.write("// do nothing\n")
            string_end_file.write("end\n\n")

            with open(os.path.join(string_folder, f"{lang}.end"), "w") as file:
                file.write("[VERSN2]\n")
                if game_type == "Most Wanted":
                    file.write(f"new negate LANGUAGES\\{lang}.BIN\n")
                elif game_type == "Carbon":
                    file.write(f"new negate LANGUAGES\\{lang}_FRONTEND.BIN\n")

                for line in data:
                    name_pair = line.strip().split("=")
                    if len(name_pair) != 2:
                        messagebox.showerror(
                            "Error",
                            f"Invalid format in input file: {line.strip()}. Use 'LABEL=IN-GAME NAME' format.",
                        )
                        return
                    insert_name, insert_name2 = name_pair
                    file.write(f"{command_type} LANGUAGES\\{lang}")
                    if game_type == "Most Wanted":
                        file.write(".BIN STRBlocks Global AUTO")
                    elif game_type == "Carbon":
                        file.write("_FRONTEND.BIN STRBlocks Frontend AUTO")
                    else:
                        file.write("_FRONTEND.BIN STRBlocks Frontend AUTO")
                    file.write(f" {insert_name}")
                    if insert_name2.strip():
                        if " " in insert_name2:
                            file.write(f' "{insert_name2.strip()}"')
                        else:
                            file.write(f" {insert_name2.strip()}")
                    file.write("\n")

                file.write("\n")

    messagebox.showinfo("Success", "Strings generated successfully.")


def open_output_folder():
    output_folder = "Output"
    os.startfile(output_folder)


# Create main window
root = tk.Tk()
root.title("Stringinator 3000 by VeeTec, Pritz and Viper4K")

screen_width = 700
screen_height = 600
x_coord = root.winfo_screenwidth() // 2 - screen_width
y_coord = (root.winfo_screenheight() - 70) // 2 - screen_height // 2
root.geometry(f"{screen_width}x{screen_height}+{x_coord+screen_width//2}+{y_coord}")
THEME_FILE = os.path.join(os.curdir, "settings", "theme.bin")

if not os.path.exists(os.path.join(os.curdir, "settings")):
    os.mkdir(os.path.join(os.curdir, "settings"))

if not os.path.exists(THEME_FILE):
    with open(THEME_FILE, "wb") as f:
        pickle.dump("dark", f)
        CURR_THEME = "dark"
else:
    with open(THEME_FILE, "rb") as f:
        CURR_THEME = pickle.load(f)

theme = Theme(root, CURR_THEME)

# Introduction text
intro_text = """Welcome to Stringinator 3000
------------------------------------------------------------------------
This tool is designed to make creating string scripts for your Binary installer a bit easier.
Please provide the input file containing Label and In-Game Name pairs with the format shown below

LABEL=IN-GAME NAME (Example: BODY_RB=ROCKET BUNNY)

Each pair should be on a separate line
------------------------------------------------------------------------"""
label_intro = tk.Label(root, text=intro_text, wraplength=580, justify="center")
label_intro.grid(row=0, column=0, columnspan=3, padx=5, pady=5)

# Input file selection
label_input_file = tk.Label(root, text="Input File")
label_input_file.grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_input_file = tk.Entry(root, width=50)
entry_input_file.grid(row=1, column=1, padx=5, pady=5)
button_browse = tk.Button(root, text="Browse", command=browse_file)
button_browse.grid(row=1, column=2, padx=5, pady=5)

# Command type dropdown menu
command_var = tk.StringVar(root)
command_var.set("add_or_update_string")  # Default value
button_command_type = tk.OptionMenu(
    root, command_var, "add_or_update_string", "add_string"
)
button_command_type.grid(row=2, column=1, padx=5, pady=5)
button_command_type.config(text="Command Type: add_or_update_string")

# Game type dropdown menu
game_var = tk.StringVar(root)
game_var.set("Most Wanted")  # Default value
button_game_type = tk.OptionMenu(root, game_var, "Most Wanted", "Carbon")
button_game_type.grid(row=3, column=1, padx=5, pady=5)
button_game_type.config(text="Game Type: Most Wanted")

# Generate commands button
button_generate = tk.Button(root, text="Generate Strings", command=generate_commands)
button_generate.grid(row=4, column=1, padx=5, pady=5)

# Open output folder button
button_open_output_folder = tk.Button(
    root, text="Open Output Folder", command=open_output_folder
)
button_open_output_folder.grid(row=5, column=1, padx=5, pady=5)

# Toggle theme button
button_toggle_theme = tk.Button(root, text="Toggle Theme", command=theme.toggle_theme)
button_toggle_theme.grid(row=6, column=1, padx=5, pady=5)


# Run the GUI
root.mainloop()
