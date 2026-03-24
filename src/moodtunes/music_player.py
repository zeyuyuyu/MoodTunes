import pygame
import time
from typing import Optional, List

class MusicPlayer:
    def __init__(self):
        pygame.mixer.init()
        self.current_track: Optional[pygame.mixer.Sound] = None
        self.next_track: Optional[pygame.mixer.Sound] = None
        self.volume = 1.0
        self.crossfade_duration = 3.0  # seconds
        self.playlist: List[str] = []
        self.current_index = 0
        self.is_playing = False

    def load_track(self, filepath: str) -> None:
        """Load an audio track from the given filepath."""
        try:
            self.current_track = pygame.mixer.Sound(filepath)
            self.current_track.set_volume(self.volume)
        except pygame.error as e:
            raise Exception(f'Error loading track: {e}')

    def add_to_playlist(self, filepath: str) -> None:
        """Add a track to the playlist."""
        self.playlist.append(filepath)

    def play(self) -> None:
        """Start playing the current track."""
        if self.current_track:
            self.current_track.play()
            self.is_playing = True

    def stop(self) -> None:
        """Stop the current track."""
        if self.current_track:
            self.current_track.stop()
            self.is_playing = False

    def set_volume(self, volume: float) -> None:
        """Set volume level (0.0 to 1.0)."""
        self.volume = max(0.0, min(1.0, volume))
        if self.current_track:
            self.current_track.set_volume(self.volume)

    def crossfade_to_next(self) -> None:
        """Smoothly transition to the next track with crossfade."""
        if not self.playlist or self.current_index >= len(self.playlist) - 1:
            return

        # Load next track
        next_index = (self.current_index + 1) % len(self.playlist)
        self.next_track = pygame.mixer.Sound(self.playlist[next_index])
        self.next_track.set_volume(0.0)
        self.next_track.play()

        # Perform crossfade
        steps = 50
        sleep_time = self.crossfade_duration / steps
        
        for i in range(steps):
            old_vol = self.volume * (1 - (i / steps))
            new_vol = self.volume * (i / steps)
            
            if self.current_track:
                self.current_track.set_volume(old_vol)
            if self.next_track:
                self.next_track.set_volume(new_vol)
                
            time.sleep(sleep_time)

        # Stop old track and update current
        if self.current_track:
            self.current_track.stop()
        self.current_track = self.next_track
        self.next_track = None
        self.current_index = next_index

    def get_current_track(self) -> Optional[str]:
        """Get the filepath of the currently playing track."""
        if 0 <= self.current_index < len(self.playlist):
            return self.playlist[self.current_index]
        return None

    def clear_playlist(self) -> None:
        """Clear the current playlist."""
        self.stop()
        self.playlist.clear()
        self.current_index = 0

    def __del__(self):
        """Clean up pygame mixer on deletion."""
        pygame.mixer.quit()