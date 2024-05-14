import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the CSV file
df = pd.read_csv('D:\\Research-All\\review-laccase-metagenome\\dye.csv')

# Count the number of occurrences of each application
application_counts = df['Application in Industry'].value_counts()

# Calculate the total for finding the percentage of each application
total = application_counts.sum()

# Preparing data for the plot
labels = application_counts.index
sizes = application_counts.values

# Generating a set of colors from a colormap
colormap = plt.cm.nipy_spectral
colors = [colormap(i) for i in np.linspace(0, 1, len(labels))]

# Plotting the donut chart
fig, ax = plt.subplots(figsize=(10, 8))
wedges, texts = ax.pie(sizes, colors=colors, startangle=90)

# Draw a circle at the center to make it a donut chart
centre_circle = plt.Circle((0,0), 0.70, color='black', fc='white')
fig.gca().add_artist(centre_circle)



ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
plt.tight_layout()

# Incorporating percentages into the legend labels
percentages = [(size / total * 100) for size in sizes]
legend_labels = [f"{label}: {percentage:.3f}%" for label, percentage in zip(labels, percentages)]

# Adding a custom legend
plt.legend(wedges, legend_labels, title="Applications", loc="center left", bbox_to_anchor=(0.9, 0, 0.5, 1))
# Adding "Laccases" text in the center of the donut plot
plt.text(0, 0, 'Laccases', ha='center', va='center', fontsize=30)

plt.show()