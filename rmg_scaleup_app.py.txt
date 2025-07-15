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
    return round(t_large_min * 60, 2)  # seconds

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

def main():
    st.title("RMG Scale-Up Calculator")

    st.header("1️⃣ Granulation Time Scale-Up Calculator")
    method_time = st.selectbox("Method", ["Tip Speed (Shear Matching)", "Tip Distance (Total Exposure Matching)"])
    D_small_time = st.slider("D_small (mm)", 50, 1000, 200)
    N_small_time = st.slider("N_small (RPM)", 10, 200, 100)
    t_small_time = st.slider("t_small (sec)", 10, 600, 180)
    D_large_time = st.slider("D_large (mm)", 100, 2000, 600)
    N_large_time = st.slider("N_large (RPM)", 10, 200, 50)

    if st.button("Calculate Granulation Time"):
        result = granulation_time_scaleup(method_time, D_small_time, N_small_time, t_small_time, D_large_time, N_large_time)
        if result is not None:
            st.success(f"Scaled Granulation Time (Large Scale): {result} seconds")

    st.markdown("---")

    st.header("2️⃣ Impeller RPM Scale-Up Calculator")
    method_rpm = st.selectbox("Method (RPM Calculator)", ["Tip Speed (Shear Matching)", "Tip Distance (Total Exposure Matching)"], key="method_rpm")
    D_small_rpm = st.slider("D_small (mm)", 50, 1000, 200, key="D_small_rpm")
    N_small_rpm = st.slider("N_small (RPM)", 10, 200, 100, key="N_small_rpm")
    t_small_rpm = st.slider("t_small (sec)", 10, 600, 180, key="t_small_rpm")
    D_large_rpm = st.slider("D_large (mm)", 100, 2000, 600, key="D_large_rpm")
    t_large_rpm = st.slider("t_large (sec)", 10, 600, 120, key="t_large_rpm")

    if st.button("Calculate Large Scale RPM"):
        result = impeller_rpm_scaleup(method_rpm, D_small_rpm, N_small_rpm, t_small_rpm, D_large_rpm, t_large_rpm)
        if result is not None:
            st.success(f"Calculated Large Scale RPM: {result} RPM")

if __name__ == "__main__":
    main()
