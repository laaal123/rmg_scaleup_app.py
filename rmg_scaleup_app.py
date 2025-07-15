import streamlit as st
import math

def granulation_time_scaleup(method, D_small_mm, N_small, t_small_sec, D_large_mm, N_large):
    D_small = D_small_mm / 1000
    D_large = D_large_mm / 1000
    t_small_min = t_small_sec / 60

    if method == "Tip Speed (Shear Matching)":
        V_small = math.pi * D_small * N_small
        t_large_min = (V_small * t_small_min) / (math.pi * D_large * N_large)
    elif method == "Tip Distance (Total Exposure Matching)":
        t_large_min = (D_small * N_small * t_small_min) / (D_large * N_large)
    else:
        st.error("Invalid method selected.")
        return None
    return round(t_large_min, 2)  # minutes

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
    return round(N_large, 2)  # RPM

def get_input_with_manual(label, slider_min, slider_max, slider_default, key):
    use_manual = st.checkbox(f"Manual input for {label}?", key=f"manual_{key}")
    if use_manual:
        val = st.number_input(f"Enter {label} (manual)", min_value=slider_min, max_value=slider_max, value=slider_default, key=f"manual_value_{key}")
    else:
        val = st.slider(label, slider_min, slider_max, slider_default, key=key)
    return val

def main():
    st.title("RMG Scale-Up Calculator")

    st.header("1️⃣ Granulation Time Scale-Up Calculator")
    method_time = st.selectbox("Method", ["Tip Speed (Shear Matching)", "Tip Distance (Total Exposure Matching)"], key="method_time")
    
    D_small_time = get_input_with_manual("D_small (mm)", 10, 2000, 200, "D_small_time")
    N_small_time = get_input_with_manual("N_small (RPM)", 10, 2000, 100, "N_small_time")
    t_small_time = get_input_with_manual("t_small (sec)", 10, 1000, 180, "t_small_time")
    D_large_time = get_input_with_manual("D_large (mm)", 10, 2000, 600, "D_large_time")
    N_large_time = get_input_with_manual("N_large (RPM)", 10, 2000, 50, "N_large_time")

    if st.button("Calculate Granulation Time"):
        result = granulation_time_scaleup(method_time, D_small_time, N_small_time, t_small_time, D_large_time, N_large_time)
        if result is not None:
            st.success(f"🕒 Scaled Granulation Time (Large Scale): {result} minutes")

    st.markdown("---")

    st.header("2️⃣ Impeller RPM Scale-Up Calculator")
    method_rpm = st.selectbox("Method (RPM Calculator)", ["Tip Speed (Shear Matching)", "Tip Distance (Total Exposure Matching)"], key="method_rpm")
    
    D_small_rpm = get_input_with_manual("D_small (mm)", 50, 1000, 200, "D_small_rpm")
    N_small_rpm = get_input_with_manual("N_small (RPM)", 10, 1000, 100, "N_small_rpm")
    t_small_rpm = get_input_with_manual("t_small (sec)", 10, 1000, 180, "t_small_rpm")
    D_large_rpm = get_input_with_manual("D_large (mm)", 100, 2000, 600, "D_large_rpm")
    t_large_rpm = get_input_with_manual("t_large (sec)", 10, 1000, 120, "t_large_rpm")

    if st.button("Calculate Large Scale RPM"):
        result = impeller_rpm_scaleup(method_rpm, D_small_rpm, N_small_rpm, t_small_rpm, D_large_rpm, t_large_rpm)
        if result is not None:
            st.success(f"🌀 Calculated Large Scale RPM: {result} RPM")

if __name__ == "__main__":
    main()
