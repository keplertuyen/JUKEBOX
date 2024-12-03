import json  # This library is used to read and write data in JSON file format.

# The Track class: Represents a song with its associated metadata.
class Track:
    def __init__(self, name, artist, youtube_url, play_count=0, rating=0):
        # Initialize the Track object with details about the song.
        self.name = name  # Name of the track.
        self.artist = artist  # Name of the artist.
        self.youtube_url = youtube_url  # URL of the track on YouTube.
        self.play_count = play_count  # The number of times the track has been played.
        self.rating = rating  # User-assigned rating for the track.

    def to_dict(self):
        # Convert the Track object into a dictionary format suitable for JSON serialization.
        return {
            'name': self.name,
            'artist': self.artist,
            'youtube_url': self.youtube_url,
            'play_count': self.play_count,
            'rating': self.rating
        }

    @classmethod
    def from_dict(cls, data):
        # Create a Track object from a dictionary. Useful for deserialization.
        return cls(
            data['name'],  # Track name.
            data['artist'],  # Artist name.
            data['youtube_url'],  # YouTube URL.
            data['play_count'],  # Play count of the track.
            data['rating']  # Rating of the track.
        )

# The TrackLibrary class: Manages a collection of tracks and handles file operations.
class TrackLibrary:
    def __init__(self):
        self.tracks = {}  # A dictionary to store Track objects, keyed by track name.

    def save_to_file(self):
        # Save the current track library to a JSON file.
        with open('library.json', 'w') as f:
            # Convert each Track object to a dictionary for serialization.
            json_data = {k: v.to_dict() for k, v in self.tracks.items()}
            json.dump(json_data, f, indent=4)  # Write the JSON data to file with indentation for readability.

    def load_from_file(self):
        # Load the track library from a JSON file.
        try:
            with open('library.json', 'r') as f:
                # Read JSON data and convert it back to Track objects.
                data = json.load(f)
                self.tracks = {k: Track.from_dict(v) for k, v in data.items()}
        except FileNotFoundError:
            self.tracks = {}
