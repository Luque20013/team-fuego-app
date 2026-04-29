import streamlit as st

# ==========================================
# --- CONFIGURACIÓN VISUAL "TEAM FUEGO PRO" ---
# ==========================================
st.set_page_config(page_title="TEAM FUEGO - Admin Mode", page_icon="🔥", layout="wide")

# CSS Avanzado para el diseño neón y marca personal
st.markdown("""
    <style>
        /* Fondo Galáctico */
        .stApp {
            background: radial-gradient(circle at top, #330800 0%, #000000 100%);
            color: #FFFFFF;
        }
        
        /* Banner de Título */
        .banner {
            background: linear-gradient(90deg, #FF0000, #FF8C00);
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 0 30px #FF4500;
            margin-bottom: 25px;
        }
        
        .banner h1 {
            color: white !important;
            font-family: 'Arial Black', sans-serif;
            letter-spacing: 5px;
            margin: 0;
            text-transform: uppercase;
        }

        /* Tarjetas de Equipos */
        .team-card {
            background: rgba(255, 255, 255, 0.05);
            border: 2px solid #FF4500;
            border-radius: 20px;
            padding: 25px;
            text-align: center;
            box-shadow: 0 0 15px rgba(255, 69, 0, 0.3);
            margin: 10px;
        }

        /* Botones Estilo Gamer */
        div.stButton > button {
            width: 100% !important;
            height: 60px !important;
            background: linear-gradient(135deg, #FF4500 0%, #B22222 100%) !important;
            color: white !important;
            border: 2px solid #FFD700 !important;
            border-radius: 30px !important;
            font-size: 20px !important;
            font-weight: bold !important;
            text-transform: uppercase !important;
            transition: 0.4s;
        }
        
        div.stButton > button:hover {
            box-shadow: 0 0 40px #FFD700 !important;
            transform: translateY(-3px);
        }

        /* Tabla de Resultados */
        .pos-table {
            width: 100%;
            border-collapse: separate;
            border-spacing: 0 10px;
        }
        .pos-table tr {
            background: rgba(255, 255, 255, 0.1);
        }
        .pos-table td, .pos-table th {
            padding: 15px;
            text-align: center;
            border-radius: 10px;
        }
        
        /* Sello BY LUQUE */
        .footer-brand {
            text-align: center;
            padding: 30px;
            margin-top: 30px;
            border-top: 1px solid rgba(255, 69, 0, 0.2);
        }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# --- LÓGICA DE CONTROL (PYTHON) ---
# ==========================================
if 'iniciado' not in st.session_state:
    st.session_state.iniciado = False
    st.session_state.equipos = ["TEAM A", "TEAM B", "TEAM C"]
    st.session_state.saldos = {e: 0 for e in st.session_state.equipos}
    st.session_state.ganados = {e: 0 for e in st.session_state.equipos}
    st.session_state.paso = 1

# --- SIDEBAR: PANEL DE ADMINISTRACIÓN ---
with st.sidebar:
    st.markdown("### 🔥 CONFIGURACIÓN")
    st.session_state.apuesta = st.number_input("APUESTA POR SET (S/)", value=2, min_value=1)
    
    st.markdown("---")
    st.subheader("📝 NOMBRES DE EQUIPOS")
    n1 = st.text_input("Equipo 1", value=st.session_state.equipos[0])
    n2 = st.text_input("Equipo 2", value=st.session_state.equipos[1])
    n3 = st.text_input("Equipo 3", value=st.session_state.equipos[2])
    
    if st.button("🚀 GUARDAR Y EMPEZAR"):
        st.session_state.equipos = [n1, n2, n3]
        st.session_state.saldos = {n: 0 for n in st.session_state.equipos}
        st.session_state.ganados = {n: 0 for n in st.session_state.equipos}
        st.session_state.local, st.session_state.visitante, st.session_state.espera = n1, n2, n3
        st.session_state.iniciado = True
        st.rerun()

    if st.button("🚨 REINICIAR TODO"):
        for k in list(st.session_state.keys()): del st.session_state[k]
        st.rerun()

# --- PANTALLA PRINCIPAL ---
st.markdown(f"""
    <div class="banner">
        <h1>TEAM FUEGO PRO</h1>
        <p style="color: #FFD700; font-weight: bold; margin: 0; letter-spacing: 2px;">
            ADMIN: LUQUE
        </p>
    </div>
""", unsafe_allow_html=True)

if not st.session_state.iniciado:
    st.warning("👈 Configura los equipos en el panel de la izquierda para comenzar la pichanga.")
else:
    # 🏟️ ZONA DE PARTIDO ACTUAL
    st.markdown(f"### 🏐 PARTIDO {st.session_state.paso} / 3 (RONDA ACTUAL)")
    
    col_l, col_vs, col_v = st.columns([2, 0.5, 2])
    
    with col_l:
        st.markdown(f'<div class="team-card"><h3>LOCAL</h3><h2>{st.session_state.local}</h2></div>', unsafe_allow_html=True)
        if st.button(f"🔥 GANÓ {st.session_state.local}", key="btn_l"):
            ganador, perdedor = st.session_state.local, st.session_state.visitante
            st.session_state.saldos[ganador] += st.session_state.apuesta
            st.session_state.saldos[perdedor] -= st.session_state.apuesta
            st.session_state.ganados[ganador] += 1
            
            # Rotación de Ronda
            if st.session_state.paso == 1:
                st.session_state.local, st.session_state.visitante, st.session_state.espera = ganador, st.session_state.espera, perdedor
                st.session_state.paso = 2
            elif st.session_state.paso == 2:
                st.session_state.local, st.session_state.visitante, st.session_state.espera = perdedor, st.session_state.espera, ganador
                st.session_state.paso = 3
            else:
                st.session_state.local, st.session_state.visitante, st.session_state.espera = st.session_state.equipos[0], st.session_state.equipos[1], st.session_state.equipos[2]
                st.session_state.paso = 1
            st.rerun()

    with col_vs:
        st.markdown("<br><h1 style='text-align:center; color:#FFD700;'>VS</h1>", unsafe_allow_html=True)

    with col_v:
        st.markdown(f'<div class="team-card"><h3>VISITANTE</h3><h2>{st.session_state.visitante}</h2></div>', unsafe_allow_html=True)
        if st.button(f"🔥 GANÓ {st.session_state.visitante}", key="btn_v"):
            ganador, perdedor = st.session_state.visitante, st.session_state.local
            st.session_state.saldos[ganador] += st.session_state.apuesta
            st.session_state.saldos[perdedor] -= st.session_state.apuesta
            st.session_state.ganados[ganador] += 1
            
            # Rotación de Ronda
            if st.session_state.paso == 1:
                st.session_state.local, st.session_state.visitante, st.session_state.espera = ganador, st.session_state.espera, perdedor
                st.session_state.paso = 2
            elif st.session_state.paso == 2:
                st.session_state.local, st.session_state.visitante, st.session_state.espera = perdedor, st.session_state.espera, ganador
                st.session_state.paso = 3
            else:
                st.session_state.local, st.session_state.visitante, st.session_state.espera = st.session_state.equipos[0], st.session_state.equipos[1], st.session_state.equipos[2]
                st.session_state.paso = 1
            st.rerun()

    st.markdown(f"""
        <div style="background: rgba(255,215,0,0.1); border-left: 5px solid #FFD700; padding: 15px; border-radius: 5px; margin: 20px 0;">
            ⏳ <b>EN ESPERA:</b> {st.session_state.espera}
        </div>
    """, unsafe_allow_html=True)

    # 💰 TABLA DE POSICIONES
    st.divider()
    st.markdown("### 📊 RESUMEN DE SALDOS")
    
    tabla_html = """<table class="pos-table"><tr><th>EQUIPO</th><th>SALDO NETO</th><th>SETS</th></tr>"""
    for e in st.session_state.equipos:
        saldo = st.session_state.saldos[e]
        color = "#00FF00" if saldo > 0 else ("#FF0000" if saldo < 0 else "white")
        tabla_html += f"""
        <tr>
            <td><b>{e}</b></td>
            <td style="color:{color}; font-weight:bold; font-size:20px;">S/ {saldo}.00</td>
            <td>{st.session_state.ganados[e]} 🏆</td>
        </tr>"""
    tabla_html += "</table>"
    st.markdown(tabla_html, unsafe_allow_html=True)

st.markdown(f"""
    <div class="footer-brand">
        <h3 style="color: #FF4500; letter-spacing: 5px; font-family: 'Arial Black'; margin-top: 5px;">
            BY LUQUE
        </h3>
    </div>
""", unsafe_allow_html=True)