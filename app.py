from flask import Flask, render_template, request, send_file, session
import pickle
import numpy as np
import pandas as pd
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.colors import HexColor, black
import datetime
import requests

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'a_very_secure_secret_key_for_sessions_12345'

# -----------------------------------------------------------
# Load Model and Scaler
# -----------------------------------------------------------
scaler = pickle.load(open("Models/scaler.pkl", 'rb'))
model = pickle.load(open("Models/model.pkl", 'rb'))
class_names = ['Lawyer', 'Doctor', 'Government Officer', 'Artist', 'Unknown',
               'Software Engineer', 'Teacher', 'Business Owner', 'Scientist',
               'Banker', 'Writer', 'Accountant', 'Designer',
               'Construction Engineer', 'Game Developer', 'Stock Investor',
               'Real Estate Developer']


# -----------------------------------------------------------
# Utility Functions
# -----------------------------------------------------------
def to_int(value, default=0):
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

def to_float(value, default=0.0):
    try:
        return float(value)
    except (ValueError, TypeError):
        return default
    
# -----------------------------------------------------------
# Career Recommendation Logic
# -----------------------------------------------------------

def Recommendations(gender, part_time_job, absence_days, extracurricular_activities,
                    weekly_self_study_hours, math_score, history_score, physics_score,
                    chemistry_score, biology_score, english_score, geography_score,
                    total_score, average_score):
    # Encode categorical variables
    gender_encoded = 1 if gender.lower() == 'female' else 0
    part_time_job_encoded = 1 if part_time_job else 0
    extracurricular_activities_encoded = 1 if extracurricular_activities else 0

    # Create feature array
    feature_array = np.array([[gender_encoded, part_time_job_encoded, absence_days, extracurricular_activities_encoded,
                               weekly_self_study_hours, math_score, history_score, physics_score,
                               chemistry_score, biology_score, english_score, geography_score, total_score,
                               average_score]])

    # Scale features
    scaled_features = scaler.transform(feature_array)

    # Predict using the model
    probabilities = model.predict_proba(scaled_features)

    # Get top five predicted classes along with their probabilities
    top_classes_idx = np.argsort(-probabilities[0])[:3]
    top_classes_names_probs = [(class_names[idx], probabilities[0][idx]) for idx in top_classes_idx]

    return top_classes_names_probs
# -----------------------------------------------------------
# YouTube Video Fetcher
# -----------------------------------------------------------
YOUTUBE_API_KEY = "AIzaSyDlib0s1iU21dXPd6YOmPd2ePpckSOWDsM"  

def fetch_youtube_videos(query, max_results=3):
    """Fetches at least 3 YouTube videos related to the given career/study name."""
    base_url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": f"{query} career guidance OR study tips OR introduction",
        "type": "video",
        "maxResults": max_results,
        "key": YOUTUBE_API_KEY,
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    videos = []
    if "items" in data:
        for item in data["items"]:
            video_id = item["id"]["videoId"]
            title = item["snippet"]["title"]
            thumbnail = item["snippet"]["thumbnails"]["medium"]["url"]
            videos.append({
                "title": title,
                "thumbnail": thumbnail,
                "url": f"https://www.youtube.com/embed/{video_id}"
            })

    # Ensure minimum 3 placeholders if API returns fewer
    while len(videos) < 3:
        videos.append({
            "title": "Career Insight Video",
            "thumbnail": "https://img.youtube.com/vi/dQw4w9WgXcQ/mqdefault.jpg",
            "url": "https://www.youtube.com/embed/dQw4w9WgXcQ"
        })
    return videos


# -----------------------------------------------------------
# Routes
# -----------------------------------------------------------
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/recommend')
def recommend():
    return render_template('recommend.html')

@app.route('/pred', methods=['POST','GET'])
def pred():
    if request.method == 'POST':
        gender = request.form['gender']
        part_time_job = request.form['part_time_job'] == 'true'
        absence_days = int(request.form['absence_days'])
        extracurricular_activities = request.form['extracurricular_activities'] == 'true'
        weekly_self_study_hours = int(request.form['weekly_self_study_hours'])
        math_score = int(request.form['math_score'])
        history_score = int(request.form['history_score'])
        physics_score = int(request.form['physics_score'])
        chemistry_score = int(request.form['chemistry_score'])
        biology_score = int(request.form['biology_score'])
        english_score = int(request.form['english_score'])
        geography_score = int(request.form['geography_score'])
        total_score = float(request.form['total_score'])
        average_score = float(request.form['average_score'])


        # Generate Recommendations
        recommendations = Recommendations(gender, part_time_job, absence_days, extracurricular_activities,
                                          weekly_self_study_hours, math_score, history_score, physics_score,
                                          chemistry_score, biology_score, english_score, geography_score,
                                          total_score, average_score)
        

         # Save for report download
        session['recommendations'] = recommendations
        session['user_input'] = {
            'Gender': gender.title(),
            'Part-Time Job': 'Yes' if part_time_job else 'No',
            'Absence Days': absence_days,
            'Extracurricular Activities': 'Yes' if extracurricular_activities else 'No',
            'Weekly Self-Study Hours': weekly_self_study_hours,
            'Total Score': f"{total_score:.2f}",
            'Average Score': f"{average_score:.2f}",
            'Math Score': math_score,
            'History Score': history_score,
            'Physics Score': physics_score,
            'Chemistry Score': chemistry_score,
            'Biology Score': biology_score,
            'English Score': english_score,
            'Geography Score': geography_score,
        }


        # 🆕 Fetch YouTube videos for each recommended study
        youtube_results = {}
        for career, _ in recommendations:
            youtube_results[career] = fetch_youtube_videos(career)

        session['recommendations'] = recommendations
        session['youtube_results'] = youtube_results

        return render_template('results.html', recommendations=recommendations, youtube_results=youtube_results)
    return render_template('home.html')

