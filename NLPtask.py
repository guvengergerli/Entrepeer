import requests
import time
import json
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
import numpy as np

time.sleep(10)

url = "http://0.0.0.0:8000/get_results"
response = requests.get(url)

while not isinstance(response.json(), list):
    print("Waiting for results...")
    time.sleep(2)
    response = requests.get(url)

companies = response.json()
print("Number of companies:", len(companies))
#print("Example output:", companies[0])

# Extract features for clustering
features = [
    f"{company['company_name']} {company['city']} {company['country']} {company['theme_gd']}"
    for company in companies
]

model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

feature_embeddings = np.array(model.encode(features, convert_to_tensor=True).tolist())

num_clusters = 50
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
cluster_assignments = kmeans.fit_predict(feature_embeddings)

company_clusters = {cluster_id: [] for cluster_id in range(num_clusters)}
for i, cluster_id in enumerate(cluster_assignments):
    company_clusters[cluster_id].append(companies[i])

for cluster_id, companies_in_cluster in company_clusters.items():
    print(f"\nCluster {cluster_id + 1}:")
    for company in companies_in_cluster:
        company_info = f"{company['company_name']} - {company['theme_gd']} - {company['city']} \ {company['country']}"
        print(f"{cluster_id + 1} {company_info}")

