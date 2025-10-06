✨ CareerPath Predictor: ML-Based Academic & Career Guidance System
This is a comprehensive, full-stack web application designed to provide students with personalized, data-driven recommendations for their future studies and career paths.

🚀 Key Features
Machine Learning Core: Utilizes a supervised classification model (trained in Studies Recommendations.ipynb on student-scores.csv) to predict suitable career aspirations.

Personalized Input: Accepts seven key subject scores (Math, Physics, English, etc.) along with self-study habits and extracurricular activities for tailored analysis.

Dynamic Visualization: The results page (results.html) presents career probabilities through interactive and engaging charts (Bar, Pie, Doughnut, and Radar) using Chart.js.

On-Demand PDF Report: A unique feature allowing users to download a professional, customized PDF summary of their scores, inputs, and final predictions, generated live using the ReportLab library within app.py.

Intuitive Web Interface: A clean, responsive, and modern design built with Bootstrap 5.

🛠️ Technology Stack
Component	Technology	Files
Backend & Web Framework	Python (3.x), Flask	app.py, package.json
Machine Learning	Scikit-learn, NumPy, Pandas	Studies Recommendations.ipynb, app.py
Data & Model Assets	CSV, Pickled Models (.pkl)	student-scores.csv, Models/scaler.pkl, Models/model.pkl
Frontend UI/UX	HTML5, CSS3, Bootstrap 5	home.html, recommend.html, results.html
Reporting & Visualization	ReportLab (PDF), Chart.js (Charts)	app.py, results.html


✨ CareerPath Predictor: ML-Based Academic & Career Guidance System
This is a comprehensive, full-stack web application designed to provide students with personalized, data-driven recommendations for their future studies and career paths.

🚀 Key Features
Machine Learning Core: Utilizes a supervised classification model (trained in Studies Recommendations.ipynb on student-scores.csv) to predict suitable career aspirations.

Personalized Input: Accepts seven key subject scores (Math, Physics, English, etc.) along with self-study habits and extracurricular activities for tailored analysis.

Dynamic Visualization: The results page (results.html) presents career probabilities through interactive and engaging charts (Bar, Pie, Doughnut, and Radar) using Chart.js.

On-Demand PDF Report: A unique feature allowing users to download a professional, customized PDF summary of their scores, inputs, and final predictions, generated live using the ReportLab library within app.py.

Intuitive Web Interface: A clean, responsive, and modern design built with Bootstrap 5.

🛠️ Technology Stack
Component	Technology	Files
Backend & Web Framework	Python (3.x), Flask	app.py, package.json
Machine Learning	Scikit-learn, NumPy, Pandas	Studies Recommendations.ipynb, app.py
Data & Model Assets	CSV, Pickled Models (.pkl)	student-scores.csv, Models/scaler.pkl, Models/model.pkl
Frontend UI/UX	HTML5, CSS3, Bootstrap 5	home.html, recommend.html, results.html
Reporting & Visualization	ReportLab (PDF), Chart.js (Charts)	app.py, results.html

Export to Sheets
📁 Repository Structure
app.py: The main Flask application file, handling routing, ML predictions, and PDF report generation.

Studies Recommendations.ipynb: Jupyter Notebook detailing the data cleaning, feature engineering, model training, and saving of the ML model and scaler.

student-scores.csv: The dataset used for training the classification model.

templates/: Directory containing HTML files (home.html, recommend.html, results.html).

Models/: Directory to store the pre-trained model.pkl and scaler.pkl objects.

⚙️ How to Run Locally
Clone the Repository: git clone <repository-url>

Install Dependencies: (Ensure all Python packages like Flask, scikit-learn, reportlab, pandas are installed.)

Run the Flask App: python app.py

Access: Open your browser to the local server address (e.g., http://127.0.0.1:5000/).
