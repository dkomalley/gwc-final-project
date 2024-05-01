import pandas as pd
from datetime import datetime
import csv
import argparse
from random import shuffle

"""  A music library enabling users to manage songs, playlists, and perform 
        various functions using implemented code structures, supported by 
        CSV data storage. """

class Playlist:
    """Represents the music library where users can create their own playlist.
    """
    
    def __init__(self, filepath):
        self.filepath = filepath
        self.now_playing_song = None
        
    
    def upload_song(self, song_title, artist, genre, \
            duration=None, release=None):
        """Uploads song details to a playlist in an iPod represented by a CSV
            file using Pandas.

        Args:
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
            
        try:
            duration_seconds = int(duration.split(':')[0]) * 60 + \
                int(duration.split(':')[1]) if duration and ':' in duration \
                    else None
        except ValueError:
            print("Invalid duration format. Please use 'mm:ss'.")
            return False
            
        try:
            existing_data = pd.read_csv(self.filepath)
        except FileNotFoundError:
            print("Error: File not found.")
            return False
        
        new_song_data = [song_title, artist, genre, \
                duration_seconds, release]
        new_song_df = pd.DataFrame([new_song_data], \
                columns=existing_data.columns)
            
        updated_data = pd.concat([existing_data, new_song_df], \
                ignore_index=True)
        updated_data['Release'] = pd.to_datetime(updated_data['Release'])
            
        try:
            updated_data.to_csv(self.filepath, index=False)
            self.new_data = updated_data
            return True
        
        except Exception as e:
            print(f"Error uploading song: {e}")
            return False
    
    
    def view_all_songs(self, order = "Recently Added"):
        """Returns all of the user's added songs in a specified order.
        
        Args:
            order(str): the sort order to return the songs; 
                    default is set to 'Recently Added'.
            
        Returns:
            list: list of all added songs according to specified order.
        """
               
        title = []
        artist = []
        genre = []
        duration = []
        release = []
        for line in f:
            
            data = line.strip().split(", ")
            title.append(data[0])
            artist.append(data[1])
            genre.append(data[2])
            duration.append(data[3])
            release.append(data[-1])
            
        dict = {'Title': title, 'Artist': artist, \
                'Genre': genre, 'Duration': duration, \
                'Release': release}
        df = pd.DataFrame(dict)

        if order == "Recently Added":
            recent = df.sort_index(ascending = False)
            return recent['Title']
        elif order == "Alphabetical":
            alpha = df.sort_values('Title')
            return alpha['Title']
        elif order == "Release Year":
            release = df.sort_values('Release')
            
            return release["Title"]
                   
        
                  
    def delete_songs(self, song_title):
        """Deletes songs off a playlist and returns the updated playlist.

        Args:
            song_title (string): name of song
        
        Returns:
            list: list of all songs on the playlist excluding the deleted songs
        """
        updated_playlist = []
        song_found = False
        with open(self.filepath, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                #to account for double quotes in csv file
                csv_song_title = row[0].strip().replace('“', '').replace('”', '').replace('"', '').lower()
                input_song_title = song_title.strip().replace('“', '').replace('”', '').replace('"', '').lower()
                if csv_song_title != input_song_title:
                    updated_playlist.append(row)
                else:
                    song_found = True

        if song_found:
            print(f"'{song_title}' found and deleted.")
        else:
            print(f"'{song_title}' not found in the playlist.")

        with open(self.filepath, mode='w', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(updated_playlist)

        return updated_playlist

    def search_by_artist(filepath, user_artist):
            """Function where the user can enter an artist's name and it will return
            every song by that artist that is downloaded on the iPod.
            
            Args:
            user_artist(str)

            Returns:
            songs_by_artist(list)
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

    def shuffle_songs(filepath):
        """A method that will take a playlist from a file and shuffle the order of the songs.

        Args:
            filepath (str): the name of the filepath with the songs that need to 
            be shuffled. 
        Returns:
            list: returns a list of the songs in the filepath shuffled, using 
            the shuffle function from the random module.
        """
        shuffled_songs = []
        with open(filepath, "r") as f:
            for line in f:
                songs = line.strip().split(',')
                song = songs[0]
                shuffled_songs.append(song)
        
        shuffle(shuffled_songs)    
        return shuffled_songs

    shuffle_songs("songs.csv")

def main():
    parser = argparse.ArgumentParser(description="Deletes a song from a playlist.")
    parser.add_argument("song_title", help="The title of the song to delete.")
    parser.add_argument("--filepath", default="playlist.csv", help="The path to the playlist CSV file.")
    args = parser.parse_args()

    playlist_manager = Playlist(args.filepath)
    updated_playlist = playlist_manager.delete_songs(args.song_title)

    print(f"Updated playlist after deleting \"{args.song_title}\":")
    for song in updated_playlist:
        print(song)
             
    

if __name__ == "__main__":
    main()