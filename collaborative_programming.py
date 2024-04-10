import csv
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
        """function where the user can enter an artist's name and it will return every song by that artist that is downloaded on the iPod 
        
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
    
    def uploadSong(self, filepath, song_title, artist, genre, duration=None, release=None):
        if not release:
            release = datetime.now().strftime('%Y-%m-%d')
            
        if duration and ':' in duration:
            parts = duration.split(':')
            minutes = int(parts[0])
            seconds = int(parts[1])
            duration_seconds = minutes * 60 + seconds
        else:
            duration_seconds = duration
            
        try:
            with open(filepath, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([song_title, artist, genre, duration_seconds, release])
            return True
        except Exception as e:
            print(f"Error uploading song: {e}")
            return False
            
        
    
    def delete_songs(self,song_title):
        """Deletes songs off a playlist and returns the updated playlist.

        Args:
            song_title (string): name of song
        
        Returns:
            list: list of all songs on the playlist excluding the deleted songs
        """
        
        