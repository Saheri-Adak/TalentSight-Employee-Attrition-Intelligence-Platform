# Import Necessary Libraries
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import shap
import matplotlib.pyplot as plt
import os

# Page config
st.set_page_config(
    page_title="TalentSight — Employee Attrition Intelligence",
    page_icon="🎯",
    layout="wide"
)

# Load models
@st.cache_resource
def load_models():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    models_dir = os.path.join(BASE_DIR, '..', 'models')
    
    xgb_pipeline = joblib.load(os.path.join(models_dir, 'xgb_pipeline.pkl'))
    kmeans_model = joblib.load(os.path.join(models_dir, 'kmeans_model.pkl'))
    kmeans_scaler = joblib.load(os.path.join(models_dir, 'kmeans_scaler.pkl'))
    optimal_threshold = joblib.load(os.path.join(models_dir, 'optimal_threshold.pkl'))
    
    return xgb_pipeline, kmeans_model, kmeans_scaler, optimal_threshold

xgb_pipeline, kmeans_model, kmeans_scaler, optimal_threshold = load_models()

# Sidebar navigation
st.sidebar.title("🎯 TalentSight")
st.sidebar.markdown("*Employee Attrition Intelligence Platform*")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate",
    ["🔍 Employee Risk Scorer", "👥 Segment Explorer", "💰 ROI Calculator"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Model Performance**")
st.sidebar.metric("XGBoost Test AUC", "0.817")
st.sidebar.metric("Optimal Threshold", "0.29")
st.sidebar.metric("Employees Analysed", "1,470")

if page == "🔍 Employee Risk Scorer":
    st.title("🔍 Employee Risk Scorer")
    st.markdown("Enter employee details below to get an attrition risk prediction with explanation.")
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("👤 Demographics")
        employee_name = st.text_input("Employee Name", value="John Doe")
        age = st.slider("Age", 18, 60, 35)
        marital_status = st.selectbox("Marital Status", ["Single", "Married", "Divorced"])
        education = st.selectbox("Education Level", [1, 2, 3, 4, 5], 
                                  format_func=lambda x: {1:"Below College", 2:"College", 
                                  3:"Bachelor", 4:"Master", 5:"Doctor"}[x])
        distance_from_home = st.slider("Distance From Home (km)", 1, 29, 5)
        num_companies_worked = st.slider("Number of Companies Worked", 0, 9, 2)

    with col2:
        st.subheader("💼 Job Details")
        department = st.selectbox("Department", ["Sales", "Research & Development", "Human Resources"])
        job_role = st.selectbox("Job Role", [
            "Sales Executive", "Research Scientist", "Laboratory Technician",
            "Manufacturing Director", "Healthcare Representative", "Manager",
            "Sales Representative", "Research Director", "Human Resources"
        ])
        job_level = st.selectbox("Job Level", [1, 2, 3, 4, 5])
        business_travel = st.selectbox("Business Travel", ["Non-Travel", "Travel_Rarely", "Travel_Frequently"])
        monthly_income = st.number_input("Monthly Income ($)", 1000, 20000, 5000, step=100)
        stock_option_level = st.selectbox("Stock Option Level", [0, 1, 2, 3])
        percent_salary_hike = st.slider("Percent Salary Hike", 11, 25, 14)

    with col3:
        st.subheader("📊 Engagement & Tenure")
        job_satisfaction = st.selectbox("Job Satisfaction", [1, 2, 3, 4],
                                         format_func=lambda x: {1:"Low", 2:"Medium", 3:"High", 4:"Very High"}[x])
        environment_satisfaction = st.selectbox("Environment Satisfaction", [1, 2, 3, 4],
                                                 format_func=lambda x: {1:"Low", 2:"Medium", 3:"High", 4:"Very High"}[x])
        work_life_balance = st.selectbox("Work Life Balance", [1, 2, 3, 4],
                                          format_func=lambda x: {1:"Bad", 2:"Good", 3:"Better", 4:"Best"}[x])
        job_involvement = st.selectbox("Job Involvement", [1, 2, 3, 4],
                                        format_func=lambda x: {1:"Low", 2:"Medium", 3:"High", 4:"Very High"}[x])
        relationship_satisfaction = st.selectbox("Relationship Satisfaction", [1, 2, 3, 4],
                                                   format_func=lambda x: {1:"Low", 2:"Medium", 3:"High", 4:"Very High"}[x])
        years_at_company = st.slider("Years at Company", 0, 40, 5)
        years_since_last_promotion = st.slider("Years Since Last Promotion", 0, 15, 1)
        years_with_curr_manager = st.slider("Years With Current Manager", 0, 17, 3)
        years_in_current_role = st.slider("Years in Current Role", 0, 18, 3)
        training_times_last_year = st.slider("Training Times Last Year", 0, 6, 2)

    st.markdown("---")
    st.subheader("💰 Payroll Information")
    pcol1, pcol2 = st.columns(2)
    with pcol1:
        overtime_month_ratio = st.slider("Overtime Frequency (% of months)", 0, 100, 10) / 100
    with pcol2:
        avg_bonus_pct = st.number_input("Average Bonus (% of salary)", 0.0, 25.0, 2.0, step=0.5)

        st.markdown("---")
    
    if st.button("🎯 Predict Attrition Risk", type="primary", use_container_width=True):
        
        # Calculate engineered features
        career_stagnation_index = years_at_company / (num_companies_worked + 1)
        promotion_velocity = years_at_company / (years_since_last_promotion + 1)
        role_stagnation_ratio = years_in_current_role / (years_at_company + 1)
        manager_stability_ratio = years_with_curr_manager / (years_at_company + 1)
        training_intensity = training_times_last_year / (years_at_company + 1)

        # Build input dataframe
        input_data = pd.DataFrame({
            'Age': [age],
            'BusinessTravel': [business_travel],
            'Department': [department],
            'DistanceFromHome': [distance_from_home],
            'Education': [education],
            'EnvironmentSatisfaction': [environment_satisfaction],
            'JobInvolvement': [job_involvement],
            'JobLevel': [job_level],
            'JobRole': [job_role],
            'JobSatisfaction': [job_satisfaction],
            'MaritalStatus': [marital_status],
            'MonthlyIncome': [monthly_income],
            'NumCompaniesWorked': [num_companies_worked],
            'PercentSalaryHike': [percent_salary_hike],
            'RelationshipSatisfaction': [relationship_satisfaction],
            'StockOptionLevel': [stock_option_level],
            'TrainingTimesLastYear': [training_times_last_year],
            'WorkLifeBalance': [work_life_balance],
            'YearsAtCompany': [years_at_company],
            'YearsSinceLastPromotion': [years_since_last_promotion],
            'salary_growth_rate': [0.10],
            'bonus_month_ratio': [min(avg_bonus_pct / 10, 0.33)],
            'overtime_month_ratio': [overtime_month_ratio],
            'avg_bonus_pct': [avg_bonus_pct],
            'career_stagnation_index': [career_stagnation_index],
            'promotion_velocity': [promotion_velocity],
            'role_stagnation_ratio': [role_stagnation_ratio],
            'manager_stability_ratio': [manager_stability_ratio],
            'training_intensity': [training_intensity]
        })

        # Get prediction
        attrition_prob = xgb_pipeline.predict_proba(input_data)[0][1]
        attrition_flag = int(attrition_prob >= optimal_threshold)

        # Display results
        st.markdown("---")
        st.subheader(f"📋 Risk Assessment — {employee_name}")

        rcol1, rcol2, rcol3 = st.columns(3)

        with rcol1:
            if attrition_flag == 1:
                st.error(f"⚠️ HIGH FLIGHT RISK")
            else:
                st.success(f"✅ LOW FLIGHT RISK")

        with rcol2:
            st.metric("Attrition Probability", f"{attrition_prob:.1%}")

        with rcol3:
            st.metric("Decision Threshold", f"{optimal_threshold:.2f}")

        # SHAP waterfall chart
        st.subheader("🔍 What's Driving This Prediction?")

        xgb_model = xgb_pipeline.named_steps['classifier']
        preprocessor = xgb_pipeline.named_steps['preprocessor']
        input_transformed = preprocessor.transform(input_data)
        feature_names = preprocessor.get_feature_names_out()

        explainer = shap.TreeExplainer(xgb_model)
        shap_values = explainer.shap_values(input_transformed)

        fig, ax = plt.subplots(figsize=(10, 6))
        shap.waterfall_plot(
            shap.Explanation(
                values=shap_values[0],
                base_values=explainer.expected_value,
                data=input_transformed[0],
                feature_names=feature_names
            ),
            max_display=10,
            show=False
        )
        st.pyplot(fig)
        plt.close()

        # Retention Strategy Recommendations
        st.markdown("---")
        st.subheader("💡 Recommended Retention Actions")

        recommendations = []

        if overtime_month_ratio > 0.5:
            recommendations.append({
                "priority": "🔴 High",
                "action": "Reduce Overtime Load",
                "detail": f"Employee works overtime {overtime_month_ratio:.0%} of months. Implement workload review and mandatory compensatory time policy."
            })

        if stock_option_level == 0:
            recommendations.append({
                "priority": "🔴 High",
                "action": "Grant Stock Options",
                "detail": "Employee has no equity stake. Extending Level 1 stock options could reduce attrition risk by up to 15 percentage points."
            })

        if monthly_income < 5000 and job_level <= 2:
            recommendations.append({
                "priority": "🟡 Medium",
                "action": "Compensation Review",
                "detail": f"Monthly income of ${monthly_income:,} is below median for Job Level {job_level}. Schedule immediate salary benchmarking."
            })

        if years_since_last_promotion >= 3:
            recommendations.append({
                "priority": "🟡 Medium",
                "action": "Career Development Discussion",
                "detail": f"No promotion in {years_since_last_promotion} years. Schedule career development conversation and define clear promotion criteria."
            })

        if job_satisfaction <= 2 or environment_satisfaction <= 2:
            recommendations.append({
                "priority": "🟡 Medium",
                "action": "Engagement Check-in",
                "detail": "Low satisfaction scores detected. Conduct confidential 1-on-1 conversation to identify specific pain points."
            })

        if marital_status == "Single" and job_level <= 2:
            recommendations.append({
                "priority": "🟢 Low",
                "action": "Social Connection Programme",
                "detail": "Single early-career employees benefit from mentorship and team social activities to build company loyalty."
            })

        if not recommendations:
            st.success("✅ No immediate interventions required. Employee profile indicates low attrition risk.")
        else:
            for rec in recommendations:
                with st.expander(f"{rec['priority']} — {rec['action']}"):
                    st.write(rec['detail'])

        # Replacement cost warning
        if attrition_flag == 1:
            replacement_cost = monthly_income * 12 * 1.5
            st.warning(f"⚠️ If this employee leaves, estimated replacement cost: **${replacement_cost:,.0f}**")

elif page == "👥 Segment Explorer":
    st.title("👥 Workforce Segment Explorer")
    st.markdown("Explore the 5 workforce segments identified by K-Means clustering.")
    st.markdown("---")

    # Load clustered data
    @st.cache_data
    def load_clustered_data():
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        return pd.read_csv(os.path.join(BASE_DIR, '..', 'data', 'processed', 
                                         'employee_master_clustered.csv'))
    
    clustered_df = load_clustered_data()

    # Segment summary cards
    st.subheader("📊 Segment Overview")
    
    segment_stats = clustered_df.groupby('Cluster_Name').agg(
        Count=('Cluster_Name', 'count'),
        Attrition_Rate=('Attrition', lambda x: (x == 'Yes').mean() * 100),
        Avg_Income=('MonthlyIncome', 'mean'),
        Avg_Age=('Age', 'mean')
    ).round(1).reset_index()
    
    segment_stats = segment_stats.sort_values('Attrition_Rate', ascending=False)

    cols = st.columns(5)
    colors = {'Overworked Juniors': '🔴', 'Disengaged Juniors': '🟡', 
              'Stagnant Mid-Seniors': '🟡', 'Senior Stable': '🟢', 
              'High Potential Fast Trackers': '🟢'}
    
    for idx, (col, (_, row)) in enumerate(zip(cols, segment_stats.iterrows())):
        with col:
            emoji = colors.get(row['Cluster_Name'], '⚪')
            st.metric(
                label=f"{emoji} {row['Cluster_Name']}",
                value=f"{row['Attrition_Rate']:.1f}%",
                delta=f"{int(row['Count'])} employees"
            )

    st.markdown("---")

    # Segment selector
    selected_segment = st.selectbox(
        "Select a segment to explore:",
        segment_stats['Cluster_Name'].tolist()
    )

    segment_data = clustered_df[clustered_df['Cluster_Name'] == selected_segment]

    scol1, scol2 = st.columns(2)

    with scol1:
        st.subheader(f"📋 {selected_segment} Profile")
        profile_features = ['Age', 'JobLevel', 'MonthlyIncome', 
                           'YearsSinceLastPromotion', 'overtime_month_ratio',
                           'career_stagnation_index']
        profile = segment_data[profile_features].mean().round(2)
        
        for feature, value in profile.items():
            st.metric(feature, f"{value:.2f}")

    with scol2:
        st.subheader("🏢 Department Breakdown")
        dept_counts = segment_data['Department'].value_counts()
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.pie(dept_counts.values, labels=dept_counts.index, autopct='%1.1f%%',
               colors=['#2196F3', '#4CAF50', '#FF9800'])
        ax.set_title(f'Department Mix — {selected_segment}')
        st.pyplot(fig)
        plt.close()

    st.markdown("---")
    st.subheader("💡 Retention Strategy")

    strategies = {
        'Overworked Juniors': "**Priority: Critical** — Implement overtime caps immediately. Review compensation for junior employees working >50% overtime months. Consider workload redistribution across teams.",
        'Disengaged Juniors': "**Priority: Medium** — Launch early career development programme. Extend stock option eligibility to Level 1 employees. Assign mentors from senior segments.",
        'Stagnant Mid-Seniors': "**Priority: Medium** — Conduct immediate promotion review for employees with >5 years since last promotion. Create lateral mobility opportunities and project leadership roles.",
        'Senior Stable': "**Priority: Low** — Focus on knowledge transfer and mentorship roles. Offer flexible working arrangements. Monitor for retirement planning needs.",
        'High Potential Fast Trackers': "**Priority: Retain** — Maintain promotion velocity. Invest in leadership development and succession planning. These employees are your future senior leaders."
    }

    st.info(strategies.get(selected_segment, "No strategy defined."))

elif page == "💰 ROI Calculator":
    st.title("💰 Retention ROI Calculator")
    st.markdown("Estimate the financial return of targeted retention interventions.")
    st.markdown("---")

    # Load data for calculations
    @st.cache_data
    def load_master_data():
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        return pd.read_csv(os.path.join(BASE_DIR, '..', 'data', 'processed',
                                         'employee_master_clustered.csv'))

    master_df = load_master_data()

    # Key assumptions
    st.subheader("⚙️ Assumptions")
    acol1, acol2 = st.columns(2)

    with acol1:
        replacement_multiplier = st.slider(
            "Replacement Cost Multiplier (× annual salary)",
            min_value=1.0, max_value=3.0, value=1.5, step=0.1
        )
        intervention_cost = st.number_input(
            "Intervention Cost per Employee ($)",
            min_value=5000, max_value=50000, value=20000, step=1000
        )

    with acol2:
        intervention_coverage = st.slider(
            "% of At-Risk Employees We Intervene With",
            min_value=0, max_value=100, value=50, step=5
        )
        intervention_success_rate = st.slider(
            "Intervention Success Rate (%)",
            min_value=0, max_value=100, value=60, step=5
        )

    st.markdown("---")

    # Calculations
    avg_monthly_income = master_df['MonthlyIncome'].mean()
    avg_annual_salary = avg_monthly_income * 12
    replacement_cost = avg_annual_salary * replacement_multiplier

    total_employees = len(master_df)
    attrition_count = (master_df['Attrition'] == 'Yes').sum()
    attrition_rate = attrition_count / total_employees

    # At-risk employees (using model threshold)
    at_risk_count = int(attrition_count * (intervention_coverage / 100))
    intervention_total_cost = at_risk_count * intervention_cost
    employees_retained = int(at_risk_count * (intervention_success_rate / 100))
    cost_avoided = employees_retained * replacement_cost
    net_saving = cost_avoided - intervention_total_cost
    roi = (net_saving / intervention_total_cost * 100) if intervention_total_cost > 0 else 0

    # Display KPI cards
    st.subheader("📊 Financial Impact")
    kcol1, kcol2, kcol3, kcol4 = st.columns(4)

    with kcol1:
        st.metric("Employees Intervened", f"{at_risk_count}")
    with kcol2:
        st.metric("Total Intervention Cost", f"${intervention_total_cost:,.0f}")
    with kcol3:
        st.metric("Estimated Cost Avoided", f"${cost_avoided:,.0f}")
    with kcol4:
        if net_saving > 0:
            st.metric("Net Saving", f"${net_saving:,.0f}", delta="Positive ROI")
        else:
            st.metric("Net Saving", f"${net_saving:,.0f}", delta="Negative ROI",
                      delta_color="inverse")

    st.markdown("---")

    # ROI sweep chart
    st.subheader("📈 ROI Across Intervention Coverage Levels")

    coverages = range(0, 101, 5)
    roi_values = []
    net_savings = []

    for cov in coverages:
        at_risk = int(attrition_count * (cov / 100))
        cost = at_risk * intervention_cost
        retained = int(at_risk * (intervention_success_rate / 100))
        avoided = retained * replacement_cost
        net = avoided - cost
        roi_val = (net / cost * 100) if cost > 0 else 0
        roi_values.append(roi_val)
        net_savings.append(net)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    axes[0].plot(list(coverages), net_savings, 'b-o', linewidth=2, markersize=4)
    axes[0].axhline(y=0, color='red', linestyle='--', alpha=0.5)
    axes[0].axvline(x=intervention_coverage, color='green', linestyle='--',
                    label=f'Current: {intervention_coverage}%')
    axes[0].set_xlabel('Intervention Coverage (%)')
    axes[0].set_ylabel('Net Saving ($)')
    axes[0].set_title('Net Saving vs Intervention Coverage')
    axes[0].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x/1e6:.1f}M'))
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    axes[1].plot(list(coverages), roi_values, 'r-o', linewidth=2, markersize=4)
    axes[1].axhline(y=0, color='black', linestyle='--', alpha=0.5)
    axes[1].axvline(x=intervention_coverage, color='green', linestyle='--',
                    label=f'Current: {intervention_coverage}%')
    axes[1].set_xlabel('Intervention Coverage (%)')
    axes[1].set_ylabel('ROI (%)')
    axes[1].set_title('ROI vs Intervention Coverage')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    st.markdown("---")
    st.subheader("📋 Segment-Level Breakdown")

    segment_roi = master_df.groupby('Cluster_Name').agg(
        Employees=('Cluster_Name', 'count'),
        Attrition_Count=('Attrition', lambda x: (x == 'Yes').sum()),
        Avg_Income=('MonthlyIncome', 'mean')
    ).reset_index()

    segment_roi['Replacement_Cost'] = segment_roi['Avg_Income'] * 12 * replacement_multiplier
    segment_roi['At_Risk'] = (segment_roi['Attrition_Count'] * intervention_coverage / 100).astype(int)
    segment_roi['Intervention_Cost'] = segment_roi['At_Risk'] * intervention_cost
    segment_roi['Retained'] = (segment_roi['At_Risk'] * intervention_success_rate / 100).astype(int)
    segment_roi['Cost_Avoided'] = segment_roi['Retained'] * segment_roi['Replacement_Cost']
    segment_roi['Net_Saving'] = segment_roi['Cost_Avoided'] - segment_roi['Intervention_Cost']

    segment_roi = segment_roi[['Cluster_Name', 'Employees', 'At_Risk',
                                'Intervention_Cost', 'Cost_Avoided', 'Net_Saving']]
    segment_roi.columns = ['Segment', 'Employees', 'Intervened',
                            'Intervention Cost', 'Cost Avoided', 'Net Saving']

    segment_roi['Intervention Cost'] = segment_roi['Intervention Cost'].apply(lambda x: f'${x:,.0f}')
    segment_roi['Cost Avoided'] = segment_roi['Cost Avoided'].apply(lambda x: f'${x:,.0f}')
    segment_roi['Net Saving'] = segment_roi['Net Saving'].apply(lambda x: f'${x:,.0f}')

    st.dataframe(segment_roi, use_container_width=True)