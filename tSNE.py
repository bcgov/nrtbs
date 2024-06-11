import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

def create_tsne_embedding(data, n_components=2, perplexity=30, learning_rate=200, n_iter=1000):
    """
    Create a t-SNE embedding from the given data.

    Parameters:
    data (np.ndarray): The input data array of shape (n_samples, n_features).
    n_components (int): The dimension of the embedded space (default is 2).
    perplexity (float): The perplexity parameter for t-SNE (default is 30).
    learning_rate (float): The learning rate for t-SNE (default is 200).
    n_iter (int): The number of iterations for optimization (default is 1000).

    Returns:
    np.ndarray: The embedded data array of shape (n_samples, n_components).
    """
    tsne = TSNE(n_components=n_components, perplexity=perplexity, learning_rate=learning_rate, n_iter=n_iter, random_state=42)
    tsne_results = tsne.fit_transform(data)
    return tsne_results

def plot_tsne_embedding(embedded_data, labels=None):
    """
    Plot the t-SNE embedding.

    Parameters:
    embedded_data (np.ndarray): The embedded data array of shape (n_samples, n_components).
    labels (np.ndarray): The labels for each data point (default is None).
    """
    plt.figure(figsize=(8, 6))
    if labels is not None:
        unique_labels = np.unique(labels)
        for label in unique_labels:
            idx = labels == label
            plt.scatter(embedded_data[idx, 0], embedded_data[idx, 1], label=label)
        plt.legend()
    else:
        plt.scatter(embedded_data[:, 0], embedded_data[:, 1])
    plt.xlabel('t-SNE Component 1')
    plt.ylabel('t-SNE Component 2')
    plt.title('t-SNE 4D to 2D Embedding')
    plt.show()

# Example usage:
# Generate random 4D data for demonstration purposes
np.random.seed(42)
data_4d = np.random.rand(100, 4)

# Create the t-SNE embedding
tsne_2d = create_tsne_embedding(data_4d)

# Optionally, create some labels for the data points
labels = np.random.choice(['Class 1', 'Class 2', 'Class 3'], size=100)

# Plot the t-SNE embedding
plot_tsne_embedding(tsne_2d, labels)
