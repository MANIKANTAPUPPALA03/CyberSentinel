import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from feature_extraction import extract_features

# Load dataset
data = pd.read_csv("malicious_phish.csv")

# Convert text labels to numeric
# 'benign' -> 0, everything else (phishing, malware, defacement) -> 1
data["label"] = data["type"].apply(lambda x: 0 if x == "benign" else 1)

print(f"Dataset loaded: {len(data)} URLs")
print(f"Benign: {len(data[data['label'] == 0])}, Malicious: {len(data[data['label'] == 1])}")

# Extract features
print("Extracting features (enhanced)...")
X = data["url"].apply(extract_features).tolist()
y = data["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("Training optimized model...")
model = RandomForestClassifier(
    n_estimators=300,           # More trees
    max_depth=20,               # Prevent overfitting
    min_samples_split=5,
    min_samples_leaf=2,
    class_weight="balanced",    # Handle imbalanced classes
    random_state=42,
    n_jobs=-1                   # Use all CPU cores
)
model.fit(X_train, y_train)

accuracy = model.score(X_test, y_test)
print(f"Model accuracy: {accuracy:.4f}")

# Show feature importance
from feature_extraction import FEATURE_NAMES
importances = sorted(zip(FEATURE_NAMES, model.feature_importances_), key=lambda x: -x[1])
print("\nTop 10 most important features:")
for name, imp in importances[:10]:
    print(f"  {name}: {imp:.4f}")

joblib.dump(model, "model.pkl")
print("\nModel saved to model.pkl")
