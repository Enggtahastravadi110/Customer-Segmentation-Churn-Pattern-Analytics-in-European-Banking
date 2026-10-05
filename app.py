import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="European Bank Churn Analytics", layout="wide", page_icon="🏦")

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    df = pd.read_csv("bank_churn_cleaned.csv")
    return df

df = load_data()

st.title("🏦 Customer Segmentation & Churn Analytics — European Banking")
st.caption("Interactive dashboard | 10,000 customers across France, Germany & Spain")

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.header("🔎 Filters")
geo_filter = st.sidebar.multiselect("Geography", sorted(df['Geography'].unique()), default=sorted(df['Geography'].unique()))
gender_filter = st.sidebar.multiselect("Gender", sorted(df['Gender'].unique()), default=sorted(df['Gender'].unique()))
age_filter = st.sidebar.multiselect("Age Group", sorted(df['AgeGroup'].astype(str).unique()), default=sorted(df['AgeGroup'].astype(str).unique()))
balance_filter = st.sidebar.multiselect("Balance Segment", sorted(df['BalanceSegment'].unique()), default=sorted(df['BalanceSegment'].unique()))

filtered = df[
    (df['Geography'].isin(geo_filter)) &
    (df['Gender'].isin(gender_filter)) &
    (df['AgeGroup'].astype(str).isin(age_filter)) &
    (df['BalanceSegment'].isin(balance_filter))
]

if filtered.empty:
    st.warning("No customers match the selected filters. Please broaden your selection.")
    st.stop()

# ---------------- KPI ROW ----------------
total_customers = len(filtered)
churn_rate = filtered['Exited'].mean() * 100
hv = filtered[filtered['BalanceSegment'] == 'High-Balance']
hv_churn_rate = hv['Exited'].mean() * 100 if len(hv) else 0
revenue_at_risk = filtered[filtered['Exited'] == 1]['Balance'].sum()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Customers", f"{total_customers:,}")
col2.metric("Churn Rate", f"{churn_rate:.2f}%")
col3.metric("High-Value Churn Rate", f"{hv_churn_rate:.2f}%")
col4.metric("Revenue at Risk", f"€{revenue_at_risk:,.0f}")

st.markdown("---")

# ---------------- TABS (Core Modules) ----------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Overall Summary",
    "🌍 Geography View",
    "👥 Age & Tenure",
    "💎 High-Value Explorer"
])

# ===== TAB 1: Overall Summary =====
with tab1:
    c1, c2 = st.columns(2)
    with c1:
        churn_counts = filtered['Exited'].map({0: 'Retained', 1: 'Churned'}).value_counts().reset_index()
        churn_counts.columns = ['Status', 'Count']
        fig = px.pie(churn_counts, names='Status', values='Count',
                     title='Retained vs Churned', color='Status',
                     color_discrete_map={'Retained': '#4C78A8', 'Churned': '#E45756'})
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        gender_churn = filtered.groupby('Gender')['Exited'].mean().reset_index()
        gender_churn['Exited'] = gender_churn['Exited'] * 100
        fig = px.bar(gender_churn, x='Gender', y='Exited', title='Churn Rate by Gender',
                     text_auto='.1f', color='Gender')
        fig.update_layout(yaxis_title='Churn Rate (%)')
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Churned vs Retained — Average Profile")
    profile = filtered.groupby('Exited')[['CreditScore', 'Age', 'Tenure', 'Balance', 'EstimatedSalary', 'NumOfProducts']].mean().round(2)
    profile.index = profile.index.map({0: 'Retained', 1: 'Churned'})
    st.dataframe(profile, use_container_width=True)

# ===== TAB 2: Geography View =====
with tab2:
    c1, c2 = st.columns(2)
    with c1:
        geo_churn = filtered.groupby('Geography')['Exited'].mean().reset_index()
        geo_churn['Exited'] = geo_churn['Exited'] * 100
        fig = px.bar(geo_churn, x='Geography', y='Exited', title='Churn Rate by Geography',
                     text_auto='.1f', color='Geography')
        fig.update_layout(yaxis_title='Churn Rate (%)')
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        geo_gender = filtered.pivot_table(index='Geography', columns='Gender', values='Exited', aggfunc='mean') * 100
        fig = px.imshow(geo_gender, text_auto='.1f', color_continuous_scale='Reds',
                         title='Churn Rate (%) — Geography × Gender')
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Churn Rate (%) — Geography × Age Group")
    geo_age = filtered.pivot_table(index='Geography', columns='AgeGroup', values='Exited', aggfunc='mean') * 100
    fig = px.imshow(geo_age, text_auto='.1f', color_continuous_scale='Reds', aspect='auto')
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(geo_age.round(2), use_container_width=True)

