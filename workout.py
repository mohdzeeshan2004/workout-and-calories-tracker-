import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import json

# Configure Streamlit
st.set_page_config(
    page_title="💪 Workout Tracker",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    [data-testid="stMetricValue"] {
        font-size: 28px;
    }
    .metric-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'workouts' not in st.session_state:
    st.session_state.workouts = []
if 'strength_logs' not in st.session_state:
    st.session_state.strength_logs = []
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}
if 'calories' not in st.session_state:
    st.session_state.calories = []

# Data persistence
DATA_DIR = Path("workout_data")
DATA_DIR.mkdir(exist_ok=True)

def save_data():
    """Save all data to JSON files"""
    with open(DATA_DIR / "workouts.json", "w") as f:
        json.dump(st.session_state.workouts, f, default=str)
    with open(DATA_DIR / "strength_logs.json", "w") as f:
        json.dump(st.session_state.strength_logs, f, default=str)
    with open(DATA_DIR / "user_data.json", "w") as f:
        json.dump(st.session_state.user_data, f, default=str)
    with open(DATA_DIR / "calories.json", "w") as f:
        json.dump(st.session_state.calories, f, default=str)

def load_data():
    """Load all data from JSON files"""
    try:
        if (DATA_DIR / "workouts.json").exists():
            with open(DATA_DIR / "workouts.json", "r") as f:
                st.session_state.workouts = json.load(f)
        if (DATA_DIR / "strength_logs.json").exists():
            with open(DATA_DIR / "strength_logs.json", "r") as f:
                st.session_state.strength_logs = json.load(f)
        if (DATA_DIR / "user_data.json").exists():
            with open(DATA_DIR / "user_data.json", "r") as f:
                st.session_state.user_data = json.load(f)
        if (DATA_DIR / "calories.json").exists():
            with open(DATA_DIR / "calories.json", "r") as f:
                st.session_state.calories = json.load(f)
    except:
        pass

# Load data on startup
load_data()

# Sidebar Navigation
st.sidebar.title("💪 Workout Tracker")
page = st.sidebar.radio(
    "Navigation",
    ["📊 Dashboard", "➕ Log Workout", "🏋️ Strength Training", "📈 Progress", "🍽️ Nutrition", "⚙️ Settings"]
)

# ======================== DASHBOARD PAGE ========================
if page == "📊 Dashboard":
    st.title("Welcome to Your Fitness Dashboard")
    
    # Get today's stats
    today = datetime.now().date()
    today_workouts = [w for w in st.session_state.workouts if datetime.fromisoformat(w['date']).date() == today]
    today_minutes = sum([w['minutes'] for w in today_workouts])
    
    today_calories = [c for c in st.session_state.calories if datetime.fromisoformat(c['date']).date() == today]
    total_calories_in = sum([c['intake'] for c in today_calories])
    
    # Quick Stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Today's Workouts", len(today_workouts), "sessions")
    with col2:
        st.metric("Minutes Trained", today_minutes, "min")
    with col3:
        if st.session_state.user_data:
            bmi = st.session_state.user_data.get('bmi', 'N/A')
            st.metric("BMI", f"{bmi:.1f}" if isinstance(bmi, (int, float)) else bmi)
        else:
            st.metric("BMI", "No Data")
    with col4:
        st.metric("Calories Logged", total_calories_in, "kcal")
    
    # Weekly Overview
    st.subheader("📅 This Week's Activity")
    week_data = {}
    for i in range(7):
        date = today - timedelta(days=i)
        day_workouts = [w for w in st.session_state.workouts if datetime.fromisoformat(w['date']).date() == date]
        week_data[date.strftime("%a")] = sum([w['minutes'] for w in day_workouts])
    
    week_df = pd.DataFrame({
        "Day": list(week_data.keys())[::-1],
        "Minutes": list(week_data.values())[::-1]
    })
    
    fig = px.bar(week_df, x="Day", y="Minutes", 
                 color="Minutes", color_continuous_scale="Viridis",
                 title="Weekly Workout Minutes")
    st.plotly_chart(fig, use_container_width=True)
    
    # Latest workouts
    st.subheader("🏃 Recent Workouts")
    if st.session_state.workouts:
        recent = sorted(st.session_state.workouts, key=lambda x: x['date'], reverse=True)[:5]
        for workout in recent:
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.write(f"**{workout['date']}** - {workout['category']}")
            with col2:
                st.write(f"{workout['minutes']} min")
            with col3:
                st.write(f"💪 {workout['intensity']}")
    else:
        st.info("No workouts logged yet. Start tracking!")

