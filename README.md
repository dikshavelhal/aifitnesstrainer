# AI Fitness Trainer

## Overview
The AI Fitness Trainer is a computer vision-based virtual trainer that provides real-time exercise tracking, posture correction, and performance evaluation. Using **MediaPipe Pose Estimation** and **OpenCV**, it detects key body landmarks, analyzes movement, and offers automated feedback to improve workout accuracy and reduce the risk of injury.

## Features
- **Real-time Posture Analysis**: Detects and evaluates exercise form using pose estimation.
- **Automated Repetition Counter**: Tracks reps automatically to ensure accurate workout logging.
- **Voice Feedback System**: Provides real-time audio guidance for corrections and encouragement.
- **Exercise Support**: Recognizes multiple exercises with movement validation.

## Tech Stack
### **Frontend:**
- HTML
- CSS

### **Backend:**
- Python
- Flask
- OpenCV
- MediaPipe Pose
- NumPy
- Pygame (for audio feedback)

## Supported Exercises
The AI Fitness Trainer currently supports the following exercises:
**Upper Body:** Bicep Curl (Right Arm), Bicep Curl (Left Arm), Shoulder Press, Push-ups
**Lower Body:** Squats, Lunges (Left Leg), Lunges (Right Leg)
**Full Body and Abs:** Jumping Jacks, High Knees, Sit-ups, Plank, Frog Press

## Setup Instructions
### **1. Clone the Repository**
```sh
git clone <repository_url>
cd ai-fitness-trainer
```

### **2. Backend Setup**
```sh
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### **3. Frontend Setup**
Open `index.html` in a browser to access the web interface.

## Usage
- Start the Flask backend.
- Open the frontend in a browser.
- Select an exercise and start performing it.
- The system will count reps, provide real-time feedback, and alert you on incorrect posture.

## Screenshots
![Screenshot 2025-04-02 182113](https://github.com/user-attachments/assets/cbe79ae5-7f35-4ea6-b69d-e7ea50327578)
![Screenshot 2025-04-02 182230](https://github.com/user-attachments/assets/eff02377-42a8-41a2-a55b-d055d2fe897a)

## Future Improvements
- Integration of **3D pose estimation** for more accurate tracking.
- AI-powered personalized workout plans.
- Support for additional exercises like **yoga and advanced strength training**.

