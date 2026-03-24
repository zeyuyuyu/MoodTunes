import os
import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt

class MusicPlayer:
    def __init__(self, audio_file):
        self.audio_file = audio_file
        self.y, self.sr = librosa.load(self.audio_file)
        self.tempo, self.beat_frames = librosa.beat.beat_track(y=self.y, sr=self.sr)
        self.chroma_stft = librosa.feature.chroma_stft(y=self.y, sr=self.sr)
        self.mfcc = librosa.feature.mfcc(y=self.y, sr=self.sr)
        self.rms = librosa.feature.rms(y=self.y)
        self.spec_cent = librosa.feature.spectral_centroid(y=self.y, sr=self.sr)
        self.spec_bw = librosa.feature.spectral_bandwidth(y=self.y, sr=self.sr)
        self.tonnetz = librosa.feature.tonnetz(y=self.y, sr=self.sr)
        self.onset_env = librosa.onset.onset_strength(y=self.y, sr=self.sr)

    def analyze_mood(self):
        """Analyze the mood of the audio file based on various audio features."""
        # Calculate the mean of each feature
        mean_chroma_stft = np.mean(self.chroma_stft)
        mean_mfcc = np.mean(self.mfcc, axis=1)
        mean_rms = np.mean(self.rms)
        mean_spec_cent = np.mean(self.spec_cent)
        mean_spec_bw = np.mean(self.spec_bw)
        mean_tonnetz = np.mean(self.tonnetz, axis=1)
        mean_onset_env = np.mean(self.onset_env)

        # Combine the features into a single feature vector
        feature_vector = np.concatenate((mean_chroma_stft, mean_mfcc, mean_rms, mean_spec_cent, mean_spec_bw, mean_tonnetz, mean_onset_env))

        # Use a pre-trained model to predict the mood
        mood = self.predict_mood(feature_vector)

        return mood

    def predict_mood(self, feature_vector):
        """Predict the mood of the audio file using a pre-trained model."""
        # Load the pre-trained model
        model = load_model('mood_prediction_model.h5')

        # Make the prediction
        mood_prediction = model.predict(np.expand_dims(feature_vector, axis=0))

        # Map the prediction to a mood label
        mood_labels = ['happy', 'sad', 'angry', 'calm']
        mood = mood_labels[np.argmax(mood_prediction)]

        return mood