# ======================== LOG WORKOUT PAGE ========================
elif page == "➕ Log Workout":
    st.title("Log Your Workout")
    
    col1, col2 = st.columns(2)
    
    with col1:
        workout_date = st.date_input("Date", value=datetime.now())
        workout_time = st.time_input("Time")
        minutes = st.number_input("Duration (minutes)", min_value=1, max_value=480, value=30)
    
    with col2:
        intensity = st.selectbox("Intensity", ["Light", "Moderate", "High", "Extreme"])
        category = st.selectbox("Workout Type", ["Strength", "Cardio", "Flexibility", "Sports"])
    
    # Muscle group targeting
    if category == "Strength":
        st.subheader("Muscle Groups Targeted")
        muscle_cols = st.columns(3)
        muscles = {}
        muscle_options = ["Chest", "Shoulders", "Triceps", "Back", "Biceps", "Legs", "Abs"]
        
        for idx, muscle in enumerate(muscle_options):
            with muscle_cols[idx % 3]:
                muscles[muscle] = st.number_input(f"{muscle} (minutes)", min_value=0, max_value=minutes, value=0)
        
        workout_data = {
            'date': str(workout_date),
            'time': str(workout_time),
            'minutes': minutes,
            'intensity': intensity,
            'category': category,
            'muscles': muscles,
            'notes': st.text_area("Notes")
        }
    
    # Cardio types
    elif category == "Cardio":
        st.subheader("Cardio Type")
        cardio_cols = st.columns(3)
        cardio = {}
        cardio_types = ["Cycling", "Treadmill", "Elliptical"]
        
        for idx, ctype in enumerate(cardio_types):
            with cardio_cols[idx]:
                cardio[ctype] = st.number_input(f"{ctype} (minutes)", min_value=0, max_value=minutes, value=0)
        
        workout_data = {
            'date': str(workout_date),
            'time': str(workout_time),
            'minutes': minutes,
            'intensity': intensity,
            'category': category,
            'cardio': cardio,
            'notes': st.text_area("Notes")
        }
    
    else:
        workout_data = {
            'date': str(workout_date),
            'time': str(workout_time),
            'minutes': minutes,
            'intensity': intensity,
            'category': category,
            'notes': st.text_area("Notes")
        }
    
    if st.button("✅ Save Workout", use_container_width=True):
        st.session_state.workouts.append(workout_data)
        save_data()
        st.success(f"Workout logged! {minutes} minutes of {category}")
        st.balloons()

