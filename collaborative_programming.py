import pandas as pd
from datetime import datetime

"""  A music library enabling users to manage songs, playlists, and perform 
        various functions using implemented code structures, supported by 
        CSV data storage. """

class Playlist:
    """ Represents the music library where users can create their own playlist.
    
    Attributes:
        song ():
        playlist_name ():
        sort_by ():
    """
    def shuffle_playlist(self, playlist):
        """A method that will take a playlist and shuffle the order of the songs.

        Args:
            playlist (list): a list of songs that are in a playlist.
        """
    def search_by_artist(filepath, user_artist):
        """function where the user can enter an artist's name and it will return
        every song by that artist that is downloaded on the iPod 
        
        Args:
        artist(str)

        Returns:
        artist_songs(list)
        """
        
        songs_by_artist = []
        with open(filepath, "r", encoding = "utf-8") as f:
            for line in f:
                songs = line.strip().split(",")
                artist = songs[1]
                if user_artist in songs[1]:
                    songs_by_artist.append(songs[0])
                    
            if user_artist not in songs[1]:
                    print(f"There are no songs by {user_artist} downloaded.")
        return songs_by_artist
        
    search_by_artist("songs.csv", "Justin Bieber")
    
    def view_all_songs(self, order = "Recently Added"):
        """Returns all of the user's added songs in a specified order.
        
        Args:
            order(str): the sort order to return the songs; 
                    default is set to 'Recently Added'.
            
        Returns:
            list: list of all added songs according to specified order.
        """
    
    def uploadSong(self, filepath, song_title, artist, genre, \
            duration=None, release=None):
        """Uploads song details to a playlist in an iPod represented by a CSV
            file using Pandas.

        Args:
            filepath (str): the path to the CSV file representing the playlist.
            song_title (str): the title of the song.
            artist (str): the artist of the song.
            genre (str): the genre of the song.
            duration (str, optional): the duration of the song in the 
                format 'mm:ss'. Defaults to None.
            release (str, optional): the release date of the song. Defaults 
                to None.

        Returns:
            bool: True if the song details were sucessfully uploaded, and False
                otherwise.
                
        Side effects:
            modifies the CSV file specified by filepath to include details of 
                the uploaded song.
            if duration is provided and in the format 'mm:ss', it calculates 
                the duration in seconds and updates the duration_seconds 
                variable accordingly.
            if an error occurs during the upload process, it prints and error 
                message.
        """
            
        duration_seconds = None
        if duration:
            if ':' in duration:
                try:
                    minutes, seconds = [int(part) for part in \
                        duration.split(':')]
                    duration_seconds = minutes * 60 + seconds
                except ValueError:
                    pass
            else:
                pass
            
        try:
            existing_data = pd.read_csv(filepath)
            
            new_song_information = pd.DataFrame([[song_title, artist, genre, \
                duration_seconds, release]], columns = ["Song Title", \
                    "Artist", "Genre", "Duration", "Release"])
            
            updated_data = pd.concat([existing_data, new_song_information], \
                ignore_index=True)
            
            updated_data.to_csv(filepath, index=False)
            return True
        except Exception as e:
            print(f"Error uploading song: {e}")
            return False
        
    # Example:
    def upload_song_to_playlist(self):
        playlist = Playlist()
        
        song_title = "Stereo Love (Radio Edit)"
        artist = "Edward Maya & Vika Jigulina"
        genre = "Dance"
        duration = "185"
        release = datetime.now().date()
        
        confirmation_message = playlist.uploadSong("songs.csv", song_title, \
            artist, genre, duration, release)
        
        print(confirmation_message)
        
        
    def delete_songs(self,song_title):
        """Deletes songs off a playlist and returns the updated playlist.

        Args:
            song_title (string): name of song
        
        Returns:
            list: list of all songs on the playlist excluding the deleted songs
        """
        
        