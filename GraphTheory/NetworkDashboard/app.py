import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network
import tempfile
import os

# Set page configuration
st.set_page_config(page_title="Network Analysis Dashboard", layout="wide")

st.title("🕸️ Interactive Network Analysis Dashboard")
st.markdown("""
Upload your data to visualize network structures.
**Instructions:** Upload a CSV, then use the sidebar to select which columns represent the **Source** (Start) and **Target** (End) of connections.
""")

# Sidebar for controls
st.sidebar.header("1. Upload Data")
uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])
delimiter = st.sidebar.selectbox("Choose CSV Delimiter", [",", ";", "\t"], index=0, help="If the data looks messy, try changing this.")

# Selection for sample data if no file is uploaded
if not uploaded_file:
    st.sidebar.info("Using sample data. Upload a CSV to analyze your own network.")
    try:
        df = pd.read_csv("data/sample_data.csv")
    except Exception:
        # Fallback if file not found locally
        data = {
            'Source': ['Alice', 'Alice', 'Bob', 'Charlie', 'Charlie', 'David', 'Eve', 'Frank', 'Bob'],
            'Target': ['Bob', 'Charlie', 'David', 'David', 'Eve', 'Eve', 'Frank', 'Alice', 'Frank'],
            'Weight': [5, 3, 2, 4, 6, 1, 3, 2, 4]
        }
        df = pd.DataFrame(data)
else:
    try:
        df = pd.read_csv(uploaded_file, sep=delimiter)
    except Exception as e:
        st.error(f"Error reading CSV: {e}")
        st.stop()

# Display raw data preview with warnings
with st.expander("🔎 View Raw Data & Debug Info", expanded=True):
    st.dataframe(df.head())
    st.write(f"**Detected Columns:** {list(df.columns)}")
    if len(df.columns) <= 1:
        st.warning("⚠️ The CSV seems to have only 1 column. This usually means the 'Delimiter' is wrong. Try changing it to ';' or Tab in the sidebar.")

# COLUMN MAPPING
st.sidebar.header("2. Map Network Columns")
all_columns = list(df.columns)

# Try to auto-select sensible defaults
source_index = 0
target_index = 1 if len(all_columns) > 1 else 0

for i, col in enumerate(all_columns):
    col_str = str(col).lower()
    if "source" in col_str or "src" in col_str or "from" in col_str:
        source_index = i
    if "target" in col_str or "dst" in col_str or "to" in col_str:
        target_index = i

# Selectpads
source_col = st.sidebar.selectbox("Select Source Column", all_columns, index=source_index, help="The column representing the starting node.")
target_col = st.sidebar.selectbox("Select Target Column", all_columns, index=target_index, help="The column representing the ending node.")

# Proceed only if selection is valid
if source_col and target_col:
    # Rename for internal logic
    # Create a new graph dataframe from selected columns
    graph_df = df[[source_col, target_col]].copy()
    graph_df.columns = ['Source', 'Target']
    
    # Clean data: drop incomplete rows
    graph_df.dropna(subset=['Source', 'Target'], inplace=True)
    
    # Force everything to string (Fixes PyVis AssertionError)
    graph_df['Source'] = graph_df['Source'].astype(str)
    graph_df['Target'] = graph_df['Target'].astype(str)
    
    # Create Graph
    G = nx.from_pandas_edgelist(graph_df, 'Source', 'Target')
    
    # Community Detection (Louvain) for coloring
    try:
        communities = nx.community.louvain_communities(G)
        for i, comm in enumerate(communities):
            for node in comm:
                G.nodes[node]['group'] = i
    except Exception as e:
        pass

    # -------------------
    # COLUMN 1: Visuals
    # -------------------
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("Interactive Graph Visualization")
        physics_toggle = st.checkbox("Enable Physics (Layout Adjustment)", value=True)
        
        # PyVis Network
        net = Network(height="500px", width="100%", bgcolor="#222222", font_color="white", select_menu=True, cdn_resources='in_line')
        net.from_nx(G)
        
        # Physics options
        if physics_toggle:
            net.toggle_physics(True)
            net.show_buttons(filter_=['physics'])
        else:
            net.toggle_physics(False)
            
        # GENERATE HTML DIRECTLY
        try:
            html_content = net.generate_html()
            st.components.v1.html(html_content, height=520, scrolling=False)
            
            if len(G.nodes) == 0:
                st.warning("⚠️ The graph has no nodes/edges. Check your column selection.")
            else:
                st.success(f"Graph generated with {len(G.nodes)} nodes and {len(G.edges)} edges.")
                
        except Exception as e:
            st.error(f"Error visualizing graph: {e}")

    # -------------------
    # COLUMN 2: Metrics
    # -------------------
    with col2:
        st.subheader("Network Metrics")
        
        # Basic Stats
        num_nodes = G.number_of_nodes()
        num_edges = G.number_of_edges()
        density = nx.density(G)
        
        st.metric("Nodes", num_nodes)
        st.metric("Edges", num_edges)
        st.metric("Density", f"{density:.3f}")
        
        try:
            avg_degree = sum(dict(G.degree()).values()) / num_nodes
            st.metric("Avg. Degree", f"{avg_degree:.2f}")
        except:
            pass
        
        st.markdown("---")
        st.write("**Centrality (Top Nodes)**")
        
        # Calculate Centrality
        if len(G) > 0:
            degree_dict = nx.degree_centrality(G)
            betweenness_dict = nx.betweenness_centrality(G)
            
            metrics_data = {
                'Node': list(degree_dict.keys()),
                'Degree': list(degree_dict.values()),
                'Betweenness': list(betweenness_dict.values())
            }
            
            metrics_df = pd.DataFrame(metrics_data).sort_values(by='Betweenness', ascending=False)
            st.dataframe(metrics_df.head(10).style.format("{:.3f}", subset=['Degree', 'Betweenness']), hide_index=True)
else:
    st.info("Please select Source and Target columns from the sidebar to generate the graph.")
