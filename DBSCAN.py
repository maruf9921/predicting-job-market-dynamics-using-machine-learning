from sklearn.cluster import DBSCAN
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# Load the Excel file
file_path = 'DBSCAN/bdjobsSkills.xlsx'  # Replace with your file path
data = pd.read_excel(file_path)

# Vectorize the "Skills" column using TF-IDF
tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_features=2000)
tfidf_matrix = tfidf_vectorizer.fit_transform(data['Skill'])

# Apply DBSCAN clustering
dbscan = DBSCAN(eps=0.5, min_samples=5, metric='cosine')
clusters = dbscan.fit_predict(tfidf_matrix)

# Add cluster labels to the DataFrame
data['Cluster'] = clusters

# Optional: Reduce dimensions for visualization
pca = PCA(n_components=2)
reduced_data = pca.fit_transform(tfidf_matrix.toarray())

# Plot the clusters
plt.figure(figsize=(10, 6))
plt.scatter(reduced_data[:, 0], reduced_data[:, 1], c=clusters, cmap='viridis', s=10)
plt.title("DBSCAN Clusters of Skills")
plt.xlabel("PCA Component 1")
plt.ylabel("PCA Component 2")
plt.colorbar(label="Cluster Label")
plt.show()

# Save the clustered data to Excel
#output_file = "bdjobsSkills_with_DBSCAN_clusters.xlsx"
#data.to_excel(output_file, index=False)
#print(f"Clustered data saved to {output_file}")
