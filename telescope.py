import subprocess
import json
import os
import tkinter as tk
#from tkinter import ttk
import getpass

# Function to read JSON file and update variables based on the chosen layout_name
def choose_layout(file_path, chosen_layout_name):
    with open(file_path, 'r') as file:
        data = json.load(file)

        if chosen_layout_name in data:
            global layout_name, layout_options, layout_ports
            layout_name = chosen_layout_name
            layout_options = data[chosen_layout_name]['layout_options']
            layout_ports = data[chosen_layout_name]['layout_ports']
            print(f"   ╚═<>layout "+layout_name+" loaded>")
        else:
            print(f"   ╚═<>Layout with name "+layout_name+" not found>")

# Function to add a new layout object to the JSON file
def create_layout(file_path, new_layout_name, new_layout_options, new_layout_ports):
    with open(file_path, 'r') as file:
        data = json.load(file)

    data[new_layout_name] = {
        'layout_options': new_layout_options,
        'layout_ports': new_layout_ports
    }

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)
        print(f"   ╚═<>Layout {new_layout_name} added>")

# Function to modify an existing layout in the JSON file
def modify_layout(file_path, layout_name, new_layout_options, new_layout_ports):
    with open(file_path, 'r') as file:
        data = json.load(file)

    if layout_name in data:
        data[layout_name]['layout_options'] = new_layout_options
        data[layout_name]['layout_ports'] = new_layout_ports

        with open(file_path, 'w') as file:
            json.dump(data, file, indent=2)
            print(f"   ╚═<>Layout {layout_name} modified>")
    else:
        print(f"   ╚═<>Layout with name {layout_name} not found>")

# Function to delete a layout from the JSON file
def delete_layout(file_path, layout_name):
    with open(file_path, 'r') as file:
        data = json.load(file)

    if layout_name in data:
        del data[layout_name]

        with open(file_path, 'w') as file:
            json.dump(data, file, indent=2)
            print(f"   ╚═<>Layout {layout_name} deleted>")
    else:
        print(f"   ╚═<>Layout with name {layout_name} not found>")

