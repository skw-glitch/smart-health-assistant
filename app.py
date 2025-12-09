import os
import pickle
import streamlit as st
from streamlit_option_menu import option_menu

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Smart Health Assistant",
    layout="wide",
    page_icon="🧑‍⚕️"
)

working_dir = os.path.dirname(os.path.abspath(__file__))

# Load models
diabetes_model = pickle.load(open(f"{working_dir}/saved_models/diabetes_model.sav", "rb"))
heart_disease_model = pickle.load(open(f"{working_dir}/saved_models/heart_disease_model.sav", "rb"))
parkinsons_model = pickle.load(open(f"{working_dir}/saved_models/parkinsons_model.sav", "rb"))
kidney_model = pickle.load(open(f"{working_dir}/saved_models/kidney_model.sav", "rb"))

# ---------- UI STYLE ----------
st.markdown(
    """
<style>
html, body, [class*="css"] {
    font-size: 16px;
}

/* Result box – centered, slightly smaller font */
.result-box {
    font-size: 18px;
    font-weight: 600;
    border-radius: 10px;
    padding: 14px 20px;
    text-align: center;
    margin: 18px auto 8px auto;
    max-width: 900px;
}
.healthy {
    background-color: rgba(0, 180, 90, 0.18);
    color: #00a651;
}
.disease {
    background-color: rgba(225, 0, 0, 0.20);
    color: #d70000;
}

/* Center ALL buttons strongly by default */
.stButton > button {
    display: block !important;
    margin-left: auto !important;
    margin-right: auto !important;
}

/* More top padding so the title is never cut off */
.block-container {
    padding-top: 3.2rem;
}

/* Heading styles */
.main-title {
    text-align: center;
    font-size: 32px;
    font-weight: 800;
    margin-bottom: 4px;
}
.main-subtitle {
    text-align: center;
    font-size: 13px;
    opacity: 0.8;
    margin-bottom: 14px;
}

/* Slightly larger labels */
label {
    font-size: 1.05rem;
}
</style>
""",
    unsafe_allow_html=True,
)

# ---------- Helper to show colored result ----------
def show_result(text: str, is_disease: bool):
    if not text:
        return
    css_class = "disease" if is_disease else "healthy"
    st.markdown(
        f'<div class="result-box {css_class}">{text}</div>',
        unsafe_allow_html=True,
    )


# ---------- Title + TOP MENU ----------
st.markdown(
    '<div class="main-title">🧑‍⚕️ Smart Health Assistant</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="main-subtitle">Early screening dashboard for multiple diseases — not a replacement for professional medical advice.</div>',
    unsafe_allow_html=True,
)

selected = option_menu(
    menu_title=None,
    options=[
        "Diabetes Prediction",
        "Heart Disease Prediction",
        "Parkinsons Prediction",
        "Kidney Disease Prediction",
    ],
    icons=["activity", "heart", "person", "droplet-half"],
    orientation="horizontal",
    styles={
        "container": {
            "padding": "4px 8px",
            "margin": "0 auto 22px auto",
            "background-color": "rgba(148,163,184,0.18)",
            "border-radius": "999px",
            "justify-content": "center",
        },
        "nav-link": {
            "font-size": "15px",
            "padding": "8px 24px",
            "margin": "0 4px",
            "border-radius": "999px",
            "color": "inherit",
        },
        "nav-link-selected": {
            "background-color": "#ef4444",
            "color": "white",
        },
    },
)

st.write("")


