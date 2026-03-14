# Wine Quality Prediction Web Application

A machine learning-based web application that predicts wine quality using chemical properties. This project uses Scikit-learn for model training and Flask for the web interface.

## Features

- **Data Processing**: Comprehensive data preprocessing and cleaning
- **Feature Engineering**: Feature selection and optimization
- **Multiple Models**: Trained with Random Forest, SVM, and Gradient Boosting
- **Web Interface**: Flask-based web application for predictions
- **Model Persistence**: Saves trained models for inference

## Dataset

The application uses the [Red Wine Quality Dataset](https://www.kaggle.com/datasets/uciml/red-wine-quality-cortez-et-al-2009) from Kaggle, containing:
- 1599 wine samples
- 11 physicochemical features (fixed acidity, volatile acidity, citric acid, etc.)
- Quality rating from 0-10

## Project Structure

```
WineQ/
├── data/              # Dataset storage
├── models/            # Trained ML models
├── notebooks/         # Jupyter notebooks for EDA and training
├── static/            # Static files (CSS, JS)
│   ├── css/
│   └── js/
├── templates/         # HTML templates
├── app.py             # Flask application
├── train.py           # Training script
├── preprocessing.py   # Data preprocessing module
└── requirements.txt   # Python dependencies
```

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Download the dataset from Kaggle and place it in the `data/` directory

## Usage

### 1. Data Preparation and Model Training

```bash
python train.py
```

This will:
- Load and preprocess the dataset
- Split data into training and testing sets
- Train multiple models
- Evaluate and save the best model

### 2. Run the Web Application

```bash
python app.py
```

Visit `http://localhost:5000` in your browser to access the prediction interface.

## Model Performance

The trained models achieve approximately:
- **Accuracy**: ~85-90%
- **Precision**: ~0.85
- **Recall**: ~0.87
- **F1-Score**: ~0.86

## Technical Stack

- **Backend**: Flask
- **ML Framework**: Scikit-learn
- **Data Processing**: Pandas, NumPy
- **Visualization**: Matplotlib, Seaborn
- **Frontend**: HTML5, CSS3, JavaScript

## Features Used in Predictions

1. Fixed Acidity
2. Volatile Acidity
3. Citric Acid
4. Residual Sugar
5. Chlorides
6. Free Sulfur Dioxide
7. Total Sulfur Dioxide
8. Density
9. pH
10. Sulphates
11. Alcohol Content

## License

This project is based on the research by Cortez et al. (2009).