# Function to list all layout names
def list_layouts(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    layout_names = list(data.keys())
    print('')
    print('+----------------------------+')
    print('|<>════════< list >════════<>|')
    print('+----------------------------+')
    print('|<>═╔══<| layouts |>          ')
    for name in layout_names:
        print('|   ╚═<>:'+name)
    print('+----------------------------+')

# Function to change options in 'configure layout command'
def options_changing():
    print('   ╚═<'+layout_name+'>[TELESCOPE]<do you want to change layout options? (y/n)>')
    conf = input('   ╚═<>:')
    if conf == 'y' :
        print('   ╚═<'+layout_name+'>[TELESCOPE]<Enter new layout options>')
        global new_options
        new_options = input('   ╚═<>:')
    else :
        print('   ╚═<'+layout_name+'>[TELESCOPE]<options not changed>')
        new_options = layout_options

# Function to change ports in 'configure layout command'
def ports_changing():
    print('   ╚═<'+layout_name+'>[TELESCOPE]<do you want to change layout ports? (y/n)>')
    conf = input('   ╚═<>:')
    if conf == 'y' :
        print('   ╚═<'+layout_name+'>[TELESCOPE]<Enter new layout ports>')
        global new_ports
        new_ports = input('   ╚═<>:')
    else :
        print('   ╚═<'+layout_name+'>[TELESCOPE]<ports not changed>')  
        new_ports = layout_ports
      
# Commands list
def help_chart() : 
    print()
    print('+------------------------------------+-------------------------------------+')
    print('|<>══════════════════════════< command list >════════════════════════════<>|')
    print('+------------------------------------+-------------------------------------+')
    print('|<>═╔══<| layouts |>                                                       |')
    print("|   ╚═<> show layouts all                   print a list of all layouts    |")
    print("|   ╚═<> show layout                        print loaded layout configs    |")
    print("|   ╚═<> create layout                      create a new layout            |")
    print("|   ╚═<> configure layout                   change loaded layout configs   |")
    print("|   ╚═<> load layout                        load a saved layout            |")
    print("|   ╚═<> remove layout                      remove a saved layout          |")
    print('|<>═══<> scan                               perform the scan               |')
    print('|<>═══<> exit                               exit from Telescope            |')
    print('+------------------------------------+-------------------------------------+')

def save_file_with_loading_bar(output_file, scan_results):
    # Create the main application window
    app = tk.Tk()
    app.title("Saving Nmap Results")

    # Create a progress bar
    #progress_bar = ttk.Progressbar(app, mode='indeterminate')
   # progress_bar.pack(pady=10)

    # Function to save the scan results in a file
    def save_results():
        with open(output_file, 'w', buffering=1, encoding='utf-8') as file:
            file.write(scan_results)
            app.after(100, app.destroy)  # Close the app after 100 milliseconds

    # Run the save function in a separate thread
    app.after(100, save_results)

    # Start the progress bar
    progress_bar.start()

    # Run the application
    app.mainloop()

def run_nmap_scan(target, nmap_options, nmap_ports):
    # Construct the Nmap command
    nmap_command = ['nmap', target] + nmap_options.split() + nmap_ports.split()

    try:
        # Run the Nmap scan using subprocess with stdout as PIPE
        process = subprocess.Popen(nmap_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)

        # Print the Nmap scan results in real-time and store them in memory
        print()
        print('+-------------------------------------------------------------------------------------------------------------------------------------+')
        print('|<>═════════════════════════════════════════════════════< Nmap scan results >═══════════════════════════════════════════════════════<>|')
        print('+-------------------------------------------------------------------------------------------------------------------------------------+')

        scan_results = ''
        for line in iter(process.stdout.readline, ''):
            print(line, end='', flush=True)  # Print to console and flush immediately
            scan_results += line  # Store in memory

        process.stdout.close()
        process.wait()

        print()
        print('+-------------------------------------------------------------------------------------------------------------------------------------+')
        print()

        # Ask for the final output file name using input (to display what you're typing)
        print("<>═╔═<" + layout_name + ">[TELESCOPE]<Enter final output file name>")
        final_output_file_name = input('   ╚═<>:')
        current_directory = os.getcwd()
        output_directory = os.path.join(current_directory, 'output')

        # Create the output directory if it doesn't exist
        os.makedirs(output_directory, exist_ok=True)

        final_output_file = os.path.join(output_directory, final_output_file_name + '.txt')

        # Display the loading bar pop-up window
        save_file_with_loading_bar(final_output_file, scan_results)

        # Print a success message
        print()
        print(f"<>═══<" + layout_name + ">[TELESCOPE]<Nmap scan results saved to {final_output_file}>")

    except subprocess.CalledProcessError as e:
        # Handle any errors that may occur during the Nmap scan
        print("<>═╔═<"+ layout_name +">[TELESCOPE]<Error during Nmap scan>")
        print('   ╚═<>:' + e.stderr)


def logo():
    print('||>═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════<||')
    print('||       ___   ______ _                                                                                                              ||')
    print('||   ==c(___(o(______(_()   ::::::::::: :::::::::: :::        ::::::::::  ::::::::   ::::::::   ::::::::  :::::::::  ::::::::::      || ')
    print('||            \\=\\               :+:     :+:        :+:        :+:        :+:    :+: :+:    :+: :+:    :+: :+:    :+: :+:             || ')
    print('||             )=\\              +:+     +:+        +:+        +:+        +:+        +:+        +:+    +:+ +:+    +:+ +:+             || ')
    print('||            //|\\\\             +#+     +#++:++#   +#+        +#++:++#   +#++:++#++ +#+        +#+    +:+ +#++:++#+  +#++:++#        || ')
    print('||           //|| \\\\            +#+     +#+        +#+        +#+               +#+ +#+        +#+    +#+ +#+        +#+             || ')
    print('||          // ||  \\\\           #+#     #+#        #+#        #+#        #+#    #+# #+#    #+# #+#    #+# #+#        #+#             || ')
    print('||         //       \\\\          ###     ########## ########## ##########  ########   ########   ########  ###        ##########      || ')
    print('||                                                                                                                                   ||')
    print('||>═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════<||')
    print('                         ++-------------------------------------------------------------------------------++')
    print("                         ||>═══════════< Welcome to Telescope - type 'help' for command list >═══════════<||")
    print('                         ++-------------------------------------------------------------------------------++')


layout_name = str()
layout_options = ()
layout_ports = ()

target = ()

new_options = ()
new_ports = ()

current_directory = os.getcwd()
json_file_path = os.path.join(current_directory, 'layouts.json')

logo()

def main():
    print('')
    print('<>═╔═<'+ layout_name +'>[TELESCOPE]<>')
    main_1()

def main_1():

        choice = input('   ╚═<>:')

        if choice == 'help' :
            help_chart()
            main()

        elif choice == 'show layouts all' :
            # List all layouts
            list_layouts(json_file_path)
            main()

        elif choice == 'sh layouts all' :
            # List all layouts
            list_layouts(json_file_path)
            main()    
        
        elif choice == 'show layout' :
            if layout_name == '' :
                print('   ╚═<>[TELESCOPE]<No layout selected, please load a layout first>')
            else :
                print('')
                print('+------------------------------------+')
                print('|<>═══════════< loaded >═══════════<>|')
                print('+------------------------------------+')
                print('|<>═╔══<| layout |>                   ')
                print('|   ╚══<name>:'+layout_name)
                print('|   ╚══<options>:'+layout_options)
                print('|   ╚══<ports>:'+layout_ports)
                print('+------------------------------------+')
                
            main()

        elif choice == 'sh layout' :
            if layout_name == '' :
                print('   ╚═<>[TELESCOPE]<No layout selected, please load a layout first>')
            else :
                print('')
                print('+-----------------------------------------------------------------------------+')
                print('|<>════════════════════════════< loaded layout >════════════════════════════<>|')
                print('+-----------------------------------------------------------------------------+')
                print('|')
                print('|<>══<name>:'+layout_name)
                print('|')
                print('|<>══<options>:'+layout_options)
                print('|')
                print('|<>══<ports>:'+layout_ports)
                print('|')
                print('+-----------------------------------------------------------------------------+')
            main()

        elif choice == 'create layout' :
            # Create a new layout
            print('   ╚═<new_layout>[TELESCOPE]<Enter layout name>')
            layout1 = input('   ╚═<>:')
            print('   ╚═<new_layout>[TELESCOPE]<Enter -nmap- options>')
            options1 = input('   ╚═<>:')
            print('   ╚═<new_layout>[TELESCOPE]<Enter -nmap- ports>')
            ports1 = input('   ╚═<>:')
            create_layout(json_file_path, layout1, options1, ports1)
            main()

        elif choice == 'remove layout' :
            # Delete a layout
            print('   ╚═<>[TELESCOPE]<Enter layout name>')
            chosen_one = input('   ╚═<>:')
            print('   ╚═<>[TELESCOPE]<Are you sure to remove \''+chosen_one+'\' layout? (YN)>' )
            confirm = input('   ╚═<>:')

            if confirm == 'y' :
                delete_layout(json_file_path, chosen_one)
                main()

            else : main()

        elif choice == 'load layout' :
            # Choose a layout
            print('   ╚═<>[TELESCOPE]<Enter layout name>')
            chosen_one = input('   ╚═<>:')
            choose_layout(json_file_path, chosen_one)
            main()

        elif choice == 'configure layout' :         
            # Modify the chosen layout
            if layout_name == '' :
                print('   ╚═<>[TELESCOPE]<no loaded layout to config>')
                main()
            else :
                options_changing()
                ports_changing()

                print('   ╚═<'+layout_name+'>[TELESCOPE]<Are you sure to change '+layout_name+' options in: '+str(new_options)+'. and '+layout_name+' ports in: '+str(new_ports)+'? (y/n)>' )
                confirm = input('   ╚═<>:')

                if confirm == 'y' :
                    modify_layout(json_file_path, layout_name, new_options, new_ports)
                    choose_layout(json_file_path, layout_name)
                    main()
                else : main()      

        elif choice == 'scan' :
            if layout_name == '' :
                print('   ╚═<>[TELESCOPE]<No layout selected, please load a layout first>')
            else :
                print('   ╚═<'+layout_name+'>[TELESCOPE]<Enter target ip or host name>')
                global target
                target = input('   ╚═<>:')
                run_nmap_scan(target, layout_options, layout_ports)
                main()

        elif choice == '' :
            main_1()
        
        elif choice == 'exit' : 
            print('   ╚═<>[TELESCOPE]<goodbye>')
            quit()

        else :
            print('   ╚═<'+layout_name+">[TELESCOPE]<Invalid choice, enter 'help' for more info.>")
            main()

if __name__ == "__main__":
    main()