# ===================== DIABETES PREDICTION PAGE =====================
if selected == "Diabetes Prediction":

    st.title("🩸 Diabetes Prediction")

    # Inputs section
    with st.container():
        col1, col2, col3 = st.columns(3)

        # [Glucose, BMI, Age, DPF, Insulin, BloodPressure]

        with col1:
            Glucose = st.number_input(
                "Glucose Level (40 – 300 mg/dL)",
                min_value=40,
                max_value=300,
            )

        with col2:
            BMI = st.number_input(
                "BMI value (18 – 67 kg/m²)",
                min_value=18.0,
                max_value=67.0,
                help="If you don't know BMI, calculate using the BMI section below.",
            )

        with col3:
            Age = st.number_input(
                "Age of the Person (21 – 81 years)",
                min_value=21,
                max_value=81,
            )

        with col1:
            Insulin = st.number_input(
                "Insulin Level (15 – 276 µU/mL)",
                min_value=15,
                max_value=276,
            )

        with col2:
            BloodPressure = st.number_input(
                "Blood Pressure (24 – 122 mm Hg)",
                min_value=24,
                max_value=122,
            )

        with col3:
            FamilyHistory = st.radio(
                "Family history of diabetes",
                ("No", "Yes"),
            )

        if FamilyHistory == "Yes":
            DiabetesPedigreeFunction = 2.5
        else:
            DiabetesPedigreeFunction = 0.08

    # ---------- BMI Calculator ----------
    st.markdown("### 🧮 BMI Calculator (Optional)")
    bmi_col1, bmi_col2 = st.columns(2)

    with bmi_col1:
        height = st.number_input(
            "Height (cm)",
            min_value=100,
            max_value=230,
            value=170,
        )
        # button directly under Height, left side
        calc_bmi = st.button("Calculate BMI")
    with bmi_col2:
        weight = st.number_input(
            "Weight (kg)",
            min_value=20,
            max_value=200,
            value=60,
        )

    if calc_bmi and height > 0:
        bmi_value = weight / ((height / 100) ** 2)
        st.success(f"Calculated BMI: {bmi_value:.2f}")
        BMI = float(f"{bmi_value:.2f}")

    diab_diagnosis = ""
    diab_is_disease = False
    diab_tips = []

    # center Get Result button, very slight shift to the right
    d1, d2, d3 = st.columns([1, 1, 0.8])
    with d2:
        diab_btn = st.button("🔍 Get Diabetes Test Result")

    if diab_btn:
        user_input = [
            Glucose,
            BMI,
            Age,
            DiabetesPedigreeFunction,
            Insulin,
            BloodPressure,
        ]

        diab_prediction = diabetes_model.predict([user_input])
        diab_is_disease = diab_prediction[0] == 1

        if diab_is_disease:
            diab_diagnosis = (
                "The prediction shows Signs of Diabetes (The Person Is Diabetic). "
                "Please take care and seek medical support, Your Health Matters."
            )
            diab_tips = [
                "Get your blood sugar (fasting, post-meal, HbA1c) checked regularly as advised by your doctor.",
                "Follow a diabetes-friendly diet: less sugar, fewer refined carbs, more veggies and fiber.",
                "Do at least 30 minutes of walking / light exercise on most days.",
                "Take prescribed medicines or insulin on time and don’t miss follow-up visits.",
            ]
        else:
            diab_diagnosis = (
                "The prediction shows No Signs of Diabetes (The Person Is Not Diabetic). "
                "Stay healthy and keep taking care of yourself, You Are Doing Great!"
            )
            diab_tips = [
                "Maintain a balanced diet and avoid excess sugar and junk food.",
                "Stay physically active with regular exercise or daily walks.",
                "Keep your weight and blood pressure in a healthy range.",
                "Go for routine health checkups to catch any changes early.",
            ]

    if diab_diagnosis:
        show_result(diab_diagnosis, diab_is_disease)
        st.markdown("#### 🩺 Health Tips")
        for tip in diab_tips:
            st.markdown(f"- ✔ {tip}")


