import color_detector as cd
import threading
import time
import tkinter as tk

class ColorDetectorThread( threading.Thread ):

    def __init__( self, *args, **kwargs ):
        super(ColorDetectorThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()
        self._kill_event = threading.Event()
        self.target_color_rgb = None
        
    def unstop( self ):
        self._stop_event.clear()
        
    def stop( self ):
        self._stop_event.set()
    
    def stopped( self ):
        return self._stop_event.is_set()
    
    def kill( self ):
        self._kill_event.set()    
    
    def killed( self ):
        return self._kill_event.is_set()
    
    def run( self ):
        try:
        
            while not self.killed():
            
                if not self.stopped():
                    coordinates = cd.detect_color_in_screenshot(self.target_color_rgb, tolerance=0)
                    if len( coordinates ):
                        print( f"Detected color at screen coordinate: {coordinates}.", flush = True )
                        cd.simple_ping_windows()

                time.sleep( 3 )
            
        except Exception as e:
            print( e, flush=True )


def start_color_detection():
    thread.target_color_rgb = cd.hex_to_rgb( f"#{color_entry.get()}"  )  
    color_entry.config( state="disabled" )
    display_button.config( command = end_color_detection, text="Stop Detection" )
    
    if thread.is_alive():
        thread.unstop()
    else:
        thread.start()


def end_color_detection():
    display_button.config(command = start_color_detection, text="Start Detection")
    color_entry.config( state="normal" )
    thread.stop()

def on_closing():
    thread.kill()
    root.destroy()

hex_color_code = None  # Example hex color code for orange
target_color_rgb = None  # Example: detecting the color red (pure red in RGB format)    
thread = ColorDetectorThread()

# Create the main window
root = tk.Tk()
root.title("Hex Color Code Display")

# Create a label
label = tk.Label(root, text="Enter Hex Color Code:")
label.pack()

# Create an entry widget for input with margin
color_entry = tk.Entry(root)
color_entry.pack(padx=10, pady=5)  # Add padx and pady for margin

# Create a button to trigger the display function
display_button = tk.Button(root, text="Start Detection", command=start_color_detection)
display_button.pack()

# Start the GUI main loop
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()

