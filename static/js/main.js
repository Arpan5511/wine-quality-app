// Wine Quality Prediction - Frontend JavaScript

// Global state
let predictionChart = null;
let currentPrediction = null;
let sampleData = {};

// Initialize application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    console.log('Initializing Wine Quality Prediction Application...');
    
    // Check model status
    checkModelStatus();
    
    // Load feature information
    loadFeatures();
    
    // Load sample data
    loadSampleData();
    
    // Setup event listeners
    setupEventListeners();
}

function setupEventListeners() {
    // Form submission
    document.getElementById('prediction-form').addEventListener('submit', handlePrediction);
    
    // Form buttons
    document.getElementById('reset-btn').addEventListener('click', resetForm);
    document.getElementById('sample-btn').addEventListener('click', showSampleSelector);
    
    // Results navigation
    document.getElementById('new-prediction-btn').addEventListener('click', () => {
        document.getElementById('results-section').style.display = 'none';
        document.getElementById('prediction-form').scrollIntoView({ behavior: 'smooth' });
    });
    
    // Modal close buttons
    document.getElementById('close-error').addEventListener('click', closeErrorModal);
    document.getElementById('error-ok').addEventListener('click', closeErrorModal);
}

async function checkModelStatus() {
    try {
        const response = await fetch('/health');
        const data = await response.json();
        
        const statusBadge = document.getElementById('status-badge');
        const statusText = document.getElementById('status-text');
        
        if (data.model_loaded) {
            statusBadge.classList.add('ready');
            statusText.textContent = '✓ Model Ready';
            document.getElementById('prediction-form').style.opacity = '1';
        } else {
            statusBadge.classList.add('error');
            statusText.textContent = '✗ Model Not Loaded';
            document.getElementById('prediction-form').style.opacity = '0.5';
            document.getElementById('prediction-form').style.pointerEvents = 'none';
            showErrorModal('Model not loaded. Please run "python train.py" to train the model first.');
        }
    } catch (error) {
        console.error('Error checking model status:', error);
        showErrorModal('Failed to connect to server.');
    }
}

async function loadFeatures() {
    try {
        const response = await fetch('/api/features');
        const data = await response.json();
        
        const featuresList = document.getElementById('features-list');
        featuresList.innerHTML = '';
        
        for (const [featureName, details] of Object.entries(data.feature_details)) {
            const featureDetail = document.createElement('div');
            featureDetail.className = 'feature-detail';
            featureDetail.innerHTML = `
                <div class="feature-name">${featureName.toUpperCase()}</div>
                <div class="feature-description">${details.description}</div>
                <div class="feature-range">Unit: ${details.unit} | Range: ${details.typical_min} - ${details.typical_max}</div>
            `;
            featuresList.appendChild(featureDetail);
        }
    } catch (error) {
        console.error('Error loading features:', error);
    }
}

async function loadSampleData() {
    try {
        const response = await fetch('/api/sample-data');
        const data = await response.json();
        sampleData = data;
        
        const samplesGrid = document.getElementById('samples-grid');
        samplesGrid.innerHTML = '';
        
        for (const [key, sample] of Object.entries(data)) {
            const sampleItem = document.createElement('div');
            sampleItem.className = 'sample-item';
            sampleItem.innerHTML = `
                <div class="sample-name">${sample.name}</div>
                <div class="sample-description">Click to load into form</div>
            `;
            sampleItem.addEventListener('click', () => loadSampleToForm(sample.data));
            samplesGrid.appendChild(sampleItem);
        }
    } catch (error) {
        console.error('Error loading sample data:', error);
    }
}

function loadSampleToForm(data) {
    for (const [key, value] of Object.entries(data)) {
        const input = document.getElementById(key);
        if (input) {
            input.value = value;
        }
    }
    document.getElementById('prediction-form').scrollIntoView({ behavior: 'smooth' });
}

function showSampleSelector() {
    const firstSample = Object.values(sampleData)[0];
    if (firstSample) {
        loadSampleToForm(firstSample.data);
    }
}

async function handlePrediction(event) {
    event.preventDefault();
    
    // Get form data
    const formData = new FormData(document.getElementById('prediction-form'));
    const data = {
        fixed_acidity: parseFloat(formData.get('fixed_acidity')),
        volatile_acidity: parseFloat(formData.get('volatile_acidity')),
        citric_acid: parseFloat(formData.get('citric_acid')),
        residual_sugar: parseFloat(formData.get('residual_sugar')),
        chlorides: parseFloat(formData.get('chlorides')),
        free_sulfur_dioxide: parseFloat(formData.get('free_sulfur_dioxide')),
        total_sulfur_dioxide: parseFloat(formData.get('total_sulfur_dioxide')),
        density: parseFloat(formData.get('density')),
        pH: parseFloat(formData.get('pH')),
        sulphates: parseFloat(formData.get('sulphates')),
        alcohol: parseFloat(formData.get('alcohol'))
    };
    
    // Validate data
    if (!validateFormData(data)) {
        showErrorModal('Please fill in all fields with valid numbers.');
        return;
    }
    
    // Show loading state
    const predictBtn = document.getElementById('predict-btn');
    const btnText = predictBtn.querySelector('.btn-text');
    const btnLoader = document.getElementById('btn-loader');
    predictBtn.disabled = true;
    btnText.style.display = 'none';
    btnLoader.style.display = 'inline';
    
    try {
        const response = await fetch('/api/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (response.ok && result.success) {
            currentPrediction = result;
            displayResults(result, data);
        } else {
            showErrorModal(result.error || 'Prediction failed. Please try again.');
        }
    } catch (error) {
        console.error('Prediction error:', error);
        showErrorModal('Error making prediction. Please try again.');
    } finally {
        // Restore button state
        predictBtn.disabled = false;
        btnText.style.display = 'inline';
        btnLoader.style.display = 'none';
    }
}