# ===================== HEART DISEASE PREDICTION PAGE =====================
if selected == "Heart Disease Prediction":

    st.title("❤️ Heart Disease Prediction")

    with st.container():
        col1, col2, col3 = st.columns(3)

        # [age, sex, cp, trestbps, chol, thalach, exang, oldpeak, slope, thal]

        with col1:
            age = st.number_input(
                "Age (years) — 18 to 100",
                min_value=18,
                max_value=100,
                value=40,
            )

        with col2:
            sex_label = st.radio(
                "Gender",
                ("Male", "Female"),
            )
            sex = 1 if sex_label == "Male" else 0

        with col3:
            cp_label = st.selectbox(
                "Type of chest discomfort",
                (
                    "Typical angina",
                    "Atypical angina",
                    "Non-anginal pain",
                    "Asymptomatic",
                ),
            )
            cp_map = {
                "Typical angina": 0,
                "Atypical angina": 1,
                "Non-anginal pain": 2,
                "Asymptomatic": 3,
            }
            cp = cp_map[cp_label]

        with col1:
            trestbps = st.number_input(
                "Blood pressure (resting, mm Hg) — 80 to 220",
                min_value=80,
                max_value=220,
                value=120,
            )

        with col2:
            chol = st.number_input(
                "Cholesterol level (mg/dL) — 100 to 600",
                min_value=100,
                max_value=600,
                value=200,
            )

        with col3:
            thalach = st.number_input(
                "Highest heart rate during exercise (bpm) — 60 to 220",
                min_value=60,
                max_value=220,
                value=150,
            )

        with col1:
            exang_label = st.radio(
                "Chest pain during exercise (Yes/No)",
                ("No", "Yes"),
            )
            exang = 1 if exang_label == "Yes" else 0

        with col2:
            oldpeak = st.number_input(
                "ECG value change after exercise — 0.0 to 6.5",
                min_value=0.0,
                max_value=6.5,
                value=1.0,
                step=0.1,
            )

        with col3:
            slope_label = st.selectbox(
                "ECG pattern during exercise",
                ("Upsloping", "Flat", "Downsloping"),
            )
            slope_map = {
                "Upsloping": 0,
                "Flat": 1,
                "Downsloping": 2,
            }
            slope = slope_map[slope_label]

        col4, _, _ = st.columns(3)
        with col4:
            thal_label = st.selectbox(
                "Heart blood flow test result (Thallium scan)",
                ("Normal", "Fixed defect", "Reversible defect"),
            )
            thal_map = {
                "Normal": 0,
                "Fixed defect": 1,
                "Reversible defect": 2,
            }
            thal = thal_map[thal_label]

    heart_diagnosis = ""
    heart_is_disease = False
    heart_tips = []

    h1, h2, h3 = st.columns([1, 1, 0.8])
    with h2:
        heart_btn = st.button("🔍 Get Heart Disease Test Result")

    if heart_btn:
        user_input = [
            age,
            sex,
            cp,
            trestbps,
            chol,
            thalach,
            exang,
            oldpeak,
            slope,
            thal,
        ]

        heart_prediction = heart_disease_model.predict([user_input])
        heart_is_disease = heart_prediction[0] == 1

        if heart_is_disease:
            heart_diagnosis = (
                "💔 The person has a Heart Disease. Please seek medical help and take extra care, "
                "Your Life And Health Are Precious."
            )
            heart_tips = [
                "Consult a cardiologist regularly and follow prescribed medicines strictly.",
                "Avoid smoking and limit alcohol; both put extra strain on your heart.",
                "Reduce oily, fried, and junk food; choose fruits, vegetables, and whole grains.",
                "Do light to moderate exercise as advised by your doctor, avoid sudden overexertion.",
            ]
        else:
            heart_diagnosis = (
                "❤️ The person doesn’t have a Heart Disease. Stay strong and keep caring for your heart, "
                "You’re Doing Amazing."
            )
            heart_tips = [
                "Maintain a heart-healthy diet low in saturated fat, salt, and sugar.",
                "Keep your blood pressure, cholesterol, and weight in a healthy range.",
                "Stay active with regular physical activity and avoid long sitting hours.",
                "Avoid tobacco in any form and manage stress with relaxation or hobbies.",
            ]

    if heart_diagnosis:
        show_result(heart_diagnosis, heart_is_disease)
        st.markdown("#### 🫀 Heart Health Tips")
        for tip in heart_tips:
            st.markdown(f"- ✔ {tip}")


