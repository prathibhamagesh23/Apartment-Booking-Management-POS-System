import os
import csv
from datetime import datetime
import sys  # To handle command-line arguments

# Exceptions
class InvalidGuestNameError(Exception):
    pass

class InvalidProductError(Exception):
    pass

class InvalidQuantityError(Exception):
    pass

class DateDiscrepancyError(Exception):
    pass

# Guest Class
class Guest:
    def __init__(self, guest_id, name, reward):
        """Constructor for Guest class with default reward_rate and redeem_rate"""
        self.guest_id = guest_id  # Unique ID
        self.name = name   
        self.reward = reward  
        self.reward_rate = 100  # Default reward rate (100%)
        self.redeem_rate = 1  # Default redeem rate (1%)

    # Getter methods for each attribute
    def get_id(self):
        return self.guest_id

    def get_name(self):
        return self.name

    def get_reward_rate(self):
        return self.reward_rate

    def get_reward(self, total_cost=None):
        """Returns the reward based on the total cost, rounded to the nearest integer."""
        if total_cost is not None:
            return round(total_cost * (self.reward_rate / 100))
        return self.reward

    def get_redeem_rate(self):
        return self.redeem_rate

    # Method to update reward points
    def update_reward(self, value):
        """Increases the reward points by the specified value."""
        self.reward += value

    # Method to display guest information
    def display_info(self):
        """Displays guest's information."""
        print(f"Guest ID: {self.guest_id}")
        print(f"Name: {self.name}")
        print(f"Reward Rate: {self.reward_rate}%")
        print(f"Rewards: {self.reward}")
        print(f"Redeem Rate: {self.redeem_rate}%")

    # Method to set reward rate
    def set_reward_rate(self, rate):
        """Adjusts the reward rate."""
        self.reward_rate = rate

    # Method to set redeem rate
    def set_redeem_rate(self, rate):
        """Adjusts the redeem rate."""
        self.redeem_rate = rate


# Product Class
class Product:
    def __init__(self, product_id, name, price):
        """Constructor for Product class"""
        self.product_id = product_id  # Unique identifier of the product
        self.name = name  # Name of the product
        self.price = price  # Unit price of the product

    # Getter methods for the attributes
    def get_id(self):
        return self.product_id

    def get_name(self):
        return self.name

    def get_price(self):
        return self.price

    # Method to display product information (empty for now, will be overridden)
    def display_info(self):
        pass  # Empty method to be overridden by subclasses


# ApartmentUnit Class
class ApartmentUnit(Product):
    def __init__(self, product_id, name, price, capacity):
        """Constructor for ApartmentUnit class, inheriting from Product"""
        super().__init__(product_id, name, price)
        self.capacity = capacity  # Maximum guests allowed in the apartment

    # Getter for capacity
    def get_capacity(self):
        return self.capacity

    # Overriding display_info to show apartment unit details
    def display_info(self):
        print(f"Apartment ID: {self.product_id}")
        print(f"Apartment Name: {self.name}")
        print(f"Rate per Night: ${self.price} (AUD)")
        print(f"Capacity: {self.capacity} guests")


# SupplementaryItem Class
class SupplementaryItem(Product):
    def __init__(self, product_id, name, price):
        """Constructor for SupplementaryItem class, inheriting from Product"""
        super().__init__(product_id, name, price)

    # Overriding display_info to show supplementary item details
    def display_info(self):
        print(f"Supplementary Item ID: {self.product_id}")
        print(f"Supplementary Item Name: {self.name}")
        print(f"Unit Price: ${self.price} (AUD)")


