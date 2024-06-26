import pandas as pd
from datetime import datetime
import csv
from argparse import ArgumentParser
from random import shuffle
from matplotlib import pyplot as plt 

"""  A music library enabling users to manage songs, playlists, and perform 
        various functions using implemented code structures, supported by 
        CSV data storage. """

class Playlist:
    """Represents the music library where users can create their own playlist.
    """
    
    def __init__(self, filepath):
        """Initializes the class attributes.
        """
        self.filepath = filepath
        self.now_playing_song = {}
        self.create_database()
        
    def __repr__(self):
        """Returns the formal representation of the object in an f-string."""
        return f"Playlist({self.filepath},{self.now_playing_song},\
            {self.new_data})"
    
        
    def create_database(self):
        """Loads data from a CSV file into a DataFrame, and reads data from the
            CSV file specified by the `filepath` attribute and stores it in the
            `new_data` attribute.

        Returns:
            pandas.DataFrame: DataFrame containing the loaded data.
        """
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
                
        Author:
            Daphne O'Malley
            
        Technique:
            conditional expressions
            concatenating on Pandas DataFrame
        """
        if self.new_data is None:
            self.create_database()   
            
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
        updated_data = updated_data.convert_dtypes()
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
                
        Author:
            Daphne O'Malley
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
                
        Author:
            Daphne O'Malley
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
            
        Author:
            Becky Takang
            
        Technique:
            optional parameters
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
        
        Author: Elise Ferguson
        Technique: f-strings with expressions
        """
        updated_playlist = []
        song_found = False
        with open(self.filepath, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                csv_song_title = \
                    row[0].strip().replace('“', '').replace('”', '')\
                        .replace('"', '').lower()
                input_song_title = song_title.strip().replace('“', '')\
                    .replace('”', '').replace('"', '').lower()
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
    
    def shuffle_songs(self):
            """A method that will take a playlist from a file and shuffle 
            the order of the songs.

            Args:
                filepath (str): the name of the filepath with the songs that
                need to be shuffled. 
            Returns:
                list: returns a list of the songs in the filepath shuffled, 
                using the shuffle function from the random module.
            
            Author: Hailey Moore
            Techniques: With statements
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
        """Shows how long a user spends listening to a certain genre of music

        Returns:
            pyplot bar graph : pyplot bar graph with the results of the \
                user's listening habits
                
        Author:
            Becky Takang
            
        Technique:
            visualizing data with pyplot
        """
        group = self.new_data.groupby('Genre')['Duration'].sum()
        bar = group.plot.bar(x = 'Genre', y = 'Duration')
        plt.xlabel('Genre')
        plt.ylabel('Duration')
        plt.title('The Amount of Time Spent Listening to Each Genre')
        return plt.show()
                
    def songs_per_artist(self):
        """
        Counts the number of songs by each artist stored on the iPod

        Args:
            filepath(str): Path to CSV file containing information about each\
                song.

        Returns: 
            songs_artist_dict(dict): A dictionary where the keys are the artist\
                  and 
                the values are the number of songs they have on the iPod.

        Author: Charlotte Drew
        Technique: List and dictionary comprehensions
        """

        with open(self.filepath, "r", encoding = "utf-8") as f:
            #Skips header line
            next(f)
            #Use list comprehension to extract artist values from CSV file
            artists = [line.strip().split(",") [1] for line in f]

            #Counts the number of songs written by each artist downloaded on 
            #the iPod using a dictionary comprehension

            songs_artist_dict = {artist: f"{artists.count(artist)} song/s." \
            for artist in set(artists)}

        return songs_artist_dict
    

    def calculate_durations(self):
        """
        Creates a list of all the songs on the iPod in order of their duration\
              and 
            also calculates the longest song with its length."

        Args:
            filepath (str): Path to csv file containing song information.

        Returns: 
            str: f string containing the list of song titles sorted by duration\
                in 
                descending order and the longest song with its length.
        
        Side effects: 
            modifies songs list by adding values from the csv file.

        Author: Charlotte Drew

        Technique: Use of a key function with sorted


        """

        with open(self.filepath, "r", encoding = "utf-8") as f:
                
                songs = []
                for line in f:
                    song_title, artist, genre, duration, release_date =\
                        line.strip().split(",")
                    if song_title == 'Title':
                        continue
                    songs.append((song_title, artist, genre, duration, \
                        release_date ))
                    
    #Sort songs in descending order by duration in seconds
        sorted_by_duration = sorted(songs, reverse = True, key=lambda x: x[3])


    #Extract song titles
        
        sorted_song_titles = [song[0] for song in sorted_by_duration]

    #Extract durations
        song_durations = [duration[3] for duration in sorted_by_duration]
    #Calculate longest song downloaded on iPod
        longest_song = max(song_durations)


        return(f" List of song titles sorted by duration in descending order: \
        {sorted_song_titles}. The longest song on this iPod is \
        {sorted_song_titles[0]} and it is {longest_song} seconds long.") 
    
    def check_playlist(self, song, favorite = False):
        """Checks if a song is in the playlist/csv, and if it is a favorite 
        song,it is added to the frozenset that will keep it as the user's 
        favorite song.

        Args:
            filepath (str): name of csv file.
            song (str): name of song being checked.
            favorite (bool, optional): whether the song is a favorite song or 
            not. Defaults to False.

        Returns:
            str: f-string that prints if the song is in the playlist, if it 
            is not, it will say None is in the playlist.
            
        Author: Hailey Moore
        Techniques: Set operations and frozensets.
        """
        check_set = set()
        with open(self.filepath, "r", encoding = "utf-8") as f:
            for line in f:
                if 'Title' in line:
                    continue
                if song in line.strip().split(','):
                    check_set.add(song)
              
            if favorite == True:
                favorites = frozenset({song})
                print(f"'{song}' is an all time favorite!")

        if check_set == set():
            return f"The song '{song}' is not in the playlist"
        else:
            return f"The song '{song}' is in the playlist."

def menu():
    """Displays menu options for the IPod.
    This function is adapted from 
    https://gist.github.com/guestl/858e882a37442316fd7cdb0ca1b8e3a5 
        (https://gist.github.com/guestl/858e882a37442316fd7cdb0ca1b8e3a5)

    We used the print statements format and while loop from this code but made
      it our own to fit our needs. However, in their example, their while loop 
      is a bit more complex and has some extra steps than ours. We just used 
      this as a basic pattern outline. We also defined functions to call from,
        whereas in the source code we used they did not. 


    """
    print("\nIPod Menu:")
    print("1. Upload a song")
    print("2. Delete a song")
    print("3. Play a song")
    print("4. Count songs per artist")
    print("5. Print list of songs ordered by duration along with longest song"
        " and its length")
    print("6. View all songs")
    print("7. View your listening habits")
    print("8. Shuffle Songs")
    print("9. Check for a song in the playlist")
    print("10. Turn off IPod")

def upload_song_menu(playlist):
    """Asks the user to provide the details of the song they want to be added to
        the playlist.

    Args:
        playlist (Playlist): the playlist object to which the song will be added
    """
    song_title = input("Enter the title of the song: ")
    artist = input("Enter the artist of the song: ")
    genre = input("Enter the genre of the song: ")
    duration = input("Enter the duration of the song (mm:ss): ")
    release = input("Enter the release date of the song (YYYY-MM-DD): ")
    
    if playlist.upload_song(song_title, artist, genre, duration, release):
        print(f"The song '{song_title}' was uploaded successfully.")
    else:
        print(f"Failed to upload the song '{song_title}'. Please try again.")

def delete_song_menu(playlist):
    """Asks the user to specify the title of the song they want to delete from
        the playlist.

    Args:
        playlist (Playlist): the playlist object from which the song will be 
            deleted.
    """
    song_title = input("Enter the title of the song to delete: ")
    playlist.delete_songs(song_title)

def play_song_menu(playlist):
    """Asks the user to specify the title of the song they want to play from the
        playlist.

    Args:
        playlist (Playlist): the playlist object from which the song will be 
            played.
    """
    song_title = input("Enter the title of the song to be played: ")
    print(playlist.play_song(song_title))

def view_all_songs_menu(playlist):
    """Asks the user to input their filtering criteria for the view_all_songs \
        function

    Args:
        playlist (Playlist): the playlist object from which the songs will \
            be returned

    """
    
    while True:
        option = input("How would you like to view your songs: Recently Added," 
        " Alphabetical, Release Year ")
        if option == 'Recently Added':
            print(playlist.view_all_songs('Recently Added'))
            break
            
        elif option == 'Alphabetical':
            print(playlist.view_all_songs('Alphabetical'))
            break
            
        elif option == 'Release Year':
            print(playlist.view_all_songs('Release Year'))
            break
            
        else:
            print(f"Please choose from one of the given options")

def songs_per_artist_menu(playlist):
    """Helps call the songs_per_aritst method in the menu"""
    print(playlist.songs_per_artist())

def calculate_durations_menu(playlist):
    """Helps call the calculate_durations method in the menu"""
    print(playlist.calculate_durations())
    
def view_your_listening_habits_menu(playlist):
    """Shows users their listening habits

    Args:
        playlist (Playlist): the playlist object from which the listening \
            habits will be displayed
    """
    print(playlist.show_listening_habits())

def shuffle_songs_menu(playlist):
    """Menu option to call the shuffling songs function.

    Args:
        playlist (Playlist): a playlist object that is being shuffled.
    """
    print(playlist.shuffle_songs())
        
def check_playlist_menu(playlist):
    """Menu option for checking a song in a playlist.

    Args:
        playlist (Playlist): a playlist object from which a song will be \
            checked
    """
    song = input("Enter the song you want to check: ")
    favorite = input("Enter True if this song is your favorite, False if not: ")
    print(playlist.check_playlist(song, favorite=False))

def main():
    """Parse command line argument and intializes the playlist manager. Also
    displays a menu for the user to select the operation they want the iPod to
    perform.
    
    Side effect:
        prints "Ipod shutting down" if option 10 is selected
        prints "Invalid choice. Please choose a valid option." if conditons are
        not met

    Author: Elise Ferguson
    Technique: ArgumentParser class
    """
    parser = ArgumentParser(description="Manage your playlist.")
    parser.add_argument("--playlist_path", default="songs.csv",\
                            help="The path to the playlist CSV file.")
    args = parser.parse_args()

    music_library_manager = Playlist(args.playlist_path)

    while True:
        menu()
        choice = input("Enter your choice (1-10): ")

        if choice == "1":
            upload_song_menu(music_library_manager)
        elif choice == "2":
            delete_song_menu(music_library_manager)
        elif choice == "3":
            play_song_menu(music_library_manager)
        elif choice == "4":
            songs_per_artist_menu(music_library_manager)
        elif choice == "5":
            calculate_durations_menu(music_library_manager)
        elif choice == "6":
            view_all_songs_menu(music_library_manager)
        elif choice == "7":
            view_your_listening_habits_menu(music_library_manager)
        elif choice == "8":
            shuffle_songs_menu(music_library_manager)
        elif choice == "9":
            check_playlist_menu(music_library_manager)
        elif choice == "10":
            print("Ipod shutting down")
            break
        else:
            print("Invalid choice. Please choose a valid option.")


if __name__ == "__main__":
    main()

