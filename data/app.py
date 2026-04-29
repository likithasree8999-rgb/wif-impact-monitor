import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="WIF Global Impact Monitor", page_icon="🌿", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Lato:wght@300;400;700&display=swap');

/* NUCLEAR OVERRIDE — forces every element */
*, *::before, *::after { box-sizing: border-box; }

html { background-color: #0d2e1e !important; }
body { background-color: #0d2e1e !important; color: #f5f0e8 !important; font-family: 'Lato', sans-serif !important; }

.stApp,
.stApp > div,
.main,
.main > div,
.block-container,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"],
[data-testid="stVerticalBlock"],
[data-testid="stVerticalBlockBorderWrapper"],
section[data-testid="stSidebar"] + div,
.css-1d391kg, .css-fg4pbf, .css-zt5igj, .css-1y4p8pa {
    background-color: #0d2e1e !important;
    background: #0d2e1e !important;
    color: #f5f0e8 !important;
}

/* SIDEBAR */
[data-testid="stSidebar"],
[data-testid="stSidebar"] > div,
[data-testid="stSidebarContent"] {
    background-color: #081c12 !important;
    background: linear-gradient(180deg, #081c12 0%, #0d2418 100%) !important;
    border-right: 1px solid rgba(200,169,110,0.25) !important;
}

/* ALL TEXT CREAM */
p, span, label, div, li, h1, h2, h3, h4, h5, h6, a,
.stMarkdown, .stText,
[data-testid="stMarkdownContainer"],
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] span,
[data-testid="stMarkdownContainer"] li,
[class*="css"] { color: #f5f0e8 !important; }

/* RADIO BUTTONS */
.stRadio > label { color: #f5f0e8 !important; }
.stRadio div[role="radiogroup"] label { color: #f5f0e8 !important; }
.stRadio div[role="radiogroup"] label p { color: #f5f0e8 !important; }

/* SLIDERS */
.stSlider label, .stSlider label p,
.stSlider [data-testid="stMarkdownContainer"] p { color: #f5f0e8 !important; }
.stSlider [data-baseweb="slider"] div { background: #4a9e6b !important; }

/* SELECT BOX */
.stSelectbox label, .stSelectbox label p { color: #f5f0e8 !important; }
.stSelectbox [data-baseweb="select"] div,
.stSelectbox [data-baseweb="select"] > div {
    background-color: #1a3c2a !important;
    border-color: rgba(200,169,110,0.3) !important;
    color: #f5f0e8 !important;
}
.stSelectbox [data-baseweb="select"] span { color: #f5f0e8 !important; }

/* METRICS */
[data-testid="metric-container"] {
    background: #1a3c2a !important;
    border: 1px solid rgba(200,169,110,0.2) !important;
    border-radius: 12px !important;
    padding: 20px !important;
}
[data-testid="metric-container"] label,
[data-testid="metric-container"] [data-testid="stMetricLabel"] p {
    color: rgba(245,240,232,0.5) !important;
    font-size: 0.68rem !important;
    text-transform: uppercase !important;
    letter-spacing: 2px !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"],
[data-testid="metric-container"] [data-testid="stMetricValue"] div {
    color: #6db88a !important;
    font-family: 'Playfair Display', serif !important;
    font-size: 2rem !important;
    font-weight: 700 !important;
}

/* HIDE STREAMLIT CHROME */
#MainMenu, footer, header, [data-testid="stToolbar"], [data-testid="stDecoration"] { visibility: hidden !important; display: none !important; }

/* ═══════════════════════════════════════════
   CUSTOM COMPONENTS
═══════════════════════════════════════════ */

/* SIDEBAR CONTENT */
.sb-wrap { padding: 24px 16px 20px; text-align: center; border-bottom: 1px solid rgba(200,169,110,0.2); margin-bottom: 20px; }
.sb-title { font-family: 'Playfair Display', serif; font-size: 1.5rem; font-weight: 900; color: #6db88a !important; }
.sb-sub   { font-size: 0.6rem; color: rgba(245,240,232,0.35) !important; letter-spacing: 3px; text-transform: uppercase; margin-top: 4px; }
.sb-box   { background: rgba(200,169,110,0.07); border: 1px solid rgba(200,169,110,0.18); border-radius: 12px; padding: 14px 12px; margin: 4px 8px 12px; font-size: 0.77rem; line-height: 1.9; }

/* HERO */
.hero {
    background: linear-gradient(135deg, rgba(74,158,107,0.18) 0%, rgba(26,60,42,0.95) 55%, rgba(200,169,110,0.1) 100%);
    border: 1px solid rgba(200,169,110,0.2);
    border-radius: 20px;
    padding: 52px 48px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
}
.hero::before { content:''; position:absolute; top:-100px; right:-80px; width:380px; height:380px; background:radial-gradient(circle,rgba(74,158,107,0.15) 0%,transparent 70%); border-radius:50%; pointer-events:none; }
.hero-badge { display:inline-block; background:rgba(200,169,110,0.12); border:1px solid rgba(200,169,110,0.35); color:#c8a96e !important; padding:5px 16px; border-radius:20px; font-size:0.68rem; font-weight:700; letter-spacing:2px; text-transform:uppercase; margin-bottom:18px; }
.hero-title { font-family:'Playfair Display',serif; font-size:2.9rem; font-weight:900; line-height:1.1; color:#f5f0e8 !important; margin-bottom:14px; }
.hero-title span { color:#4a9e6b !important; }
.hero-sub { font-size:1rem; color:rgba(245,240,232,0.65) !important; line-height:1.7; max-width:580px; font-weight:300; }

/* KPI GRID */
.kg { display:grid; grid-template-columns:repeat(4,1fr); gap:16px; margin-bottom:16px; }
.kpi { background:linear-gradient(135deg,#1a3c2a,#0f2d1e); border:1px solid rgba(200,169,110,0.12); border-radius:16px; padding:26px 20px; position:relative; overflow:hidden; }
.kpi::before { content:''; position:absolute; top:0;left:0;right:0; height:2px; }
.g1::before { background:linear-gradient(90deg,#4a9e6b,#6db88a); }
.b1::before { background:linear-gradient(90deg,#c8a96e,#e8c87a); }
.t1::before { background:linear-gradient(90deg,#2d7a4f,#4a9e6b); }
.a1::before { background:linear-gradient(90deg,#a07840,#c8a96e); }
.ki { font-size:1.7rem; margin-bottom:12px; }
.kv { font-family:'Playfair Display',serif; font-size:2.4rem; font-weight:900; line-height:1; margin-bottom:6px; }
.g1 .kv { color:#6db88a !important; }
.b1 .kv { color:#c8a96e !important; }
.t1 .kv { color:#8ecfa6 !important; }
.a1 .kv { color:#e8c87a !important; }
.kl { font-size:0.66rem; font-weight:700; letter-spacing:2px; text-transform:uppercase; color:rgba(245,240,232,0.4) !important; margin-bottom:4px; }
.ks { font-size:0.71rem; color:rgba(245,240,232,0.25) !important; }

/* SECTION HEADER */
.sh { display:flex; align-items:center; gap:12px; font-family:'Playfair Display',serif; font-size:1.5rem; font-weight:700; color:#f5f0e8 !important; margin:36px 0 18px; padding-bottom:14px; border-bottom:1px solid rgba(200,169,110,0.15); }
.sl { width:28px; height:3px; border-radius:2px; flex-shrink:0; }
.slg { background:linear-gradient(90deg,#4a9e6b,#6db88a); box-shadow:0 0 8px rgba(74,158,107,0.5); }
.slb { background:linear-gradient(90deg,#c8a96e,#e8c87a); box-shadow:0 0 8px rgba(200,169,110,0.5); }
.slt { background:linear-gradient(90deg,#2d7a4f,#4a9e6b); box-shadow:0 0 8px rgba(45,122,79,0.5); }

/* CARDS */
.pc { background:linear-gradient(135deg,rgba(26,60,42,0.8),rgba(13,46,30,0.9)); border:1px solid rgba(200,169,110,0.1); border-left:3px solid #4a9e6b; border-radius:14px; padding:22px; margin-bottom:12px; }
.pt { font-family:'Playfair Display',serif; font-size:1.1rem; font-weight:700; color:#f5f0e8 !important; margin-bottom:6px; }
.pm { font-size:0.79rem; color:rgba(245,240,232,0.45) !important; line-height:1.6; }
.tg { display:inline-block; background:rgba(74,158,107,0.15); border:1px solid rgba(74,158,107,0.4); color:#6db88a !important; padding:3px 12px; border-radius:20px; font-size:0.67rem; font-weight:700; }
.tb { display:inline-block; background:rgba(200,169,110,0.15); border:1px solid rgba(200,169,110,0.4); color:#c8a96e !important; padding:3px 12px; border-radius:20px; font-size:0.67rem; font-weight:700; }
.mr { background:rgba(26,60,42,0.6); border:1px solid rgba(74,158,107,0.12); border-radius:10px; padding:13px 18px; margin-bottom:10px; font-size:0.87rem; color:rgba(245,240,232,0.8) !important; }
.mr b { color:#6db88a !important; }

/* CALCULATOR */
.cr { background:linear-gradient(135deg,rgba(74,158,107,0.14),rgba(26,60,42,0.9)); border:1px solid rgba(74,158,107,0.22); border-radius:18px; padding:28px 22px; margin-bottom:14px; text-align:center; }
.cv { font-family:'Playfair Display',serif; font-size:2.7rem; font-weight:900; color:#6db88a !important; line-height:1; margin-bottom:8px; }
.cl { font-size:0.67rem; font-weight:700; letter-spacing:2px; text-transform:uppercase; color:rgba(245,240,232,0.4) !important; }
.ec { background:rgba(26,60,42,0.7); border:1px solid rgba(200,169,110,0.1); border-radius:14px; padding:22px 14px; text-align:center; margin-bottom:12px; }
.ei { font-size:2.4rem; margin-bottom:10px; }
.ev { font-family:'Playfair Display',serif; font-size:2rem; font-weight:900; color:#c8a96e !important; margin-bottom:4px; }
.el { font-size:0.67rem; color:rgba(245,240,232,0.38) !important; letter-spacing:1.5px; text-transform:uppercase; }
.es { font-size:0.66rem; color:rgba(245,240,232,0.22) !important; margin-top:4px; }

/* PROGRAMS & SDG */
.pg { background:linear-gradient(135deg,rgba(26,60,42,0.8),rgba(13,46,30,0.85)); border:1px solid rgba(74,158,107,0.14); border-radius:14px; padding:20px; margin-bottom:12px; }
.pi { font-size:1.9rem; margin-bottom:10px; }
.pti { font-family:'Playfair Display',serif; font-size:1rem; font-weight:700; color:#6db88a !important; margin-bottom:5px; }
.pd { font-size:0.77rem; color:rgba(245,240,232,0.45) !important; line-height:1.5; }
.sg { background:linear-gradient(135deg,rgba(200,169,110,0.07),rgba(26,60,42,0.8)); border:1px solid rgba(200,169,110,0.14); border-radius:12px; padding:18px 13px; margin-bottom:12px; text-align:center; }
.sn { font-size:0.61rem; font-weight:700; letter-spacing:2px; color:#c8a96e !important; text-transform:uppercase; margin-bottom:5px; }
.sti { font-family:'Playfair Display',serif; font-size:0.92rem; font-weight:700; color:#f5f0e8 !important; margin-bottom:5px; }
.sd { font-size:0.69rem; color:rgba(245,240,232,0.37) !important; line-height:1.5; }

/* FOOTER */
.ft { text-align:center; padding:36px 20px; margin-top:56px; border-top:1px solid rgba(200,169,110,0.1); font-size:0.77rem; color:rgba(245,240,232,0.22) !important; line-height:2.2; }
.ft a { color:#4a9e6b !important; text-decoration:none; margin:0 12px; }
.ft b { color:#6db88a !important; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.read_csv("data/projects.csv"), pd.read_csv("data/offices.csv")

projects_df, offices_df = load_data()

T = dict(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#f5f0e8", font_family="Lato")

def C(fig, h=380):
    fig.update_layout(**T, height=h, margin=dict(l=0,r=0,t=16,b=0), coloraxis_showscale=False,
        xaxis=dict(gridcolor="rgba(245,240,232,0.06)", color="rgba(245,240,232,0.35)"),
        yaxis=dict(gridcolor="rgba(245,240,232,0.06)", color="rgba(245,240,232,0.35)"))
    return fig

# ── SIDEBAR
with st.sidebar:
    st.markdown("""
    <div class="sb-wrap">
        <div class="sb-title">🌿 WIF Monitor</div>
        <div class="sb-sub">Global Impact Dashboard</div>
    </div>""", unsafe_allow_html=True)
    page = st.radio("", ["🌍  Global Overview","📊  Project Deep Dive","🌱  Carbon Calculator","👥  Community Impact"], label_visibility="collapsed")
    st.markdown("""
    <div class="sb-box">
        <div style="color:#c8a96e;font-weight:700;font-size:0.66rem;letter-spacing:2px;text-transform:uppercase;margin-bottom:10px;">Partner Organizations</div>
        🌐 worldviewusa.org<br>🌿 wif.foundation<br>✅ Verra VCS Verified<br><br>
        <div style="color:rgba(245,240,232,0.28);font-size:0.64rem;">UN FAO Recognized · 46 Years · 6 Countries</div>
    </div>
    <div style="text-align:center;font-size:0.64rem;color:rgba(245,240,232,0.18);padding:8px 0;">
        Built by Likitha Sree Yarabarla<br><span style="color:#4a9e6b;">linkedin.com/in/likitha-sree</span>
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
if "Global" in page:
    st.markdown("""
    <div class="hero">
        <div class="hero-badge">🏆 UN FAO Recognized &nbsp;·&nbsp; Verra VCS Verified &nbsp;·&nbsp; 46 Years</div>
        <div class="hero-title">Worldview International Foundation<br><span>Global Impact Monitor</span></div>
        <div class="hero-sub">Tracking carbon sequestration, community development, and mangrove ecosystem restoration across 7 verified projects in Myanmar and Malaysia.</div>
    </div>
    <div class="kg">
        <div class="kpi g1"><div class="ki">🌿</div><div class="kv">16,735+</div><div class="kl">Hectares Restored</div><div class="ks">Across 7 projects · 2 countries</div></div>
        <div class="kpi b1"><div class="ki">💨</div><div class="kv">26.3M</div><div class="kl">Tonnes CO₂e Estimated</div><div class="ks">Total over all crediting periods</div></div>
        <div class="kpi t1"><div class="ki">👥</div><div class="kv">140K+</div><div class="kl">Community Members</div><div class="ks">Across 125+ villages</div></div>
        <div class="kpi a1"><div class="ki">⏳</div><div class="kv">46</div><div class="kl">Years Experience</div><div class="ks">Global operations since 1979</div></div>
    </div>
    <div class="kg">
        <div class="kpi b1"><div class="ki">📉</div><div class="kv">1.17M</div><div class="kl">Tonnes CO₂e / Year</div><div class="ks">Annual reduction · active projects</div></div>
        <div class="kpi g1"><div class="ki">✅</div><div class="kv">6</div><div class="kl">Verra VCS Verified</div><div class="ks">Independently audited projects</div></div>
        <div class="kpi t1"><div class="ki">🚗</div><div class="kv">255K</div><div class="kl">Cars Off the Road</div><div class="ks">Equivalent annual impact</div></div>
        <div class="kpi a1"><div class="ki">🌍</div><div class="kv">7</div><div class="kl">Active Projects</div><div class="ks">Myanmar · Malaysia · Expanding</div></div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="sh"><div class="sl slg"></div>Global Restoration Sites</div>', unsafe_allow_html=True)
    all_pts = pd.concat([
        projects_df[["project_id","name","lat","lon","hectares","people","status","country"]].assign(mt="🌿 Project"),
        offices_df.rename(columns={"office":"name"})[["name","lat","lon","country"]].assign(mt="🏢 Office",project_id="",hectares=50,people=0,status="Office")
    ], ignore_index=True)
    fig_map = px.scatter_mapbox(all_pts,lat="lat",lon="lon",color="mt",size="hectares",size_max=40,
        hover_name="name",hover_data={"hectares":True,"people":True,"country":True,"lat":False,"lon":False},
        color_discrete_map={"🌿 Project":"#4a9e6b","🏢 Office":"#c8a96e"},
        mapbox_style="carto-darkmatter",zoom=2.2,center={"lat":12,"lon":90},height=500)
    fig_map.update_layout(**T,margin=dict(l=0,r=0,t=0,b=0),
        legend=dict(font=dict(color="#f5f0e8",size=12),bgcolor="rgba(13,46,30,0.85)",bordercolor="rgba(200,169,110,0.2)"))
    st.plotly_chart(fig_map, use_container_width=True)

    c1,c2=st.columns(2)
    with c1:
        st.markdown('<div class="sh"><div class="sl slg"></div>Hectares by Project</div>', unsafe_allow_html=True)
        f=px.bar(projects_df.sort_values("hectares"),x="hectares",y="project_id",orientation="h",
            color="hectares",color_continuous_scale=[[0,"#0d2e1e"],[0.5,"#2d7a4f"],[1,"#4a9e6b"]],text="hectares")
        f.update_traces(texttemplate="%{text:,}",textposition="outside",textfont_color="rgba(245,240,232,0.65)")
        st.plotly_chart(C(f), use_container_width=True)
    with c2:
        st.markdown('<div class="sh"><div class="sl slb"></div>CO₂e by Project (M tonnes)</div>', unsafe_allow_html=True)
        f2=px.bar(projects_df[projects_df["co2e_million"]>0].sort_values("co2e_million"),x="co2e_million",y="project_id",orientation="h",
            color="co2e_million",color_continuous_scale=[[0,"#1a0e00"],[0.5,"#a07840"],[1,"#c8a96e"]],text="co2e_million")
        f2.update_traces(texttemplate="%{text}M",textposition="outside",textfont_color="rgba(245,240,232,0.65)")
        st.plotly_chart(C(f2), use_container_width=True)

    st.markdown('<div class="sh"><div class="sl slt"></div>Project Crediting Periods</div>', unsafe_allow_html=True)
    clrs=["#4a9e6b","#6db88a","#c8a96e","#e8c87a","#2d7a4f","#8ecfa6","#a07840"]
    fg=go.Figure()
    for i,row in projects_df.iterrows():
        fg.add_trace(go.Bar(x=[row["end_year"]-row["start_year"]],y=[row["project_id"]],base=[row["start_year"]],
            orientation="h",marker_color=clrs[i%len(clrs)],marker_opacity=0.85,name=row["project_id"],
            text=f"{int(row['start_year'])}–{int(row['end_year'])}",textposition="inside",insidetextanchor="middle",
            hovertemplate=f"<b>{row['name']}</b><br>{int(row['start_year'])}–{int(row['end_year'])}<extra></extra>"))
    fg.update_layout(**T,barmode="overlay",showlegend=False,height=300,margin=dict(l=0,r=0,t=16,b=0),
        xaxis=dict(gridcolor="rgba(245,240,232,0.05)",color="rgba(245,240,232,0.35)",range=[2010,2072],title="Year"),
        yaxis=dict(gridcolor="rgba(245,240,232,0.05)",color="rgba(245,240,232,0.35)"))
    st.plotly_chart(fg, use_container_width=True)

elif "Project" in page:
    st.markdown("""
    <div class="hero">
        <div class="hero-badge">📋 Verra VCS Verified Projects</div>
        <div class="hero-title">Project <span>Deep Dive</span></div>
        <div class="hero-sub">Explore each mangrove restoration project — carbon targets, community reach, and live Verra verification.</div>
    </div>""", unsafe_allow_html=True)

    sel=st.selectbox("Select a Project",options=projects_df["project_id"].tolist(),
        format_func=lambda x:f"{x}  —  {projects_df[projects_df['project_id']==x]['name'].values[0]}")
    proj=projects_df[projects_df["project_id"]==sel].iloc[0]
    badge=f'<span class="tg">✅ VCS ID {int(proj["vcs_id"])}</span>' if pd.notna(proj["vcs_id"]) and proj["vcs_id"]!=0 else '<span class="tb">🔄 In Development</span>'
    st.markdown(f"""
    <div class="pc">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:16px;flex-wrap:wrap;">
            <div><div class="pt">{proj['name']}</div><div class="pm">📍 {proj['region']}, {proj['country']}</div><div class="pm" style="margin-top:8px;color:rgba(245,240,232,0.5);">{proj['description']}</div></div>
            <div>{badge}</div>
        </div>
    </div>""", unsafe_allow_html=True)

    c1,c2,c3,c4=st.columns(4)
    c1.metric("Hectares",f"{int(proj['hectares']):,}")
    c2.metric("People",f"{int(proj['people']):,}")
    c3.metric("Villages",f"{int(proj['villages'])}")
    c4.metric("Period",f"{int(proj['start_year'])}–{int(proj['end_year'])}")

    col1,col2=st.columns(2)
    with col1:
        st.markdown('<div class="sh"><div class="sl slg"></div>Carbon Sequestration Projection</div>', unsafe_allow_html=True)
        if proj["co2e_million"]>0:
            yrs=int(proj["end_year"]-proj["start_year"])
            fc=go.Figure()
            fc.add_trace(go.Scatter(x=list(range(int(proj["start_year"]),int(proj["end_year"])+1)),
                y=[proj["annual_co2e"]*y/1e6 for y in range(yrs+1)],fill="tozeroy",
                fillcolor="rgba(74,158,107,0.1)",line=dict(color="#4a9e6b",width=3),name="Cumulative CO₂e"))
            st.plotly_chart(C(fc,300), use_container_width=True)
            cars=int(proj["annual_co2e"]/4.6); homes=int(proj["annual_co2e"]/7.5)
            st.markdown(f"""
            <div class="mr">💨 <b>{proj['co2e_million']}M tonnes CO₂e</b> total estimated over crediting period</div>
            <div class="mr">🚗 Removes <b>{cars:,} cars</b> from the road annually</div>
            <div class="mr">🏠 Powers <b>{homes:,} homes</b> every year</div>""", unsafe_allow_html=True)
        else:
            st.info("Carbon estimates in development for this project")
    with col2:
        st.markdown('<div class="sh"><div class="sl slb"></div>Project Location</div>', unsafe_allow_html=True)
        fm=px.scatter_mapbox(pd.DataFrame([proj]),lat="lat",lon="lon",hover_name="name",size=[proj["hectares"]],size_max=30,
            color_discrete_sequence=["#4a9e6b"],mapbox_style="carto-darkmatter",zoom=5,center={"lat":proj["lat"],"lon":proj["lon"]},height=280)
        fm.update_layout(**T,margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fm, use_container_width=True)
        if pd.notna(proj["vcs_id"]) and proj["vcs_id"]!=0:
            url=f"https://registry.verra.org/app/projectDetail/VCS/{int(proj['vcs_id'])}"
            st.markdown(f"""<div style="text-align:center;margin-top:16px;"><a href="{url}" target="_blank" style="display:inline-block;background:rgba(74,158,107,0.15);border:1px solid rgba(74,158,107,0.4);color:#6db88a;padding:10px 28px;border-radius:10px;text-decoration:none;font-size:0.85rem;font-weight:700;">✅ View on Verra Registry →</a></div>""", unsafe_allow_html=True)

    st.markdown('<div class="sh"><div class="sl slt"></div>All Projects</div>', unsafe_allow_html=True)
    for _,row in projects_df.iterrows():
        b=f'<span class="tg">VCS {int(row["vcs_id"])}</span>' if pd.notna(row["vcs_id"]) and row["vcs_id"]!=0 else '<span class="tb">In Development</span>'
        st.markdown(f"""<div class="pc"><div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;"><div><div class="pt">{row['project_id']} — {row['name']}</div><div class="pm">📍 {row['region']}, {row['country']} &nbsp;·&nbsp; 🌿 {int(row['hectares']):,} ha &nbsp;·&nbsp; 👥 {int(row['people']):,} people &nbsp;·&nbsp; 📅 {int(row['start_year'])}–{int(row['end_year'])}</div></div><div>{b}</div></div></div>""", unsafe_allow_html=True)

elif "Carbon" in page:
    st.markdown("""
    <div class="hero">
        <div class="hero-badge">🌱 Interactive Carbon Calculator</div>
        <div class="hero-title">What Does Mangrove<br><span>Restoration Actually Mean?</span></div>
        <div class="hero-sub">Translate hectares into real-world climate impact — cars off the road, homes powered, and carbon credit market value.</div>
    </div>""", unsafe_allow_html=True)

    col1,col2=st.columns([1,1])
    with col1:
        st.markdown('<div class="sh"><div class="sl slg"></div>Configure Your Calculation</div>', unsafe_allow_html=True)
        ha   =st.slider("Hectares of Mangrove Restored",100,20000,int(projects_df["hectares"].sum()),100)
        rate =st.slider("CO₂ Rate (tonnes/hectare/year)",4.0,12.0,6.5,0.5)
        yrs  =st.slider("Projection Period (years)",5,40,20,5)
        price=st.slider("Carbon Credit Price (USD/tonne)",5,100,25,5)
    with col2:
        st.markdown('<div class="sh"><div class="sl slb"></div>Your Impact Results</div>', unsafe_allow_html=True)
        ann=ha*rate; tot=ann*yrs; val=tot*price
        st.markdown(f"""
        <div class="cr"><div class="cv">{ann:,.0f}</div><div class="cl">Tonnes CO₂e Sequestered Annually</div></div>
        <div class="cr" style="background:linear-gradient(135deg,rgba(200,169,110,0.12),rgba(26,60,42,0.9));border-color:rgba(200,169,110,0.25);"><div class="cv" style="color:#c8a96e !important;">{tot/1e6:.2f}M</div><div class="cl">Total Tonnes CO₂e over {yrs} Years</div></div>
        <div class="cr" style="background:linear-gradient(135deg,rgba(232,200,122,0.12),rgba(26,60,42,0.9));border-color:rgba(232,200,122,0.25);"><div class="cv" style="color:#e8c87a !important;">${val/1e6:.1f}M</div><div class="cl">Carbon Credit Market Value</div></div>""", unsafe_allow_html=True)

    st.markdown('<div class="sh"><div class="sl slt"></div>Real World Equivalents (Annual)</div>', unsafe_allow_html=True)
    e1,e2,e3=st.columns(3)
    with e1: st.markdown(f"""<div class="ec"><div class="ei">🚗</div><div class="ev">{int(ann/4.6):,}</div><div class="el">Cars Removed</div><div class="es">4.6 tonnes CO₂/car/year</div></div>""", unsafe_allow_html=True)
    with e2: st.markdown(f"""<div class="ec"><div class="ei">🏠</div><div class="ev">{int(ann/7.5):,}</div><div class="el">Homes Powered</div><div class="es">7.5 tonnes CO₂/home/year</div></div>""", unsafe_allow_html=True)
    with e3: st.markdown(f"""<div class="ec"><div class="ei">✈️</div><div class="ev">{int(ann/0.255):,}</div><div class="el">Flights Avoided</div><div class="es">255kg CO₂/flight</div></div>""", unsafe_allow_html=True)

    st.markdown('<div class="sh"><div class="sl slg"></div>Sequestration Projection</div>', unsafe_allow_html=True)
    yr_range=list(range(2025,2025+yrs+1)); cumul=[ann*y/1e6 for y in range(yrs+1)]
    fp=go.Figure()
    fp.add_trace(go.Scatter(x=yr_range,y=cumul,fill="tozeroy",fillcolor="rgba(74,158,107,0.09)",line=dict(color="#4a9e6b",width=3),name="Cumulative CO₂e"))
    fp.add_trace(go.Bar(x=yr_range[1:],y=[ann/1e6]*yrs,name="Annual",marker_color="rgba(200,169,110,0.3)",yaxis="y2"))
    fp.update_layout(**T,height=340,margin=dict(l=0,r=0,t=16,b=0),
        xaxis=dict(gridcolor="rgba(245,240,232,0.05)",color="rgba(245,240,232,0.35)"),
        yaxis=dict(gridcolor="rgba(245,240,232,0.05)",color="rgba(245,240,232,0.35)",title="Cumulative M tCO₂e"),
        yaxis2=dict(overlaying="y",side="right",color="rgba(245,240,232,0.35)",title="Annual M tCO₂e"),
        legend=dict(font=dict(color="#f5f0e8"),bgcolor="rgba(13,46,30,0.85)"))
    st.plotly_chart(fp, use_container_width=True)

elif "Community" in page:
    st.markdown("""
    <div class="hero">
        <div class="hero-badge">👥 People at the Frontlines of Climate Change</div>
        <div class="hero-title">Community <span>Impact Dashboard</span></div>
        <div class="hero-sub">140,000+ community members co-governing sustainable development. Restoration isn't just about trees — it's about the people who depend on them.</div>
    </div>
    <div class="kg">
        <div class="kpi g1"><div class="ki">👥</div><div class="kv">140K+</div><div class="kl">Community Members</div></div>
        <div class="kpi b1"><div class="ki">🏘️</div><div class="kv">125+</div><div class="kl">Villages Reached</div></div>
        <div class="kpi t1"><div class="ki">📅</div><div class="kv">46</div><div class="kl">Years Community Dev</div></div>
        <div class="kpi a1"><div class="ki">🌍</div><div class="kv">6</div><div class="kl">Countries</div></div>
    </div>""", unsafe_allow_html=True)

    col1,col2=st.columns(2)
    with col1:
        st.markdown('<div class="sh"><div class="sl slg"></div>People Impacted by Project</div>', unsafe_allow_html=True)
        fp2=px.bar(projects_df.sort_values("people"),x="people",y="project_id",orientation="h",
            color="people",color_continuous_scale=[[0,"#0d2e1e"],[0.5,"#2d7a4f"],[1,"#4a9e6b"]],text="people")
        fp2.update_traces(texttemplate="%{text:,}",textposition="outside",textfont_color="rgba(245,240,232,0.65)")
        st.plotly_chart(C(fp2), use_container_width=True)
    with col2:
        st.markdown('<div class="sh"><div class="sl slb"></div>Villages by Project</div>', unsafe_allow_html=True)
        fpie=px.pie(projects_df,values="villages",names="project_id",hole=0.42,
            color_discrete_sequence=["#4a9e6b","#6db88a","#c8a96e","#e8c87a","#2d7a4f","#8ecfa6","#a07840"])
        fpie.update_layout(**T,height=380,margin=dict(l=0,r=0,t=16,b=0),legend=dict(font=dict(color="#f5f0e8"),bgcolor="rgba(0,0,0,0)"))
        fpie.update_traces(textfont_color="#f5f0e8")
        st.plotly_chart(fpie, use_container_width=True)

    st.markdown('<div class="sh"><div class="sl slt"></div>Community Development Programs</div>', unsafe_allow_html=True)
    progs=[("🎓","Vocational Training","Skills programs equipping community members with sustainable livelihood skills"),
        ("💰","Income Generation","Cash-for-work schemes and revolving funds creating direct economic opportunity"),
        ("📚","Education & Awareness","Youth education programs and environmental knowledge improvement"),
        ("🏗️","Health & Infrastructure","Road construction, clean water access, and community infrastructure"),
        ("🐟","Aquaculture Support","Sustainable fishing programs tied to restored mangrove ecosystems"),
        ("⚡","Renewable Energy","Clean energy access programs in partnership with restoration sites")]
    p1,p2=st.columns(2)
    for i,(ic,ti,de) in enumerate(progs):
        with(p1 if i%2==0 else p2):
            st.markdown(f"""<div class="pg"><div class="pi">{ic}</div><div class="pti">{ti}</div><div class="pd">{de}</div></div>""", unsafe_allow_html=True)

    st.markdown('<div class="sh"><div class="sl slb"></div>UN Sustainable Development Goals</div>', unsafe_allow_html=True)
    sdgs=[("SDG 1","No Poverty","Community livelihoods generate sustainable income"),
        ("SDG 2","Zero Hunger","Aquaculture and food security via restored ecosystems"),
        ("SDG 3","Good Health","Clean water and storm protection improve health"),
        ("SDG 4","Quality Education","Youth and vocational training programs"),
        ("SDG 13","Climate Action","1.17M tonnes CO₂e reduced annually"),
        ("SDG 14","Life Below Water","Marine ecosystem restoration"),
        ("SDG 15","Life on Land","Biodiversity across 16,735+ hectares"),
        ("SDG 17","Partnerships","Community governance and global collaboration")]
    cols=st.columns(4)
    for i,(nu,ti,de) in enumerate(sdgs):
        with cols[i%4]:
            st.markdown(f"""<div class="sg"><div class="sn">{nu}</div><div class="sti">{ti}</div><div class="sd">{de}</div></div>""", unsafe_allow_html=True)

st.markdown("""
<div class="ft">
    Built by <b>Likitha Sree Yarabarla</b> · Analytics Engineer · Climate Data Infrastructure<br>
    Supporting Worldview Development USA & Worldview International Foundation<br><br>
    <a href="https://worldviewusa.org" target="_blank">worldviewusa.org</a>
    <a href="https://wif.foundation" target="_blank">wif.foundation</a>
    <a href="https://linkedin.com/in/likitha-sree" target="_blank">LinkedIn</a>
</div>""", unsafe_allow_html=True)