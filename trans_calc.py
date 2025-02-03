import streamlit as st

# Set page configuration for wide layout
st.set_page_config(page_title="Wire Length Calculator", layout="wide")

# Title in color
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🌡️ Trans Calc-TC </h1>", unsafe_allow_html=True)

# Form for input
with st.form("input_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔥 Temperature Parameters", unsafe_allow_html=True)
        lt = st.number_input("Low Temperature (°C)", format="%f", help="Enter the reference low temperature", value=None)
        ht = st.number_input("High Temperature (°C)", format="%f", help="Enter the reference high temperature", value=None)
        
        st.markdown("### ⚡ Wire Selection", unsafe_allow_html=True)
        wire_type = st.selectbox(
            "Material Type",
            ["Copper(Cu)", "Balco"],
            index=None,
            placeholder="Select wire material",
            help="Choose between Copper or Balco alloy"
        )
    
    with col2:
        st.markdown("### 📊 Output Parameters", unsafe_allow_html=True)
        ltb = st.number_input("Low Temperature Output (mV/V)", format="%f", help="Enter output at low temperature")
        htb = st.number_input("High Temperature Output (mV/V)", format="%f", help="Enter output at high temperature")
        br = st.number_input("Bridge Resistance (Ω)", format="%d", help="Enter bridge resistance value")

    submitted = st.form_submit_button("🚀 Calculate", use_container_width=True)

# Handle form submission and validation
if submitted:
    error_messages = []
    
    if (lt is None or ht is None or 
        not all([lt, ht, ltb, htb, br]) or 
        not wire_type):
        
        if lt is None:
            error_messages.append("❌ Low Temperature must be entered.")
        if ht is None:
            error_messages.append("❌ High Temperature must be entered.")
        if not all([lt, ht, ltb, htb, br]):
            error_messages.append("❌ All fields must be filled.")
        if not wire_type:
            error_messages.append("❌ Wire type must be selected.")
        
        for error in error_messages:
            st.error(error)
    else:
        # Perform calculations
        try:
            BA = (htb - ltb) / (ht - lt)
            tracker = "P+S+" if BA > 0 else "P-S+"
            
            if wire_type == "Copper(Cu)":
                R = (abs((htb - ltb)/1000) * br) * 4 / (0.004 * abs(ht - lt))
                L = (1 / 5.484) * R * 1000
            else:  # Balco
                R = (abs(htb - ltb)/1000 * br) * 4 / (0.0045 * abs(ht - lt))
                L = (1 / 62.9921) * R * 1000
            
            # Success message and results
            st.success("🎉 Calculation Successful!")
            
            # Display results in columns
            col_result1, col_result2 = st.columns(2)
            with col_result1:
                st.metric("Optimal Wire Length", f"{round(L, 1)} mm", help="Recommended wire length for optimal performance")
            with col_result2:
                st.metric("Bridge Configuration", tracker, help="Recommended bridge arm configuration")
            
            # Detailed results in an expander
            with st.expander("📈 Calculation Details"):
                st.write(f"**Bridge Arm Ratio:** {BA:.4f}")
                st.write(f"**Calculated Resistance:** {R:.2f} Ω")
                st.write(f"**Temperature Range:** {lt}°C to {ht}°C")
        
        except ZeroDivisionError:
            st.error("⚠️ Temperature values cannot be identical.")
        except Exception as e:
            st.error(f"⚠️ Calculation error: {str(e)}")

# Documentation sidebar
with st.sidebar:
    st.header("📖 User Guide")
    st.markdown("""
    **Instructions:**
    1. Enter temperature parameters.
    2. Provide output measurements.
    3. Select wire material.
    4. Click "Calculate" to get results.
    
    ⚠️ **Important Notes:**
    - Low Temperature must be below 0°C (original VBA requirement).
    - All fields are mandatory for calculation to proceed.
    """)
    st.divider()
    st.markdown("⚙️ **Calculation Methodology:**")
    st.caption("Maintains original TRANS CALC formulas for copper and balco wire calculations.")
