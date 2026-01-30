# 💪 Workout Tracker App

A comprehensive Streamlit-based fitness tracking application with features for monitoring workouts, strength training, nutrition, and progress analysis.

## 🚀 Features

### 📊 Dashboard
- Quick stats: Daily workouts, minutes trained, BMI, calories logged
- Weekly activity overview with interactive bar charts
- Recent workout history at a glance

### ➕ Workout Logging
- Log daily workouts with date, time, duration, and intensity
- Track muscle groups for strength training (Chest, Shoulders, Triceps, Back, Biceps, Legs, Abs)
- Log cardio workouts with breakdown: Cycling, Treadmill, Elliptical
- Add notes for each workout
- Intensity levels: Light, Moderate, High, Extreme

### 🏋️ Strength Training
- Detailed strength exercise logging
- Track: Exercise name, weight, reps, sets, RPE (Rate of Perceived Exertion)
- Filter logs by muscle group
- Visualize progress over time for individual exercises
- Historical records with sortable data tables

### 📈 Progress Analytics
- **Muscle Groups Tab**: See total minutes trained per muscle group
- **Total Volume Tab**: Monthly training volume and workout type distribution
- **Weekly Report Tab**: Last 4 weeks summary with workout counts and averages
- Interactive charts using Plotly for better insights

### 🍽️ Nutrition Tracking
- Log meals by type (Breakfast, Lunch, Dinner, Snack)
- Track calories, protein, carbs, and fats
- Today's macro breakdown with pie chart
- Weekly calorie intake trend
- Daily calorie goal tracking
- Recent meals quick view

### ⚙️ Settings & Profile
- Body measurements: Height, weight, age
- Automatic BMI calculation with status
- Fitness goals: Weight Loss, Muscle Gain, General Fitness, Endurance
- Daily calorie goal setup
- Data management: Clear specific data sections
- Export all data as JSON

## 📋 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone or download the project**
   ```bash
   # If cloning
   git clone <repository-url>
   cd workout-tracker
   ```

2. **Create a virtual environment (optional but recommended)**
   ```bash
   python -m venv venv
   
   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app**
   ```bash
   streamlit run workout_tracker.py
   ```

The app will open in your default browser at `http://localhost:8501`

## 📖 Usage Guide

### Dashboard
- Start here to see your overall fitness summary
- View your weekly activity trend
- Check recent workouts

### Log Workout
1. Select date and time
2. Choose duration and intensity
3. Select workout type (Strength, Cardio, Flexibility, Sports)
4. If Strength: Input minutes for each muscle group
5. If Cardio: Specify minutes for cycling, treadmill, or elliptical
6. Add optional notes
7. Click "Save Workout"

### Strength Training
1. Enter exercise details (name, muscle group)
2. Input weight, reps, sets, and RPE
3. Add notes if needed
4. View your strength training history
5. Track individual exercise progress with charts

### Progress
- **Muscle Groups**: See which muscle groups you're training most
- **Total Volume**: Understand your overall training volume by month
- **Weekly Report**: Review your last 4 weeks of training

### Nutrition
1. Log meals with calories and macros (protein, carbs, fats)
2. View today's calorie and macro summary
3. See the pie chart of macro distribution
4. Track weekly calorie intake trends

### Settings
1. Update body measurements (height, weight, age)
2. Set fitness goal and daily calorie target
3. View calculated BMI and status
4. Manage data (clear sections or export as JSON)

## 💾 Data Storage

All data is automatically saved to JSON files in a `workout_data/` directory:
- `workouts.json` - All workout logs
- `strength_logs.json` - Strength training records
- `calories.json` - Nutrition logs
- `user_data.json` - Profile information and goals

Data persists between sessions, so your history is always available.

## 📊 Data Export

You can download all your data as a JSON file from Settings page. This is useful for:
- Backup purposes
- Sharing with a trainer
- Analyzing with other tools
- Migrating to another platform

## 🎨 Customization

The app uses Streamlit's built-in theming. You can customize appearance by creating a `.streamlit/config.toml` file:

```toml
[theme]
primaryColor = "#667eea"
backgroundColor = "#f0f2f6"
secondaryBackgroundColor = "#e0e0e0"
textColor = "#31333F"
```

## 🐛 Troubleshooting

**App doesn't start:**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (should be 3.8+)

**Data not saving:**
- Check that the `workout_data/` directory exists and is writable
- Verify file permissions

**Charts not displaying:**
- Ensure Plotly is installed: `pip install plotly`
- Check browser compatibility (modern browser recommended)

## 🚀 Future Enhancements

Potential features to add:
- Integration with fitness trackers (Fitbit, Apple Watch)
- Social features (share workouts, compare progress)
- AI-powered workout recommendations
- REST days tracking
- Injury log
- Supplement tracker
- User authentication for cloud sync
- Mobile app version

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## 📧 Support

For issues or questions, please create an issue in the repository.

---

**Happy Training! 💪**
