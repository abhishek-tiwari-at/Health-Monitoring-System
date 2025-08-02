import streamlit as st
from kafka import KafkaConsumer
import json
from datetime import datetime
import pandas as pd
from collections import Counter

# Page config
st.set_page_config(page_title="Cardio Risk Alerts with Visuals", layout="wide")
st.title("🚨 Real-Time Cardio Risk Detection Dashboard")

# Kafka consumer setup
consumer = KafkaConsumer(
    'cardio_topic_alert',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='latest',
    group_id='dashboard_group',
    enable_auto_commit=True
)

# Function to evaluate rules for manual input
def evaluate_rules(event):
    """
    Evaluates the event against the defined cardio risk rules.
    Returns a dictionary with riskLevel and triggeredRule if a rule matches.
    Returns None if no rule matches.
    """
    ap_hi = float(event.get('ap_hi', 0))
    ap_lo = float(event.get('ap_lo', 0))
    cholesterol = float(event.get('cholesterol', 0))
    age = float(event.get('age', 0))
    gluc = float(event.get('gluc', 0))
    weight = float(event.get('weight', 0))
    active = float(event.get('active', 0))
    alco = float(event.get('alco', 0))
    id_val = float(event.get('id', 0))

    # Rule 1
    if (ap_hi <= 129.50 and
            cholesterol <= 2.50 and
            age <= 22203.50 and
            ap_lo > 98.00 and
            age > 19828.50):
        return {
            'riskLevel': 'High Risk',
            'triggeredRule': 'Rule 1: ap_hi <= 129.50 and cholesterol <= 2.50 and age <= 22203.50 and ap_lo > 98.00 and age > 19828.50'
        }

    # Rule 2
    if (ap_hi <= 129.50 and
            cholesterol <= 2.50 and
            age > 22203.50 and
            ap_lo > 78.00 and
            active <= 0.5):
        return {
            'riskLevel': 'High Risk',
            'triggeredRule': 'Rule 2: ap_hi <= 129.50 and cholesterol <= 2.50 and age > 22203.50 and ap_lo > 78.00 and active <= 0.5'
        }

    # Rule 3
    if (ap_hi <= 129.50 and
            cholesterol > 2.50 and
            age <= 19317.50 and
            gluc <= 2.50 and
            ap_lo <= 72.50):
        return {
            'riskLevel': 'High Risk',
            'triggeredRule': 'Rule 3: ap_hi <= 129.50 and cholesterol > 2.50 and age <= 19317.50 and gluc <= 2.50 and ap_lo <= 72.50'
        }

    # Rule 4
    if (ap_hi <= 129.50 and
            cholesterol > 2.50 and
            age <= 19317.50 and
            gluc <= 2.50 and
            ap_lo <= 72.50):
        return {
            'riskLevel': 'High Risk',
            'triggeredRule': 'Rule 4: ap_hi <= 129.50 and cholesterol > 2.50 and age <= 19317.50 and gluc <= 2.50 and ap_lo <= 72.50'
        }

    # Rule 5
    if (ap_hi <= 129.50 and
            cholesterol > 2.50 and
            age <= 19317.50 and
            gluc > 2.50 and
            weight > 79.50):
        return {
            'riskLevel': 'High Risk',
            'triggeredRule': 'Rule 5: ap_hi <= 129.50 and cholesterol > 2.50 and age <= 19317.50 and gluc > 2.50 and weight > 79.50'
        }

    # Rule 6
    if (ap_hi <= 129.50 and
            cholesterol > 2.50 and
            age > 19317.50 and
            ap_lo <= 79.50 and
            weight <= 67.50):
        return {
            'riskLevel': 'High Risk',
            'triggeredRule': 'Rule 6: ap_hi <= 129.50 and cholesterol > 2.50 and age > 19317.50 and ap_lo <= 79.50 and weight <= 67.50'
        }

    # Rule 7
    if (ap_hi <= 129.50 and
            cholesterol > 2.50 and
            age > 19317.50 and
            ap_lo <= 79.50 and
            weight > 67.50):
        return {
            'riskLevel': 'High Risk',
            'triggeredRule': 'Rule 7: ap_hi <= 129.50 and cholesterol > 2.50 and age > 19317.50 and ap_lo <= 79.50 and weight > 67.50'
        }

    # Rule 8
    if (ap_hi <= 129.50 and
            cholesterol > 2.50 and
            age > 19317.50 and
            ap_lo > 79.50 and
            age <= 19839.50):
        return {
            'ruleLevel': 'High Risk',
            'triggeredRule': 'Rule 8: ap_hi <= 129.50 and cholesterol > 2.50 and age > 19317.50 and ap_lo > 79.50 and age <= 19839.50'
        }

    # Rule 9
    if (ap_hi <= 129.50 and
            cholesterol > 2.50 and
            age > 19317.50 and
            ap_lo > 79.50 and
            age > 19839.50):
        return {
            'riskLevel': 'High Risk',
            'triggeredRule': 'Rule 9: ap_hi <= 129.50 and cholesterol > 2.50 and age > 19317.50 and ap_lo > 79.50 and age > 19839.50'
        }

    # Rule 10
    if (ap_hi > 129.50 and
            ap_hi <= 133.50 and
            ap_lo <= 88.50 and
            age <= 19804.50 and
            cholesterol <= 1.50):
        return {
            'riskLevel': 'High Risk',
            'triggeredRule': 'Rule 10: ap_hi > 129.50 and ap_hi <= 133.50 and ap_lo <= 88.50 and age <= 19804.50 and cholesterol <= 1.50'
        }

    # Rule 11
    if (ap_hi > 129.50 and
            ap_hi <= 133.50 and
            ap_lo <= 88.50 and
            age <= 19804.50 and
            cholesterol > 1.50):
        return {
            'riskLevel': 'High Risk',
            'triggeredRule': 'Rule 11: ap_hi > 129.50 and ap_hi <= 133.50 and ap_lo <= 88.50 and age <= 19804.50 and cholesterol > 1.50'
        }

    # Rule 12
    if (ap_hi > 129.50 and
            ap_hi > 133.50 and
            ap_lo <= 5.00 and
            id_val <= 56213.00):
        return {
            'riskLevel': 'High Risk',
            'triggeredRule': 'Rule 12: ap_hi > 129.50 and ap_hi > 133.50 and ap_lo <= 5.00 and id <= 56213.00'
        }

    # Rule 13
    if (ap_hi > 129.50 and
            ap_hi > 133.50 and
            ap_lo > 5.00 and
            ap_hi <= 138.50 and
            alco <= 0.50):
        return {
            'riskLevel': 'High Risk',
            'triggeredRule': 'Rule 13: ap_hi > 129.50 and ap_hi > 133.50 and ap_lo > 5.00 and ap_hi <= 138.50 and alco <= 0.50'
        }

    # Rule 14
    if (ap_hi > 129.50 and
            ap_hi > 133.50 and
            ap_lo > 5.00 and
            ap_hi > 138.50):
        return {
            'riskLevel': 'High Risk',
            'triggeredRule': 'Rule 14: ap_hi > 129.50 and ap_hi > 133.50 and ap_lo > 5.00 and ap_hi > 138.50'
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
        id_val = st.number_input("Patient ID", min_value=0, max_value=99999, value=1)
        age = st.slider("Age (days)", min_value=0.0, max_value=30000.0, value=20000.0, step=1.0)
        ap_hi = st.slider("Systolic BP (ap_hi)", min_value=50, max_value=200, value=120)
        ap_lo = st.slider("Diastolic BP (ap_lo)", min_value=30, max_value=150, value=80)
        cholesterol = st.selectbox("Cholesterol Level", options=[1, 2, 3])
    
    with col2:
        gluc = st.selectbox("Glucose Level", options=[1, 2, 3])
        weight = st.slider("Weight (kg)", min_value=30.0, max_value=150.0, value=70.0, step=0.1)
        active = st.selectbox("Physical Activity", options=[0, 1], format_func=lambda x: 'Yes' if x == 1 else 'No')
        alco = st.selectbox("Alcohol Consumption", options=[0, 1], format_func=lambda x: 'Yes' if x == 1 else 'No')

    submit_button = st.form_submit_button(label="Evaluate Risk")

# Process manual input
if submit_button:
    event = {
        'id': id_val,
        'age': age,
        'ap_hi': ap_hi,
        'ap_lo': ap_lo,
        'cholesterol': cholesterol,
        'gluc': gluc,
        'weight': weight,
        'active': active,
        'alco': alco
    }
    result = evaluate_rules(event)
    
    st.subheader("📊 Manual Risk Evaluation Result")
    if result:
        st.markdown(f"**Risk Level**: {result['riskLevel']} 🚨")
        st.markdown(f"**Triggered Rule**: {result['triggeredRule']}")
    else:
        st.markdown("**Risk Level**: Low Risk ✅")

# Original Kafka processing loop
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
    alert_str = f"🧑‍⚕️ **(id: {event['id']})**(Risk Level: {event['riskLevel']})**\n- ⏱️ Time: `{alert_time_str}`\n- 📌 **Reason**: {event['triggeredRule']}"

    alerts_displayed.insert(0, alert_str)
    alerts_displayed = alerts_displayed[:20]
    alert_box.markdown("\n---\n".join(alerts_displayed))