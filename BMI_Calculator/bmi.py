# app.py - Main Streamlit Application
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import datetime
import json
import os

# Set page configuration
st.set_page_config(
    page_title="BMI Calculator Dashboard",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stAlert {
        padding: 0.5rem;
        margin-bottom: 1rem;
    }
    .result-box {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .metric-container {
        display: flex;
        justify-content: space-between;
        flex-wrap: wrap;
    }
    .metric-card {
        background-color: #2ecc71;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 0.5rem 0;
        width: 48%;
    }
    </style>
    """, unsafe_allow_html=True)


# Utility functions
def calculate_bmi(weight, height, units="metric"):
    """Calculate BMI based on weight and height"""
    if units == "metric":
        # Weight in kg, height in cm
        height_m = height / 100  # Convert cm to m
        bmi = weight / (height_m ** 2)
    else:
        # Weight in pounds, height in inches
        bmi = (weight * 703) / (height ** 2)

    return round(bmi, 1)


def get_bmi_category(bmi):
    """Return BMI category based on value"""
    if bmi < 18.5:
        return "Underweight", "#3498db"  # Blue
    elif 18.5 <= bmi < 25:
        return "Normal weight", "#2ecc71"  # Green
    elif 25 <= bmi < 30:
        return "Overweight", "#f39c12"  # Orange
    elif 30 <= bmi < 35:
        return "Obesity (Class 1)", "#e67e22"  # Dark Orange
    elif 35 <= bmi < 40:
        return "Obesity (Class 2)", "#e74c3c"  # Red
    else:
        return "Obesity (Class 3)", "#c0392b"  # Dark Red


def create_gauge_chart(bmi):
    """Create a gauge chart to visualize BMI"""
    category, color = get_bmi_category(bmi)

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=bmi,
        domain={"x": [0, 1], "y": [0, 1]},
        title={"text": "BMI", "font": {"size": 24}},
        gauge={
            "axis": {"range": [None, 50], "tickwidth": 1, "tickcolor": "darkblue"},
            "bar": {"color": color},
            "bgcolor": "white",
            "borderwidth": 2,
            "bordercolor": "gray",
            "steps": [
                {"range": [0, 18.5], "color": "#3498db"},
                {"range": [18.5, 25], "color": "#2ecc71"},
                {"range": [25, 30], "color": "#f39c12"},
                {"range": [30, 35], "color": "#e67e22"},
                {"range": [35, 40], "color": "#e74c3c"},
                {"range": [40, 50], "color": "#c0392b"}
            ],
        }
    ))

    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=50, b=20),
    )

    return fig


def load_user_data():
    """Load saved BMI history"""
    if 'bmi_history' not in st.session_state:
        st.session_state.bmi_history = []

    return st.session_state.bmi_history


def save_bmi_calculation(weight, height, bmi, units):
    """Save current BMI calculation to history"""
    if 'bmi_history' not in st.session_state:
        st.session_state.bmi_history = []

    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    bmi_data = {
        "date": date,
        "weight": weight,
        "height": height,
        "units": units,
        "bmi": bmi,
        "category": get_bmi_category(bmi)[0]
    }

    st.session_state.bmi_history.append(bmi_data)


def create_history_chart(history):
    """Create a line chart showing BMI history"""
    if not history:
        return None

    df = pd.DataFrame(history)
    df['date'] = pd.to_datetime(df['date'])

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df['date'], df['bmi'], marker='o', linestyle='-', color='#3498db')
    ax.axhspan(0, 18.5, color='#3498db', alpha=0.1)
    ax.axhspan(18.5, 25, color='#2ecc71', alpha=0.1)
    ax.axhspan(25, 30, color='#f39c12', alpha=0.1)
    ax.axhspan(30, 35, color='#e67e22', alpha=0.1)
    ax.axhspan(35, 40, color='#e74c3c', alpha=0.1)
    ax.axhspan(40, 50, color='#c0392b', alpha=0.1)

    ax.set_xlabel('Date')
    ax.set_ylabel('BMI')
    ax.set_title('BMI History')
    ax.grid(True, linestyle='--', alpha=0.7)

    plt.tight_layout()
    return fig


# Main application
def main():
    # Sidebar inputs
    st.sidebar.title("BMI Calculator")

    # Unit selection
    units = st.sidebar.radio("Select Units", ["Metric (kg, cm)", "Imperial (lb, in)"])

    if units == "Metric (kg, cm)":
        weight_unit = "kg"
        height_unit = "cm"
        unit_system = "metric"
    else:
        weight_unit = "lb"
        height_unit = "in"
        unit_system = "imperial"

    # Weight input
    weight = st.sidebar.number_input(f"Weight ({weight_unit})", min_value=0.0, max_value=500.0,
                                     value=70.0 if unit_system == "metric" else 154.0, step=0.1)

    # Height input
    if unit_system == "metric":
        height = st.sidebar.number_input(f"Height ({height_unit})", min_value=0.0, max_value=300.0, value=170.0,
                                         step=0.1)
    else:
        height = st.sidebar.number_input(f"Height ({height_unit})", min_value=0.0, max_value=120.0, value=67.0,
                                         step=0.1)

    # Additional optional inputs
    with st.sidebar.expander("Additional Information (Optional)"):
        age = st.number_input("Age", min_value=0, max_value=120, value=30)
        gender = st.radio("Gender", ["Male", "Female", "Other"])

    # Calculate button
    calculate_button = st.sidebar.button("Calculate BMI", type="primary")

    # Load history data
    bmi_history = load_user_data()

    # Main content area
    st.title("BMI Calculator Dashboard")

    tabs = st.tabs(["Calculator", "History", "Information"])

    with tabs[0]:
        if calculate_button or len(bmi_history) > 0:
            # Calculate BMI
            if calculate_button:
                bmi = calculate_bmi(weight, height, unit_system)
                category, color = get_bmi_category(bmi)

                # Save calculation
                save_bmi_calculation(weight, height, bmi, unit_system)
            else:
                # Display most recent calculation
                latest = bmi_history[-1]
                bmi = latest["bmi"]
                category, color = get_bmi_category(bmi)

            # Display results
            col1, col2 = st.columns([1, 1])

            with col1:
                st.markdown(f"""
                <div class="result-box" style="background-color: {color}20; border: 1px solid {color};">
                    <h2 style="color: {color};">Your BMI: {bmi}</h2>
                    <h3>Category: {category}</h3>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("### What does this mean?")
                st.write(f"Your BMI of {bmi} indicates that you are in the **{category}** category.")

                if category == "Underweight":
                    st.info(
                        "Being underweight may indicate nutritional deficiencies or other health issues. Consider consulting with a healthcare provider.")
                elif category == "Normal weight":
                    st.success(
                        "Your weight is within the healthy range. Maintain a balanced diet and regular exercise.")
                elif category == "Overweight":
                    st.warning(
                        "Being overweight may increase your risk of certain health conditions. Consider adopting healthier eating habits and increasing physical activity.")
                else:
                    st.error(
                        "Obesity is associated with increased risk for many health conditions. It's recommended to consult with healthcare providers about weight management strategies.")

            with col2:
                # Display gauge chart
                gauge_chart = create_gauge_chart(bmi)
                st.plotly_chart(gauge_chart, use_container_width=True)

                # Ideal weight range
                if unit_system == "metric":
                    lower_weight = round((18.5 * (height / 100) ** 2), 1)
                    upper_weight = round((24.9 * (height / 100) ** 2), 1)
                    st.info(f"Ideal weight range for your height: {lower_weight} - {upper_weight} kg")
                else:
                    lower_weight = round((18.5 * height ** 2) / 703, 1)
                    upper_weight = round((24.9 * height ** 2) / 703, 1)
                    st.info(f"Ideal weight range for your height: {lower_weight} - {upper_weight} lb")

            # Health metrics
            st.markdown("### Health Metrics")
            metric_col1, metric_col2 = st.columns([1, 1])

            with metric_col1:
                st.markdown("""
                <div class="metric-card">
                    <h4>BMI Limitations</h4>
                    <p>BMI doesn't distinguish between muscle and fat or account for body composition.</p>
                </div>
                """, unsafe_allow_html=True)

            with metric_col2:
                st.markdown("""
                <div class="metric-card">
                    <h4>Next Steps</h4>
                    <p>Track your BMI over time and consider other health metrics for a complete picture.</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Enter your details and click 'Calculate BMI' to see your results.")

    with tabs[1]:
        st.subheader("BMI History")

        if not bmi_history:
            st.info("No BMI calculations saved yet. Calculate your BMI to start tracking.")
        else:
            # Show history chart
            history_chart = create_history_chart(bmi_history)
            if history_chart:
                st.pyplot(history_chart)

            # Show history table
            df = pd.DataFrame(bmi_history)
            st.dataframe(df, use_container_width=True)

            # Clear history button
            if st.button("Clear History"):
                st.session_state.bmi_history = []
                st.experimental_rerun()

    with tabs[2]:
        st.subheader("About BMI")
        st.write("""
        Body Mass Index (BMI) is a value derived from an individual's weight and height. It provides a simple numeric measure of a person's thickness or thinness, allowing health professionals to discuss weight problems more objectively with their patients.

        ### BMI Categories:
        - **Underweight**: BMI less than 18.5
        - **Normal weight**: BMI between 18.5 and 24.9
        - **Overweight**: BMI between 25 and 29.9
        - **Obesity (Class 1)**: BMI between 30 and 34.9
        - **Obesity (Class 2)**: BMI between 35 and 39.9
        - **Obesity (Class 3)**: BMI of 40 or greater

        ### Limitations of BMI:
        - Does not account for differences in muscle mass, bone density, and overall body composition
        - May not be accurate for athletes, elderly individuals, or pregnant women
        - Does not consider where fat is stored in the body (abdominal fat poses higher health risks)
        - Does not directly measure body fat percentage

        BMI should be used as one of several tools to assess health and risk factors, not as the sole determinant.
        """)


if __name__ == "__main__":
    main()