from matplotlib import pyplot as plt
def plot_image(image, title=None):
    plt.imshow(image)
    if title is not None:
        plt.title(title)
    plt.axis('off')
def plot_images(images, titles=None, cols=5):
    rows = (len(images) + cols - 1) // cols
    plt.figure(figsize=(15, 3 * rows))
    for i, image in enumerate(images):
        plt.subplot(rows, cols, i + 1)
        plot_image(image, title=titles[i] if titles else None)
    plt.tight_layout()
    plt.show()
plt.plot([1,2,3,4,5],[21,34,45,65,76])
plt.title('Sample Line Plot')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.show()
import numpy as np
x = np.linspace(0, 10, 100)
y = np.sin(x)
plt.plot(x, y)
plt.title('Sine Wave')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.show()
import seaborn as sns
import pandas as pd
data = pd.DataFrame({
    'Category': ['A', 'B', 'C', 'D'],
    'Values': [10, 20, 15, 25]
})
sns.barplot(x='Category', y='Values', data=data)
plt.title('Bar Plot')
plt.xlabel('Category')
plt.ylabel('Values')
plt.show()
import plotly.express as px
df = px.data.iris()
fig = px.scatter(df, x='sepal_width', y='sepal_length', color='species')
fig.update_layout(title='Iris Dataset Scatter Plot', xaxis_title='Sepal Width', yaxis_title='Sepal Length')
fig.show()
