import matplotlib.pyplot as plt
import numpy as np

# Data for the three columns
categories = ['Category A', 'Category B', 'Category C']
values = [25, 40, 35]  # Replace these values with your data

# Calculate the mean
mean_value = np.mean(values)

# Create the bar plot
plt.figure(figsize=(8, 6))

plt.bar(categories, values, color='skyblue')
plt.axhline(y=mean_value, color='red', linestyle='--', label='Mean')

plt.xlabel('Categories')
plt.ylabel('Values')
plt.title('Bar Graph with Mean Line')

# Show the legend
plt.legend()

# Display the mean value as text on the graph
plt.text(0.1, mean_value + 1, f'Mean: {mean_value:.2f}', color='red', fontsize=12, ha='center')

plt.show()