# -----------------------------------------------------------
# PDF Report Generation
# -----------------------------------------------------------
@app.route("/download_report")
def download_report():
    recommendations = session.get('recommendations')
    user_input = session.get('user_input')

    if not recommendations or not user_input:
        return "No recommendation data found. Please run the recommendation form first.", 404

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    margin = 60

    # --- Dark Theme Colors ---
    BG_COLOR = HexColor("#0B1221")          # Deep navy background
    CARD_BG = HexColor("#111827")           # Slightly lighter navy
    HEADER_COLOR = HexColor("#4F46E5")      # Indigo accent
    ACCENT_COLOR = HexColor("#06B6D4")      # Cyan accent
    TEXT_COLOR = colors.white               # Main text
    SUBTEXT_COLOR = HexColor("#A1A1AA")     # Light gray for subtext
    BORDER_COLOR = HexColor("#1F2937")      # Border lines

    # --- Background ---
    p.setFillColor(BG_COLOR)
    p.rect(0, 0, width, height, fill=1, stroke=0)

    # --- Header Section ---
    p.setFillColor(HEADER_COLOR)
    p.rect(0, height - 90, width, 90, fill=1, stroke=0)
    p.setFont("Helvetica-Bold", 26)
    p.setFillColor(colors.white)
    p.drawString(margin, height - 50, "Career Recommendation Report")

    p.setFont("Helvetica", 10)
    p.setFillColor(SUBTEXT_COLOR)
    p.drawRightString(width - margin, height - 65, f"Generated on {datetime.date.today():%B %d, %Y}")

    # --- Section 1: Top Recommended Careers ---
    y = height - 120
    p.setFillColor(ACCENT_COLOR)
    p.setFont("Helvetica-Bold", 16)
    p.drawString(margin, y, "Top Recommended Careers")

    y -= 12
    p.setFillColor(BORDER_COLOR)
    p.rect(margin, y - 1, width - 2 * margin, 1, fill=1, stroke=0)
    y -= 30

    card_height = 65
    for i, (career, prob) in enumerate(recommendations, 1):
        confidence = f"{prob * 100:.2f}%"

        # Draw background card
        p.setFillColor(CARD_BG)
        p.roundRect(margin, y - card_height + 10, width - 2 * margin, card_height, 8, stroke=0, fill=1)

        # Add border glow
        p.setStrokeColor(ACCENT_COLOR)
        p.setLineWidth(0.8)
        p.roundRect(margin, y - card_height + 10, width - 2 * margin, card_height, 8, stroke=1, fill=0)

        # Text inside card
        confidence = f"{(prob * 100):.2f}%"
        text_y = y - card_height / 2 + 10  # center vertically

        # Career Name (left)
        p.setFillColor(TEXT_COLOR)
        p.setFont("Helvetica-Bold", 13)
        p.drawString(margin + 25, text_y, f"{i}. {career}")

        # Confidence (right)
        p.setFont("Helvetica", 11)
        p.setFillColor(SUBTEXT_COLOR)
        p.drawRightString(width - margin - 25, text_y, f"Confidence: {confidence}")

        y -= card_height + 10
        if y < 160:
            p.showPage()
            # Redraw background for next page
            p.setFillColor(BG_COLOR)
            p.rect(0, 0, width, height, fill=1, stroke=0)
            y = height - 100

    # --- Section 2: User Input Summary ---
    y -= 10
    p.setFillColor(ACCENT_COLOR)
    p.setFont("Helvetica-Bold", 16)
    p.drawString(margin, y, "User Input Summary")

    y -= 12
    p.setFillColor(BORDER_COLOR)
    p.rect(margin, y - 1, width - 2 * margin, 1, fill=1, stroke=0)
    y -= 30

    # Display user inputs in grid (2 columns)
    col_gap = (width - 2 * margin) / 2
    items = list(user_input.items())
    line_height = 22

    for i, (key, val) in enumerate(items):
        col = 0 if i % 2 == 0 else 1
        x = margin + col * col_gap
        if col == 0 and i != 0:
            y -= line_height
        if y < 120:
            p.showPage()
            p.setFillColor(BG_COLOR)
            p.rect(0, 0, width, height, fill=1, stroke=0)
            y = height - 100

        # Draw labels
        p.setFillColor(SUBTEXT_COLOR)
        p.setFont("Helvetica-Bold", 10)
        p.drawString(x, y, f"{key}:")
        # Draw values with spacing
        p.setFillColor(TEXT_COLOR)
        p.setFont("Helvetica", 10)
        p.drawString(x + 130, y, str(val))

    # --- Footer Section ---
    p.setFillColor(HEADER_COLOR)
    p.rect(0, 0, width, 60, fill=1, stroke=0)
    p.setFillColor(colors.white)
    p.setFont("Helvetica-BoldOblique", 10)
    p.drawCentredString(width / 2, 35, "“Your career path begins with the right choice — keep exploring!”")

    p.setFont("Helvetica-Oblique", 8)
    p.setFillColor(SUBTEXT_COLOR)
    p.drawCentredString(width / 2, 18, f"© {datetime.date.today().year} CareerRecommend | Empowering Smarter Futures")

    # --- Finalize PDF ---
    p.save()
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="Career_Recommendation_Report.pdf",
        mimetype="application/pdf"
    )




# -----------------------------------------------------------
# Run Flask App
# -----------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
