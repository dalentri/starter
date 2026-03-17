from pygame import mixer
from pygame.mixer import music


# Responsible for controlling the music
class MusicControls:
    def __init__(self):
        # initializes the mixer
        mixer.init()
        self.song_path = ""
        self.current_volume = 0.5
        self.song_playing = False
        self.shuffle_mode = False

    def load_song(self, song_path):
        # update the state of the object to be the passed in path
        self.song_path = song_path
        # load the song
        music.load(song_path)

    def pause_song(self):
        if self.song_playing:
            music.pause()
        else:
            pass

    def unpause_song(self):
        if not self.song_playing:
            music.unpause()
        else:
            pass

    def play_song(self):
        music.play()
        pass

    def skip_song(self):
        pass

    def set_shuffle(self):
        pass

    def get_volume(self):
        pass

    def set_volume(self):
        pass
