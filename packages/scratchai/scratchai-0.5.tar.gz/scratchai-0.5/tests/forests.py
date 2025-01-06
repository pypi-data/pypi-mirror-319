from scratchai.forests import RandomForestClassifier
from scratchai.metrics import accuracy
from tests.data import load_classification

X, y = load_classification(500)

model = RandomForestClassifier(50)
model.fit(X, y, oob_eval=True)
print(f"OOB score: {model.oob_score:.2f}")

y_pred = model.predict(X)
print(f"Accracy: {accuracy(y, y_pred):.2f}")