function validateFormData(data) {
    for (const value of Object.values(data)) {
        if (isNaN(value) || value === null || value === '') {
            return false;
        }
    }
    return true;
}

function displayResults(prediction, inputData) {
    // Show results section
    const resultsSection = document.getElementById('results-section');
    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth' });
    
    // Update score display
    const scoreNumber = document.getElementById('score-number');
    const scoreFill = document.getElementById('score-bar-fill');
    const categoryBadge = document.getElementById('category-badge');
    const categoryDescription = document.getElementById('category-description');
    const qualityText = document.getElementById('quality-text');
    
    const score = prediction.prediction;
    const category = prediction.category;
    
    // Animate score
    animateValue(scoreNumber, 0, score, 1000);
    animateValue(scoreFill, 0, (score / 10) * 100, 1000, '%');
    
    // Update category
    categoryBadge.textContent = category;
    categoryBadge.className = `category-badge ${category.toLowerCase()}`;
    
    // Set description and quality text
    const descriptions = {
        'Poor': {
            text: 'This wine has significant quality issues. It may have excessive acidity, poor balance, or oxidation problems.',
            color: '#e74c3c'
        },
        'Average': {
            text: 'This wine is acceptable with some room for improvement. It has decent chemical balance but lacks distinction.',
            color: '#f39c12'
        },
        'Good': {
            text: 'This wine demonstrates good quality with well-balanced chemical properties. It should be enjoyable.',
            color: '#27ae60'
        },
        'Excellent': {
            text: 'This wine shows excellent quality with superior chemical balance and composition. Highly recommended!',
            color: '#2980b9'
        }
    };
    
    const desc = descriptions[category];
    categoryDescription.textContent = `(${score.toFixed(1)}/10)`;
    qualityText.textContent = desc.text;
    qualityText.parentElement.style.borderLeftColor = desc.color;
    
    // Update chart
    updateChart(inputData);
}

function animateValue(element, start, end, duration, unit = '') {
    const startTime = performance.now();
    
    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const value = start + (end - start) * progress;
        
        if (unit === '%') {
            element.style.width = value.toFixed(0) + unit;
        } else {
            element.textContent = value.toFixed(2);
        }
        
        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }
    
    requestAnimationFrame(update);
}

function updateChart(data) {
    const ctx = document.getElementById('predictionChart').getContext('2d');
    
    // Destroy existing chart if it exists
    if (predictionChart) {
        predictionChart.destroy();
    }
    
    const features = Object.keys(data);
    const values = Object.values(data);
    
    // Normalize values to 0-10 scale for visualization
    const normalizedValues = values.map((val, idx) => {
        const ranges = {
            0: [4.6, 15.9],      // fixed_acidity
            1: [0.12, 1.58],     // volatile_acidity
            2: [0, 1],            // citric_acid
            3: [0.9, 15.5],      // residual_sugar
            4: [0.012, 0.611],   // chlorides
            5: [1, 72],           // free_sulfur_dioxide
            6: [6, 289],          // total_sulfur_dioxide
            7: [0.9901, 1.0037], // density
            8: [2.74, 4.01],     // pH
            9: [0.33, 2],        // sulphates
            10: [8.4, 14.9]      // alcohol
        };
        
        const [min, max] = ranges[idx] || [0, 100];
        return ((val - min) / (max - min)) * 10;
    });
    
    predictionChart = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: features.map(f => f.replace(/_/g, ' ').toUpperCase()),
            datasets: [{
                label: 'Wine Properties',
                data: normalizedValues,
                borderColor: '#8B0000',
                backgroundColor: 'rgba(139, 0, 0, 0.1)',
                pointBackgroundColor: '#8B0000',
                pointBorderColor: '#fff',
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: '#8B0000',
                pointRadius: 5,
                pointHoverRadius: 7,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                r: {
                    beginAtZero: true,
                    max: 10,
                    ticks: {
                        stepSize: 2
                    }
                }
            },
            plugins: {
                legend: {
                    labels: {
                        font: { size: 12 }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return context.label + ': ' + context.parsed.r.toFixed(2);
                        }
                    }
                }
            }
        }
    });
}

function resetForm() {
    document.getElementById('prediction-form').reset();
    document.getElementById('results-section').style.display = 'none';
}

function showErrorModal(message) {
    document.getElementById('error-message').textContent = message;
    document.getElementById('error-modal').style.display = 'block';
}

function closeErrorModal() {
    document.getElementById('error-modal').style.display = 'none';
}

// Close modal when clicking outside
window.addEventListener('click', function(event) {
    const modal = document.getElementById('error-modal');
    if (event.target === modal) {
        modal.style.display = 'none';
    }
});
