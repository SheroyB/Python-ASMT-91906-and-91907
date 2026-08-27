'''This program is the first version of a screentime awareness app,
it lets a parent log screen time on the console and view the total.'''

while True: #Main loop that keeps showing the menu until the user exits
    print("\nScreentime Awareness App - Version 1")
    print("1. Log screen time")
    print("2. View total screen time")
    print("3. Exit")

    choice = input("Choose an option (1-3): ")

    if choice == "1": #Log screen time
        while True:
            try:
                app_name = input("Which app or device was used?: ")
                if not app_name.isalpha(): #Checks that user entered only letters
                    print("App name must only contain letters")
                    continue
                break
            except TypeError:
                continue

        while True:
            try:
                minutes = int(input("Minutes spent on this app: "))
                if minutes <= 0: #Checks that user entered a number greater than 0
                    print("Minutes must be greater than 0")
                    continue
                break
            except (ValueError, TypeError): #Doesn't allow the user to enter strings or leave the question blank
                print("Please enter a valid number")

        with open("screentime_log.txt", "a") as log_file: #Saving the entry into an external txt file
            log_file.write(f"\n{app_name},{minutes}")

        print(f"Logged {minutes} minutes on {app_name}.")

    elif choice == "2": #View total screen time
        try:
            with open("screentime_log.txt", "r") as log_file: #Loading entries from the txt file
                lines = log_file.readlines()
        except FileNotFoundError:
            lines = []

        total_minutes = 0
        for line in lines: #Adding up the minutes from every saved entry
            line = line.strip()
            if line == "": #Skips any blank lines in the file
                continue
            parts = line.split(",")
            if len(parts) == 2:
                total_minutes = total_minutes + int(parts[1])

        if total_minutes == 0:
            print("No screentime has been logged yet.")
        else:
            print(f"Total screentime logged: {total_minutes} minutes")

    elif choice == "3": #Exit the program
        print("Goodbye.")
        break

    else: #Catches any input that isn't 1, 2 or 3
        print("Please enter a number from 1 to 3.")
