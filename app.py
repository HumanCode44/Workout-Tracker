
import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Custom Workout Planner", layout="centered")

st.title("🏋️ Workout Planner")
st.markdown("Use this tool to either generate a suggested workout or build your own custom session.")

# --- User Inputs ---
st.sidebar.header("Today's Setup")
mood = st.sidebar.selectbox("How are you feeling?", ["Low", "Medium", "High"])
day = st.sidebar.selectbox("What day is it?", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
mode = st.sidebar.radio("Choose Mode:", ["Suggested Workout", "Custom Workout"])

# --- Sample Workout Templates ---
workouts = {
    "monday": {
        "low": ["Incline DB press", "Dips"],
        "medium": ["Bench press", "Incline bench press", "Pec fly", "Tricep pushdown", "Overhead triceps extension"],
        "high": ["Bench press", "Incline bench press", "Pec fly", "Dips", "Cable crossover", "Tricep pushdown", "Overhead triceps extension"]
    },
    "tuesday": {
        "low": ["Lat pulldown", "Straight-arm pulldown"],
        "medium": ["Pull-ups", "Barbell row", "Seated cable row", "Face pulls", "Bicep curls"],
        "high": ["Pull-ups", "Barbell row", "T-bar row", "Lat pulldown", "Seated cable row", "Face pulls", "Bicep curls", "Hammer curls"]
    },
    "wednesday": {
        "low": ["Rest"],
        "medium": ["Light Walk"],
        "high": ["Cardio"]
    },
    "thursday": {
        "low": ["Lateral raises", "Overhead press"],
        "medium": ["Overhead press", "Lateral raises", "Front raises", "Rear delt fly"],
        "high": ["Overhead press", "Arnold press", "Lateral raises", "Front raises", "Rear delt fly", "Shrugs"]
    },
    "friday": {
        "low": ["Bodyweight squats", "Leg curl machine"],
        "medium": ["Back squat", "Leg press", "Leg curl", "Walking lunges", "Calf raises"],
        "high": ["Back squat", "Hack Squat", "Romanian deadlift", "Leg press", "Walking lunges", "Calf raises", "Hip thrusts"]
    },
    "saturday": {
        "low": ["Rest"],
        "medium": ["Light Walk"],
        "high": ["Cardio"]
    },
    "sunday": {
        "low": ["Rest"],
        "medium": ["Light Walk"],
        "high": ["Cardio"]
    # Add more days as needed
}
}
# --- Suggested Workout Display ---
if mode == "Suggested Workout":
    focus_day = day.lower()
    suggested = workouts.get(focus_day, {}).get(mood.lower(), [])
    st.subheader("💡 Suggested Workout")
    if suggested:
        workout_entries = []
        for exercise in suggested:
            if "x" in exercise.split(" ")[0].lower():
                sets_reps, name = exercise.split(" ", 1)
                try:
                    suggested_sets, suggested_reps = map(int, sets_reps.lower().split("x"))
                except ValueError:
                    suggested_sets, suggested_reps = 3, 10
                    name = exercise
            else:
                name = exercise
                suggested_sets, suggested_reps = 3, 10

            st.markdown(f"**{name}** — Suggested: {suggested_sets} sets x {suggested_reps} reps")

            weight = st.number_input(f"{name} - Enter Weight (lbs)", min_value=0, max_value=1000, value=0, key=f"{name}_weight")
            sets = st.number_input(f"{name} - Sets Completed", min_value=1, max_value=10, value=suggested_sets, key=f"{name}_sets")
            reps = st.number_input(f"{name} - Reps per Set", min_value=1, max_value=20, value=suggested_reps, key=f"{name}_reps")

            workout_entries.append({
                "Date": date.today().isoformat(),
                "Day": day,
                "Mood": mood,
                "Workout Name": "Suggested Workout",
                "Exercise": name,
                "Sets": sets,
                "Reps": reps,
                "Weight": weight
            })

        if st.button("Save Suggested Workout"):
            df = pd.DataFrame(workout_entries)
            df.to_csv("suggested_workout_log.csv", mode="a", header=False, index=False)
            st.success("Workout saved to suggested_workout_log.csv")
    else:
        st.info("No template found for this day and mood.")

# --- Custom Workout Entry ---
elif mode == "Custom Workout":
    st.subheader("Create a Custom Workout")
    with st.form("custom_workout"):
        workout_name = st.text_input("Workout Name")
        exercise = st.text_input("Exercise Name")
        sets = st.number_input("Sets", min_value=1, max_value=10, value=3)
        reps = st.number_input("Reps", min_value=1, max_value=20, value=10)
        weight = st.number_input("Weight (lbs)", min_value=0, max_value=1000, value=0)
        add_exercise = st.form_submit_button("Add to Workout")

    # --- Session State to Track Workout ---
    if "workout_log" not in st.session_state:
        st.session_state.workout_log = []

    # Add new entry if submitted
    if add_exercise and workout_name and exercise:
        st.session_state.workout_log.append({
            "Date": date.today().isoformat(),
            "Day": day,
            "Mood": mood,
            "Workout Name": workout_name,
            "Exercise": exercise,
            "Sets": sets,
            "Reps": reps,
            "Weight": weight
        })

    # --- Display Logged Workout ---
    st.subheader("Your Workout Log")
    if st.session_state.workout_log:
        df = pd.DataFrame(st.session_state.workout_log)
        st.dataframe(df, use_container_width=True)

        if st.button("Clear Log"):
            st.session_state.workout_log.clear()
        if st.button("Save Custom Workout Log"):
            df.to_csv("custom_workout_log.csv", mode="a", header=False, index=False)
            st.success("Custom workout log saved to custom_workout_log.csv")
    else:
        st.info("No exercises logged yet.")

