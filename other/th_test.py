import threading, time

def generate_geojson():
    while True:
        print("Hi!")
        time.sleep(10)
        # Code to fetch data and write to vehicles.geojson
        pass  # Replace with actual logic

thread = threading.Thread(target=generate_geojson, daemon=True)
thread.start()