# ===== TAB 3: Age & Tenure =====
with tab3:
    c1, c2 = st.columns(2)
    with c1:
        age_churn = filtered.groupby('AgeGroup', observed=True)['Exited'].mean().reset_index()
        age_churn['Exited'] = age_churn['Exited'] * 100
        fig = px.bar(age_churn, x='AgeGroup', y='Exited', title='Churn Rate by Age Group',
                     text_auto='.1f', color='AgeGroup')
        fig.update_layout(yaxis_title='Churn Rate (%)')
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        tenure_churn = filtered.groupby('TenureGroup', observed=True)['Exited'].mean().reset_index()
        tenure_churn['Exited'] = tenure_churn['Exited'] * 100
        fig = px.bar(tenure_churn, x='TenureGroup', y='Exited', title='Churn Rate by Tenure Group',
                     text_auto='.1f', color='TenureGroup')
        fig.update_layout(yaxis_title='Churn Rate (%)')
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Customer Count vs Churn Rate by Age Group")
    age_summary = filtered.groupby('AgeGroup', observed=True).agg(
        CustomerCount=('Exited', 'count'),
        ChurnRate=('Exited', 'mean')
    ).reset_index()
    age_summary['ChurnRate'] = age_summary['ChurnRate'] * 100

    fig = px.bar(age_summary, x='AgeGroup', y='CustomerCount', text_auto=True,
                 title='Customer Volume by Age Group (bars) with Churn Rate overlay (line)')
    fig2 = px.line(age_summary, x='AgeGroup', y='ChurnRate')
    fig2.update_traces(yaxis='y2', line_color='red')
    fig.add_trace(fig2.data[0])
    fig.update_layout(
        yaxis=dict(title='Customer Count'),
        yaxis2=dict(title='Churn Rate (%)', overlaying='y', side='right')
    )
    st.plotly_chart(fig, use_container_width=True)

# ===== TAB 4: High-Value Explorer =====
with tab4:
    hv_filtered = filtered[filtered['BalanceSegment'] == 'High-Balance']
    hv_churned = hv_filtered[hv_filtered['Exited'] == 1]

    total_hv_balance = hv_filtered['Balance'].sum()
    pct_revenue_at_risk = (revenue_at_risk / total_hv_balance * 100) if total_hv_balance > 0 else 0

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("High-Value Churn Rate", f"{hv_churn_rate:.2f}%")
    k2.metric("Revenue at Risk", f"€{revenue_at_risk:,.0f}")
    k3.metric("% of HV Balance at Risk", f"{pct_revenue_at_risk:.2f}%")
    k4.metric("Total High-Value Balance", f"€{total_hv_balance:,.0f}")

    st.subheader("Age vs Balance — Churn Overlay")
    sample = filtered.sample(min(2000, len(filtered)), random_state=42)
    fig = px.scatter(sample, x='Age', y='Balance', color=sample['Exited'].map({0: 'Retained', 1: 'Churned'}),
                      symbol='Geography', opacity=0.6,
                      color_discrete_map={'Retained': '#4C78A8', 'Churned': '#E45756'},
                      title='Age vs Balance by Churn Status')
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("High-Value Churners — Geography × Age Group")
    if len(hv_churned) > 0:
        hv_matrix = pd.crosstab(hv_churned['Geography'], hv_churned['AgeGroup'], normalize=True) * 100
        st.dataframe(hv_matrix.round(2), use_container_width=True)
    else:
        st.info("No high-value churners in the current filter selection.")

    st.subheader("High-Value Churner Records")
    st.dataframe(
        hv_churned[['CustomerId', 'Geography', 'Gender', 'Age', 'Balance', 'EstimatedSalary', 'CreditScore']]
        .sort_values('Balance', ascending=False),
        use_container_width=True
    )

st.markdown("---")
st.caption("Built with Python & Streamlit | Data: European Retail Bank Customer Dataset | Project by Taha S. Travadi")
