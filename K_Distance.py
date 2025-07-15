import pandas as pd
from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer

# Load the Excel file
file_path = 'DBSCAN/bdjobsSkills.xlsx'  # Replace with your file path
data = pd.read_excel(file_path)

# Convert text to numerical format using TF-IDF
tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
tfidf_matrix = tfidf_vectorizer.fit_transform(data['Skill'])

# Number of neighbors (k)
k = 5  # Typically set to the same value as `min_samples`

# Compute the k-nearest neighbors
nbrs = NearestNeighbors(n_neighbors=k).fit(tfidf_matrix)
distances, indices = nbrs.kneighbors(tfidf_matrix)

# Sort the distances to the k-th nearest neighbor
k_distances = sorted(distances[:, k-1])

# Plot the k-distance graph
plt.figure(figsize=(10, 6))
plt.plot(k_distances)
plt.title('K-Distance Plot')
plt.xlabel('Data Points (sorted by distance)')
plt.ylabel(f'{k}-th Nearest Neighbor Distance')
plt.grid(True)
plt.show()
