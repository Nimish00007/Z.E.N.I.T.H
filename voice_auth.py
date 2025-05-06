# voice_auth.py (MFCC + delta version)

import numpy as np
import sounddevice as sd
import scipy.io.wavfile as wav
import librosa
from sklearn.metrics.pairwise import cosine_similarity
import os

def extract_features(file_path):
    try:
        y, sr = librosa.load(file_path, sr=None)
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        delta = librosa.feature.delta(mfcc)
        delta2 = librosa.feature.delta(mfcc, order=2)
        combined = np.vstack([mfcc, delta, delta2])
        return np.mean(combined.T, axis=0)
    except Exception as e:
        print("Error extracting features:", e)
        return None

def record_voice(duration=8, fs=44100):
    print("Speak now for voice authentication...")
    try:
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
        sd.wait()
        recorded_path = "jarvis3.wav"
        wav.write(recorded_path, fs, recording)
        return recorded_path
    except Exception as e:
        print("Recording error:", e)
        return None

def authenticate(reference_file="jarvis3.wav", threshold=1.0):
    if not os.path.exists(reference_file):
        print("Reference voice file not found.")
        return False

    ref_features = extract_features(reference_file)
    if ref_features is None:
        print("Failed to extract reference features.")
        return False

    recorded_path = record_voice()
    if not recorded_path:
        return False

    test_features = extract_features(recorded_path)
    if test_features is None:
        print("Failed to extract test features.")
        return False

    similarity = cosine_similarity([ref_features], [test_features])[0][0]
    print(f"Voice similarity: {similarity:.2f}")

    return similarity >= threshold