# ======================== STRENGTH TRAINING PAGE ========================
elif page == "🏋️ Strength Training":
    st.title("Strength Training Log")
    
    col1, col2 = st.columns(2)
    
    with col1:
        exercise_name = st.text_input("Exercise Name", placeholder="e.g., Bench Press")
        muscle_group = st.selectbox("Muscle Group", ["Chest", "Shoulders", "Triceps", "Back", "Biceps", "Legs", "Abs"])
    
    with col2:
        log_date = st.date_input("Date", value=datetime.now())
        reps = st.number_input("Reps", min_value=1, max_value=100, value=10)
    
    col3, col4 = st.columns(2)
    
    with col3:
        weight = st.number_input("Weight (kg)", min_value=0.0, step=0.5, value=0.0)
        sets = st.number_input("Sets", min_value=1, max_value=10, value=3)
    
    with col4:
        rpe = st.slider("RPE (Rate of Perceived Exertion)", 1, 10, 7)
        notes = st.text_area("Notes")
    
    if st.button("💾 Save Strength Entry", use_container_width=True):
        strength_entry = {
            'date': str(log_date),
            'exercise': exercise_name,
            'muscle_group': muscle_group,
            'weight': weight,
            'reps': reps,
            'sets': sets,
            'rpe': rpe,
            'notes': notes
        }
        st.session_state.strength_logs.append(strength_entry)
        save_data()
        st.success(f"Strength log saved: {exercise_name}")
        st.balloons()
    
    # View strength logs
    st.subheader("📋 Strength Training History")
    if st.session_state.strength_logs:
        # Filter by muscle group
        muscle_filter = st.selectbox("Filter by Muscle Group", ["All"] + list(set([s['muscle_group'] for s in st.session_state.strength_logs])))
        
        filtered_logs = st.session_state.strength_logs
        if muscle_filter != "All":
            filtered_logs = [s for s in filtered_logs if s['muscle_group'] == muscle_filter]
        
        df_logs = pd.DataFrame(filtered_logs)
        df_logs = df_logs.sort_values('date', ascending=False)
        
        st.dataframe(df_logs, use_container_width=True)
        
        # Progress chart for top exercises
        if len(filtered_logs) > 0:
            exercises = list(set([s['exercise'] for s in filtered_logs]))
            selected_exercise = st.selectbox("Track Exercise Progress", exercises)
            
            exercise_data = sorted(
                [s for s in filtered_logs if s['exercise'] == selected_exercise],
                key=lambda x: x['date']
            )
            
            if exercise_data:
                df_progress = pd.DataFrame(exercise_data)
                df_progress['date'] = pd.to_datetime(df_progress['date'])
                
                fig = px.line(df_progress, x='date', y='weight', 
                             title=f"{selected_exercise} Progress",
                             markers=True, labels={'date': 'Date', 'weight': 'Weight (kg)'})
                st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No strength logs yet. Start tracking your lifts!")

# ======================== PROGRESS PAGE ========================
elif page == "📈 Progress":
    st.title("Your Progress")
    
    tab1, tab2, tab3 = st.tabs(["Muscle Groups", "Total Volume", "Weekly Report"])
    
    with tab1:
        st.subheader("🎯 Muscle Group Distribution")
        
        # Aggregate muscle group data
        muscle_totals = {muscle: 0 for muscle in ["Chest", "Shoulders", "Triceps", "Back", "Biceps", "Legs", "Abs"]}
        
        for workout in st.session_state.workouts:
            if 'muscles' in workout:
                for muscle, minutes in workout['muscles'].items():
                    muscle_totals[muscle] += minutes
        
        df_muscles = pd.DataFrame({
            "Muscle Group": list(muscle_totals.keys()),
            "Minutes": list(muscle_totals.values())
        }).sort_values("Minutes", ascending=True)
        
        fig = px.barh(df_muscles, x="Minutes", y="Muscle Group",
                     color="Minutes", color_continuous_scale="Teal",
                     title="Total Minutes by Muscle Group")
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("📊 Total Training Volume")
        
        # Monthly volume
        workout_df = pd.DataFrame(st.session_state.workouts)
        if not workout_df.empty:
            workout_df['date'] = pd.to_datetime(workout_df['date'])
            workout_df['month'] = workout_df['date'].dt.to_period('M')
            
            monthly_volume = workout_df.groupby('month')['minutes'].sum().reset_index()
            monthly_volume['month'] = monthly_volume['month'].astype(str)
            
            fig = px.bar(monthly_volume, x='month', y='minutes',
                        title="Monthly Training Volume",
                        labels={'month': 'Month', 'minutes': 'Minutes'},
                        color='minutes', color_continuous_scale="Viridis")
            st.plotly_chart(fig, use_container_width=True)
            
            # Workout category distribution
            category_dist = workout_df.groupby('category')['minutes'].sum().reset_index()
            fig = px.pie(category_dist, values='minutes', names='category',
                        title="Workout Type Distribution")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No workout data yet")
    
    with tab3:
        st.subheader("📋 Weekly Report")
        
        # Get last 4 weeks
        today = datetime.now().date()
        weeks_data = []
        
        for week in range(4):
            week_start = today - timedelta(days=today.weekday() + 7*week)
            week_end = week_start + timedelta(days=6)
            
            week_workouts = [w for w in st.session_state.workouts 
                            if week_start <= datetime.fromisoformat(w['date']).date() <= week_end]
            
            total_minutes = sum([w['minutes'] for w in week_workouts])
            workouts_count = len(week_workouts)
            
            weeks_data.append({
                'Week': f"{week_start.strftime('%b %d')} - {week_end.strftime('%b %d')}",
                'Workouts': workouts_count,
                'Total Minutes': total_minutes,
                'Avg Duration': total_minutes / workouts_count if workouts_count > 0 else 0
            })
        
        df_weeks = pd.DataFrame(weeks_data)
        st.dataframe(df_weeks, use_container_width=True)

