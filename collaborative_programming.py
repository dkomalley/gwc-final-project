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
    def search_by_artist(self, artist):
        """function where the user can enter an artist's name and it will return every song by that artist that is downloaded on the iPod 
        
        Args:
        artist(str)

        Returns:
        artist_songs(list)
        """

    def view_all_songs(self, order = "Recently Added"):
        """Returns all of the user's added songs in a specified order.
        
        Args:
            order(str): the sort order to return the songs; 
                    default is set to 'Recently Added'.
            
        Returns:
            list: list of all added songs according to specified order.
        """
    
    def delete_songs(self,song_title):
        """Deletes songs off a playlist and returns the updated playlist.

        Args:
            song_title (string): name of song
        
        Returns:
            list: list of all songs on the playlist excluding the deleted songs
        """