# ===================== PARKINSON'S PREDICTION PAGE =====================
if selected == "Parkinsons Prediction":

    st.title("🧠 Parkinson's Disease Prediction")

    with st.container():
        col1, col2, col3 = st.columns(3)

        with col1:
            Fo = st.number_input(
                "Average vocal frequency (Hz) — 70 to 300",
                min_value=70.0,
                max_value=300.0,
                step=0.1,
            )

        with col2:
            Fhi = st.number_input(
                "Highest vocal frequency (Hz) — 80 to 600",
                min_value=80.0,
                max_value=600.0,
                step=0.1,
            )

        with col3:
            Flo = st.number_input(
                "Lowest vocal frequency (Hz) — 50 to 260",
                min_value=50.0,
                max_value=260.0,
                step=0.1,
            )

        with col1:
            Jitter_percent = st.number_input(
                "Pitch variation (%) — 0.001 to 0.03",
                min_value=0.001,
                max_value=0.03,
                step=0.001,
                format="%.4f",
            )

        with col2:
            Shimmer = st.number_input(
                "Voice amplitude variation — 0.01 to 0.2",
                min_value=0.01,
                max_value=0.2,
                step=0.001,
            )

        with col3:
            HNR = st.number_input(
                "Harmonics-to-noise ratio (HNR) — 5 to 45",
                min_value=5.0,
                max_value=45.0,
                step=0.1,
            )

        with col1:
            RPDE = st.number_input(
                "Voice pattern recurrence score — 0.1 to 1.0",
                min_value=0.1,
                max_value=1.0,
                step=0.01,
            )

        with col2:
            DFA = st.number_input(
                "Signal stability index — 0.4 to 1.5",
                min_value=0.4,
                max_value=1.5,
                step=0.01,
            )

    parkinsons_diagnosis = ""
    park_is_disease = False
    park_tips = []

    p1, p2, p3 = st.columns([1, 1, 0.8])
    with p2:
        park_btn = st.button("🔍 Get Parkinson's Test Result")

    if park_btn:
        user_input = [
            Fo,
            Fhi,
            Flo,
            Jitter_percent,
            Shimmer,
            HNR,
            RPDE,
            DFA,
        ]

        parkinsons_prediction = parkinsons_model.predict([user_input])
        park_is_disease = parkinsons_prediction[0] == 1

        if park_is_disease:
            parkinsons_diagnosis = (
                "💔 The person shows signs of Parkinson’s Disease. Early care, treatment, and support can make a big "
                "difference, every step, every movement, every moment matters."
            )
            park_tips = [
                "Consult a neurologist early to discuss diagnosis, treatment, and physiotherapy.",
                "Do regular gentle exercises, stretching, or yoga to maintain balance and flexibility.",
                "Speech and occupational therapy can help with communication and daily activities.",
                "Sleep well, manage stress, and seek emotional support from family or support groups.",
            ]
        else:
            parkinsons_diagnosis = (
                "💚 The person doesn’t show signs of Parkinson’s Disease. Keep your body active and your mind strong, "
                "your movement and strength are in your control."
            )
            park_tips = [
                "Stay physically active with walking, stretching, and light exercise.",
                "Keep your brain engaged with reading, learning, puzzles, and social interaction.",
                "Maintain a balanced diet and good sleep routine.",
                "If you notice tremors, stiffness, or slowness in future, get yourself checked early.",
            ]

    if parkinsons_diagnosis:
        show_result(parkinsons_diagnosis, park_is_disease)
        st.markdown("#### 🧠 Brain & Movement Health Tips")
        for tip in park_tips:
            st.markdown(f"- ✔ {tip}")


