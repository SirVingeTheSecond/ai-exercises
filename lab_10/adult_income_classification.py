"""
Lab 10 ▸ Exercise 2 — Decision-Tree on Adult-Income
==================================================
Pipeline:  One-Hot categorical  + passthrough numeric  →  DecisionTree.
"""

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.pipeline import Pipeline
from sklearn.metrics import ConfusionMatrixDisplay

# ── load ------------------------------------------------------------------- #
df = pd.read_csv("adult_income.csv")               # <- file from Lab 10

X = df.drop("income_high", axis=1)
y = df["income_high"]

cat_cols = X.select_dtypes("object").columns.tolist()
num_cols = X.select_dtypes(exclude="object").columns.tolist()

pre = ColumnTransformer(
    [("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
     ("num", "passthrough",                        num_cols)]
)

pipe = Pipeline([
    ("prep", pre),
    ("clf",  DecisionTreeClassifier(random_state=0))
])

param_grid = {
    "clf__criterion":          ["entropy", "gini"],
    "clf__max_depth":          [4, 6, 8, None],
    "clf__min_samples_leaf":   [1, 5, 10],
    "clf__ccp_alpha":          [0.0, 0.002, 0.005],
}

X_tr, X_te, y_tr, y_te = train_test_split(
    X, y, test_size=.2, stratify=y, random_state=0
)

grid = GridSearchCV(pipe, param_grid, cv=5, n_jobs=-1)
grid.fit(X_tr, y_tr)

best = grid.best_estimator_
print("Best hyper-parameters:", grid.best_params_)
print("Train accuracy:", round(best.score(X_tr, y_tr), 3))
print("Test  accuracy:",  round(best.score(X_te, y_te), 3))

# ── confusion matrix ------------------------------------------------------- #
ConfusionMatrixDisplay.from_estimator(best, X_te, y_te)
plt.title("Adult-Income  —  Confusion Matrix")
plt.show()

# ── optional: show first 3 levels of the tree ------------------------------ #
plt.figure(figsize=(14, 7))
plot_tree(
    best.named_steps["clf"],
    max_depth=3,
    filled=True,
    fontsize=6
)
plt.title("Pruned Decision Tree  (top 3 levels)")
plt.show()