# ======================== NUTRITION PAGE ========================
elif page == "🍽️ Nutrition":
    st.title("Nutrition & Calories Tracker")
    
    col1, col2 = st.columns(2)
    
    with col1:
        cal_date = st.date_input("Date", value=datetime.now())
        meal_type = st.selectbox("Meal Type", ["Breakfast", "Lunch", "Dinner", "Snack"])
    
    with col2:
        food_item = st.text_input("Food Item", placeholder="e.g., Chicken Rice")
        calories_intake = st.number_input("Calories (kcal)", min_value=0, max_value=5000, value=500)
    
    protein = st.number_input("Protein (g)", min_value=0.0, value=0.0)
    carbs = st.number_input("Carbs (g)", min_value=0.0, value=0.0)
    fats = st.number_input("Fats (g)", min_value=0.0, value=0.0)
    notes = st.text_area("Notes")
    
    if st.button("📝 Log Meal", use_container_width=True):
        calorie_entry = {
            'date': str(cal_date),
            'meal_type': meal_type,
            'food': food_item,
            'intake': calories_intake,
            'protein': protein,
            'carbs': carbs,
            'fats': fats,
            'notes': notes
        }
        st.session_state.calories.append(calorie_entry)
        save_data()
        st.success(f"Meal logged: {food_item} ({calories_intake} kcal)")
    
    st.subheader("📊 Calorie Analysis")
    
    if st.session_state.calories:
        # Today's calories
        today = datetime.now().date()
        today_calories = [c for c in st.session_state.calories 
                         if datetime.fromisoformat(c['date']).date() == today]
        
        col1, col2, col3, col4 = st.columns(4)
        total_cal = sum([c['intake'] for c in today_calories])
        total_protein = sum([c['protein'] for c in today_calories])
        total_carbs = sum([c['carbs'] for c in today_calories])
        total_fats = sum([c['fats'] for c in today_calories])
        
        with col1:
            st.metric("Total Calories", f"{total_cal} kcal")
        with col2:
            st.metric("Protein", f"{total_protein}g")
        with col3:
            st.metric("Carbs", f"{total_carbs}g")
        with col4:
            st.metric("Fats", f"{total_fats}g")
        
        # Macro breakdown pie chart
        if total_protein + total_carbs + total_fats > 0:
            macro_fig = px.pie(
                values=[total_protein*4, total_carbs*4, total_fats*9],
                names=['Protein', 'Carbs', 'Fats'],
                title="Today's Macro Distribution"
            )
            st.plotly_chart(macro_fig, use_container_width=True)
        
        # Weekly calorie trend
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("### 📅 Weekly Calorie Intake")
            calorie_df = pd.DataFrame(st.session_state.calories)
            calorie_df['date'] = pd.to_datetime(calorie_df['date'])
            daily_calories = calorie_df.groupby('date')['intake'].sum().reset_index()
            daily_calories['date'] = daily_calories['date'].dt.strftime('%a')
            
            fig = px.bar(daily_calories, x='date', y='intake',
                        title="Daily Calorie Intake",
                        labels={'date': 'Day', 'intake': 'Calories (kcal)'},
                        color='intake', color_continuous_scale="RdYlGn_r")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.write("### 🥗 Recent Meals")
            recent_meals = sorted(st.session_state.calories, key=lambda x: x['date'], reverse=True)[:10]
            meal_df = pd.DataFrame(recent_meals)
            st.dataframe(meal_df[['date', 'meal_type', 'food', 'intake']], use_container_width=True)
    else:
        st.info("No meals logged yet. Start tracking your nutrition!")

