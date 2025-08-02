import streamlit as st
from kafka import KafkaConsumer
import json
from datetime import datetime
import pandas as pd
from collections import Counter

# Page config
st.set_page_config(page_title="Stroke Detection Alerts with Visuals", layout="wide")
st.title("🚨 Real-Time Stroke Detection Dashboard")

# Kafka consumer setup
consumer = KafkaConsumer(
    'stroke_topic_alert',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='latest',
    group_id='dashboard_group',
    enable_auto_commit=True
)

# Function to evaluate stroke rules for manual input
def evaluate_stroke_rules(event):
    """
    Evaluates the event against the defined stroke risk rules.
    Returns a dictionary with riskLevel and triggeredRule if a rule matches.
    Returns None if no rule matches.
    """
    age = float(event.get('age', 0))
    avg_glucose_level = float(event.get('avg_glucose_level', 0))
    hypertension = float(event.get('hypertension', 0))
    bmi = float(event.get('bmi', 0))
    smoking_status = event.get('smoking_status', '')

    # Rule 1: age > 67.50 AND avg_glucose_level > 167.67
    if age > 67.50 and avg_glucose_level > 167.67:
        return {
            'riskLevel': 'High Risk',
            'triggeredRule': 'Rule 1: age > 67.50 and avg_glucose_level > 167.67'
        }

    # Rule 2: age < 54.4 AND hypertension > 0.5 AND bmi > 32.1 AND smoking_status == 'smokes'
    if (age < 54.4 and
            hypertension > 0.5 and
            bmi > 32.1 and
            smoking_status == 'smokes'):
        return {
            'riskLevel': 'High Risk',
            'triggeredRule': 'Rule 2: age < 54.4 and hypertension > 0.5 and bmi > 32.1 and smoking_status == smokes'
        }

    return None

# Containers for visuals and alerts (Original Dashboard)
st.subheader("📊 Real-Time Visualizations")
col1, col2 = st.columns(2)

with col1:
    st.markdown("**Cumulative Alerts Over Time**")
    line_chart = st.line_chart()

with col2:
    st.markdown("**Alert Reasons Distribution**")
    bar_chart = st.bar_chart()

st.subheader("🔔 Live Stroke Alerts")
alert_box = st.empty()

# Data structures to accumulate stats
timestamps = []
cumulative_counts = []
reason_counter = Counter()
alerts_displayed = []

# Track cumulative total
total_alerts = 0

# New Section: Manual Event Input
st.subheader("📋 Manual Patient Vital Input")
with st.form(key='vital_form'):
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.slider("Age", min_value=0, max_value=100, value=50)
        avg_glucose_level = st.slider("Average Glucose Level", min_value=50.0, max_value=300.0, value=100.0, step=0.1)
        smoking_status = st.selectbox("Smoking Status", options=['smokes', 'formerly smoked', 'never smoked', 'unknown'])
    
    with col2:
        hypertension = st.selectbox("Hypertension", options=[0, 1], format_func=lambda x: 'Yes' if x == 1 else 'No')
        bmi = st.slider("BMI", min_value=10.0, max_value=60.0, value=25.0, step=0.1)

    submit_button = st.form_submit_button(label="Evaluate Stroke Risk")

# Process manual input
if submit_button:
    event = {
        'age': age,
        'avg_glucose_level': avg_glucose_level,
        'hypertension': hypertension,
        'bmi': bmi,
        'smoking_status': smoking_status
    }
    result = evaluate_stroke_rules(event)
    
    st.subheader("📊 Manual Stroke Risk Evaluation Result")
    if result:
        st.markdown(f"**Risk Level**: {result['riskLevel']} 🚨")
        st.markdown(f"**Triggered Rule**: {result['triggeredRule']}")
    else:
        st.markdown("**Risk Level**: Low Risk ✅")

# Infinite loop processing messages (Original Kafka Loop)
for message in consumer:
    alert = message.value
    event = alert['event']

    # Parse time and update cumulative count
    ts = datetime.fromtimestamp(event['detection_timestamp'] / 1000)
    timestamps.append(ts)
    total_alerts += 1
    cumulative_counts.append(total_alerts)

    # Update cumulative line chart
    df_time = pd.DataFrame({'Total Alerts': cumulative_counts}, index=pd.to_datetime(timestamps))
    line_chart.add_rows(df_time.tail(50))  # show last 50 points

    # Update reason distribution
    reason_counter[event['triggeredRule']] += 1
    df_reason = pd.DataFrame.from_dict(reason_counter, orient='index', columns=['count'])
    bar_chart.add_rows(df_reason)

    # Prepare and display alert details
    alert_time_str = ts.strftime('%Y-%m-%d %H:%M:%S')
    alert_str = f"🧑‍⚕️**(ID :{event['id']})**\n **(Risk Level: {event['riskLevel']})**\n- ⏱️ Time: `{alert_time_str}`\n- 📌 **Reason**: {event['triggeredRule']}"

    alerts_displayed.insert(0, alert_str)
    alerts_displayed = alerts_displayed[:20]
    alert_box.markdown("\n---\n".join(alerts_displayed))