"""
IFC Monitoring System - Streamlit Frontend
"""

import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "https://ifc-backend-ph0n.onrender.com/api/v1")
REFRESH_INTERVAL = 30  # seconds

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'access_token' not in st.session_state:
    st.session_state.access_token = None
if 'user_info' not in st.session_state:
    st.session_state.user_info = None

def authenticate(username: str, password: str) -> bool:
    """Authenticate user and store token"""
    try:
        data = {
            'username': username,
            'password': password
        }
        
        response = requests.post(
            f"{API_BASE_URL}/auth/login",
            data=data,
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )
        
        if response.status_code == 200:
            token_data = response.json()
            st.session_state.access_token = token_data['access_token']
            st.session_state.authenticated = True
            
            # Get user info
            headers = {'Authorization': f'Bearer {st.session_state.access_token}'}
            user_response = requests.get(f"{API_BASE_URL}/auth/me", headers=headers)
            
            if user_response.status_code == 200:
                st.session_state.user_info = user_response.json()
            
            return True
        else:
            st.error("Credenciais inválidas")
            return False
            
    except Exception as e:
        st.error(f"Erro na autenticação: {str(e)}")
        return False

def make_api_request(endpoint: str, method: str = 'GET', data: dict = None):
    """Make authenticated API request"""
    if not st.session_state.access_token:
        return None
    
    headers = {'Authorization': f'Bearer {st.session_state.access_token}'}
    
    try:
        if method == 'GET':
            response = requests.get(f"{API_BASE_URL}{endpoint}", headers=headers)
        elif method == 'POST':
            response = requests.post(f"{API_BASE_URL}{endpoint}", headers=headers, json=data)
        elif method == 'PUT':
            response = requests.put(f"{API_BASE_URL}{endpoint}", headers=headers, json=data)
        elif method == 'DELETE':
            response = requests.delete(f"{API_BASE_URL}{endpoint}", headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Erro na API: {response.status_code}")
            return None
            
    except Exception as e:
        st.error(f"Erro na requisição: {str(e)}")
        return None

def login_page():
    """Login page"""
    st.title("🔐 IFC Monitoring System")
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.subheader("Login")
        
        with st.form("login_form"):
            username = st.text_input("Usuário")
            password = st.text_input("Senha", type="password")
            submit_button = st.form_submit_button("Entrar")
            
            if submit_button:
                if authenticate(username, password):
                    st.success("Login realizado com sucesso!")
                    time.sleep(1)
                    st.rerun()

def dashboard_page():
    """Main dashboard page"""
    st.title("📊 Dashboard - IFC Monitoring System")
    
    # User info
    if st.session_state.user_info:
        st.sidebar.success(f"Bem-vindo, {st.session_state.user_info['full_name']}")
        st.sidebar.info(f"Role: {st.session_state.user_info['role']}")
        
        if st.sidebar.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.access_token = None
            st.session_state.user_info = None
            st.rerun()
    
    # Auto-refresh
    if st.sidebar.checkbox("Auto-refresh", value=True):
        time.sleep(REFRESH_INTERVAL)
        st.rerun()
    
    # Statistics cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Sensores Ativos", "12", "2")
    with col2:
        st.metric("Alertas Ativos", "3", "-1")
    with col3:
        st.metric("Localizações", "8", "0")
    with col4:
        st.metric("Leituras Hoje", "1,247", "45")
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Tendência de Temperatura")
        
        # Simulate temperature data
        dates = pd.date_range(start=datetime.now() - timedelta(hours=24), 
                             end=datetime.now(), freq='H')
        temperatures = [20 + 10 * (i % 24) / 24 + (i % 3) for i in range(len(dates))]
        
        df_temp = pd.DataFrame({
            'timestamp': dates,
            'temperature': temperatures
        })
        
        fig = px.line(df_temp, x='timestamp', y='temperature', 
                     title='Temperatura (°C)')
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("💧 Umidade")
        
        # Simulate humidity data
        humidity = [60 + 20 * (i % 24) / 24 + (i % 2) for i in range(len(dates))]
        
        df_humidity = pd.DataFrame({
            'timestamp': dates,
            'humidity': humidity
        })
        
        fig = px.line(df_humidity, x='timestamp', y='humidity', 
                     title='Umidade (%)')
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    # Recent alerts
    st.subheader("🚨 Alertas Recentes")
    
    alerts_data = [
        {"Sensor": "TEMP-001", "Tipo": "Temperatura Alta", "Severidade": "Alta", "Hora": "10:30"},
        {"Sensor": "HUM-002", "Tipo": "Umidade Crítica", "Severidade": "Crítica", "Hora": "09:15"},
        {"Sensor": "PRESS-003", "Tipo": "Pressão Baixa", "Severidade": "Média", "Hora": "08:45"},
    ]
    
    df_alerts = pd.DataFrame(alerts_data)
    st.dataframe(df_alerts, use_container_width=True)

def sensors_page():
    """Sensors management page"""
    st.title("📡 Gestão de Sensores")
    
    # Get sensors data
    sensors_data = make_api_request('/sensors/')
    
    if sensors_data:
        st.subheader("Lista de Sensores")
        
        # Create DataFrame
        sensors_df = pd.DataFrame(sensors_data.get('sensors', []))
        
        if not sensors_df.empty:
            st.dataframe(sensors_df, use_container_width=True)
        else:
            st.info("Nenhum sensor encontrado")
    else:
        st.error("Erro ao carregar dados dos sensores")
    
    st.markdown("---")
    
    # Add new sensor form
    with st.expander("➕ Adicionar Novo Sensor"):
        with st.form("add_sensor"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Nome do Sensor")
                sensor_type = st.selectbox("Tipo", ["temperature", "humidity", "pressure", "vibration"])
                device_id = st.text_input("ID do Dispositivo")
            
            with col2:
                location_id = st.number_input("ID da Localização", min_value=1)
                unit = st.text_input("Unidade")
                update_interval = st.number_input("Intervalo (segundos)", min_value=1, value=60)
            
            if st.form_submit_button("Adicionar Sensor"):
                sensor_data = {
                    "name": name,
                    "sensor_type": sensor_type,
                    "device_id": device_id,
                    "location_id": location_id,
                    "unit": unit,
                    "update_interval": update_interval
                }
                
                result = make_api_request('/sensors/', 'POST', sensor_data)
                if result:
                    st.success("Sensor adicionado com sucesso!")
                    st.rerun()

def alerts_page():
    """Alerts management page"""
    st.title("🚨 Gestão de Alertas")
    
    # Alert status filter
    status_filter = st.selectbox("Filtrar por Status", 
                                ["Todos", "Ativo", "Reconhecido", "Resolvido"])
    
    # Get alerts data
    alerts_data = make_api_request('/alerts/')
    
    if alerts_data:
        alerts_df = pd.DataFrame(alerts_data.get('alerts', []))
        
        if not alerts_df.empty:
            # Filter by status
            if status_filter != "Todos":
                status_map = {"Ativo": "active", "Reconhecido": "acknowledged", "Resolvido": "resolved"}
                alerts_df = alerts_df[alerts_df['status'] == status_map[status_filter]]
            
            st.dataframe(alerts_df, use_container_width=True)
            
            # Alert actions
            st.subheader("Ações em Lote")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("Reconhecer Todos"):
                    st.info("Funcionalidade em desenvolvimento")
            
            with col2:
                if st.button("Resolver Todos"):
                    st.info("Funcionalidade em desenvolvimento")
            
            with col3:
                if st.button("Enviar Relatório"):
                    st.info("Funcionalidade em desenvolvimento")
        else:
            st.info("Nenhum alerta encontrado")
    else:
        st.error("Erro ao carregar alertas")

def locations_page():
    """Locations management page"""
    st.title("📍 Gestão de Localizações")
    
    # Get locations data
    locations_data = make_api_request('/locations/')
    
    if locations_data:
        st.subheader("Lista de Localizações")
        
        locations_df = pd.DataFrame(locations_data.get('locations', []))
        
        if not locations_df.empty:
            st.dataframe(locations_df, use_container_width=True)
        else:
            st.info("Nenhuma localização encontrada")
    else:
        st.error("Erro ao carregar localizações")
    
    st.markdown("---")
    
    # Add new location form
    with st.expander("➕ Adicionar Nova Localização"):
        with st.form("add_location"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Nome da Localização")
                building = st.text_input("Edifício")
                floor = st.text_input("Andar")
                room = st.text_input("Sala")
            
            with col2:
                zone = st.text_input("Zona")
                responsible_person = st.text_input("Responsável")
                phone = st.text_input("Telefone")
                email = st.text_input("Email")
            
            if st.form_submit_button("Adicionar Localização"):
                location_data = {
                    "name": name,
                    "building": building,
                    "floor": floor,
                    "room": room,
                    "zone": zone,
                    "responsible_person": responsible_person,
                    "phone": phone,
                    "email": email
                }
                
                result = make_api_request('/locations/', 'POST', location_data)
                if result:
                    st.success("Localização adicionada com sucesso!")
                    st.rerun()

def readings_page():
    """Sensor readings page"""
    st.title("📊 Leituras dos Sensores")
    
    # Date range selector
    col1, col2 = st.columns(2)
    
    with col1:
        start_date = st.date_input("Data Início", value=datetime.now() - timedelta(days=1))
    with col2:
        end_date = st.date_input("Data Fim", value=datetime.now())
    
    # Get readings data
    readings_data = make_api_request('/readings/')
    
    if readings_data:
        readings_df = pd.DataFrame(readings_data.get('readings', []))
        
        if not readings_df.empty:
            # Convert timestamp to datetime
            readings_df['timestamp'] = pd.to_datetime(readings_df['timestamp'])
            
            # Filter by date range
            readings_df = readings_df[
                (readings_df['timestamp'].dt.date >= start_date) &
                (readings_df['timestamp'].dt.date <= end_date)
            ]
            
            st.subheader("Leituras Recentes")
            st.dataframe(readings_df, use_container_width=True)
            
            # Charts
            if len(readings_df) > 0:
                st.subheader("📈 Gráfico de Leituras")
                
                sensor_id = st.selectbox("Selecionar Sensor", readings_df['sensor_id'].unique())
                
                sensor_data = readings_df[readings_df['sensor_id'] == sensor_id]
                
                fig = px.line(sensor_data, x='timestamp', y='value', 
                             title=f'Leituras do Sensor {sensor_id}')
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Nenhuma leitura encontrada")
    else:
        st.error("Erro ao carregar leituras")

def ifc_page():
    """IFC file management page"""
    st.title("🏗️ Gestão de Plantas IFC")
    
    # Tabs for different IFC functions
    tab1, tab2, tab3 = st.tabs(["Upload de Arquivos", "Visualização 3D", "Espaços"])
    
    with tab1:
        st.subheader("📁 Upload de Arquivos IFC")
        
        # File upload
        uploaded_file = st.file_uploader(
            "Selecione um arquivo IFC",
            type=['ifc'],
            help="Formatos suportados: .ifc (máximo 100MB)"
        )
        
        if uploaded_file is not None:
            st.success(f"Arquivo selecionado: {uploaded_file.name}")
            st.info(f"Tamanho: {uploaded_file.size / (1024*1024):.2f} MB")
            
            if st.button("Upload Arquivo"):
                with st.spinner("Fazendo upload..."):
                    try:
                        # Prepare file data
                        files = {'file': (uploaded_file.name, uploaded_file.getvalue(), 'application/octet-stream')}
                        
                        # Upload to API
                        response = requests.post(
                            f"{API_BASE_URL}/ifc/upload",
                            files=files,
                            headers={'Authorization': f'Bearer {st.session_state.access_token}'}
                        )
                        
                        if response.status_code == 200:
                            st.success("Arquivo IFC enviado com sucesso!")
                            st.json(response.json())
                        else:
                            st.error(f"Erro no upload: {response.text}")
                            
                    except Exception as e:
                        st.error(f"Erro: {str(e)}")
        
        # List uploaded files
        st.subheader("📋 Arquivos IFC Carregados")
        
        try:
            response = requests.get(
                f"{API_BASE_URL}/ifc/files",
                headers={'Authorization': f'Bearer {st.session_state.access_token}'}
            )
            
            if response.status_code == 200:
                files_data = response.json()
                
                if files_data.get('ifc_files'):
                    for file_info in files_data['ifc_files']:
                        with st.expander(f"📄 {file_info['original_filename']}"):
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                st.write(f"**Status:** {file_info['processing_status']}")
                                st.write(f"**Tamanho:** {file_info['file_size'] / (1024*1024):.2f} MB")
                            
                            with col2:
                                st.write(f"**Projeto:** {file_info.get('project_name', 'N/A')}")
                                st.write(f"**Versão IFC:** {file_info.get('ifc_version', 'N/A')}")
                            
                            with col3:
                                if file_info['processing_status'] == 'failed':
                                    st.error("Processamento falhou")
                                elif file_info['processing_status'] == 'completed':
                                    st.success("Processado com sucesso")
                                else:
                                    st.warning("Processando...")
                                
                                if st.button(f"Reprocessar", key=f"reprocess_{file_info['id']}"):
                                    try:
                                        reprocess_response = requests.post(
                                            f"{API_BASE_URL}/ifc/files/{file_info['id']}/process",
                                            headers={'Authorization': f'Bearer {st.session_state.access_token}'}
                                        )
                                        if reprocess_response.status_code == 200:
                                            st.success("Reprocessamento iniciado!")
                                            st.rerun()
                                    except Exception as e:
                                        st.error(f"Erro: {str(e)}")
            else:
                st.error("Erro ao carregar arquivos")
                
        except Exception as e:
            st.error(f"Erro: {str(e)}")
    
    with tab2:
        st.subheader("🌐 Visualização 3D da Planta")
        
        # Get available IFC files
        try:
            response = requests.get(
                f"{API_BASE_URL}/ifc/files",
                headers={'Authorization': f'Bearer {st.session_state.access_token}'}
            )
            
            if response.status_code == 200:
                files_data = response.json()
                processed_files = [f for f in files_data.get('ifc_files', []) if f['processing_status'] == 'completed']
                
                if processed_files:
                    selected_file = st.selectbox(
                        "Selecione uma planta para visualizar",
                        options=[f['id'] for f in processed_files],
                        format_func=lambda x: next(f['original_filename'] for f in processed_files if f['id'] == x)
                    )
                    
                    if selected_file:
                        # Get spaces for visualization
                        spaces_response = requests.get(
                            f"{API_BASE_URL}/ifc/files/{selected_file}/spaces",
                            headers={'Authorization': f'Bearer {st.session_state.access_token}'}
                        )
                        
                        if spaces_response.status_code == 200:
                            spaces_data = spaces_response.json()
                            spaces = spaces_data.get('spaces', [])
                            
                            if spaces:
                                # Create 3D visualization
                                create_3d_visualization(spaces)
                            else:
                                st.info("Nenhum espaço encontrado neste arquivo IFC")
                        else:
                            st.error("Erro ao carregar espaços")
                else:
                    st.info("Nenhum arquivo IFC processado disponível")
            else:
                st.error("Erro ao carregar arquivos")
                
        except Exception as e:
            st.error(f"Erro: {str(e)}")
    
    with tab3:
        st.subheader("🏠 Espaços da Planta")
        
        # Get spaces from all processed files
        try:
            response = requests.get(
                f"{API_BASE_URL}/ifc/files",
                headers={'Authorization': f'Bearer {st.session_state.access_token}'}
            )
            
            if response.status_code == 200:
                files_data = response.json()
                processed_files = [f for f in files_data.get('ifc_files', []) if f['processing_status'] == 'completed']
                
                if processed_files:
                    selected_file = st.selectbox(
                        "Selecione uma planta",
                        options=[f['id'] for f in processed_files],
                        format_func=lambda x: next(f['original_filename'] for f in processed_files if f['id'] == x),
                        key="spaces_file_selector"
                    )
                    
                    if selected_file:
                        spaces_response = requests.get(
                            f"{API_BASE_URL}/ifc/files/{selected_file}/spaces",
                            headers={'Authorization': f'Bearer {st.session_state.access_token}'}
                        )
                        
                        if spaces_response.status_code == 200:
                            spaces_data = spaces_response.json()
                            spaces = spaces_data.get('spaces', [])
                            
                            if spaces:
                                # Display spaces table
                                spaces_df = pd.DataFrame(spaces)
                                st.dataframe(spaces_df, use_container_width=True)
                                
                                # Spaces summary
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.metric("Total de Espaços", len(spaces))
                                with col2:
                                    unique_types = spaces_df['space_type'].nunique() if 'space_type' in spaces_df.columns else 0
                                    st.metric("Tipos de Espaço", unique_types)
                                with col3:
                                    total_area = spaces_df['area'].sum() if 'area' in spaces_df.columns else 0
                                    st.metric("Área Total", f"{total_area:.1f} m²")
                            else:
                                st.info("Nenhum espaço encontrado")
                        else:
                            st.error("Erro ao carregar espaços")
                else:
                    st.info("Nenhum arquivo processado disponível")
            else:
                st.error("Erro ao carregar arquivos")
                
        except Exception as e:
            st.error(f"Erro: {str(e)}")

def create_3d_visualization(spaces):
    """Create 3D visualization of building spaces"""
    if not spaces:
        st.info("Nenhum espaço disponível para visualização")
        return
    
    # Create sample 3D visualization using Plotly
    import plotly.graph_objects as go
    import plotly.express as px
    
    # Extract coordinates and create 3D scatter plot
    x_coords = []
    y_coords = []
    z_coords = []
    space_names = []
    space_areas = []
    space_types = []
    
    for space in spaces:
        x_coords.append(space.get('x_coordinate', 0))
        y_coords.append(space.get('y_coordinate', 0))
        z_coords.append(space.get('z_coordinate', 0))
        space_names.append(space.get('name', 'Unknown'))
        space_areas.append(space.get('area', 25))
        space_types.append(space.get('space_type', 'space'))
    
    # Create 3D scatter plot
    fig = go.Figure(data=go.Scatter3d(
        x=x_coords,
        y=y_coords,
        z=z_coords,
        mode='markers',
        marker=dict(
            size=8,
            color=space_areas,
            colorscale='Viridis',
            opacity=0.8,
            colorbar=dict(title="Área (m²)")
        ),
        text=space_names,
        hovertemplate='<b>%{text}</b><br>' +
                      'X: %{x:.1f}<br>' +
                      'Y: %{y:.1f}<br>' +
                      'Z: %{z:.1f}<br>' +
                      '<extra></extra>'
    ))
    
    fig.update_layout(
        title='Visualização 3D dos Espaços',
        scene=dict(
            xaxis_title='X (metros)',
            yaxis_title='Y (metros)',
            zaxis_title='Z (metros)',
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.5)
            )
        ),
        height=600
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Create 2D floor plan
    st.subheader("📐 Planta Baixa")
    
    fig_2d = px.scatter(
        x=x_coords,
        y=y_coords,
        color=space_areas,
        size=space_areas,
        hover_name=space_names,
        title="Planta Baixa dos Espaços",
        labels={'x': 'X (metros)', 'y': 'Y (metros)', 'color': 'Área (m²)'}
    )
    
    fig_2d.update_layout(height=500)
    st.plotly_chart(fig_2d, use_container_width=True)

def main():
    """Main application"""
    st.set_page_config(
        page_title="IFC Monitoring System",
        page_icon="🏭",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    .main-header {
        font-size: 2rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    </style>
    """, unsafe_allow_html=True)
    
    if not st.session_state.authenticated:
        login_page()
    else:
        # Sidebar navigation
        st.sidebar.title("🏭 IFC Monitoring")
        
        page = st.sidebar.selectbox(
            "Navegação",
            ["Dashboard", "Sensores", "Alertas", "Localizações", "Leituras", "Plantas IFC"]
        )
        
        # Main content
        if page == "Dashboard":
            dashboard_page()
        elif page == "Sensores":
            sensors_page()
        elif page == "Alertas":
            alerts_page()
        elif page == "Localizações":
            locations_page()
        elif page == "Leituras":
            readings_page()
        elif page == "Plantas IFC":
            ifc_page()

if __name__ == "__main__":
    main()
