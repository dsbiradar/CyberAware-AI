# train.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
import joblib

# Load dataset
df = pd.read_csv("cyber_dataset.csv")
X, y = df["text"], df["label"]

# Train-test split (stratified)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Pipeline with Tfidf and Naive Bayes
model = Pipeline([
    ("tfidf", TfidfVectorizer(max_features=10000, ngram_range=(1,2), stop_words='english')),
    ("clf", MultinomialNB())
])

# Train
model.fit(X_train, y_train)

# Evaluate
accuracy = model.score(X_test, y_test)
print("✅ Model Accuracy:", accuracy)

# Save model
joblib.dump(model, "cyber_model.pkl")
print("✅ Model saved: cyber_model.pkl")
