import multiprocessing
multiprocessing.set_start_method('forkserver', force=True)

import pyLDAvis
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA


# Load the Excel file
file_path = 'DBSCAN/bdjobsSkills.xlsx'
data = pd.read_excel(file_path)

# Vectorize the text using CountVectorizer
count_vectorizer = CountVectorizer(stop_words='english', max_features=5000)
count_matrix = count_vectorizer.fit_transform(data['Skill'])

# Evaluate LDA for different topic counts
scores = []
for n_topics in range(2, 30):  # Test from 2 to 10 topics
    lda = LatentDirichletAllocation(n_components=n_topics, random_state=42)
    topic_dist = lda.fit_transform(count_matrix)
    score = silhouette_score(topic_dist, topic_dist.argmax(axis=1))
    scores.append((n_topics, score))

# Select the best number of topics
best_n_topics = max(scores, key=lambda x: x[1])[0]
print(f"Best number of topics: {best_n_topics}")

# Run LDA with the best number of topics
lda_model = LatentDirichletAllocation(n_components=best_n_topics, random_state=42)
topic_distribution = lda_model.fit_transform(count_matrix)
data['Topic'] = topic_distribution.argmax(axis=1)

# Visualize the topics using pyLDAvis
vocab = count_vectorizer.get_feature_names_out()
lda_vis_data = pyLDAvis.prepare(
    topic_term_dists=lda_model.components_,
    doc_topic_dists=topic_distribution,
    doc_lengths=count_matrix.sum(axis=1).A1,
    vocab=vocab,
    term_frequency=count_matrix.sum(axis=0).A1,
    R=50  # Number of terms to display per topic
)

# Save the visualization
pyLDAvis.save_html(lda_vis_data, "LDAvis.html")
print("LDA visualization saved.")


# Save the results to an Excel file
excel_file_name = "bdjobsLDACluster.xlsx"
data.to_excel(excel_file_name, index=False)
print(f"Clustered data saved to {excel_file_name}")
# Optional: Reduce dimensions for visualization
pca = PCA(n_components=2)
reduced_data = pca.fit_transform(count_matrix.toarray())
# Plot the clusters
plt.figure(figsize=(10, 6))
plt.scatter(reduced_data[:, 0], reduced_data[:, 1], c=data['Topic'], cmap='viridis', s=10)
plt.title("LDA Clusters of Skills")
plt.xlabel("PCA Component 1")
plt.ylabel("PCA Component 2")
plt.colorbar(label="Topic Label")
plt.show()
