import streamlit as st
from prediction_helper import predict

#  CSS
st.markdown("""
<style>
    /* Title styling */
    .main-title {
        text-align: center;
        color: #1e3c72;
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 10px;
    }

    .subtitle {
        text-align: center;
        color: #4a5568;
        font-size: 1.1rem;
        margin-bottom: 30px;
    }

    /* Section headers */
    .section-title {
        color: #1e3c72;
        font-weight: 700;
        font-size: 1.3rem;
        margin-top: 25px;
        margin-bottom: 15px;
        padding-left: 10px;
        border-left: 4px solid #1e3c72;
    }

    /* Button styling */
    .stButton > button {
        background: #1e3c72;
        color: white;
        font-weight: 700;
        padding: 12px 30px;
        border-radius: 8px;
        border: none;
        font-size: 16px;
        width: 100%;
        margin: 20px 0;
    }

    /* Results styling */
    .result-card {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        text-align: center;
        border: 2px solid #e2e8f0;
    }

    .result-value {
        font-size: 28px;
        font-weight: 800;
        color: #1e3c72;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Set the page configuration
st.set_page_config(page_title="Lauki Finance: Credit Risk Modelling", page_icon="📊")

# Title section
st.markdown('<h1 class="main-title">🏦 Lauki Finance: Credit Risk Modelling</h1>', unsafe_allow_html=True)
# st.markdown('<p class="subtitle">Advanced Credit Risk Assessment & Prediction System</p>', unsafe_allow_html=True)

# Applicant Information Section
st.markdown('<div class="section-title">👤 Applicant Information</div>', unsafe_allow_html=True)
row1 = st.columns(3)

with row1[0]:
    age = st.number_input('Age', min_value=18, step=1, max_value=100, value=28, key='age')
with row1[1]:
    income = st.number_input('Income (₹)', min_value=0, value=1200000, key='income')
with row1[2]:
    loan_amount = st.number_input('Loan Amount (₹)', min_value=0, value=2560000, key='loan_amount')

# Financial Metrics Section
st.markdown('<div class="section-title">📊 Financial Metrics</div>', unsafe_allow_html=True)
row2 = st.columns(3)

with row2[0]:
    # Calculate loan to income ratio
    loan_to_income_ratio = loan_amount / income if income > 0 else 0
    st.metric(label="Loan to Income Ratio", value=f"{loan_to_income_ratio:.2f}")

with row2[1]:
    loan_tenure_months = st.number_input('Loan Tenure (months)', min_value=0, step=1, value=36, key='tenure')
with row2[2]:
    avg_dpd_per_delinquency = st.number_input('Avg DPD', min_value=0, value=20, key='avg_dpd')

# Credit History Section
st.markdown('<div class="section-title">📈 Credit History</div>', unsafe_allow_html=True)
row3 = st.columns(3)

with row3[0]:
    delinquency_ratio = st.number_input('Delinquency Ratio (%)', min_value=0, max_value=100, step=1, value=30,
                                        key='delinquency')
with row3[1]:
    credit_utilization_ratio = st.number_input('Credit Utilization (%)', min_value=0, max_value=100, step=1, value=30,
                                               key='utilization')
with row3[2]:
    num_open_accounts = st.number_input('Open Loan Accounts', min_value=1, max_value=4, step=1, value=2, key='accounts')

# Loan Details Section
st.markdown('<div class="section-title">🏠 Loan Details</div>', unsafe_allow_html=True)
row4 = st.columns(3)

with row4[0]:
    residence_type = st.selectbox('Residence Type', ['Owned', 'Rented', 'Mortgage'], key='residence')
with row4[1]:
    loan_purpose = st.selectbox('Loan Purpose', ['Education', 'Home', 'Auto', 'Personal'], key='purpose')
with row4[2]:
    loan_type = st.selectbox('Loan Type', ['Unsecured', 'Secured'], key='loan_type')

# Add some spacing
st.markdown("<br>", unsafe_allow_html=True)

# Calculate Risk Button
if st.button('📊 Calculate Credit Risk', type='primary'):
    # Call the predict function
    probability, credit_score, rating = predict(
        age, income, loan_amount, loan_tenure_months, avg_dpd_per_delinquency,
        delinquency_ratio, credit_utilization_ratio, num_open_accounts,
        residence_type, loan_purpose, loan_type
    )

    # Display results
    st.markdown("---")
    st.markdown("<h2 style='text-align: center; color: #1e3c72;'>📋 Risk Assessment Results</h2>",
                unsafe_allow_html=True)

    # Results in 3 columns
    result_col1, result_col2, result_col3 = st.columns(3)

    with result_col1:
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown("**Default Probability**")
        st.markdown(f'<div class="result-value">{probability:.2%}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with result_col2:
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown("**Credit Score**")
        st.markdown(f'<div class="result-value">{credit_score}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with result_col3:
        # Color code rating
        rating_lower = rating.lower()
        if "poor" in rating_lower or "high" in rating_lower:
            rating_color = "#ef4444"  # red
        elif "fair" in rating_lower or "moderate" in rating_lower:
            rating_color = "#f59e0b"  # amber
        elif "good" in rating_lower:
            rating_color = "#10b981"  # green
        else:
            rating_color = "#1e3c72"  # blue

        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown("**Risk Rating**")
        st.markdown(f'<div class="result-value" style="color: {rating_color};">{rating}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Add footer
# st.markdown("---")
# st.markdown("*Note: This is a predictive model. Actual loan decisions may vary based on additional factors.*")