# ======================== SETTINGS PAGE ========================
elif page == "⚙️ Settings":
    st.title("Settings & Profile")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Body Measurements")
        height = st.number_input("Height (cm)", min_value=100.0, max_value=250.0, 
                                value=st.session_state.user_data.get('height', 170.0))
        weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0,
                               value=st.session_state.user_data.get('weight', 70.0))
        age = st.number_input("Age", min_value=1, max_value=120,
                             value=st.session_state.user_data.get('age', 25))
    
    with col2:
        st.subheader("🎯 Goals")
        goal = st.selectbox("Fitness Goal", 
                           ["Weight Loss", "Muscle Gain", "General Fitness", "Endurance"],
                           index=0 if not st.session_state.user_data else 
                                 ["Weight Loss", "Muscle Gain", "General Fitness", "Endurance"].index(
                                     st.session_state.user_data.get('goal', "Weight Loss")))
        daily_goal_cal = st.number_input("Daily Calorie Goal (kcal)", min_value=1000, max_value=5000, value=2000)
    
    # Calculate BMI
    bmi = weight / ((height / 100) ** 2)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("BMI", f"{bmi:.2f}", st.session_state.user_data.get('bmi', 0))
    with col2:
        # BMI Category
        if bmi < 18.5:
            bmi_status = "Underweight"
        elif bmi < 25:
            bmi_status = "Normal Weight"
        elif bmi < 30:
            bmi_status = "Overweight"
        else:
            bmi_status = "Obese"
        st.write(f"**BMI Status:** {bmi_status}")
    
    if st.button("💾 Save Profile", use_container_width=True):
        st.session_state.user_data = {
            'height': height,
            'weight': weight,
            'age': age,
            'goal': goal,
            'daily_goal_cal': daily_goal_cal,
            'bmi': bmi
        }
        save_data()
        st.success("Profile saved successfully!")
    
    st.divider()
    
    # Data Management
    st.subheader("📁 Data Management")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🗑️ Clear Workouts", use_container_width=True):
            st.session_state.workouts = []
            save_data()
            st.warning("All workout data cleared!")
    
    with col2:
        if st.button("🗑️ Clear Strength Logs", use_container_width=True):
            st.session_state.strength_logs = []
            save_data()
            st.warning("All strength logs cleared!")
    
    with col3:
        if st.button("🗑️ Clear Calories", use_container_width=True):
            st.session_state.calories = []
            save_data()
            st.warning("All calorie data cleared!")
    
    st.divider()
    
    # Export data
    st.subheader("📤 Export Data")
    if st.button("📥 Download All Data as JSON", use_container_width=True):
        all_data = {
            'workouts': st.session_state.workouts,
            'strength_logs': st.session_state.strength_logs,
            'calories': st.session_state.calories,
            'user_data': st.session_state.user_data
        }
        st.download_button(
            label="Download JSON",
            data=json.dumps(all_data, indent=2, default=str),
            file_name=f"fitness_data_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json"
        )
