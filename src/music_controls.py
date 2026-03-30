from pygame import mixer
from pygame.mixer import music
import pygame
import os


# Responsible for controlling the music
class MusicControls:
    def __init__(self):
        # initializes the mixer
        mixer.init()
        self.song_path = ""
        self.current_volume = 0.5
        self.song_playing = False
        # Takes note if the song actually made progress for unpause
        self.song_elapsed = False
        self.shuffle_mode = False
        self.repeat_mode = False

        self.SONG_FINISHED = pygame.USEREVENT + 1
        music.set_endevent(self.SONG_FINISHED)

        os.environ["SDL_VIDEODRIVER"] = "dummy"
        pygame.init()
        pygame.display.set_mode((1, 1))

    def load_song(self, song_path):
        # update the state of the object to be the passed in path
        self.song_path = song_path
        # load the song
        music.load(song_path)

        self.song_elapsed = False

    def pause_song(self):
        if self.song_playing:
            music.pause()
            self.song_playing = False
        else:
            pass

    def unpause_song(self):
        if not self.song_playing:
            music.unpause()
            self.song_playing = True
        else:
            pass

    def play_song(self):
        music.play()
        self.song_playing = True
        self.song_elapsed = True

    # TODO: Add volume controls
    def set_volume_up(self):
        pass

    def set_volume_down(self):
        pass

    def get_pos(self):
        return music.get_pos()

    def repeat(self):
        self.repeat_mode = not self.repeat_mode
