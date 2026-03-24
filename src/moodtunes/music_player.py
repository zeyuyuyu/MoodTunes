import random
from typing import List, Optional, Dict

class MusicPlayer:
    def __init__(self):
        self.current_track: Optional[str] = None
        self.queue: List[Dict] = []
        self.mood_categories = {
            'happy': ['pop', 'dance', 'upbeat'],
            'relaxed': ['ambient', 'classical', 'jazz'],
            'energetic': ['rock', 'electronic', 'hip-hop'],
            'melancholic': ['blues', 'indie', 'acoustic']
        }
        self.is_playing: bool = False
        self.volume: float = 1.0
        self.repeat_mode: str = 'off'  # 'off', 'one', 'all'

    def add_to_queue(self, track: Dict) -> None:
        """Add a track to the play queue"""
        self.queue.append(track)

    def add_mood_based_tracks(self, mood: str, tracks: List[Dict]) -> None:
        """Add tracks that match the specified mood to queue"""
        if mood not in self.mood_categories:
            raise ValueError(f'Invalid mood: {mood}')
            
        matching_tracks = [
            track for track in tracks
            if any(genre in track.get('genres', []) 
                  for genre in self.mood_categories[mood])
        ]
        self.queue.extend(matching_tracks)

    def shuffle_queue(self) -> None:
        """Randomly shuffle the current queue"""
        random.shuffle(self.queue)

    def clear_queue(self) -> None:
        """Clear all tracks from queue"""
        self.queue = []

    def skip_track(self) -> Optional[Dict]:
        """Skip to next track in queue"""
        if not self.queue:
            self.current_track = None
            self.is_playing = False
            return None
            
        if self.repeat_mode == 'one' and self.current_track:
            return self.current_track
            
        next_track = self.queue.pop(0)
        if self.repeat_mode == 'all':
            self.queue.append(next_track)
            
        self.current_track = next_track
        return next_track

    def previous_track(self) -> Optional[Dict]:
        """Return to previous track"""
        if not self.queue or not self.current_track:
            return None
            
        self.queue.insert(0, self.current_track)
        return self.queue[0]

    def set_volume(self, volume: float) -> None:
        """Set player volume (0.0 to 1.0)"""
        if not 0 <= volume <= 1:
            raise ValueError('Volume must be between 0 and 1')
        self.volume = volume

    def set_repeat_mode(self, mode: str) -> None:
        """Set repeat mode (off/one/all)"""
        if mode not in ['off', 'one', 'all']:
            raise ValueError('Invalid repeat mode')
        self.repeat_mode = mode

    def get_queue_info(self) -> Dict:
        """Get current queue status and info"""
        return {
            'current_track': self.current_track,
            'queue_length': len(self.queue),
            'is_playing': self.is_playing,
            'volume': self.volume,
            'repeat_mode': self.repeat_mode
        }

    def play(self) -> None:
        """Start or resume playback"""
        if self.queue and not self.current_track:
            self.current_track = self.queue.pop(0)
        self.is_playing = True

    def pause(self) -> None:
        """Pause playback"""
        self.is_playing = False