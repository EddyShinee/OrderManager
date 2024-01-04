import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, roc_auc_score
import joblib

# Tạo dữ liệu giả định
np.random.seed(42)
data_size = 100
data = {
    "Open": np.random.rand(data_size) * 100,
    "High": np.random.rand(data_size) * 100,
    "Low": np.random.rand(data_size) * 100,
    "Close": np.random.rand(data_size) * 100,
    "Volume": np.random.rand(data_size) * 1000
}
stock_data = pd.DataFrame(data)

# Tính đặc trưng và tạo nhãn
stock_data['Target'] = ((stock_data['Close'] - stock_data['Open']) > 0).astype(int)
stock_data['MA_5'] = stock_data['Close'].rolling(window=5).mean().fillna(method='bfill')

# Chia dữ liệu
X = stock_data[['Open', 'High', 'Low', 'Close', 'Volume', 'MA_5']]
y = stock_data['Target']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Huấn luyện mô hình
clf = DecisionTreeClassifier(random_state=42)
param_grid = {
    'criterion': ['gini', 'entropy'],
    'max_depth': [None, 10, 20, 30, 40, 50],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}
grid_search = GridSearchCV(clf, param_grid, cv=5, scoring='accuracy')
grid_search.fit(X_train, y_train)

# Mô hình tối ưu
best_clf = grid_search.best_estimator_

# Đánh giá mô hình
predictions = best_clf.predict(X_test)
print("Classification Report:")
print(classification_report(y_test, predictions))
print("ROC AUC Score:", roc_auc_score(y_test, predictions))

# Lưu mô hình
joblib.dump(best_clf, 'decision_tree_model.joblib')

# Giả sử bạn có dữ liệu mới và muốn dự đoán
# Ví dụ: new_data = pd.DataFrame(...)
# predictions_new = best_clf.predict(new_data)
# decisions = ['Buy' if pred == 1 else 'Sell' for pred in predictions_new]
# print(decisions)
