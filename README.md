import random
import time
import datetime
import json

class ShopSense:
    def __init__(self, location_name):
        self.location_name = location_name
        self.current_occupancy = 0
        self.history = []

    def update_occupancy(self):
        # Simulate data from thermal/silhouette sensors
        new_occupancy = random.randint(0, 50)
        self.current_occupancy = new_occupancy
        self.history.append({"timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "occupancy": new_occupancy})

    def get_live_count(self):
        return self.current_occupancy

    def is_good_time_to_visit(self):
        # Simulate a threshold for a "good" time to visit
        return self.current_occupancy < 20

    def get_history(self):
        return self.history

    def save_history_to_file(self):
        filename = f"{self.location_name}_history.json"
        with open(filename, "w") as file:
            json.dump(self.history, file)
        return filename

def display_menu():
    print("\nBON/ShopSense - Real-time Occupancy Information")
    print("1. Get Live Count")
    print("2. Check if it's a Good Time to Visit")
    print("3. Manual Update")
    print("4. View Occupancy History")
    print("5. Save Occupancy History to File")
    print("6. Exit")

def main():
    dmv = ShopSense("DMV")

    while True:
        display_menu()
        choice = input("Select an option (1-6): ")

        try:
            if choice == "1":
                print(f"Live count at {dmv.location_name}: {dmv.get_live_count()} people")
            elif choice == "2":
                if dmv.is_good_time_to_visit():
                    print("It's a good time to visit!")
                else:
                    print("It might be crowded. Consider waiting for a better time.")
            elif choice == "3":
                dmv.update_occupancy()
                print("Manual update completed.")
            elif choice == "4":
                history = dmv.get_history()
                for entry in history:
                    print(f"{entry['timestamp']} - Occupancy: {entry['occupancy']}")
            elif choice == "5":
                filename = dmv.save_history_to_file()
                print(f"Occupancy history saved to file: {filename}")
            elif choice == "6":
                print("Exiting BON/ShopSense. Thank you!")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 6.")
        except Exception as e:
            print(f"An error occurred: {e}")

        # Simulate a delay between updates
        time.sleep(60)

if __name__ == "__main__":
    main()


