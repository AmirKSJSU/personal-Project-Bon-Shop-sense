import random
import time
import datetime
import sqlite3


class Sensor:
    """Simulates a single sensor with specific accuracy and range."""

    def __init__(self, sensor_type, max_count=50):
        self.sensor_type = sensor_type
        self.max_count = max_count

    def get_reading(self):
        """Generate a simulated reading for the sensor."""
        
        noise = random.randint(-3, 3)
        return max(0, random.randint(0, self.max_count) + noise)


class ShopSense:
    """Main system for occupancy monitoring at a single location."""

    def __init__(self, location_name):
        self.location_name = location_name
        self.sensors = [
            Sensor("thermal"),
            Sensor("silhouette"),
            Sensor("infrared"),
        ]
        self.current_occupancy = 0
        self.conn = sqlite3.connect(f"{location_name}_occupancy.db")
        self.create_table()

    def create_table(self):
        """Create a table for storing occupancy history."""
        with self.conn:
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS occupancy_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    occupancy INTEGER NOT NULL,
                    location TEXT NOT NULL,
                    peak_hour BOOLEAN
                )
                """
            )

    def update_occupancy(self):
        """Update occupancy using data from multiple sensors."""
        readings = [sensor.get_reading() for sensor in self.sensors]
        
        self.current_occupancy = int(sum(readings) / len(readings))
        peak_hour = self.is_peak_hour()
        with self.conn:
            self.conn.execute(
                """
                INSERT INTO occupancy_history (timestamp, occupancy, location, peak_hour)
                VALUES (?, ?, ?, ?)
                """,
                (
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    self.current_occupancy,
                    self.location_name,
                    peak_hour,
                ),
            )

    def get_live_count(self):
        """Return the current occupancy."""
        return self.current_occupancy

    def is_good_time_to_visit(self):
        """Determine if it's a good time to visit based on occupancy threshold."""
        return self.current_occupancy < 20

    def is_peak_hour(self):
        """Simulate peak hour determination based on the time of day."""
        now = datetime.datetime.now()
        return 12 <= now.hour < 14 or 17 <= now.hour < 19

    def get_history(self):
        """Retrieve occupancy history from the database."""
        with self.conn:
            return self.conn.execute(
                "SELECT timestamp, occupancy, peak_hour FROM occupancy_history WHERE location = ?",
                (self.location_name,),
            ).fetchall()

    def save_history_to_file(self):
        """Save occupancy history to a CSV file."""
        history = self.get_history()
        filename = f"{self.location_name}_history.csv"
        with open(filename, "w") as file:
            file.write("timestamp,occupancy,peak_hour\n")
            for entry in history:
                file.write(f"{entry[0]},{entry[1]},{entry[2]}\n")
        return filename

    def __del__(self):
        """Ensure the database connection is closed properly."""
        self.conn.close()


def display_menu(location_name):
    """Display the menu for user interaction."""
    print(f"\nBON/ShopSense - Real-time Occupancy Information for {location_name}")
    print("1. Get Live Count")
    print("2. Check if it's a Good Time to Visit")
    print("3. Manual Update")
    print("4. View Occupancy History")
    print("5. Save Occupancy History to File")
    print("6. Exit")


def main():
    
    locations = ["DMV", "Mall", "Airport"]
    shopsense_instances = {loc: ShopSense(loc) for loc in locations}

    print("Welcome to BON/ShopSense!")
    print("Available Locations:")
    for i, loc in enumerate(locations, start=1):
        print(f"{i}. {loc}")
    loc_choice = int(input("Select a location (1-3): "))
    location_name = locations[loc_choice - 1]
    shop = shopsense_instances[location_name]

    while True:
        display_menu(location_name)
        choice = input("Select an option (1-6): ")

        try:
            if choice == "1":
                print(f"Live count at {location_name}: {shop.get_live_count()} people")
            elif choice == "2":
                if shop.is_good_time_to_visit():
                    print("It's a good time to visit!")
                else:
                    print("It might be crowded. Consider waiting for a better time.")
            elif choice == "3":
                shop.update_occupancy()
                print("Manual update completed.")
            elif choice == "4":
                history = shop.get_history()
                if history:
                    for entry in history:
                        peak_status = "Yes" if entry[2] else "No"
                        print(f"{entry[0]} - Occupancy: {entry[1]} (Peak Hour: {peak_status})")
                else:
                    print("No history data available.")
            elif choice == "5":
                filename = shop.save_history_to_file()
                print(f"Occupancy history saved to file: {filename}")
            elif choice == "6":
                print("Exiting BON/ShopSense. Thank you!")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 6.")
        except Exception as e:
            print(f"An error occurred: {e}")

        
        time.sleep(5)  


if __name__ == "__main__":
    main()


