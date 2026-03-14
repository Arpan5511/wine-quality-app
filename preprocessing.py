"""
Data preprocessing module for Wine Quality prediction.
Handles data loading, cleaning, feature engineering, and normalization.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectKBest, f_regression, mutual_info_regression
import os
import warnings

warnings.filterwarnings('ignore')


class WineDataPreprocessor:
    """Handles all data preprocessing for wine quality prediction."""
    
    def __init__(self, data_path=None, test_size=0.2, random_state=42):
        """
        Initialize the preprocessor.
        
        Args:
            data_path: Path to the CSV dataset
            test_size: Proportion of data for testing
            random_state: Random seed for reproducibility
        """
        self.data_path = data_path
        self.test_size = test_size
        self.random_state = random_state
        self.scaler = StandardScaler()
        self.feature_names = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        
    def load_data(self, file_path=None):
        """Load wine quality dataset."""
        if file_path is None:
            file_path = self.data_path
            
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Dataset not found at {file_path}")
        
        df = pd.read_csv(file_path, sep=';')
        print(f"Dataset loaded: {df.shape[0]} samples, {df.shape[1]} features")
        return df
    
    def handle_missing_values(self, df):
        """Handle missing values in the dataset."""
        print(f"\nMissing values before handling:\n{df.isnull().sum()}")
        
        # Fill missing numeric values with median
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if df[col].isnull().sum() > 0:
                df[col].fillna(df[col].median(), inplace=True)
        
        print(f"Missing values after handling:\n{df.isnull().sum()}")
        return df
    
    def remove_outliers(self, df, threshold=3):
        """Remove outliers using z-score method."""
        from scipy import stats
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        initial_shape = df.shape[0]
        
        # Calculate z-scores and remove rows with outliers
        z_scores = np.abs(stats.zscore(df[numeric_cols]))
        df = df[(z_scores < threshold).all(axis=1)]
        
        removed = initial_shape - df.shape[0]
        print(f"Removed {removed} outliers using z-score threshold of {threshold}")
        return df
    
    def feature_selection(self, X, y, k=10, method='f_regression'):
        """
        Select top K features using feature selection methods.
        
        Args:
            X: Feature matrix
            y: Target vector
            k: Number of features to select
            method: 'f_regression' or 'mutual_info'
        """
        if method == 'mutual_info':
            selector = SelectKBest(score_func=mutual_info_regression, k=k)
        else:
            selector = SelectKBest(score_func=f_regression, k=k)
        
        X_selected = selector.fit_transform(X, y)
        selected_features = X.columns[selector.get_support()].tolist()
        
        print(f"\nSelected {k} best features: {selected_features}")
        return X_selected, selected_features
    
    def preprocess(self, df, target_col='quality', feature_selection_k=None, 
                   remove_outliers_flag=True):
        """
        Complete preprocessing pipeline.
        
        Args:
            df: DataFrame to preprocess
            target_col: Name of target column
            feature_selection_k: Number of features to select (None to keep all)
            remove_outliers_flag: Whether to remove outliers
        
        Returns:
            X_train, X_test, y_train, y_test, selected_features
        """
        print("="*50)
        print("PREPROCESSING PIPELINE")
        print("="*50)
        
        # Step 1: Handle missing values
        df = self.handle_missing_values(df)
        
        # Step 2: Remove outliers
        if remove_outliers_flag:
            df = self.remove_outliers(df)
        
        # Step 3: Separate features and target
        X = df.drop(columns=[target_col])
        y = df[target_col]
        
        self.feature_names = X.columns.tolist()
        
        print(f"\nDataset shape after preprocessing: {X.shape}")
        print(f"Target distribution:\n{y.value_counts().sort_index()}")
        
        # Step 4: Feature selection (optional)
        selected_features = self.feature_names
        if feature_selection_k and feature_selection_k < X.shape[1]:
            X, selected_features = self.feature_selection(X, y, k=feature_selection_k)
            X = pd.DataFrame(X, columns=selected_features)
        
        # Step 5: Train-test split
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=self.test_size, random_state=self.random_state, stratify=y
        )
        
        print(f"\nTrain set size: {self.X_train.shape}")
        print(f"Test set size: {self.X_test.shape}")
        
        # Step 6: Feature scaling
        self.X_train = self.scaler.fit_transform(self.X_train)
        self.X_test = self.scaler.transform(self.X_test)
        
        print("\nFeatures scaled using StandardScaler")
        print("="*50)
        
        return self.X_train, self.X_test, self.y_train, self.y_test, selected_features
    
    def get_scaler(self):
        """Return the fitted scaler for inference."""
        return self.scaler
    
    def get_feature_names(self):
        """Return the feature names used in training."""
        return self.feature_names


def preprocess_single_sample(sample_dict, scaler, feature_names):
    """
    Preprocess a single sample for prediction.
    
    Args:
        sample_dict: Dictionary with feature values
        scaler: Fitted StandardScaler
        feature_names: List of feature names
    
    Returns:
        Scaled sample array
    """
    # Create array in correct feature order
    sample = np.array([sample_dict.get(feature, 0) for feature in feature_names]).reshape(1, -1)
    
    # Scale the sample
    scaled_sample = scaler.transform(sample)
    
    return scaled_sample
