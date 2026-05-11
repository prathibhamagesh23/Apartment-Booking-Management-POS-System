# Dictionary to store guest names and their reward points
g_r = {
    "Alyssa": 20,
    "Luigi": 32
}

# Dictionary to store apartment details with correct building rates and capacities
a_d = {
    "U12swan": {"p": 95.0, "c": 2},
    "U209duck": {"p": 148.7, "c": 4},
    "U49goose": {"p": 212.2, "c": 3}
}

# Dictionary to store supplementary items and their costs
s_c = {
    "bfast": 5.2,
    "carp": 10.0,
    "tp": 2.5
}

# Function to show menu options
def show_menu():
    print("\nMenu:")
    print("1. Make a booking")
    print("2. Add/update information of an apartment unit")
    print("3. Add/update supplementary items")
    print("4. Display existing guests")
    print("5. Display existing apartment units")
    print("6. Display existing supplementary items")
    print("7. Display booking history")
    print("8. Exit the program")

# Function to check if the input is alphabetic

#function checks if a given input consists only of alphabetic characters.
def is_alpha(name):
    return name.isalpha()

# Function to add or update apartment information
#The update_apartment function allows users to add or update apartment details. It prompts for input in the format id price capacity`and performs several validations. It checks if the ID is correctly formatted, the price is positive, and the capacity is a positive integer. If any validation fails, it prompts the user to correct the input. Once valid, it updates the apartment information in the dictionary.
def update_apartment():
    while True:
        inp = input("Enter apartment (id price capacity): ")
        data = inp.split()
        
        if len(data) != 3:
            print("Invalid format. Use: id price capacity")
            continue
        
        a_id, price, cap = data
        
        # Validate apartment ID format
        if not (a_id.startswith('U') and a_id[1:-4].isdigit() and
                a_id[-4:] in ['duck', 'goose', 'swan']):
            print("Invalid ID. Format: U<num><building> (e.g., U12duck).")
            continue
        
        # Validate price
        if not price.replace('.', '', 1).isdigit() or float(price) <= 0:
            print("Invalid price. Should be positive.")
            continue
        
        # Validate capacity
        if not cap.isdigit() or int(cap) <= 0:
            print("Invalid capacity. Should be positive.")
            continue
        
        # Update apartment details
        a_d[a_id] = {"p": float(price), "c": int(cap)}
        print(f"Apartment {a_id} updated.")
        break

# Function to add or update supplementary items
#The update_supplementary function updates supplementary items by prompting for input in the format item price. It validates that each item follows the `item price` format and that the price is positive. If any input is invalid, the user is asked to correct it. Once all items are validated, they are updated in the s_c dictionary.
def update_supplementary():
    while True:
        inp = input("Enter supplementary items (item price): ")
        items = inp.split(',')
        valid = True
        for item in items:
            parts = item.split()
            if len(parts) != 2:
                print("Invalid format. Use 'item price'.")
                valid = False
                break
            item_id, cost = parts
            if not cost.replace('.', '', 1).isdigit() or float(cost) <= 0:
                print(f"Invalid cost for '{item_id}'.")
                valid = False
                break
        if valid:
            for item in items:
                parts = item.split()
                item_id, cost = parts
                s_c[item_id] = float(cost)
            print("Supplementary items updated.")
            break

# Function to display all guests
#Displays all guests and their reward points by iterating over the g_r dictionary
def show_guests():
    print("\nGuests:")
    for guest, points in g_r.items():
        print(f"{guest}: {points} points")

# Function to display all apartments
#Shows all apartments with their ID, price per night, and bed count by iterating over the a_d dictionary.
def show_apartments():
    print("\nApartments:")
    for a_id, details in a_d.items():
        print(f"{a_id}: ${details['p']} per night, {details['c']} beds")

# Function to display all supplementary items
#Lists all supplementary items and their costs by iterating over the s_c dictionary.
def show_supplementary():
    print("\nSupplementary items:")
    for item_id, cost in s_c.items():
        print(f"{item_id}: ${cost}")

