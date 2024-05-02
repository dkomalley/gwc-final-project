import pandas as pd
from datetime import datetime
import csv
import argparse
from random import shuffle
from matplotlib import pyplot as plt

"""  A music library enabling users to manage songs, playlists, and perform 
        various functions using implemented code structures, supported by 
        CSV data storage. """

class Playlist:
    """Represents the music library where users can create their own playlist.
    """
    
    def __init__(self, filepath):
        self.filepath = filepath
        self.now_playing_song = {}
        self.new_data = None
        
    def create_database(self):
        self.new_data = pd.read_csv(self.filepath)
        
        return self.new_data
    
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
        
        if 'Release' not in existing_data.columns:
            print("Error: 'Release' column not found in the CSV file.")
            return False
        
        new_song_data = [song_title, artist, genre, \
                duration_seconds, release]
        
        columns = self.new_data.columns

        new_song_df = pd.DataFrame([new_song_data], columns = columns)
        
            
        updated_data = pd.concat([self.new_data, new_song_df],ignore_index=True)
        updated_data['Release']= pd.to_datetime(updated_data['Release'])
        
            
        try:
            updated_data.to_csv(self.filepath, index=False)
            self.new_data = updated_data
           
            return True
        except Exception as e:
            print(f"Error uploading song: {e}")
            return False
        
    def play_song(self, song_title):
        """Attempts to find and play a song by title from a CSV file.

        Args:
            song_title (str): the title of the song that is going to be played.

        Returns:
            str: a message indicating the details about the currently playing
                song if applicable, or a message indicating that the song was
                not found.
        
        Side effects:
            modifies the 'now_playing_song' attribute with the details of the
                song that was found.
        """
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                for song in reader:
                    csv_title = song[0].strip().lower()
                    if csv_title == song_title.lower().strip():
                        self.now_playing_song = {}
                        keys = ['Title', 'Artist', 'Genre', 'Duration', \
                            'Release']
                        for i in range(len(keys)):
                            self.now_playing_song[keys[i]] = song[i].strip()
                        now_playing = self.display_now_playing()
                        return now_playing
                return "Song not found."
        except FileNotFoundError:
            return f"Couldn't find the file '{self.filepath}'."
        except Exception as e:
            return f"Error: {e}"

    def display_now_playing(self):
        """Displays the details of the song that is currently playing.

        Returns:
            str: a message that indicates the details of the song that is 
                currently being played, or a message indicating that no song is
                currently playing.
        """
        if self.now_playing_song:
            return (f"Now playing: '{self.now_playing_song['Title']}' by " 
                    f"{self.now_playing_song['Artist']} "
                    f" from the genre {self.now_playing_song['Genre']}."
                    f" Duration: {self.now_playing_song['Duration']} seconds,"
                    f" released on {self.now_playing_song['Release']}.")
        else:
            return "No song is currently playing."
  
   
    def view_all_songs(self, order = "Recently Added"):
        """Returns all of the user's added songs in a specified order.
        
        Args:
            order(str): the sort order to return the songs; 
                    default is set to 'Recently Added'.
            
        Returns:
            list: list of all added songs according to specified order.
        """
        
        
        if order == "Recently Added":
            recent = self.new_data.sort_index(ascending = False)
            return recent['Title']
        
        elif order == "Alphabetical":
            alpha = self.new_data.sort_values('Title')
            return alpha['Title']
        elif order == "Release Year":
            release = self.new_data.sort_values('Release')

            return release['Title']
                   
                
    def delete_songs(self,song_title):
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
            header_skipped = False
            for row in reader:
                if not header_skipped:
                    if "Title" in row:
                        header_skipped = True
                        continue
                if row:
                    csv_song_title = row[0].strip().replace('“', '').replace('”', '').replace('"', '').lower()
                    input_song_title = song_title.strip().replace('“', '').replace('”', '').replace('"', '').lower()
                    if csv_song_title != input_song_title:
                        updated_playlist.append(row)
                    else:
                        song_found = True
        #When returning data from this function, we maybe should only return whether or not the song was deleted
        if song_found:
            print(f"'{song_title}' found and deleted.")
        else:
            print(f"'{song_title}' not found in the playlist.")

        with open(self.filepath, mode='w', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(updated_playlist)

        return updated_playlist
        # Should we instead return the updated dataframe instead of the list? - BT
    

    def shuffle_songs(self):
            """A method that will take a playlist from a file and shuffle the order of the songs.

            Args:
                filepath (str): the name of the filepath with the songs that need to 
                be shuffled. 
            Returns:
                list: returns a list of the songs in the filepath shuffled, using 
                the shuffle function from the random module.
            """
            shuffled_songs = []
            with open(self.filepath, "r", encoding = "utf-8") as f:
                reader = csv.reader(f)
                for line in reader:
                    if line[0] == 'Title':
                        continue 
                    shuffled_songs.append(line[0])

            shuffle(shuffled_songs)    
            return shuffled_songs
    
    
    def show_listening_habits(self):
        bar = self.new_data.plot.bar(x = 'Genre', y = 'Duration')
        
        return bar
                
    def songs_per_artist(self):
        """
        Counts the number of songs by each artist stored on the iPod

        Args:
        filepath(str): Path to CSV file containing information about each song

        Returns:
        dict: A dictionary where the keys are the artist and the values are the number of songs they have on the iPod
        """
        with open(self.filepath, "r", encoding = "utf-8") as f:
                #Use list comprehension to extract artist values from the csv
                artists = [line.strip().split(",")[1] for line in f]
                #print(set(artists))

        #Counting the number of each song on the iPod written by each aritst using a dictionary comprehension
                songs_artist_dict = {artist: f"{artists.count(artist)} songs/s" for artist in set(artists)}
               #Put the f string in your conditional expression instead of the for loop you had

        #Added a return instead of your print because the function needs a return and can't return None
        return songs_artist_dict
    

#Don't need this function as the view_all_songs function allows users to sort the songs by duration already
    def sort_by_duration(self):
        """
        Sorts the songs by duration in seconds

        Args:
        filepath (str): Path to csv file containing song information.

        Returns: str: f string containing the list of song titles sorted by duration in descending order.
        Side effects: modifies songs list by adding values from the csv file.
        """

        with open(self.filepath, "r", encoding = "utf-8") as f:

                songs = []
                for line in f:
                    song_title, artist, genre, duration, release_date = line.strip().split(",")
                    songs.append((song_title, artist, genre, duration, release_date ))
    #Sort songs in descending order by duration in seconds
        sorted_by_duration = sorted(songs, reverse = True, key=lambda x: x[3])
    #Extract song titles
        sorted_song_titles = [song[0] for song in sorted_by_duration]

        return (f" List of song titles sorted by duration in descending order: {sorted_song_titles}")

                              


def main():
    parser = argparse.ArgumentParser(description="Deletes a song from a playlist.")
    parser.add_argument("song_title", help="The title of the song to delete.")
    parser.add_argument("--playlist_path", default="playlist.csv", help="The path to the playlist CSV file.")
    args = parser.parse_args()

    playlist_manager = Playlist(args.playlist_path)
    updated_playlist = playlist_manager.delete_songs(args.song_title)

    print(f"Updated playlist after deleting \"{args.song_title}\":")
    for song in updated_playlist:
        print(song)

if __name__ == "__main__":
    main()
