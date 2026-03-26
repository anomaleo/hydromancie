import threading
import time

def background_task():
    print("Task started...")
    time.sleep(3) # Simulate a long operation
    print("Task finished.")


# HYDROMANIC MAIN ENTRY 
if __name__ == "__main__":
# Create a new thread
    thread = threading.Thread(target=background_task)

# Start the thread
    thread.start()

# Wait for the background thread to complete
    thread.join()

    print("Main thread continues after the background task is done.")
