import pygame
import numpy as np
from typing import Optional, List
import time

class MusicPlayer:
    def __init__(self):
        pygame.mixer.init()
        self.current_song: Optional[pygame.mixer.Sound] = None
        self.next_song: Optional[pygame.mixer.Sound] = None
        self.is_playing: bool = False
        self.volume: float = 1.0
        self.crossfade_duration: float = 3.0  # seconds
        self.playlist: List[str] = []
        self.current_index: int = 0

    def load_song(self, filepath: str) -> None:
        try:
            self.current_song = pygame.mixer.Sound(filepath)
            self.current_song.set_volume(self.volume)
        except pygame.error as e:
            raise Exception(f'Failed to load audio file: {e}')

    def add_to_playlist(self, filepath: str) -> None:
        self.playlist.append(filepath)

    def play(self) -> None:
        if self.current_song:
            self.current_song.play()
            self.is_playing = True

    def stop(self) -> None:
        if self.current_song:
            self.current_song.stop()
            self.is_playing = False

    def set_volume(self, volume: float) -> None:
        self.volume = max(0.0, min(1.0, volume))
        if self.current_song:
            self.current_song.set_volume(self.volume)

    def crossfade_to_next(self) -> None:
        if not self.playlist or self.current_index >= len(self.playlist) - 1:
            return

        # Load next song
        next_index = (self.current_index + 1) % len(self.playlist)
        self.next_song = pygame.mixer.Sound(self.playlist[next_index])
        
        # Prepare both songs
        if self.current_song:
            current_vol = self.volume
            self.next_song.set_volume(0)
            self.next_song.play()
            
            # Perform crossfade
            steps = 50
            fade_step = current_vol / steps
            sleep_time = self.crossfade_duration / steps
            
            for step in range(steps):
                new_current_vol = current_vol - (fade_step * step)
                new_next_vol = fade_step * step
                
                self.current_song.set_volume(max(0, new_current_vol))
                self.next_song.set_volume(min(current_vol, new_next_vol))
                time.sleep(sleep_time)
            
            # Clean up
            self.current_song.stop()
            self.current_song = self.next_song
            self.next_song = None
            self.current_index = next_index

    def set_crossfade_duration(self, duration: float) -> None:
        """Set the duration of crossfade in seconds"""
        self.crossfade_duration = max(0.1, duration)

    def get_current_song(self) -> Optional[str]:
        if 0 <= self.current_index < len(self.playlist):
            return self.playlist[self.current_index]
        return None

    def clear_playlist(self) -> None:
        self.stop()
        self.playlist.clear()
        self.current_index = 0
