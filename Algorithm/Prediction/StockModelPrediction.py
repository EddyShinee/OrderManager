import logging

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.tree import DecisionTreeClassifier


class StockModelSelector:
    def __init__(self):
        self.column_transformer = None
        self.best_model = None
        logging.basicConfig(level=logging.INFO)

    def preprocess_data(self, data: pd.DataFrame, features: list, target: str) -> tuple:
        """
        Preprocess the data: imputing missing values and splitting into features and target.
        """
        if not all(item in data.columns for item in features + [target]):
            raise ValueError("Some features or target not found in the dataset.")

        X = data[features]
        y = data[target]

        self.column_transformer = ColumnTransformer(
            [('imputer', SimpleImputer(strategy='median'), features)],
            remainder='passthrough'
        )
        X_transformed = self.column_transformer.fit_transform(X)
        return pd.DataFrame(X_transformed, columns=features), y

    def train_model(self, X: pd.DataFrame, y: pd.Series) -> None:
        """
        Train the model using RandomizedSearchCV for hyperparameter tuning.
        """
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        cv_splits = max(2, min(5, np.min(np.bincount(y_train.astype(int)))))

        param_dist_tree = {'max_depth': [None, 10, 20], 'min_samples_split': [2, 5]}
        param_dist_forest = {'n_estimators': [50, 100, 200], 'max_depth': [None, 10, 20]}
        # Assuming each parameter grid has 6 combinations
        n_iter_tree = min(6, len(param_dist_tree['max_depth']) * len(param_dist_tree['min_samples_split']))
        n_iter_forest = min(6, len(param_dist_forest['n_estimators']) * len(param_dist_forest['max_depth']))

        tree_model = RandomizedSearchCV(DecisionTreeClassifier(random_state=42),
                                        param_dist_tree, cv=cv_splits, n_iter=n_iter_tree)
        forest_model = RandomizedSearchCV(RandomForestClassifier(random_state=42),
                                          param_dist_forest, cv=cv_splits, n_iter=n_iter_forest)

        tree_model.fit(X_train, y_train)
        forest_model.fit(X_train, y_train)

        if tree_model.best_score_ > forest_model.best_score_:
            self.best_model = tree_model.best_estimator_
            logging.info("Decision Tree selected with score: %s", tree_model.best_score_)
        else:
            self.best_model = forest_model.best_estimator_
            logging.info("Random Forest selected with score: %s", forest_model.best_score_)

    def train_and_evaluate(self, data: pd.DataFrame, features: list, target: str) -> None:
        """
        Train and evaluate the model.
        """
        X, y = self.preprocess_data(data, features, target)
        self.train_model(X, y)

    def predict(self, X_new: pd.DataFrame) -> np.ndarray:
        if self.best_model is None:
            raise Exception("No model is trained yet.")

        if not all(feature in X_new.columns for feature in self.column_transformer.transformers_[0][2]):
            raise ValueError("Missing features in the input data for prediction.")

        X_new_transformed = self.column_transformer.transform(X_new)

        # Use the original feature names if the transformations do not alter them
        return self.best_model.predict(
            pd.DataFrame(X_new_transformed, columns=self.column_transformer.transformers_[0][2]))

# Usage remains the same
