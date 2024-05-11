import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import joblib

# Load your dataset (assuming it's in a CSV file)
# Adjust the file path and delimiter according to your dataset
dataset = pd.read_csv('XSS_dataset.csv', delimiter='\t', header=None, names=['text', 'label'])

# Preprocess the text data (e.g., remove HTML tags)
dataset['text'] = dataset['text'].str.replace(r'<[^>]*>', '')

# Split the dataset into features (X) and labels (y)
X = dataset['text']
y = dataset['label']

# Vectorize features
vectorizer = TfidfVectorizer()
X_vectorized = vectorizer.fit_transform(X)

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_vectorized, y, test_size=0.2, random_state=42)

# Train an SVM model
model = SVC(kernel='linear')
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Model accuracy:", accuracy)

# Save the trained model
joblib.dump(model, 'xss_detection_model.joblib')