# Order Class
class Order:
    def __init__(self, guest, products, total_cost, earned_rewards, order_datetime):
        """Constructor for Order class"""
        self.guest = guest  # Guest who makes the purchase
        self.products = products  # List of (product, quantity) tuples
        self.total_cost = total_cost
        self.earned_rewards = earned_rewards
        self.order_datetime = order_datetime

    # Method to compute the total cost, discount, final cost, and reward
    def compute_cost(self, discount_rate=0):
        """Compute the original cost, discount, final cost, and reward."""
        # Calculate original cost
        original_cost = sum(product.get_price() * quantity for product, quantity in self.products)

        # Calculate discount
        discount = original_cost * (discount_rate / 100)

        # Calculate final cost after applying discount
        final_cost = original_cost - discount

        # Calculate rewards based on the final cost
        earned_rewards = round(final_cost * (self.guest.get_reward_rate() / 100))

        return original_cost, discount, final_cost, earned_rewards

    # Method to display the order information
    def display_order(self):
        """Displays the order summary"""
        original_cost, discount, final_cost, earned_rewards = self.compute_cost()
        print(f"\nOrder by Guest: {self.guest.get_name()}")
        print(f"Order Date and Time: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        for product, quantity in self.products:
            print(f"{quantity} x {product.get_name()} @ ${product.get_price()} each")
        print(f"Total Cost: ${original_cost:.2f} (AUD)")
        if discount > 0:
            print(f"Discount Applied: -${discount:.2f} (AUD)")
        print(f"Final Cost: ${final_cost:.2f} (AUD)")
        print(f"Earned Rewards: {earned_rewards} points")


# Bundle Class
class Bundle(Product):
    def __init__(self, bundle_id, name, components, price):
        """Constructor for the Bundle class"""
        super().__init__(bundle_id, name, price)
        self.components = components  # List of tuples (product, quantity)

    # Overriding display_info to show bundle details
    def display_info(self):
        print(f"Bundle ID: {self.product_id}")
        print(f"Bundle Name: {self.name}")
        component_str = ', '.join([f"{quantity} x {product.get_id()}" if quantity > 1 else f"{product.get_id()}"
                                   for product, quantity in self.components])
        print(f"Components: {component_str}")
        print(f"Total Price: ${self.price:.2f} (AUD)")

    # Method to calculate and set the bundle price as 80% of the total component prices
    def calculate_bundle_price(self):
        total_price = sum(product.get_price() * quantity for product, quantity in self.components)
        self.price = total_price * 0.8

    # Method to update the components of the bundle
    def update_components(self, new_components):
        """Updates the components of the bundle and recalculates the price"""
        self.components = new_components
        self.calculate_bundle_price()

    # Method to get the components of the bundle
    def get_components(self):
        """Returns the components of the bundle"""
        return self.components


# Records Class
class Records:
    def __init__(self):
        self.guests = []
        self.products = []
        self.orders = []

    def update_product(self, updated_product):
        """Updates an existing product in the product list."""
        for i, product in enumerate(self.products):
            if product.get_id() == updated_product.get_id():
                self.products[i] = updated_product
                return
        print(f"Product {updated_product.get_id()} not found. Cannot update.")


    def read_guests(self, file_name):
        try:
            with open(file_name, mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    guest_id, name, reward_rate, reward, redeem_rate = row
                    guest = Guest(guest_id, name, int(reward))
                    guest.set_reward_rate(int(reward_rate))
                    guest.set_redeem_rate(int(redeem_rate))
                    self.guests.append(guest)
        except FileNotFoundError:
            print(f"Error: {file_name} not found.")

    def read_products(self, file_name):
        try:
            with open(file_name, mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0].startswith('U'):
                        product_id, name, price, capacity = row
                        apartment = ApartmentUnit(product_id, name, float(price), int(capacity))
                        self.products.append(apartment)
                    elif row[0].startswith('SI'):
                        product_id, name, price = row
                        item = SupplementaryItem(product_id, name, float(price))
                        self.products.append(item)
                    elif row[0].startswith('B'):
                        bundle_id, name, *component_ids, price = row
                        components = []
                        component_count = {}

                        # Count each component in the bundle
                        for component_id in component_ids[:-1]:
                            if component_id in component_count:
                                component_count[component_id] += 1
                            else:
                                component_count[component_id] = 1
                                
                        # Find and add each component to the bundle
                        for component_id, quantity in component_count.items():
                            product = self.find_product(component_id)
                            if product:
                                components.append((product, quantity))

                        # Create the bundle with the discounted price
                        bundle = Bundle(bundle_id, name, components, float(price))
                        self.products.append(bundle)
        except FileNotFoundError:
            print(f"Error: {file_name} not found.")

    def find_guest(self, search_value):
        search_value = search_value.strip().lower()
        for guest in self.guests:
            if guest.get_id().lower() == search_value or guest.get_name().strip().lower() == search_value:
                return guest
        return None

    def find_product(self, search_value):
        search_value = search_value.strip().lower()
        for product in self.products:
            if product.get_id().lower() == search_value or product.get_name().strip().lower() == search_value:
                return product
        return None

    def add_order(self, order):
        self.orders.append(order)

    def list_guests(self):
        for guest in self.guests:
            guest.display_info()

    def list_products(self, product_type=None):
        if product_type == "apartment":
            print("\n=== Apartment Units ===")
            for product in self.products:
                if isinstance(product, ApartmentUnit):
                    product.display_info()
        elif product_type == "supplementary":
            print("\n=== Supplementary Items ===")
            for product in self.products:
                if isinstance(product, SupplementaryItem):
                    product.display_info()
        elif product_type is None:
            print("\n=== Products and Bundles ===")
            for product in self.products:
                if isinstance(product, Bundle):
                    product.display_info()
                else:
                    product.display_info()

    def save_orders_to_csv(self, file_name="orders.csv"):
        try:
            with open(file_name, mode='w', newline='') as file:
                writer = csv.writer(file)
                for order in self.orders:
                    order_data = [order.guest.get_name()] + [f"{quantity} x {product.get_id()}" for product, quantity in order.products]
                    total_cost, discount, final_cost, earned_rewards = order.compute_cost()
                    order_data.append(f"{final_cost:.2f}")
                    order_data.append(str(earned_rewards))
                    order_data.append(datetime.now().strftime("%d/%m/%Y %H:%M"))
                    writer.writerow(order_data)
            print(f"Orders saved to {file_name}")
        except Exception as e:
            print(f"Error saving orders: {e}")

    def read_orders(self, file_name):
        """Reads orders from the orders CSV file and adds them to the orders list."""
        try:
            with open(file_name, mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    guest_name = row[0]
                    guest = self.find_guest(guest_name)

                    # Parse products
                    products = []
                    for item in row[1:-3]:
                        try:
                            # Adjusted to allow for no space between quantity and 'x'
                            if 'x' in item:
                                parts = item.split('x')
                                quantity = parts[0].strip()
                                product_id = parts[1].strip()
                                product = self.find_product(product_id)
                                if product:
                                    products.append((product, int(quantity)))
                                else:
                                    print(f"Product {product_id} not found.")
                            else:
                                print(f"Error parsing product info: '{item}'. Expected format 'quantity x product_id'.")
                                continue  # Skip this item if not formatted correctly
                        except ValueError:
                            print(f"Error parsing product info: '{item}'.")
                            continue  # Skip this item and continue with the next one

                    # Retrieve total cost and earned rewards
                    total_cost = float(row[-3])
                    earned_rewards = int(row[-2])

                    # Strip any leading/trailing spaces from the date string
                    order_datetime_str = row[-1].strip()
                    order_datetime = datetime.strptime(order_datetime_str, "%d/%m/%Y %H:%M")

                    # Create and add the order
                    order = Order(guest, products, total_cost, earned_rewards, order_datetime)
                    self.orders.append(order)

        except FileNotFoundError:
            print(f"Cannot load the order file: {file_name}")
        except Exception as e:
            print(f"Error loading orders: {e}")

    def generate_statistics(self):
        guest_totals = {}
        product_totals = {}

        # Calculate total spending per guest and total quantity of each product
        for order in self.orders:
            guest_name = order.guest.get_name()
            total_cost, discount, final_cost, earned_rewards = order.compute_cost()

            if guest_name in guest_totals:
                guest_totals[guest_name] += final_cost
            else:
                guest_totals[guest_name] = final_cost

            for product, quantity in order.products:
                product_name = product.get_name()
                if product_name in product_totals:
                    product_totals[product_name] += quantity
                else:
                    product_totals[product_name] = quantity

        # Get top 3 most valuable guests
        top_guests = sorted(guest_totals.items(), key=lambda x: x[1], reverse=True)[:3]

        # Get top 3 most popular products
        top_products = sorted(product_totals.items(), key=lambda x: x[1], reverse=True)[:3]

        # Display the statistics
        print("\n=== Statistics ===")
        print("Top 3 Most Valuable Guests:")
        for guest, total in top_guests:
            print(f"{guest}: ${total:.2f}")

        print("\nTop 3 Most Popular Products:")
        for product, quantity in top_products:
            print(f"{product}: {quantity} units")

        # Save the statistics to a text file
        with open("stats.txt", mode='w') as file:
            file.write("Top 3 Most Valuable Guests:\n")
            for guest, total in top_guests:
                file.write(f"{guest}: ${total:.2f}\n")

            file.write("\nTop 3 Most Popular Products:\n")
            for product, quantity in top_products:
                file.write(f"{product}: {quantity} units\n")
        print("\nStatistics saved to stats.txt")

# Operations Class
class Operations:
    def __init__(self, records):
        """Constructor for Operations class"""
        self.records = records  # Instance of Records class

    def start_program(self):
        """Checks for CSV files and loads data before showing the menu."""
        guest_file = "guests.csv"
        product_file = "products.csv"
        order_file = "orders.csv"

        # Check for command-line arguments for file names
        if len(sys.argv) >= 3:
            guest_file = sys.argv[1]
            product_file = sys.argv[2]
            if len(sys.argv) == 4:
                order_file = sys.argv[3]

        try:
            self.records.read_guests(guest_file)
            self.records.read_products(product_file)
            self.records.read_orders(order_file)  # Load previous orders
            print("Data loaded successfully.")
            self.display_menu()
        except Exception as e:
            print(f"Error loading files: {e}")
            print("Exiting program...")

    def display_menu(self):
        """Displays the menu and handles user input."""
        while True:
            print("\n=== Pythonia Apartment Booking System ===")
            print("1. Make a booking")
            print("2. Display existing guests")
            print("3. Display existing apartment units")
            print("4. Display existing supplementary items")
            print("5. Display all products and bundles")
            print("6. Add/Update apartment units")
            print("7. Add/Update supplementary items")
            print("8. Add/Update bundle products")
            print("9. Adjust reward rate of all guests")
            print("10. Adjust redeem rate of all guests")
            print("11. Display all orders")
            print("12. Generate key statistics")
            print("13. Display guest order history")
            print("14. Exit")
            choice = input("Choose an option: ")

            if choice == "1":
                self.make_booking()
            elif choice == "2":
                self.records.list_guests()
            elif choice == "3":
                self.records.list_products("apartment")
            elif choice == "4":
                self.records.list_products("supplementary")
            elif choice == "5":
                self.records.list_products()  # Show all products including bundles
            elif choice == "6":
                self.add_update_apartment()
            elif choice == "7":
                self.add_update_supplementary_item()
            elif choice == "8":
                self.add_update_bundle()
            elif choice == "9":
                self.adjust_reward_rate()
            elif choice == "10":
                self.adjust_redeem_rate()
            elif choice == "11":
                self.display_orders()
            elif choice == "12":
                self.records.generate_statistics()
            elif choice == "13":
                self.display_guest_order_history()
            elif choice == "14":
                print("Exiting program...")
                break
            else:
                print("Invalid option. Please try again.")

    # Method to make a booking
    def make_booking(self):
        """Handles the process of making a booking for a guest with multiple products."""
        while True:
            guest_name_or_id = input("Enter guest name or ID: ").strip()
            guest = self.records.find_guest(guest_name_or_id)
            if not guest:
                print("Guest not found. Adding new guest.")
                while True:
                    try:
                        guest_id = int(input("Enter guest ID (number): ").strip())
                        break
                    except ValueError:
                        print("Invalid input. Guest ID should be a number.")
                while True:
                    guest_name = input("Enter guest name: ").strip()
                    if guest_name.isalpha():
                        break
                    else:
                        print("Invalid input. Guest name should contain only alphabetic characters.")
                while True:
                    try:
                        reward_points = int(input("Enter initial reward points: "))
                        if reward_points >= 0:
                            break
                        else:
                            print("Reward points must be a non-negative integer.")
                    except ValueError:
                        print("Invalid input. Please enter a valid number for reward points.")
                guest = Guest(guest_id, guest_name, reward_points)
                self.records.guests.append(guest)
                print(f"New guest {guest_name} added successfully with ID {guest_id}.")
                break
            else:
                print(f"Welcome back, {guest.get_name()}.")
                guest.display_info()
                break

        # Date validation for check-in and check-out
        booking_datetime = datetime.now()
        booking_date = booking_datetime.date()

        while True:
            try:
                checkin_date_str = input("Enter check-in date (DD/MM/YYYY): ")
                checkout_date_str = input("Enter check-out date (DD/MM/YYYY): ")
                
                checkin_date = datetime.strptime(checkin_date_str, "%d/%m/%Y").date()
                checkout_date = datetime.strptime(checkout_date_str, "%d/%m/%Y").date()
                
                current_date = datetime.now().date()  # Get the current date
                
                if checkin_date < current_date:
                    raise DateDiscrepancyError("Check-in date cannot be earlier than today.")
                
                if checkout_date <= checkin_date:
                    raise DateDiscrepancyError("Check-out date must be after the check-in date.")
                
                break  # If no exceptions, break the loop
                
            except ValueError:
                print("Invalid date format. Please enter the date in DD/MM/YYYY format.")
            except DateDiscrepancyError as e:
                print(e)

        num_guests = int(input("Enter the number of guests: "))
        apartment_id = input("Enter the apartment ID: ").strip()
        apartment = self.records.find_product(apartment_id)
        length_of_stay = (checkout_date - checkin_date).days
        total_cost = apartment.get_price() * length_of_stay

        products = [(apartment, length_of_stay)]

        if num_guests > apartment.get_capacity():
            extra_beds_needed = num_guests - apartment.get_capacity()
            extra_bed_quantity = extra_beds_needed
            while True:
                extra_bed_id = input("Enter the extra bed product ID: ").strip()
                extra_bed = self.records.find_product(extra_bed_id)
                if not extra_bed or not isinstance(extra_bed, SupplementaryItem):
                    print("Invalid extra bed ID. Please try again.")
                else:
                    products.append((extra_bed, extra_bed_quantity))
                    print(f"Added {extra_bed_quantity} extra beds for ${extra_bed.get_price() * extra_bed_quantity:.2f}.")
                    break

        need_car_park = input("Do you need a car park? (yes/no): ").strip().lower()
        if need_car_park == "yes":
            while True:
                car_park_id = input("Enter the car park product ID: ").strip()
                car_park = self.records.find_product(car_park_id)
                if not car_park or not isinstance(car_park, SupplementaryItem):
                    print("Invalid car park ID. Please try again.")
                else:
                    car_park_quantity = int(input(f"Enter quantity of car parks (minimum: {length_of_stay}): "))
                    if car_park_quantity < length_of_stay:
                        car_park_quantity = length_of_stay
                    products.append((car_park, car_park_quantity))
                    print(f"Added {car_park_quantity} car parks for ${car_park.get_price() * car_park_quantity:.2f}.")
                    break

        add_more_items = input("Do you want to add more supplementary items? (yes/no): ").strip().lower()
        while add_more_items == "yes":
            supplementary_item_id = input("Enter the supplementary item ID: ").strip()
            supplementary_item = self.records.find_product(supplementary_item_id)
            if not supplementary_item or not isinstance(supplementary_item, SupplementaryItem):
                print("Invalid supplementary item ID. Please try again.")
            else:
                supplementary_quantity = int(input(f"Enter quantity of {supplementary_item.get_name()}: "))
                products.append((supplementary_item, supplementary_quantity))
                print(f"Added {supplementary_quantity} x {supplementary_item.get_name()} for ${supplementary_item.get_price() * supplementary_quantity:.2f}.")
            add_more_items = input("Do you want to add more supplementary items? (yes/no): ").strip().lower()

        order = Order(guest, products, total_cost, guest.get_reward(), booking_datetime)
        self.records.add_order(order)
        order.display_order()

        redeem = input("Redeem reward points? (yes/no): ").strip().lower()
        discount = 0
        if redeem == "yes" and guest.get_reward() >= 100:
            redeem_points = guest.get_reward()
            discount = redeem_points // 100  # $1 for every 100 points
            guest.update_reward(-redeem_points)
            print(f"Redeemed {redeem_points} points for a ${discount:.2f} discount.")

        final_cost = order.compute_cost(discount)[2]
        guest.update_reward(round(final_cost))
        print(f"Final Total Cost After Discount: ${final_cost:.2f}")
        print(f"Earned Rewards: {round(final_cost)} points")

    # Display all orders
    def display_orders(self):
        """Displays all the orders that have been made."""
        if not self.records.orders:
            print("No orders available.")
        else:
            for i, order in enumerate(self.records.orders, 1):
                print(f"\nOrder {i}:")
                order.display_order()

    # Add/Update apartment units
    def add_update_apartment(self):
        """Adds or updates an apartment unit."""
        apartment_id = input("Enter the apartment ID: ").strip()
        existing_apartment = self.records.find_product(apartment_id)

        if existing_apartment and isinstance(existing_apartment, ApartmentUnit):
            print(f"Updating apartment {existing_apartment.get_name()}.")
        else:
            print("Adding a new apartment.")

        name = input("Enter apartment name: ").strip()
        price = float(input("Enter price per night: "))
        capacity = int(input("Enter capacity: "))

        apartment = ApartmentUnit(apartment_id, name, price, capacity)
        if existing_apartment:
            self.records.update_product(apartment)
        else:
            self.records.add_product(apartment)

        print(f"Apartment {name} successfully added/updated.")

    # Add/Update supplementary items
    def add_update_supplementary_item(self):
        """Adds or updates a supplementary item."""
        item_id = input("Enter the supplementary item ID: ").strip()
        existing_item = self.records.find_product(item_id)

        if existing_item and isinstance(existing_item, SupplementaryItem):
            print(f"Updating supplementary item {existing_item.get_name()}.")
        else:
            print("Adding a new supplementary item.")

        name = input("Enter item name: ").strip()
        price = float(input("Enter price: "))

        item = SupplementaryItem(item_id, name, price)
        if existing_item:
            self.records.update_product(item)
        else:
            self.records.add_product(item)

        print(f"Supplementary item {name} successfully added/updated.")

    # Add/Update bundles
    def add_update_bundle(self):
        """Adds or updates a bundle product."""
        bundle_id = input("Enter the bundle ID: ").strip()
        existing_bundle = self.records.find_product(bundle_id)

        if existing_bundle and isinstance(existing_bundle, Bundle):
            print(f"Updating bundle {existing_bundle.get_name()}.")
        else:
            print("Adding a new bundle.")

        name = input("Enter bundle name: ").strip()
        component_ids = input("Enter product IDs for the bundle (comma-separated): ").split(",")
        components = []
        total_price = 0

        for component_id in component_ids:
            product = self.records.find_product(component_id.strip())
            if product:
                quantity = component_ids.count(component_id.strip())  # Get the quantity
                components.append((product, quantity))
                total_price += product.get_price() * quantity
            else:
                print(f"Product {component_id.strip()} not found. Skipping.")

        bundle_price = 0.8 * total_price  # 80% of the total price of components
        bundle = Bundle(bundle_id, name, components, bundle_price)

        if existing_bundle:
            self.records.update_product(bundle)
        else:
            self.records.add_product(bundle)

        print(f"Bundle {name} successfully added/updated.")

    # Adjust reward rate for all guests
    def adjust_reward_rate(self):
        """Adjusts the reward rate for all guests."""
        while True:
            try:
                new_rate = float(input("Enter the new reward rate (%): "))
                if new_rate <= 0:
                    raise ValueError("Reward rate must be positive.")
                break
            except ValueError as e:
                print(f"Invalid input: {e}. Please try again.")

        for guest in self.records.guests:
            guest.set_reward_rate(new_rate)

        print(f"Reward rate updated to {new_rate}% for all guests.")

    # Method to display the guest order history
    def display_guest_order_history(self):
        """Displays the order history of a specific guest."""
        guest_name_or_id = input("Enter guest name or ID: ").strip()
        guest = self.records.find_guest(guest_name_or_id)

        if not guest:
            print(f"No guest found with name/ID '{guest_name_or_id}'.")
            return

        guest_orders = [order for order in self.records.orders if order.guest == guest]

        if not guest_orders:
            print(f"No order history found for guest '{guest.get_name()}'.")
        else:
            print(f"\nOrder history for guest: {guest.get_name()}")
            print(f"{'Order ID':<10} {'Products Ordered':<30} {'Total Cost':<15} {'Earned Rewards':<15}")
            print("-" * 70)
            
            for i, order in enumerate(guest_orders, 1):
                product_summary = ', '.join([f"{quantity} x {product.get_name()}" for product, quantity in order.products])
                total_cost, _, final_cost, earned_rewards = order.compute_cost()
                print(f"{i:<10} {product_summary:<30} {final_cost:<15.2f} {earned_rewards:<15}")

    # Adjust redeem rate for all guests
    def adjust_redeem_rate(self):
        """Adjusts the redeem rate for all guests."""
        while True:
            try:
                new_rate = float(input("Enter the new redeem rate (%): "))
                if new_rate < 1:
                    raise ValueError("Redeem rate must be greater than 1%.")
                break
            except ValueError as e:
                print(f"Invalid input: {e}. Please try again.")

        for guest in self.records.guests:
            guest.set_redeem_rate(new_rate)

        print(f"Redeem rate updated to {new_rate}% for all guests.")

    # Display the booking receipt
    def display_booking_receipt(self, guest, products, total_cost, discount, final_cost, booking_datetime, length_of_stay, extra_beds_needed, car_park_quantity, supplementary_items=[]):
        """Displays a booking receipt with all details."""
        print("\n=== Booking Receipt ===")
        print(f"Guest Name: {guest.get_name()}")
        print(f"Number of Guests: {len(products)}")
        print(f"Apartment/Bundle Name: {products[0][0].get_name()}")
        print(f"Apartment/Bundle Rate: ${products[0][0].get_price():.2f} per night")
        print(f"Check-in Date: {booking_datetime.strftime('%d/%m/%Y')}")
        print(f"Check-out Date: {(booking_datetime + timedelta(days=length_of_stay)).strftime('%d/%m/%Y')}")
        print(f"Length of Stay: {length_of_stay} nights")
        print(f"Booking Date and Time: {booking_datetime.strftime('%d/%m/%Y %H:%M')}")
        print(f"Sub-total for Apartment/Bundle: ${total_cost:.2f}")

        # List supplementary items in the receipt
        if len(supplementary_items) > 0:
            print("Supplementary Items:")
            for supplementary_item, supplementary_quantity in supplementary_items:
                supplementary_cost = supplementary_item.get_price() * supplementary_quantity
                print(f"{supplementary_item.get_id()} {supplementary_item.get_name()} x{supplementary_quantity} @ ${supplementary_item.get_price():.2f} = ${supplementary_cost:.2f}")

        # Display additional costs for extra beds and car parks if applicable
        if extra_beds_needed > 0:
            extra_bed_cost = products[1][0].get_price() * extra_beds_needed
            print(f"Extra Beds: {extra_beds_needed} beds for {length_of_stay} nights @ ${products[1][0].get_price():.2f} per bed = ${extra_bed_cost:.2f}")

        if car_park_quantity > 0:
            car_park_cost = products[-1][0].get_price() * car_park_quantity
            print(f"Car Parks: {car_park_quantity} parks for {length_of_stay} nights @ ${products[-1][0].get_price():.2f} per park = ${car_park_cost:.2f}")

        # Display total cost summary and discount if any
        print(f"Total Cost Before Discount: ${total_cost:.2f}")
        if discount > 0:
            print(f"Reward Points Redeemed: {discount // 100}")
            print(f"Discount Applied: -${discount:.2f}")
        print(f"Final Total Cost After Discount: ${final_cost:.2f}")
        print(f"Earned Rewards: {round(final_cost)} points")
        print("Thank you for your booking! We hope you enjoy your stay.\n")

if __name__ == "__main__":
    records = Records()
    operations = Operations(records)
    operations.start_program()


