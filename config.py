"""
Configuration file for Wine Quality Prediction application.
"""

import os

# Application settings
DEBUG = True
TESTING = False

# Data settings
DATA_PATH = 'data/winequality-red.csv'
MODELS_PATH = 'models/'

# Model settings
TEST_SIZE = 0.2
RANDOM_STATE = 42
FEATURE_SELECTION_K = None  # None to keep all features

# Training settings
TRAIN_RANDOM_FOREST = True
TRAIN_GRADIENT_BOOSTING = True
TRAIN_SVR = True

# Random Forest hyperparameters
RF_N_ESTIMATORS = 100
RF_MAX_DEPTH = 15
RF_MIN_SAMPLES_SPLIT = 5
RF_MIN_SAMPLES_LEAF = 2

# Gradient Boosting hyperparameters
GB_N_ESTIMATORS = 100
GB_LEARNING_RATE = 0.1
GB_MAX_DEPTH = 5
GB_SUBSAMPLE = 0.8

# SVR hyperparameters
SVR_KERNEL = 'rbf'
SVR_C = 100
SVR_EPSILON = 0.1

# Feature names
FEATURE_NAMES = [
    'fixed acidity',
    'volatile acidity',
    'citric acid',
    'residual sugar',
    'chlorides',
    'free sulfur dioxide',
    'total sulfur dioxide',
    'density',
    'pH',
    'sulphates',
    'alcohol'
]

# Target column
TARGET_COLUMN = 'quality'

# Quality categories
QUALITY_CATEGORIES = {
    'poor': (0, 4),
    'average': (4, 6),
    'good': (6, 8),
    'excellent': (8, 10)
}

# Typical ranges for features
FEATURE_RANGES = {
    'fixed acidity': (4.6, 15.9),
    'volatile acidity': (0.12, 1.58),
    'citric acid': (0, 1),
    'residual sugar': (0.9, 15.5),
    'chlorides': (0.012, 0.611),
    'free sulfur dioxide': (1, 72),
    'total sulfur dioxide': (6, 289),
    'density': (0.9901, 1.0037),
    'pH': (2.74, 4.01),
    'sulphates': (0.33, 2),
    'alcohol': (8.4, 14.9)
}
