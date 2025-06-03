"""
Lab 10 ▸ Exercise 1 — Decision-Tree on Social Network Ads
=========================================================
Takeaways:
    • Check overfitting ➜ compare TRAIN vs TEST accuracy (or cross-val).
    • Fix via complexity params:  max_depth, min_samples_leaf, ccp_alpha.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score, ConfusionMatrixDisplay

# ── load data -------------------------------------------------------------- #
data = pd.read_csv("social_network_ads.csv")
X = data.iloc[:, :-1].values      # Age, EstimatedSalary
y = data.iloc[:, -1].values       # Purchased (0/1)

# visual exploration -------------------------------------------------------- #
plt.figure(figsize=(10,4))
for i, col in enumerate(data.columns[:-1], 1):
    plt.subplot(1,2,i)
    plt.hist(data[col], bins=10, color="steelblue", edgecolor="k")
    plt.title(col)
plt.tight_layout(); plt.show()

plt.figure(figsize=(6,6))
plt.scatter(X[y==0,0], X[y==0,1], c="orange", label="Not buy")
plt.scatter(X[y==1,0], X[y==1,1], c="dodgerblue", label="Buy")
plt.xlabel("Age"); plt.ylabel("Salary"); plt.legend(); plt.show()

# ── split ------------------------------------------------------------------ #
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=.2, random_state=0)

# ── baseline model (possible overfit) -------------------------------------- #
base = DecisionTreeClassifier(criterion="entropy", random_state=0)
base.fit(X_tr, y_tr)
base_train_acc = base.score(X_tr, y_tr)
base_test_acc  = base.score(X_te, y_te)
print(f"Baseline train acc={base_train_acc:.3f} | test acc={base_test_acc:.3f}")

# ── 5-fold CV for variance ---------------------------------------- #
cv_scores = cross_val_score(base, X, y, cv=5)
print("Baseline 5-fold CV mean=", cv_scores.mean().round(3))

# ── if gap > 0.1 -> treat as overfitting ----------------------------------- #
# to reduce complexity
best = DecisionTreeClassifier(
    criterion="entropy",
    max_depth=3,
    min_samples_leaf=5,
    ccp_alpha=0.002,      # minimal cost-complexity pruning
    random_state=0
).fit(X_tr, y_tr)

tuned_train_acc = best.score(X_tr, y_tr)
tuned_test_acc  = best.score(X_te, y_te)
print(f"Tuned    train acc={tuned_train_acc:.3f} | test acc={tuned_test_acc:.3f}")

# ── confusion matrix for tuned model -------------------------------------- #
ConfusionMatrixDisplay.from_estimator(best, X_te, y_te)
plt.title("Confusion matrix (tuned)"); plt.show()

# ── tree visual before / after -------------------------------------------- #
plt.figure(figsize=(12,4))
plt.subplot(1,2,1)
plot_tree(base, filled=True, feature_names=["Age","Salary"], class_names=["no","yes"], max_depth=3)
plt.title("Original tree (partial)")

plt.subplot(1,2,2)
plot_tree(best, filled=True, feature_names=["Age","Salary"], class_names=["no","yes"])
plt.title("Pruned tree")
plt.tight_layout(); plt.show()

# ── new sample ------------------------------------------------------------- #
sample = np.array([[30, 87_000]])
print("Prediction for [30, 87k] (tuned) ➜", best.predict(sample)[0])