# ===================== KIDNEY DISEASE PREDICTION PAGE =====================
if selected == "Kidney Disease Prediction":

    st.title("💧 Kidney Disease Prediction")

    with st.container():
        # Row 1
        r1c1, r1c2, r1c3 = st.columns(3)
        with r1c1:
            k_age = st.number_input(
                "Age (years) — 1 to 100",
                min_value=1,
                max_value=100,
                value=40,
            )
        with r1c2:
            k_bp = st.number_input(
                "Blood Pressure (mm Hg) — 50 to 200",
                min_value=50.0,
                max_value=200.0,
                value=80.0,
            )
        with r1c3:
            k_sg = st.number_input(
                "Urine Specific Gravity — 1.005 to 1.025",
                min_value=1.005,
                max_value=1.025,
                value=1.015,
                step=0.001,
                format="%.3f",
            )

        # Row 2
        r2c1, r2c2, r2c3 = st.columns(3)
        with r2c1:
            k_al = st.number_input(
                "Urine Albumin Level — 0 to 5",
                min_value=0.0,
                max_value=5.0,
                value=1.0,
                step=1.0,
            )
        with r2c2:
            k_bgr = st.number_input(
                "Random Blood Glucose (mg/dL) — 50 to 500",
                min_value=50.0,
                max_value=500.0,
                value=120.0,
            )
        with r2c3:
            k_bu = st.number_input(
                "Blood Urea (mg/dL) — 1 to 400",
                min_value=1.0,
                max_value=400.0,
                value=40.0,
            )

        # Row 3
        r3c1, r3c2, r3c3 = st.columns(3)
        with r3c1:
            k_sc = st.number_input(
                "Serum Creatinine (mg/dL) — 0.4 to 15",
                min_value=0.4,
                max_value=15.0,
                value=1.2,
            )
        with r3c2:
            k_hemo = st.number_input(
                "Hemoglobin (g/dL) — 3 to 20",
                min_value=3.0,
                max_value=20.0,
                value=13.0,
            )
        with r3c3:
            k_wc = st.number_input(
                "White Blood Cell Count (cells/mm³) — 2000 to 25000",
                min_value=2000,
                max_value=25000,
                value=8000,
            )

        # Row 4
        r4c1, r4c2, r4c3 = st.columns(3)
        with r4c1:
            k_htn_label = st.radio(
                "Hypertension (High Blood Pressure)",
                ("No", "Yes"),
            )
            k_htn = 1 if k_htn_label == "Yes" else 0
        with r4c2:
            k_dm_label = st.radio(
                "Diabetes",
                ("No", "Yes"),
            )
            k_dm = 1 if k_dm_label == "Yes" else 0
        with r4c3:
            k_ane_label = st.radio(
                "Anemia",
                ("No", "Yes"),
            )
            k_ane = 1 if k_ane_label == "Yes" else 0

    kidney_diagnosis = ""
    kidney_is_disease = False
    kidney_tips = []

    k1, k2, k3 = st.columns([1, 1, 0.8])
    with k2:
        kidney_btn = st.button("🔍 Get Kidney Disease Test Result")

    if kidney_btn:
        kidney_input = [
            k_age,
            k_bp,
            k_sg,
            k_al,
            k_bgr,
            k_bu,
            k_sc,
            k_hemo,
            k_wc,
            k_htn,
            k_dm,
            k_ane,
        ]

        kidney_prediction = kidney_model.predict([kidney_input])
        kidney_is_disease = kidney_prediction[0] == 1

        if kidney_is_disease:
            kidney_diagnosis = (
                "💔 The person shows signs of Kidney Disease. Please seek timely medical care and protect your health, "
                "early support can make the biggest difference for your kidneys and your life."
            )
            kidney_tips = [
                "Drink enough water unless your doctor has told you to restrict fluids.",
                "Limit salty, oily, and highly processed foods to reduce kidney load.",
                "Avoid unnecessary painkillers and self-medication, many drugs can harm kidneys.",
                "Keep your blood pressure, blood sugar, and cholesterol under control with proper treatment.",
            ]
        else:
            kidney_diagnosis = (
                "💚 The person doesn’t show signs of Kidney Disease. Keep staying hydrated and caring for your body, "
                "your kidneys are working strong for you."
            )
            kidney_tips = [
                "Drink adequate clean water daily, unless a doctor says otherwise.",
                "Avoid frequent and unnecessary use of painkillers without prescription.",
                "Maintain healthy BP and sugar levels, especially if you have diabetes or hypertension.",
                "Get yearly kidney function tests if you are diabetic, hypertensive, or have family history.",
            ]

    if kidney_diagnosis:
        show_result(kidney_diagnosis, kidney_is_disease)
        st.markdown("#### 💧 Kidney Health Tips")
        for tip in kidney_tips:
            st.markdown(f"- ✔ {tip}")


# ---------- Global doctor note at bottom ----------
st.markdown("---")
st.markdown(
    "<p style='text-align:center; font-size:13px; opacity:0.75;'>"
    "⚠️ This tool is only for educational screening and awareness. "
    "Always consult a qualified doctor for diagnosis, treatment, and medical decisions."
    "</p>",
    unsafe_allow_html=True,
)
