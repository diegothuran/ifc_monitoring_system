"""
Utility functions for Streamlit IFC Monitoring App
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import requests
from typing import Dict, List, Optional, Any

def make_authenticated_request(endpoint: str, method: str = 'GET', data: dict = None) -> Optional[Dict]:
    """Make authenticated API request"""
    if 'access_token' not in st.session_state or not st.session_state.access_token:
        return None
    
    headers = {'Authorization': f'Bearer {st.session_state.access_token}'}
    api_base = st.session_state.get('api_base_url', 'http://localhost:8000/api/v1')
    
    try:
        if method == 'GET':
            response = requests.get(f"{api_base}{endpoint}", headers=headers)
        elif method == 'POST':
            response = requests.post(f"{api_base}{endpoint}", headers=headers, json=data)
        elif method == 'PUT':
            response = requests.put(f"{api_base}{endpoint}", headers=headers, json=data)
        elif method == 'DELETE':
            response = requests.delete(f"{api_base}{endpoint}", headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Erro na API: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        st.error(f"Erro na requisição: {str(e)}")
        return None

def create_metric_card(title: str, value: str, delta: str = None, delta_color: str = "normal"):
    """Create a metric card"""
    st.metric(
        label=title,
        value=value,
        delta=delta,
        delta_color=delta_color
    )

def create_time_series_chart(df: pd.DataFrame, x_col: str, y_col: str, 
                           title: str, color: str = None) -> go.Figure:
    """Create a time series chart"""
    fig = px.line(df, x=x_col, y=y_col, title=title, color=color)
    fig.update_layout(
        height=400,
        xaxis_title=x_col.replace('_', ' ').title(),
        yaxis_title=y_col.replace('_', ' ').title(),
        hovermode='x unified'
    )
    return fig

def create_gauge_chart(value: float, min_val: float, max_val: float, 
                      title: str, color: str = "blue") -> go.Figure:
    """Create a gauge chart"""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = value,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': title},
        delta = {'reference': (max_val + min_val) / 2},
        gauge = {
            'axis': {'range': [min_val, max_val]},
            'bar': {'color': color},
            'steps': [
                {'range': [min_val, max_val * 0.5], 'color': "lightgray"},
                {'range': [max_val * 0.5, max_val * 0.8], 'color': "yellow"},
                {'range': [max_val * 0.8, max_val], 'color': "red"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': max_val * 0.9
            }
        }
    ))
    
    fig.update_layout(height=300)
    return fig

def format_timestamp(timestamp_str: str) -> str:
    """Format timestamp string for display"""
    try:
        dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        return dt.strftime('%d/%m/%Y %H:%M:%S')
    except:
        return timestamp_str

def get_alert_color(severity: str) -> str:
    """Get color for alert severity"""
    colors = {
        'low': '#17becf',
        'medium': '#ff7f0e',
        'high': '#d62728',
        'critical': '#8b0000'
    }
    return colors.get(severity.lower(), '#17becf')

def get_sensor_icon(sensor_type: str) -> str:
    """Get icon for sensor type"""
    icons = {
        'temperature': '🌡️',
        'humidity': '💧',
        'pressure': '📊',
        'vibration': '📳',
        'air_quality': '🌬️'
    }
    return icons.get(sensor_type.lower(), '📡')

def create_alert_summary(alerts_data: List[Dict]) -> pd.DataFrame:
    """Create alert summary DataFrame"""
    if not alerts_data:
        return pd.DataFrame()
    
    df = pd.DataFrame(alerts_data)
    
    # Format timestamps
    if 'triggered_at' in df.columns:
        df['triggered_at'] = df['triggered_at'].apply(format_timestamp)
    
    # Select relevant columns
    columns = ['id', 'title', 'sensor_id', 'severity', 'status', 'triggered_at']
    available_columns = [col for col in columns if col in df.columns]
    
    return df[available_columns]

def create_sensor_summary(sensors_data: List[Dict]) -> pd.DataFrame:
    """Create sensor summary DataFrame"""
    if not sensors_data:
        return pd.DataFrame()
    
    df = pd.DataFrame(sensors_data)
    
    # Add icon column
    if 'sensor_type' in df.columns:
        df['icon'] = df['sensor_type'].apply(get_sensor_icon)
    
    # Format timestamps
    timestamp_cols = ['created_at', 'updated_at', 'installation_date', 'last_calibration']
    for col in timestamp_cols:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: format_timestamp(x) if pd.notna(x) else 'N/A')
    
    return df

def validate_form_data(form_data: Dict, required_fields: List[str]) -> List[str]:
    """Validate form data and return list of errors"""
    errors = []
    
    for field in required_fields:
        if field not in form_data or not form_data[field]:
            errors.append(f"Campo '{field}' é obrigatório")
    
    return errors

def show_success_message(message: str):
    """Show success message"""
    st.success(message)
    time.sleep(2)

def show_error_message(message: str):
    """Show error message"""
    st.error(message)

def show_warning_message(message: str):
    """Show warning message"""
    st.warning(message)

def show_info_message(message: str):
    """Show info message"""
    st.info(message)
