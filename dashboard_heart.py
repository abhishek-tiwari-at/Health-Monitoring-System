# # import streamlit as st
# # from kafka import KafkaConsumer
# # import json
# # from datetime import datetime
# # import pandas as pd
# # from collections import Counter

# # # Page config
# # st.set_page_config(page_title="Heart Disease Alerts with Visuals", layout="wide")
# # st.title("🚨 Real-Time Heart Disease Detection Dashboard")

# # # Kafka consumer setup
# # consumer = KafkaConsumer(
# #     'heart_topic_alert',
# #     bootstrap_servers=['localhost:9092'],
# #     value_deserializer=lambda m: json.loads(m.decode('utf-8')),
# #     auto_offset_reset='latest',
# #     group_id='dashboard_group',
# #     enable_auto_commit=True
# # )

# # # Containers for visuals and alerts
# # st.subheader("📊 Real-Time Visualizations")
# # col1, col2 = st.columns(2)

# # with col1:
# #     st.markdown("**Cumulative Alerts Over Time**")
# #     line_chart = st.line_chart()

# # with col2:
# #     st.markdown("**Alert Reasons Distribution**")
# #     bar_chart = st.bar_chart()


# # st.subheader("🔔 Live stroke Alerts")
# # alert_box = st.empty()

# # # Data structures to accumulate stats
# # timestamps = []
# # cumulative_counts = []
# # reason_counter = Counter()
# # alerts_displayed = []

# # # Track cumulative total
# # total_alerts = 0

# # # Infinite loop processing messages
# # for message in consumer:
# #     alert = message.value
# #     event = alert['event']

# #     # Parse time and update cumulative count
# #     ts = datetime.fromtimestamp(event['detection_timestamp'] / 1000)
# #     timestamps.append(ts)
# #     total_alerts += 1
# #     cumulative_counts.append(total_alerts)

# #     # Update cumulative line chart
# #     df_time = pd.DataFrame({'Total Alerts': cumulative_counts}, index=pd.to_datetime(timestamps))
# #     line_chart.add_rows(df_time.tail(50))  # show last 50 points

# #     # Update reason distribution
# #     reason_counter[event['triggeredRule']] += 1
# #     df_reason = pd.DataFrame.from_dict(reason_counter, orient='index', columns=['count'])
# #     bar_chart.add_rows(df_reason)

# #     # Prepare and display alert details
# #     alert_time_str = ts.strftime('%Y-%m-%d %H:%M:%S')
# #     alert_str = f"🧑‍⚕️ **(Risk Level: {event['riskLevel']})**\n- ⏱️ Time: `{alert_time_str}`\n- 📌 **Reason**: {event['triggeredRule']}"

# #     alerts_displayed.insert(0, alert_str)
# #     alerts_displayed = alerts_displayed[:20]
# #     alert_box.markdown("\n---\n".join(alerts_displayed))

import streamlit as st
from kafka import KafkaConsumer
import json
from datetime import datetime
import pandas as pd
from collections import Counter

# Page config
st.set_page_config(page_title="Heart Disease Alerts with Visuals", layout="wide")
st.title("🚨 Real-Time Heart Disease Detection Dashboard")

# Kafka consumer setup
consumer = KafkaConsumer(
    'heart_topic_alert',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='latest',
    group_id='dashboard_group',
    enable_auto_commit=True
)