#The validate_date function checks if a given date string is in the dd/mm/yyyy format. It splits the input into day, month, and year, then verifies if these values are within valid ranges (1-31 for days, 1-12 for months, and a positive number for the year). If the date is valid, it returns True; otherwise, it returns False.
def validate_date(date_str):
    try:
        day, month, year = map(int, date_str.split('/'))
        if 1 <= day <= 31 and 1 <= month <= 12 and year > 0:
            return True
    except ValueError:
        pass
    return False

# Function to calculate days between two dates
#The days_between function calculates the number of days between two dates provided in dd/mm/yyyy format. It converts each date into a total number of days by approximating months as 30 days and years as 365 days. The difference between these two values gives the number of days between the two dates.
def days_between(start, end):
    d1d, d1m, d1y = map(int, start.split('/'))
    d2d, d2m, d2y = map(int, end.split('/'))
    
    d1 = d1y * 365 + d1m * 30 + d1d
    d2 = d2y * 365 + d2m * 30 + d2d
    
    return d2 - d1

# Function to make a booking
#The make_booking function facilitates the booking process by guiding users through several steps. It starts by asking for the guest's name, ensuring it is alphabetic, and adds the guest to the g_r dictionary if they are new. The function then prompts for and validates the apartment ID, displaying capacity details and checking if the ID is already present in the a_d dictionary. It verifies the number of guests, allows for extra beds within capacity limits, and requests check-in and check-out dates. 
#Following date validation, the function calculates the stay length and checks it against the provided duration. Users select supplementary items from a list, with their costs added to the total price. After calculating the final price and displaying the booking details, the function updates the guest's reward points based on the length of stay.
def make_booking():
    while True:
        # Input guest name
        while True:
            guest_name = input("Enter guest name: ")
            if is_alpha(guest_name):
                if guest_name not in g_r:
                    g_r[guest_name] = 0
                break
            print("Invalid name. Only letters allowed.")
        
        # Input apartment ID
        while True:
            a_id = input("Enter apartment ID: ").strip()
            if (a_id.startswith('U') and 
                a_id[1:-4].isdigit() and 
                a_id[-4:] in ['duck', 'goose', 'swan']):
                
                if a_id not in a_d:
                    print(f"Apartment ID {a_id} is new. Adding.")
                    a_d[a_id] = {"p": 0.0, "c": 0}
                break
            else:
                print("Invalid ID. Format: U<num><building> (e.g., U78duck).")
        
        # Display apartment capacity details
        print(f"\nApartment ID {a_id} has a capacity of {a_d[a_id]['c']} guests.")
        
        # Input and validate number of guests
        while True:
            num_guests = input("Enter number of guests: ")
            if num_guests.isdigit() and int(num_guests) > 0:
                num_guests = int(num_guests)
                if num_guests <= a_d[a_id]['c']:
                    break
                else:
                    print("Guests exceed capacity. Consider extra beds.")
                    break
            else:
                print("Invalid number. Should be positive.")
        
        # Input and validate extra beds
        while True:
            extra_beds = input("Enter extra beds (0-2): ")
            if extra_beds.isdigit() and 0 <= int(extra_beds) <= 2:
                extra_beds = int(extra_beds)
                if num_guests > (a_d[a_id]['c'] + extra_beds * 2):
                    print("Guests exceed max capacity with extra beds.")
                else:
                    break
            else:
                print("Invalid number. Between 0 and 2.")
        
        # Input and validate check-in and check-out dates
        while True:
            check_in_date = input("Enter check-in date (dd/mm/yyyy): ")
            if validate_date(check_in_date):
                break
            print("Invalid check-in date. Use dd/mm/yyyy.")
        
        while True:
            check_out_date = input("Enter check-out date (dd/mm/yyyy): ")
            if validate_date(check_out_date):
                break
            print("Invalid check-out date. Use dd/mm/yyyy.")
        
        # Input and validate length of stay
        while True:
            stay_length = input("Enter stay length in nights: ")
            if stay_length.isdigit() and int(stay_length) > 0:
                stay_length = int(stay_length)
                calc_stay_length = days_between(check_in_date, check_out_date)
                if stay_length == calc_stay_length:
                    break
                else:
                    print("Stay length doesn't match dates. Re-enter.")
            else:
                print("Invalid length. Positive integer.")
        
        # Input and validate booking date
        while True:
            booking_date = input("Enter booking date (dd/mm/yyyy): ")
            if validate_date(booking_date):
                break
            print("Invalid booking date. Use dd/mm/yyyy.")
        
        # Display supplementary items and get user selection
        selected_items = {}
        while True:
            print("\nSupplementary items:")
            print("1. car_park - $25 (per night)")
            print("2. breakfast - $21 (per person)")
            print("3. toothpaste - $5 (per tube)")
            print("4. extra_bed - $50 (per night)")
            
            supp_choice = input("Enter item number (1, 2, 3, 4) or 'done': ")
            
            if supp_choice == 'done':
                break
            elif supp_choice in ['1', '2', '3', '4']:
                item_key = ['carp', 'bfast', 'tp', 'x_bed'][int(supp_choice) - 1]
                selected_items[item_key] = s_c[item_key]
            else:
                print("Invalid choice. Enter 1, 2, 3, 4 or 'done'.")
        
        # Calculate total price
        total_price = a_d[a_id]['p'] * stay_length
        total_price += sum(selected_items.values())
        
        # Round total price
        total_price = round(total_price, 2)
        
        print(f"\nApartment ID: {a_id}")
        print(f"Check-in: {check_in_date}")
        print(f"Check-out: {check_out_date}")
        print(f"Booking date: {booking_date}")
        print(f"Stay length: {stay_length} nights")
        print(f"Total Price: ${total_price:.2f}")
        
        # Update guest reward points
        g_r[guest_name] += int(stay_length * 10)
        print(f"Updated reward points for {guest_name}: {g_r[guest_name]}")
        break

