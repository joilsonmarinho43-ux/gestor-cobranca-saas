import streamlit as st
import pandas as pd
import os
from datetime import datetime
from core.database import get_supabase

# =================================================================
# 1. ARQUITETURA DE DESIGN & CONFIGURAÇÃO (UI/UX ENGINE)
# =================================================================

def apply_enterprise_theme():
    """Aplica o Design System profissional via CSS injetado."""
    st.set_page_config(
        page_title="Sol da Vida | ERP Enterprise",
        page_icon="☀️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.markdown("""
        <style>
            /* Reset e Typography */
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
            html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
            
            /* Main Dashboard Cards */
            .metric-container {
                background-color: #ffffff;
                padding: 1.5rem;
                border-radius: 12px;
                border: 1px solid #edf2f7;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            }
            
            /* Status Indicators */
            .status-pill {
                padding: 4px 12px;
                border-radius: 20px;
                font-size: 12px;
                font-weight: 600;
                background-color: #e6fffa;
                color: #2c7a7b;
            }
            
            /* Customer Card */
            .customer-card {
                background: white;
                border-radius: 10px;
                padding: 20px;
                margin-bottom: 15px;
                border-left: 5px solid #3182ce;
                transition: transform 0.2s;
            }
            .customer-card:hover { transform: translateY(-2px); box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); }
        </style>
    """, unsafe_allow_html=True)

# =================================================================
# 2. CAMADA DE SERVIÇOS (BUSINESS LOGIC & DATA)
# =================================================================

class EnterpriseDataService:
    """Centraliza todas as operações de dados com cache inteligente."""
    
    def __init__(self):
        self.db = get_supabase()

    @st.cache_data(ttl=300)
    def get_kpi_metrics(_self):
        """Calcula KPIs em tempo real com cache de 5 minutos."""
        try:
            clients = _self.db.table("clientes").select("valor_mensal").execute()
            pending = _self.db.table("parcelas").select("valor").eq("status", "pendente").execute()
            
            metrics = {
                "total_clients": len(clients.data) if clients.data else 0,
                "mrr": sum(float(c.get("valor_mensal") or 0) for c in clients.data) if clients.data else 0.0,
                "arpu": 0.0,
                "outstanding": sum(float(p.get("valor") or 0) for p in pending.data) if pending.data else 0.0
            }
            if metrics["total_clients"] > 0:
                metrics["arpu"] = metrics["mrr"] / metrics["total_clients"]
                
            return metrics
        except Exception:
            return {"total_clients": 0, "mrr": 0.0, "arpu": 0.0, "outstanding": 0.0}

    def list_clients(self, search_query=None):
        """Retorna lista de clientes com suporte a busca."""
        query = self.db.table("clientes").select("*")
        if search_query:
            query = query.ilike("nome", f"%{search_query}%")
        return query.order("nome").execute()

# =================================================================
# 3. INTERFACE DE NAVEGAÇÃO & MODULOS
# =================================================================

def render_dashboard(service):
    st.subheader("Painel de Controle Estratégico")
    kpis = service.get_kpi_metrics()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Clientes Ativos", kpis["total_clients"])
    with col2:
        st.metric("MRR (Recorrência)", f"R$ {kpis['mrr']:,.2f}")
    with col3:
        st.metric("ARPU (Média p/ Cliente)", f"R$ {kpis['arpu']:,.2f}")
    with col4:
        st.metric("Inadimplência Total", f"R$ {kpis['outstanding']:,.2f}", delta_color="inverse")
    
    st.markdown("---")
    # Gráfico de Projeção (Mockup para visual SaaS)
    st.caption("Projeção de Crescimento Linear")
    st.line_chart(pd.DataFrame([kpis['mrr']*0.8, kpis['mrr']*0.9, kpis['mrr']], columns=["Receita"]))

def render_clients_module(service):
    st.subheader("Gestão de Carteira de Clientes")
    
    c1, c2 = st.columns([3, 1])
    search = c1.text_input("Filtrar por nome ou documento...", placeholder="Digite para buscar...")
    if c2.button("Novo Cadastro", use_container_width=True, type="primary"):
        st.info("Formulário de cadastro disparado via Modal.")

    data = service.list_clients(search)
    
    if not data.data:
        st.warning("Nenhum registro encontrado para os critérios de busca.")
        return

    for item in data.data:
        with st.container():
            st.markdown(f"""
                <div class="customer-card">
                    <table style="width:100%; border:none;">
                        <tr>
                            <td style="width:70%;">
                                <div style="font-size:18px; font-weight:700; color:#1a202c;">{item['nome']}</div>
                                <div style="color:#718096; font-size:14px;">Contrato: R$ {item.get('valor_mensal', 0):,.2f} | Ref: {item.get('id')}</div>
                            </td>
                            <td style="text-align:right; vertical-align:middle;">
                                <span class="status-pill">ATIVO</span>
                            </td>
                        </tr>
                    </table>
                </div>
            """, unsafe_allow_html=True)
            
            # Botões de ação em colunas Streamlit para funcionalidade real
            btn_col1, btn_col2, btn_col3, _ = st.columns([1, 1, 1, 5])
            tel = str(item.get("telefone", "")).replace(" ", "").replace("-", "")
            if tel:
                btn_col1.link_button("💬 WhatsApp", f"https://wa.me/{tel}")
            btn_col2.button("📄 Detalhes", key=f"det_{item['id']}")
            btn_col3.button("⚙️ Ajustes", key=f"cfg_{item['id']}")

# =================================================================
# 4. ENTRY POINT (MAIN LOOP)
# =================================================================

def main():
    apply_enterprise_theme()
    service = EnterpriseDataService()

    # Sidebar Profissional
    with st.sidebar:
        st.title("☀️ Sol da Vida")
        st.markdown("---")
        app_mode = st.radio(
            "Módulos Operacionais",
            ["Dashboard", "Clientes", "Financeiro", "Relatórios"],
            label_visibility="collapsed"
        )
        st.v_spacer(height=20)
        st.caption(f"Sistema Operacional v2.0.4\n\n© {datetime.now().year} Enterprise Solutions")

    # Roteamento de Páginas
    if app_mode == "Dashboard":
        render_dashboard(service)
    elif app_mode == "Clientes":
        render_clients_module(service)
    elif app_mode == "Financeiro":
        st.subheader("Controle Financeiro")
        st.info("Processamento de fluxo de caixa e conciliação bancária.")
    elif app_mode == "Relatórios":
        st.subheader("Business Intelligence")
        st.info("Geração de relatórios PDF/Excel para diretoria.")

if __name__ == "__main__":
    main()
    
