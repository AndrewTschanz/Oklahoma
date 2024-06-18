
import numpy as np
import matplotlib.pyplot as plt

# Generate some fake data
np.random.seed(0)  # For reproducibility
x = np.linspace(0, 10, 100)
y = np.sin(x) + np.random.normal(scale=0.5, size=x.shape)

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(x, y, label='Fake Data')

# Add titles and labels
plt.title('Plot of Fake Data')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')

# Add a legend
plt.legend()

# Display the plot
plt.show()