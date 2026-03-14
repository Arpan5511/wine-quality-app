# Quick Start Guide for Wine Quality Prediction Web Application

## Overview
This is a machine learning-based web application for predicting red wine quality using chemical properties. The application uses Scikit-learn for model training and Flask for the web interface.

## Prerequisites
- Python 3.7+
- pip (Python package manager)
- Git (optional)

## Installation Steps

### 1. Create Virtual Environment
Open PowerShell/Command Prompt in the project directory and run:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Download Dataset
You have two options:

**Option A: Manual Download (Recommended)**
1. Visit: https://www.kaggle.com/datasets/uciml/red-wine-quality-cortez-et-al-2009
2. Sign in to Kaggle (create free account if needed)
3. Click the "Download" button
4. Extract the downloaded file
5. Place `winequality-red.csv` in the `data/` folder

**Option B: Kaggle CLI (If you have kaggle-cli installed)**
```bash
kaggle datasets download -d uciml/red-wine-quality-cortez-et-al-2009 -p data/
cd data
unzip red-wine-quality-cortez-et-al-2009.zip
```

### 4. Train the Model
```bash
python train.py
```

This will:
- Load and preprocess the dataset
- Train multiple ML models (Random Forest, Gradient Boosting, SVR)
- Evaluate each model
- Save the best model to the `models/` directory

**Expected Output:**
```
WINE QUALITY PREDICTION - MODEL TRAINING PIPELINE

Step 1: Loading and Preprocessing Data...
Dataset loaded: 1599 samples, 12 features

Step 2: Training Multiple Models...
Training Random Forest...
Training Gradient Boosting...
Training Support Vector Regression...

Step 3: Evaluating Models...
Step 4: Model Comparison and Selection...

✓ TRAINING COMPLETED SUCCESSFULLY!
```

### 5. Run the Web Application
```bash
python app.py
```

**Expected Output:**
```
WINE QUALITY PREDICTION - WEB APPLICATION

Loading model...
✓ Model, scaler, and features loaded successfully!

Starting Flask application...
Visit http://localhost:5000 to access the application
```

### 6. Access the Application
Open your web browser and navigate to:
```
http://localhost:5000
```

## Project Structure

```
WineQ/
├── data/                      # Dataset storage
│   └── winequality-red.csv   # Downloaded dataset
├── models/                    # Trained ML models
│   ├── gradient_boosting_model.pkl
│   ├── scaler.pkl
│   └── feature_names.pkl
├── notebooks/                 # Jupyter notebooks
├── static/                    # Static web files
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
├── templates/                 # HTML templates
│   └── index.html
├── app.py                     # Flask web application
├── train.py                   # Model training script
├── preprocessing.py           # Data preprocessing module
├── requirements.txt           # Python dependencies
├── SETUP.md                   # This file
└── README.md                  # Project documentation
```

## Features

### Chemical Properties Used
1. **Fixed Acidity** - Most acids involved in wine (tartaric acid)
2. **Volatile Acidity** - Acetic acid content (vinegar taste indicator)
3. **Citric Acid** - Freshness and flavor contributor
4. **Residual Sugar** - Sugar remaining after fermentation
5. **Chlorides** - Salt content
6. **Free Sulfur Dioxide** - Acts as preservative
7. **Total Sulfur Dioxide** - Total SO2 content
8. **Density** - Related to alcohol and sugar content
9. **pH** - Acidity level (0-14 scale)
10. **Sulphates** - Wine additive (antimicrobial/antioxidant)
11. **Alcohol** - Alcohol content by volume

### Quality Categories
- **Poor** (< 4.0) - Significant quality issues
- **Average** (4.0 - 6.0) - Acceptable with room for improvement
- **Good** (6.0 - 8.0) - Good quality, well-balanced
- **Excellent** (> 8.0) - Superior quality, highly recommended

## Using the Web Application

### Making Predictions
1. Enter the 11 chemical properties of your wine sample
2. Use the "Typical Range" hints as guidance
3. Click "Predict Quality" button
4. View the prediction results with visualization

### Loading Sample Data
- Click "Load Sample" button to populate form with example wines
- Or click on any sample in the "Sample Wines" section

### API Endpoints

**Prediction Endpoint:**
```bash
POST /api/predict
Content-Type: application/json

{
  "fixed_acidity": 7.4,
  "volatile_acidity": 0.7,
  "citric_acid": 0.0,
  "residual_sugar": 1.9,
  "chlorides": 0.076,
  "free_sulfur_dioxide": 11.0,
  "total_sulfur_dioxide": 34.0,
  "density": 0.9978,
  "pH": 3.51,
  "sulphates": 0.56,
  "alcohol": 9.4
}
```

**Get Features Info:**
```bash
GET /api/features
```

**Get Sample Data:**
```bash
GET /api/sample-data
```

**Health Check:**
```bash
GET /health
```

## Troubleshooting

### Model Not Loaded
**Problem:** "Model not loaded. Please train the model first."
**Solution:** Run `python train.py` to train the model

### Dataset Not Found
**Problem:** "Dataset not found at: data/winequality-red.csv"
**Solution:** Download the dataset from Kaggle and place it in the `data/` folder

### Port Already in Use
**Problem:** "Address already in use"
**Solution:** Change the port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Change 5000 to 5001
```

### Import Errors
**Problem:** "ModuleNotFoundError: No module named 'sklearn'"
**Solution:** Ensure virtual environment is activated and dependencies are installed:
```bash
venv\Scripts\activate
pip install -r requirements.txt
```

## Model Performance

The trained Gradient Boosting model typically achieves:
- **R² Score**: ~0.45-0.50 (explains 45-50% of variance)
- **RMSE**: ~0.65-0.75 (quality points)
- **MAE**: ~0.50-0.60 (mean absolute error)

## Deactivating Virtual Environment

When finished, deactivate the virtual environment:
```bash
deactivate
```

## Additional Resources

- [UCI Wine Quality Dataset](https://www.kaggle.com/datasets/uciml/red-wine-quality-cortez-et-al-2009)
- [Scikit-learn Documentation](https://scikit-learn.org/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the README.md for more detailed information
3. Check the console output for error messages
4. Ensure all dependencies are correctly installed

## License

This project is based on the research by Cortez et al. (2009) on red wine quality.
