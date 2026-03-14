"""

Model training script for Wine Quality prediction.
Trains and evaluates multiple ML models.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import joblib
import os
from preprocessing import WineDataPreprocessor


class WineModelTrainer:
    """Handles model training and evaluation."""
    
    def __init__(self, models_dir='models'):
        """Initialize the trainer."""
        self.models_dir = models_dir
        if not os.path.exists(models_dir):
            os.makedirs(models_dir)
        self.models = {}
        self.results = {}
    
    def train_random_forest(self, X_train, y_train, n_estimators=100, max_depth=15, random_state=42):
        """Train Random Forest model."""
        print("\nTraining Random Forest...")
        model = RandomForestRegressor(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=random_state,
            n_jobs=-1,
            min_samples_split=5,
            min_samples_leaf=2
        )
        model.fit(X_train, y_train)
        self.models['random_forest'] = model
        print("✓ Random Forest trained successfully")
        return model
    
    def train_gradient_boosting(self, X_train, y_train, n_estimators=100, learning_rate=0.1, random_state=42):
        """Train Gradient Boosting model."""
        print("Training Gradient Boosting...")
        model = GradientBoostingRegressor(
            n_estimators=n_estimators,
            learning_rate=learning_rate,
            max_depth=5,
            random_state=random_state,
            subsample=0.8
        )
        model.fit(X_train, y_train)
        self.models['gradient_boosting'] = model
        print("✓ Gradient Boosting trained successfully")
        return model
    
    def train_svr(self, X_train, y_train, kernel='rbf', C=100):
        """Train Support Vector Regression model."""
        print("Training Support Vector Regression...")
        model = SVR(kernel=kernel, C=C, epsilon=0.1, gamma='scale')
        model.fit(X_train, y_train)
        self.models['svr'] = model
        print("✓ SVR trained successfully")
        return model
    
    def evaluate_model(self, model, X_test, y_test, model_name):
        """Evaluate model performance."""
        y_pred = model.predict(X_test)
        
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        results = {
            'MSE': mse,
            'RMSE': rmse,
            'MAE': mae,
            'R2': r2
        }
        
        self.results[model_name] = results
        
        print(f"\n{model_name.upper()} Results:")
        print(f"  MSE:  {mse:.4f}")
        print(f"  RMSE: {rmse:.4f}")
        print(f"  MAE:  {mae:.4f}")
        print(f"  R²:   {r2:.4f}")
        
        return results, y_pred
    
    def compare_models(self):
        """Compare all trained models."""
        print("\n" + "="*60)
        print("MODEL COMPARISON")
        print("="*60)
        
        best_model = None
        best_score = -float('inf')
        best_model_name = None
        
        for model_name, metrics in self.results.items():
            r2 = metrics['R2']
            print(f"{model_name.upper():25} | R² Score: {r2:.4f}")
            
            if r2 > best_score:
                best_score = r2
                best_model_name = model_name
                best_model = self.models[model_name]
        
        print("="*60)
        print(f"Best Model: {best_model_name.upper()} with R² = {best_score:.4f}")
        print("="*60)
        
        return best_model, best_model_name
    
    def save_model(self, model, model_name, scaler):
        """Save model and scaler to disk."""
        model_path = os.path.join(self.models_dir, f'{model_name}_model.pkl')
        scaler_path = os.path.join(self.models_dir, 'scaler.pkl')
        
        joblib.dump(model, model_path)
        joblib.dump(scaler, scaler_path)
        
        print(f"Model saved to: {model_path}")
        print(f"Scaler saved to: {scaler_path}")
        
        return model_path, scaler_path


def download_dataset():
    """
    Instructions for downloading the dataset from Kaggle.
    """
    print("\n" + "="*70)
    print("DATASET DOWNLOAD INSTRUCTIONS")
    print("="*70)
    print("""
To download the wine quality dataset:

1. Visit: https://www.kaggle.com/datasets/uciml/red-wine-quality-cortez-et-al-2009
2. Sign in to Kaggle (create account if needed)
3. Click "Download" button
4. Extract the downloaded file
5. Place 'winequality-red.csv' in the 'data/' folder

Alternative (using Kaggle CLI):
    kaggle datasets download -d uciml/red-wine-quality-cortez-et-al-2009 -p data/
    unzip data/red-wine-quality-cortez-et-al-2009.zip -d data/

Confirm dataset location: data/winequality-red.csv
""")
    print("="*70 + "\n")


def main():
    """Main training pipeline."""
    print("\n" + "="*70)
    print("WINE QUALITY PREDICTION - MODEL TRAINING PIPELINE")
    print("="*70 + "\n")
    
    # Dataset path
    dataset_path = 'data/winequality-red.csv'
    
    # Check if dataset exists
    if not os.path.exists(dataset_path):
        print(f"❌ Dataset not found at: {dataset_path}")
        download_dataset()
        return
    
    # Initialize preprocessor
    print("Step 1: Loading and Preprocessing Data...")
    print("-" * 70)
    preprocessor = WineDataPreprocessor(data_path=dataset_path)
    
    # Load data
    df = preprocessor.load_data(dataset_path)
    
    # Preprocess data
    X_train, X_test, y_train, y_test, selected_features = preprocessor.preprocess(
        df, 
        target_col='quality',
        feature_selection_k=None,  # Keep all features
        remove_outliers_flag=True
    )
    
    # Initialize trainer
    print("\nStep 2: Training Multiple Models...")
    print("-" * 70)
    trainer = WineModelTrainer(models_dir='models')
    
    # Train models
    trainer.train_random_forest(X_train, y_train)
    trainer.train_gradient_boosting(X_train, y_train)
    trainer.train_svr(X_train, y_train)
    
    # Evaluate models
    print("\nStep 3: Evaluating Models...")
    print("-" * 70)
    
    for model_name, model in trainer.models.items():
        trainer.evaluate_model(model, X_test, y_test, model_name)
    
    # Compare and select best model
    print("\nStep 4: Model Comparison and Selection...")
    print("-" * 70)
    best_model, best_model_name = trainer.compare_models()
    
    # Save best model
    print("\nStep 5: Saving Best Model...")
    print("-" * 70)
    trainer.save_model(best_model, best_model_name, preprocessor.get_scaler())
    
    # Save feature names
    feature_names_path = os.path.join('models', 'feature_names.pkl')
    joblib.dump(selected_features, feature_names_path)
    print(f"Feature names saved to: {feature_names_path}")
    
    print("\n" + "="*70)
    print("✓ TRAINING COMPLETED SUCCESSFULLY!")
    print("="*70)
    print(f"\nNext step: Run the web application with 'python app.py'")
    print("Then visit http://localhost:5000 to make predictions!\n")


if __name__ == '__main__':
    main()