# Function to display booking history for a guest
#The show_hist function displays a guest's booking and order history. It first prompts for a guest's name and checks if it exists in the guests dictionary. If the name is valid, it prints a simulated booking history with order details, total costs, and earned rewards. After displaying the history, it asks if the user wants to view another guest's history and continues based on the response.
def show_hist():
    while True:
        # Prompt the user to enter a guest name
        g_name = input("Enter the main guest name: ")
        
        # Check if the guest name exists in the guest dictionary
        if g_name not in guests:
            print("Invalid guest name. Please enter a valid guest name.")
            continue
        
        # Simulated booking history display
        print(f"\nThis is the booking and order history for {g_name}.")
        print("List                Total Cost Earned Rewards")
        print("Order 1 1 x U12swan        95.0     95")
        print("Order 2 1 x U209duck, 2 x breakfast  148.7   149")
        print("Order 3 2 x U49goose, 4 x breakfast, 1 carpark  424.4  424")
        
        # Continue to display or exit
        cont_disp = input("Do you want to display another guest's booking history? (yes/no): ")
        if cont_disp.lower() != 'yes':
            break

# Main loop
#The main loop presents a menu to the user with various options such as making a booking, updating apartment or supplementary items, showing guests, apartments, and supplementary items, or displaying booking history. The loop processes the user's choice and calls the corresponding function or exits the program if the option is '8'. Invalid options prompt the user to choose again.
while True:
    show_menu()
    c = input("Choose an option: ").strip()
    if c == '1':
        make_booking()
    elif c == '2':
        update_apartment()
    elif c == '3':
        update_supplementary()
    elif c == '4':
        show_guests()
    elif c == '5':
        show_apartments()
    elif c == '6':
        show_supplementary()
    elif c == '7':
        show_hist()
    elif c == '8':
        print("Exiting the program.")
        break
    else:
        print("Invalid option. Please choose again.")

