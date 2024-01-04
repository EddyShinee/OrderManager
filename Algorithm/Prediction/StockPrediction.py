import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, roc_auc_score
import joblib

class StockPredictor:
    def __init__(self):
        self.model = None

    def train_model(self, data, feature_columns, target_column):
        X = data[feature_columns]
        y = data[target_column]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        param_grid = {
            'criterion': ['gini', 'entropy'],
            'max_depth': [None, 10, 20, 30, 40, 50],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4]
        }
        grid_search = GridSearchCV(DecisionTreeClassifier(random_state=42), param_grid, cv=5, scoring='accuracy')
        grid_search.fit(X_train, y_train)
        self.model = grid_search.best_estimator_

        predictions = self.model.predict(X_test)
        print("Classification Report:")
        print(classification_report(y_test, predictions))
        print("ROC AUC Score:", roc_auc_score(y_test, predictions))

    def save_model(self, filename):
        joblib.dump(self.model, filename)

    def load_model(self, filename):
        self.model = joblib.load(filename)

    def predict(self, X_new):
        return self.model.predict(X_new)

# Ví dụ sử dụng class
# Giả sử bạn có một DataFrame thực tế 'real_data' với các cột cần thiết
# feature_columns = ['Open', 'High', 'Low', 'Close', 'Volume', 'MA_5']
# target_column = 'Target'

# predictor = StockPredictor()
# predictor.train_model(real_data, feature_columns, target_column)
# predictor.save_model('decision_tree_model.joblib')

# Để dự đoán với dữ liệu mới
# X_new = pd.DataFrame(...)  # Tạo DataFrame mới
# predictions = predictor.predict(X_new)
