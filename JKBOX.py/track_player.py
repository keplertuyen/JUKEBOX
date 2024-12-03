import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont
import webbrowser
import sv_ttk

# Import necessary modules for managing and updating the track library
from track_library import TrackLibrary
from create_track_list import AddTrackWindow
from create_track_list import FindTrackWindow
from update_track import RemoveTrackWindow
from update_track import UpdateTrackWindow

# Class to manage the "View Tracks" window
class ViewTracksWindow:
    def __init__(self, parent, library):
        # Initialize the window and set up the title and size
        self.window = tk.Toplevel(parent)
        self.window.title("View Tracks")
        self.window.geometry("600x200")
        self.library = library  # Store the library object
        sv_ttk.set_theme("dark")  # Set dark theme for the UI
        self.setup_gui()  # Set up the graphical user interface

    def setup_gui(self):
        # Create a treeview for displaying track data
        columns = ('Track', 'Artist', 'Rating', 'Play Count')
        self.track_tree = ttk.Treeview(self.window, columns=columns, show='headings')
        
        # Set column headings and adjust column widths
        for col in columns:
            self.track_tree.heading(col, text=col)
            self.track_tree.column(col, width=150)

        # Add a scrollbar for the treeview to handle long lists
        scrollbar = ttk.Scrollbar(self.window, orient=tk.VERTICAL, command=self.track_tree.yview)
        self.track_tree.configure(yscrollcommand=scrollbar.set)

        # Pack the treeview and scrollbar into the window
        self.track_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Bind double-click event to play the selected track
        self.track_tree.bind('<Double-1>', self.play_selected_track)
        
        # Load and display tracks in the treeview
        self.update_track_list()

    def update_track_list(self):
        # Clear any existing tracks in the list
        for item in self.track_tree.get_children():
            self.track_tree.delete(item)
        
        # Insert updated track data from the library into the treeview
        for track_id, track in self.library.tracks.items():
            self.track_tree.insert(
                '',
                'end',
                values=(track.name, track.artist, track.rating, track.play_count),
                tags=(track_id,)
            )

    def play_selected_track(self, event):
        # Get the track id of the selected item
        selected_item = self.track_tree.selection()[0]
        track_id = self.track_tree.item(selected_item, "tags")[0]
        track = self.library.tracks[track_id]
        
        # Increment the play count and update the list
        track.play_count += 1
        self.update_track_list()
        
        # Open the track's YouTube URL in the default browser
        webbrowser.open(track.youtube_url)

# Main application class to manage the Jukebox
class MainApplication:
    def __init__(self):
        self.root = tk.Tk()  # Initialize the root window for the app
        self.root.title("🎵 JukeBox")  # Set the title of the main window
        self.root.geometry("500x600")  # Set the size of the main window
        self.library = TrackLibrary()  # Initialize the track library
        
        # Try to load the track data from a file, handle errors if any
        try:
            self.library.load_from_file()
        except Exception as e:
            print(f"Error loading library: {e}")
            self.library.tracks = []  # Use an empty list if loading fails

        sv_ttk.set_theme("dark")  # Set dark theme for the UI
        self.setup_gui()  # Set up the GUI layout

    def setup_gui(self):
        # Define fonts for title and subtitle text
        title_font = tkfont.Font(family="Helvetica", size=20, weight="bold")
        subtitle_font = tkfont.Font(family="Helvetica", size=12)

        # Title frame setup
        title_frame = ttk.Frame(self.root)
        title_frame.pack(side="top", fill="x", pady=30)

        ttk.Label(
            title_frame, 
            text="JukeBoxxxxxx",  # Title label for the app
            font=("Comic Sans MS", 30),
            anchor="center"
        ).pack(expand=True)

        ttk.Label(
            title_frame,
            text="Select an option to manage your music library",  # Subtitle label
            font=("Comic Sans MS", 10),
            anchor="center"
        ).pack(expand=True)

        # Button frame to hold action buttons
        button_frame = ttk.Frame(self.root)
        button_frame.pack(expand=True, fill="both", padx=60, pady=20)

        # Define action buttons for the application
        buttons = [
            ("View Tracks", self.open_view_tracks),
            ("Add Track", self.open_add_track),
            ("Find Track", self.open_find_track),
            ("Remove Track", self.open_remove_track),
            ("Update Track", self.open_update_track)
        ]

        # Create and pack each button into the frame
        for text, command in buttons:
            btn = ttk.Button(
                button_frame,
                text=text,
                command=command,
                width=10  # Increased button width for better UI
            )
            btn.pack(pady=10, fill="x")  # Use pack layout with vertical spacing

        # Footer frame for exit button and status label
        footer_frame = ttk.Frame(self.root)
        footer_frame.pack(side="bottom", fill="x", pady=20)

        # Exit button setup
        ttk.Button(
            footer_frame,
            text="Exit",
            command=self.root.destroy,  # Close the app when clicked
            style="Accent.TButton"
        ).pack(anchor="center")

        # Status label at the bottom
        self.status_label = ttk.Label(
            footer_frame,
            text="Ready to rock your music library! 🎧",  # Display status
            font=("Comic Sans MS", 20)
        )
        self.status_label.pack(anchor="center", pady=(10,0))

    # Methods to open various windows for track management
    def open_view_tracks(self):
        ViewTracksWindow(self.root, self.library)

    def open_add_track(self):
        AddTrackWindow(self.root, self.library)

    def open_find_track(self):
        FindTrackWindow(self.root, self.library)

    def open_remove_track(self):
        RemoveTrackWindow(self.root, self.library)

    def open_update_track(self):
        # Opens the window for updating track details
        UpdateTrackWindow(self.root, self.library)

    # Run the main application loop
    def run(self):
        self.root.mainloop()

# If this script is run directly, start the main application
if __name__ == "__main__":
    app = MainApplication()
    app.run()
