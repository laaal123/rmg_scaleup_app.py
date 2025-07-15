import streamlit as st
import math

# --- Granulation Time Calculation (in seconds) ---
def granulation_time_scaleup(method, D_small_mm, N_small, t_small_sec, D_large_mm, N_large):
    D_small = D_small_mm / 1000  # Convert to meters
    D_large = D_large_mm / 1000
    t_small_min = t_small_sec / 60  # Convert to minutes

    if method == "Tip Speed (Shear Matching)":
        V_small = math.pi * D_small * N_small
        t_large_min = (V_small * t_small_min) / (math.pi * D_large * N_large)
    elif method == "Tip Distance (Total Exposure Matching)":
        t_large_min = (D_small * N_small * t_small_min) / (D_large * N_large)
    else:
        st.error("Invalid method selected.")
        return None
    return round(t_large_min * 60, 2)  # Return in seconds

# --- Impeller RPM Calculation ---
def impeller_rpm_scaleup(method, D_small_mm, N_small, t_small_sec, D_large_mm, t_large_sec):
    D_small = D_small_mm / 1000
    D_large = D_large_mm / 1000
    t_small_min = t_small_sec / 60
    t_large_min = t_large_sec / 60

    if method == "Tip Speed (Shear Matching)":
        numerator = math.pi * D_small * N_small * t_small_min
        denominator = math.pi * D_large * t_large_min
        N_large = numerator / denominator
    elif method == "Tip Distance (Total Exposure Matching)":
        numerator = D_small * N_small * t_small_min
        denominator = D_large * t_large_min
        N_large = numerator / denominator
    else:
        st.error("Invalid method selected.")
        return None
    return round(N_large, 2)

# --- Streamlit App ---
def main():
    st.title("🔄 RMG Scale-Up Calculator")
    st.markdown("Built for pharmaceutical granulation process scaling based on impeller diameter and speed.")

    st.header("1️⃣ Granulation Time Scale-Up")
    method_time = st.selectbox("Select Scaling Method", ["Tip Speed (Shear Matching)", "Tip Distance (Total Exposure Matching)"])
    D_small = st.number_input("Small Scale Impeller Diameter (mm)", min_value=10.0, value=200.0)
    N_small = st.number_input("Small Scale RPM", min_value=10.0, value=100.0)
    t_small_sec = st.number_input("Small Scale Granulation Time (seconds)", min_value=1.0, value=180.0)
    D_large = st.number_input("Large Scale Impeller Diameter (mm)", min_value=10.0, value=600.0)
    N_large = st.number_input("Large Scale RPM", min_value=10.0, value=50.0)

    if st.button("🕒 Calculate Granulation Time"):
        result = granulation_time_scaleup(method_time, D_small, N_small, t_small_sec, D_large, N_large)
        if result is not None:
            st.success(f"Scaled Granulation Time (Large Scale): **{result} seconds**")

    st.markdown("---")

    st.header("2️⃣ Impeller RPM Scale-Up")
    method_rpm = st.selectbox("Select Scaling Method (RPM)", ["Tip Speed (Shear Matching)", "Tip Distance (Total Exposure Matching)"])
    D_small_rpm = st.number_input("Small Scale Impeller Diameter (mm)", min_value=10.0, value=200.0, key="D_small_rpm")
    N_small_rpm = st.number_input("Small Scale RPM", min_value=10.0, value=100.0, key="N_small_rpm")
    t_small_rpm = st.number_input("Small Scale Time (seconds)", min_value=1.0, value=180.0, key="t_small_rpm")
    D_large_rpm = st.number_input("Large Scale Impeller Diameter (mm)", min_value=10.0, value=600.0, key="D_large_rpm")
    t_large_rpm = st.number_input("Large Scale Time (seconds)", min_value=1.0, value=120.0, key="t_large_rpm")

    if st.button("⚙️ Calculate Large Scale RPM"):
        result = impeller_rpm_scaleup(method_rpm, D_small_rpm, N_small_rpm, t_small_rpm, D_large_rpm, t_large_rpm)
        if result is not None:
            st.success(f"Required Large Scale RPM: **{result} RPM**")

if __name__ == "__main__":
    main()