# Function to evaluate rules for manual input
def evaluate_rules(event):
    """
    Evaluates the event against the defined rules.
    Returns a dictionary with riskLevel and triggeredRule if a rule matches.
    Returns None if no rule matches.
    """
    ST_Slope = event.get('ST_Slope')
    ChestPainType = event.get('ChestPainType')
    MaxHR = float(event.get('MaxHR', 0))
    ExerciseAngina = event.get('ExerciseAngina')
    Cholesterol = float(event.get('Cholesterol', 0))
    Sex = event.get('Sex')
    Age = float(event.get('Age', 0))
    Oldpeak = float(event.get('Oldpeak', 0))
    RestingBP = float(event.get('RestingBP', 0))

    # Rule 1
    if (ST_Slope in ['Down', 'Flat'] and
            ChestPainType == 'ASY' and
            MaxHR <= 175 and
            ExerciseAngina == 'N' and
            Cholesterol <= 192):
        return {
            'riskLevel': 'High Risk',
            'triggeredRule': 'Rule 1: ST_Slope=[Down, Flat], ChestPain=ASY, MaxHR<=175, ExerciseAngina=N, Cholesterol<=192'
        }

    # Rule 2
    if (ST_Slope in ['Down', 'Flat'] and
            ChestPainType == 'ASY' and
            MaxHR <= 175 and
            ExerciseAngina == 'N' and
            Cholesterol > 192):
        return {
            'riskLevel': 'High Risk',
            'triggeredRule': 'Rule 2: ST_Slope=[Down, Flat], ChestPain=ASY, MaxHR<=175, ExerciseAngina=N, Cholesterol>192'
        }

    # Rule 3
    if (ST_Slope in ['Down', 'Flat'] and
            ChestPainType == 'ASY' and
            MaxHR <= 175 and
            ExerciseAngina == 'Y'):
        return {
            'riskLevel': 'High Risk',
            'triggeredRule': 'Rule 3: ST_Slope=[Down, Flat], ChestPain=ASY, MaxHR<=175, ExerciseAngina=Y'
        }

    # Rule 8
    if (ST_Slope in ['Down', 'Flat'] and
            ChestPainType in ['ATA', 'NAP', 'TA'] and
            Sex == 'M' and
            Age <= 65 and
            muodifiedCholesterol <= 192):
        return {
            'riskLevel': 'High Risk',
            'triggeredRule': 'Rule 8: ST_Slope=[Down, Flat], ChestPain=[ATA, NAP, TA], Sex=M, Age<=65, Cholesterol<=192'
        }

    # Rule 10
    if (ST_Slope in ['Down', 'Flat'] and
            ChestPainType in ['ATA', 'NAP', 'TA'] and
            Sex == 'M' and
            Age > 65 and
            MaxHR <= 143):
        return {
            'riskLevel': 'High Risk',
            'triggeredRule': 'Rule 10: ST_Slope=[Down, Flat], ChestPain=[ATA, NAP, TA], Sex=M, Age>65, MaxHR<=143'
        }

    # Rule 11
    if (ST_Slope in ['Down', 'Flat'] and
            ChestPainType in ['ATA', 'NAP', 'TA'] and
            Sex == 'M' and
            Age > 65 and
            MaxHR > 143):
        return {
            'riskLevel': 'High Risk',
            'triggeredRule': 'Rule 11: ST_Slope=[Down, Flat], ChestPain=[ATA, NAP, TA], Sex=M, Age>65, MaxHR>143'
        }

    # Rule 13
    if (ST_Slope == 'UP' and
            0.10 < Oldpeak <= 1.25 and
            Cholesterol <= 42 and
            RestingBP <= 126):
        return {
            'riskLevel': 'High Risk',
            'triggeredRule': 'Rule 13: ST_Slope=UP, 0.10<Oldpeak<=1.25, Cholesterol<=42, RestingBP<=126'
        }

    # Rule 15
    if (ST_Slope == 'UP' and
            Oldpeak <= 1.25 and
            Cholesterol <= 42 and
            RestingBP > 126 and
            MaxHR <= 102):
        return {
            'riskLevel': 'High Risk',
            'triggeredRule': 'Rule 15: ST_Slope=UP, Oldpeak<=1.25, Cholesterol<=42, RestingBP>126, MaxHR<=102'
        }

    # Rule 20
    if (ST_Slope == 'UP' and
            1.25 < Oldpeak <= 2.40 and
            Age <= 65 and
            ExerciseAngina == 'Y'):
        return {
            'riskLevel': 'High Risk',
            'triggeredRule': 'Rule 20: ST_Slope=UP, 1.25<Oldpeak<=2.40, Age<=65, ExerciseAngina=Y'
        }

    # Rule 21
    if (ST_Slope == 'UP' and
            Oldpeak > 2.40 and
            Age <= 65):
        return {
            'riskLevel': 'High Risk',
            'triggeredRule': 'Rule 21: ST_Slope=UP, Oldpeak>2.40, Age<=65'
        }

    # Rule 22
    if (ST_Slope == 'UP' and
            Oldpeak > 1.25 and
            Age > 65 and
            RestingBP <= 156 and
            MaxHR <= 172):
        return {
            'riskLevel': 'High Risk',
            'triggeredRule': 'Rule 22: ST_Slope=UP, Oldpeak>1.25, Age>65, RestingBP<=156, MaxHR<=172'
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
        ST_Slope = st.selectbox("ST Slope", options=['Up', 'Flat', 'Down'])
        ChestPainType = st.selectbox("Chest Pain Type", options=['ASY', 'ATA', 'NAP', 'TA'])
        ExerciseAngina = st.selectbox("Exercise Angina", options=['Y', 'N'])
        Sex = st.selectbox("Sex", options=['M', 'F'])
    
    with col2:
        Age = st.slider("Age", min_value=20, max_value=100, value=50)
        MaxHR = st.slider("Max Heart Rate (MaxHR)", min_value=60, max_value=220, value=120)
        Cholesterol = st.slider("Cholesterol", min_value=0, max_value=600, value=200)
        RestingBP = st.slider("Resting Blood Pressure", min_value=80, max_value=200, value=120)
        Oldpeak = st.slider("Oldpeak", min_value=0.0, max_value=6.0, value=1.0, step=0.1)

    submit_button = st.form_submit_button(label="Evaluate Risk")

# Process manual input
if submit_button:
    event = {
        'ST_Slope': ST_Slope,
        'ChestPainType': ChestPainType,
        'MaxHR': MaxHR,
        'ExerciseAngina': ExerciseAngina,
        'Cholesterol': Cholesterol,
        'Sex': Sex,
        'Age': Age,
        'Oldpeak': Oldpeak,
        'RestingBP': RestingBP
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
    alert_str = f"🧑‍⚕️ **(Risk Level: {event['riskLevel']})**\n- ⏱️ Time: `{alert_time_str}`\n- 📌 **Reason**: {event['triggeredRule']}"

    alerts_displayed.insert(0, alert_str)
    alerts_displayed = alerts_displayed[:20]
    alert_box.markdown("\n---\n".join(alerts_displayed))