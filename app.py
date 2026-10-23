import streamlit as st
import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Sentinel | Network Threat Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = Path(__file__).parent

# =========================================================
# ADVANCED DARK UI
# =========================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');

    :root {
      --bg: #07111f;
      --panel: #0d1b2b;
      --panel2: #102337;
      --line: rgba(148, 190, 220, .16);
      --text: #e9f3fc;
      --muted: #8ea8bf;
      --cyan: #4de2e8;
      --green: #62f6b0;
      --red: #ff6b83;
      --amber: #ffd166;
    }

    html, body, [class*="css"] {
      font-family: 'Manrope', sans-serif;
    }
    .stApp {
      background:
        radial-gradient(ellipse at 12% 0%, rgba(26, 107, 145, .22), transparent 34%),
        radial-gradient(ellipse at 95% 8%, rgba(34, 184, 155, .10), transparent 28%),
        var(--bg);
      color: var(--text);
    }
    [data-testid="stHeader"] { background: rgba(7,17,31,.72); }
    [data-testid="stSidebar"] {
      background: linear-gradient(180deg, #0a1828 0%, #081321 100%);
      border-right: 1px solid var(--line);
    }
    [data-testid="stSidebar"] * { color: var(--text); }
    .block-container { padding-top: 1.6rem; padding-bottom: 3rem; max-width: 1500px; }

    h1, h2, h3 { color: var(--text) !important; letter-spacing: -.035em; }
    p, label, .stMarkdown { color: var(--text); }
    [data-testid="stCaptionContainer"] { color: var(--muted); }

    .hero {
      padding: 1.6rem 1.7rem;
      border: 1px solid rgba(77,226,232,.24);
      border-radius: 22px;
      background: linear-gradient(120deg, rgba(15,39,59,.96), rgba(10,28,43,.82));
      box-shadow: 0 18px 55px rgba(0,0,0,.18);
      margin-bottom: 1.2rem;
      position: relative;
      overflow: hidden;
    }
    .hero:after {
      content: "";
      position: absolute; width: 230px; height: 230px; right: -65px; top: -100px;
      border: 1px solid rgba(77,226,232,.17); border-radius: 50%;
      box-shadow: 0 0 0 25px rgba(77,226,232,.025), 0 0 0 52px rgba(77,226,232,.02);
    }
    .eyebrow {
      color: var(--cyan); font-family: 'DM Mono', monospace;
      text-transform: uppercase; letter-spacing: .16em; font-size: .72rem;
    }
    .hero-title { font-size: clamp(1.8rem, 3.2vw, 2.8rem); font-weight: 800; margin: .4rem 0 .35rem; line-height: 1.12; }
    .hero-sub { color: #a9c1d5; max-width: 760px; font-size: .98rem; }
    .status-pill {
      display: inline-flex; align-items: center; gap: .45rem;
      padding: .38rem .7rem; border-radius: 99px;
      border: 1px solid rgba(98,246,176,.3); background: rgba(98,246,176,.08);
      color: var(--green); font-family: 'DM Mono', monospace; font-size: .72rem;
    }
    .metric-card {
      border: 1px solid var(--line); border-radius: 17px; padding: 1.05rem 1.15rem;
      background: linear-gradient(145deg, rgba(16,35,55,.95), rgba(10,25,40,.92));
      min-height: 128px;
    }
    .metric-label { color: var(--muted); font-size: .78rem; letter-spacing: .07em; text-transform: uppercase; }
    .metric-value { font-size: 1.85rem; font-weight: 800; margin-top: .45rem; line-height: 1.1; }
    .metric-note { color: #8ea8bf; font-size: .75rem; margin-top: .5rem; }
    .section-head {
      margin: 1.4rem 0 .8rem; font-size: 1.15rem; font-weight: 800;
      display: flex; align-items: center; gap: .55rem;
    }
    .section-sub { color: var(--muted); font-size: .86rem; margin-top: -.35rem; margin-bottom: .85rem; }
    .panel {
      border: 1px solid var(--line); background: rgba(13,27,43,.82);
      border-radius: 18px; padding: 1.1rem 1.15rem;
    }
    .mini-label { font-size: .72rem; color: var(--muted); text-transform: uppercase; letter-spacing: .1em; }
    .mini-value { font-size: 1.15rem; font-weight: 800; margin-top: .25rem; }
    .risk-high { color: var(--red); }
    .risk-low { color: var(--green); }
    .mono { font-family: 'DM Mono', monospace; }
    div[data-testid="stFileUploader"] {
      border: 1px dashed rgba(77,226,232,.35); border-radius: 16px;
      background: rgba(13,34,52,.55); padding: .55rem;
    }
    .stButton > button, .stDownloadButton > button {
      border-radius: 11px; border: 1px solid rgba(77,226,232,.4);
      background: linear-gradient(100deg, #28bfc9, #36d9b1);
      color: #061420; font-weight: 800; min-height: 2.7rem;
    }
    .stButton > button:hover, .stDownloadButton > button:hover {
      border-color: var(--cyan); color: #061420; filter: brightness(1.06);
    }
    div[data-baseweb="select"] > div, div[data-baseweb="input"] > div {
      background-color: #102337; border-color: var(--line);
    }
    [data-testid="stDataFrame"] {
      border: 1px solid var(--line); border-radius: 12px; overflow: hidden;
    }
    hr { border-color: var(--line); }
    .footer {
      color: #6f899f; font-size: .75rem; text-align: center;
      border-top: 1px solid var(--line); padding-top: 1.1rem; margin-top: 2.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# MODEL LOADING
# =========================================================
@st.cache_resource
def load_artifacts():
    model = joblib.load(BASE_DIR / "intrusion_model.joblib")
    features = joblib.load(BASE_DIR / "feature_names.joblib")
    return model, list(features)

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.markdown(
        """
        <div style="padding:.45rem 0 1.15rem;">
          <div style="font-size:1.8rem;">🛡️ <span style="font-weight:800;letter-spacing:-.04em;">SENTINEL</span></div>
          <div style="color:#8ea8bf;font-family:'DM Mono',monospace;font-size:.68rem;letter-spacing:.14em;">
            NETWORK THREAT INTELLIGENCE
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    page = st.radio(
        "WORKSPACE",
        ["Overview", "Traffic Analysis", "Prediction Explorer", "About & Limitations"],
        label_visibility="visible",
    )
    st.markdown("---")
    st.markdown("**MODEL STATUS**")
    try:
        model, features = load_artifacts()
        st.success("Model artifacts loaded")
        st.caption(f"{len(features):,} expected input features")
    except FileNotFoundError:
        model, features = None, []
        st.error("Model files not found")
        st.caption("Keep both .joblib files beside app.py.")
    except Exception as e:
        model, features = None, []
        st.error(f"Could not load model: {e}")

    st.markdown("---")
    st.caption("PROJECT BUILD · 2026")
    st.caption("Random Forest · Streamlit")

# =========================================================
# HERO
# =========================================================
st.markdown(
    """
    <div class="hero">
      <div class="eyebrow">CYBER DEFENCE / ML ANALYTICS</div>
      <div class="hero-title">Network Intrusion<br>Detection System</div>
      <div class="hero-sub">
        Analyze network-flow CSV data with a trained machine-learning classifier.
        Inspect predictions, review traffic patterns, and export an investigation report.
      </div>
      <div style="margin-top:1rem;">
        <span class="status-pill">● OFFLINE DATA ANALYSIS</span>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# UPLOAD
# =========================================================
if model is None:
    st.warning(
        "Model artifacts are unavailable. Place intrusion_model.joblib and "
        "feature_names.joblib in the same folder as app.py, then refresh."
    )
    st.stop()

left, right = st.columns([1.55, 1], gap="large")
with left:
    st.markdown('<div class="section-head">⬆️ Ingest network telemetry</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Upload a compatible network traffic CSV",
        type=["csv"],
        help="The CSV must contain every feature used during model training.",
        key="traffic_csv",
    )
with right:
    st.markdown('<div class="section-head">◈ Analysis protocol</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="panel">
          <div class="mini-label">INPUT</div><div class="mini-value">CSV · Network flow features</div>
          <hr>
          <div class="mini-label">ENGINE</div><div class="mini-value">Random Forest classifier</div>
          <hr>
          <div class="mini-label">OUTPUT</div><div class="mini-value">Benign / Potential Attack</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

if uploaded_file is None:
    st.markdown(
        """
        <div class="panel" style="margin-top:1rem;">
          <div class="eyebrow">READY FOR ANALYSIS</div>
          <h3 style="margin:.5rem 0;">Waiting for a dataset</h3>
          <p style="color:#8ea8bf;margin:0;">
            Upload a CSV file above to unlock traffic classification, risk summaries,
            searchable predictions, and downloadable results.
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    try:
        df = pd.read_csv(uploaded_file, low_memory=False)
        df.columns = df.columns.astype(str).str.strip()

        if df.empty:
            st.error("The uploaded CSV contains no records.")
            st.stop()

        missing = [col for col in features if col not in df.columns]
        if missing:
            st.error(
                f"{len(missing)} required model feature(s) are missing. "
                "Upload a CSV compatible with the training dataset."
            )
            with st.expander("View missing feature names"):
                st.code("\n".join(missing[:100]))
            st.stop()

        # Feature preprocessing follows the notebook's numeric cleanup.
        X = df[features].apply(pd.to_numeric, errors="coerce")
        X = X.replace([np.inf, -np.inf], np.nan).fillna(0)

        with st.spinner("Analyzing network flows..."):
            predictions = model.predict(X)

            # Use the probability for class label 1, rather than assuming
            # class 1 is always the second probability column.
            attack_prob = np.full(len(df), np.nan, dtype=float)
            if hasattr(model, "predict_proba"):
                class_list = list(getattr(model, "classes_", []))
                if 1 in class_list:
                    class_index = class_list.index(1)
                    attack_prob = model.predict_proba(X)[:, class_index] * 100

        results = df.copy()
        results["Prediction"] = np.where(np.asarray(predictions) == 1, "Attack", "Benign")
        results["Attack_Probability_%"] = np.round(attack_prob, 2)

        total = len(results)
        attacks = int((np.asarray(predictions) == 1).sum())
        benign = total - attacks
        attack_rate = (attacks / total * 100) if total else 0.0
        avg_attack_probability = (
            float(np.nanmean(attack_prob)) if np.isfinite(attack_prob).any() else None
        )
        timestamp = datetime.now().strftime("%d %b %Y · %H:%M")

        if page == "Overview":
            st.markdown('<div class="section-head">◈ Threat overview</div>', unsafe_allow_html=True)
            st.caption(f"Analysis generated {timestamp}. Counts represent model predictions, not verified ground truth.")

            m1, m2, m3, m4 = st.columns(4, gap="medium")
            cards = [
                (m1, "RECORDS ANALYZED", f"{total:,}", "Rows in uploaded file", "#e9f3fc"),
                (m2, "POTENTIAL ATTACKS", f"{attacks:,}", f"{attack_rate:.2f}% of records", "#ff6b83"),
                (m3, "BENIGN PREDICTIONS", f"{benign:,}", "Classified as benign", "#62f6b0"),
                (m4, "AVG. ATTACK SCORE", f"{avg_attack_probability:.1f}%" if avg_attack_probability is not None else "N/A", "Mean model probability for class 1", "#4de2e8"),
            ]
            for col, label, value, note, accent in cards:
                with col:
                    st.markdown(
                        f"""
                        <div class="metric-card">
                          <div class="metric-label">{label}</div>
                          <div class="metric-value" style="color:{accent};">{value}</div>
                          <div class="metric-note">{note}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

            st.markdown('<div class="section-head">📊 Traffic distribution</div>', unsafe_allow_html=True)
            chart_col, risk_col = st.columns([1.35, 1], gap="large")
            counts = results["Prediction"].value_counts().reindex(["Benign", "Attack"], fill_value=0)
            with chart_col:
                fig = px.bar(
                    x=counts.index,
                    y=counts.values,
                    color=counts.index,
                    color_discrete_map={"Benign": "#62f6b0", "Attack": "#ff6b83"},
                    labels={"x": "Predicted class", "y": "Records"},
                    template="plotly_dark",
                )
                fig.update_layout(
                    showlegend=False, height=340, margin=dict(l=10, r=10, t=20, b=10),
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(family="Manrope", color="#dcebf7"),
                )
                fig.update_xaxes(showgrid=False)
                fig.update_yaxes(gridcolor="rgba(142,168,191,.12)")
                st.plotly_chart(fig, use_container_width=True)

            with risk_col:
                fig2 = go.Figure(
                    go.Pie(
                        labels=["Benign", "Potential Attack"],
                        values=[benign, attacks],
                        hole=.72,
                        marker=dict(colors=["#62f6b0", "#ff6b83"], line=dict(color="#0d1b2b", width=3)),
                        textinfo="label+percent",
                        textfont=dict(size=12),
                    )
                )
                fig2.update_layout(
                    height=340, showlegend=False,
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(l=10, r=10, t=20, b=10),
                    annotations=[dict(text=f"{total:,}<br><sup>flows</sup>", x=.5, y=.5, showarrow=False,
                                       font=dict(size=21, color="#e9f3fc", family="Manrope"))],
                )
                st.plotly_chart(fig2, use_container_width=True)

            st.markdown('<div class="section-head">🔎 Recent predictions</div>', unsafe_allow_html=True)
            preview_cols = [c for c in ["Prediction", "Attack_Probability_%"] if c in results.columns]
            preview = pd.concat([results[preview_cols], results.drop(columns=preview_cols)], axis=1) if preview_cols else results
            st.dataframe(preview.head(10), use_container_width=True, hide_index=True)

        elif page == "Traffic Analysis":
            st.markdown('<div class="section-head">📈 Traffic analysis</div>', unsafe_allow_html=True)
            st.caption("Explore predicted class balance and attack-probability distribution.")
            col_a, col_b = st.columns(2, gap="large")
            with col_a:
                counts = results["Prediction"].value_counts().reindex(["Benign", "Attack"], fill_value=0)
                fig = px.bar(
                    x=counts.index, y=counts.values, color=counts.index,
                    color_discrete_map={"Benign": "#62f6b0", "Attack": "#ff6b83"},
                    labels={"x": "Predicted class", "y": "Records"}, template="plotly_dark",
                )
                fig.update_layout(showlegend=False, height=360, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig, use_container_width=True)
            with col_b:
                valid_probs = pd.Series(attack_prob).dropna()
                if not valid_probs.empty:
                    fig = px.histogram(
                        x=valid_probs, nbins=24, labels={"x": "Attack probability (%)", "y": "Records"},
                        template="plotly_dark", color_discrete_sequence=["#4de2e8"],
                    )
                    fig.update_layout(height=360, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Probability scores are unavailable for this model.")
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.markdown("**Dataset summary**")
            summary = pd.DataFrame({
                "Metric": ["Total records", "Predicted benign", "Predicted attacks", "Predicted attack rate"],
                "Value": [f"{total:,}", f"{benign:,}", f"{attacks:,}", f"{attack_rate:.2f}%"],
            })
            st.dataframe(summary, hide_index=True, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        elif page == "Prediction Explorer":
            st.markdown('<div class="section-head">🧭 Prediction explorer</div>', unsafe_allow_html=True)
            f1, f2, f3 = st.columns([1, 1.25, 1.3])
            with f1:
                class_filter = st.selectbox("Predicted class", ["All", "Attack", "Benign"])
            with f2:
                search_text = st.text_input("Search column names", placeholder="e.g. Flow Duration")
            with f3:
                max_rows = st.selectbox("Rows to display", [100, 250, 500, 1000, 5000], index=2)

            filtered = results
            if class_filter != "All":
                filtered = filtered[filtered["Prediction"] == class_filter]
            if search_text.strip():
                matching_cols = [c for c in filtered.columns if search_text.lower() in str(c).lower()]
                if matching_cols:
                    show_cols = list(dict.fromkeys(matching_cols + ["Prediction", "Attack_Probability_%"]))
                    show_cols = [c for c in show_cols if c in filtered.columns]
                    filtered = filtered[show_cols]
                else:
                    st.info("No column names matched your search. Showing the standard prediction columns.")
                    show_cols = [c for c in ["Prediction", "Attack_Probability_%"] if c in filtered.columns]
                    filtered = filtered[show_cols + [c for c in results.columns if c not in show_cols][:8]]
            st.caption(f"Showing {min(len(filtered), max_rows):,} of {len(filtered):,} matching records.")
            st.dataframe(filtered.head(max_rows), use_container_width=True, hide_index=True)

            st.markdown('<div class="section-head">⬇️ Export findings</div>', unsafe_allow_html=True)
            csv_data = results.to_csv(index=False).encode("utf-8")
            st.download_button(
                "Download complete prediction report (CSV)",
                data=csv_data,
                file_name="intrusion_detection_report.csv",
                mime="text/csv",
                use_container_width=True,
            )
            st.caption("The exported file includes all uploaded columns plus Prediction and Attack_Probability_%.")

        else:
            st.markdown('<div class="section-head">ℹ️ About this project</div>', unsafe_allow_html=True)
            st.markdown(
                """
                <div class="panel">
                  <h3>Machine learning for network-flow classification</h3>
                  <p style="color:#a9c1d5;">
                    This educational prototype uses a trained Random Forest classifier to label
                    rows from an uploaded CSV as <b>Benign</b> or <b>Potential Attack</b>.
                  </p>
                  <hr>
                  <div class="mini-label">TECHNOLOGY STACK</div>
                  <p>Python · Pandas · NumPy · Scikit-learn · Joblib · Streamlit · Plotly</p>
                  <div class="mini-label">IMPORTANT LIMITATIONS</div>
                  <ul style="color:#a9c1d5;">
                    <li>Processes uploaded CSV files only; it does not capture live packets.</li>
                    <li>Does not block, quarantine, or remediate network activity.</li>
                    <li>Predictions are model outputs, not confirmed incidents or ground truth.</li>
                    <li>Performance depends on the training data, feature compatibility, and class distribution.</li>
                    <li>Attack probability is a model score and should not be treated as a calibrated real-world risk estimate.</li>
                  </ul>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.warning("Educational prototype only. Do not use as the sole basis for real-world security decisions.")

        st.markdown(
            '<div class="footer">SENTINEL · ML NETWORK INTRUSION DETECTION SYSTEM · EDUCATIONAL PROTOTYPE</div>',
            unsafe_allow_html=True,
        )

    except pd.errors.EmptyDataError:
        st.error("The uploaded file appears to be empty or is not a valid CSV.")
    except Exception as e:
        st.error(f"Could not process this CSV: {e}")
        st.caption("Check that the uploaded file contains the expected numeric features and is compatible with the training dataset.")
