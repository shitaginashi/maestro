import numpy as np

lib = np.load('latent_library.npy')

# Check the variance of the first few dimensions
# If Dim 0 has very high variance and correlates with Riser/Hit/Suckback, 
# then the library is "Physically Mapped".
variances = np.var(lib, axis=0)
top_indices = np.argsort(variances)[-5:]

print(f"Top 5 Dimensions by Variance: {top_indices}")
print(f"Sample Row (first 10 dims): {lib[0, :10]}")