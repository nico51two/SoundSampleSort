import os
import librosa
import numpy as np
from sklearn.cluster import KMeans

# Load audio files
audio_folder = 'path/to/audio/folder'
audio_files = os.listdir(audio_folder)
audio_samples = []
for file in audio_files:
    if file.endswith('.wav'):
        audio_file = os.path.join(audio_folder, file)
        y, sr = librosa.load(audio_file, sr=None)
        audio_samples.append(y)

# Extract audio features
features = []
for audio_sample in audio_samples:
    mfccs = librosa.feature.mfcc(y=audio_sample, sr=sr, n_mfcc=13)
    spectral_centroids = librosa.feature.spectral_centroid(y=audio_sample, sr=sr)
    spectral_contrast = librosa.feature.spectral_contrast(y=audio_sample, sr=sr)
    spectral_rolloff = librosa.feature.spectral_rolloff(y=audio_sample, sr=sr)
    zero_crossing_rate = librosa.feature.zero_crossing_rate(y=audio_sample)
    feature_vector = np.concatenate((mfccs.mean(axis=1), spectral_centroids.mean(), spectral_contrast.mean(), spectral_rolloff.mean(), zero_crossing_rate.mean()))
    features.append(feature_vector)

# Cluster audio features
kmeans = KMeans(n_clusters=5, random_state=0).fit(features)
labels = kmeans.labels_

# Move audio files to respective folders
for i, file in enumerate(audio_files):
    if file.endswith('.wav'):
        src_path = os.path.join(audio_folder, file)
        dst_folder = os.path.join(audio_folder, 'cluster_' + str(labels[i]))
        if not os.path.exists(dst_folder):
            os.makedirs(dst_folder)
        dst_path = os.path.join(dst_folder, file)
        os.rename(src_path, dst_path)
