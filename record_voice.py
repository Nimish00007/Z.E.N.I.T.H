import sounddevice as sd
import soundfile as sf
import numpy as np
import librosa
import tempfile
from sklearn.metrics.pairwise import cosine_similarity

# STEP 3: Extract MFCC Features
def extract_mfcc(filepath):
    y, sr = librosa.load(filepath, sr=None)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    mfcc_scaled = np.mean(mfcc.T, axis=0)
    return mfcc_scaled

# STEP 4: Authenticate User
def authenticate(reference_path):
    print("Speak the passphrase to authenticate...")
    fs = 44100
    duration = 4  # seconds

    # Record live voice
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
        sf.write(tmp_file.name, recording, fs)
        recorded_path = tmp_file.name

    # Extract MFCCs
    ref_feat = extract_mfcc(reference_path).reshape(1, -1)
    test_feat = extract_mfcc(recorded_path).reshape(1, -1)

    # Compare similarity
    similarity = cosine_similarity(ref_feat, test_feat)[0][0]
    print(f"Voice similarity score: {similarity:.2f}")

    return similarity > 0.85  # You can adjust the threshold if needed

# Example usage
if __name__ == "__main__":
    if authenticate("jarvis3.wav"):
        print("Authentication successful! Welcome back.")
    else:
        print("Authentication failed. Access denied.")
