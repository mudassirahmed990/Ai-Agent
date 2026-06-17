import streamlit as st

def render_metric_card(title: str, value: str, delta: str = None):
    delta_html = f"<p style='margin:6px 0 0 0; color:#10b981; font-size:0.78rem; font-weight:500;'>{delta}</p>" if delta else ""
    st.markdown(f"""
    <div class="metric-card">
        <h4>{title}</h4>
        <h2>{value}</h2>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)

def render_report_card(report):
    priority = report.get('priority') or 'Unknown'
    category = report.get('category') or 'Uncategorized'
    status   = report.get('status') or 'Pending'
    desc     = report.get('description') or ''
    ts       = report.get('timestamp') or ''
    loc      = report.get('location') or ''

    p_word = priority.split()[0].lower() if priority else 'medium'
    s_word = status.lower()

    desc_short = (desc[:120] + '…') if len(desc) > 120 else desc

    # Category icon map
    icons = {
        "Robbery": "🔫", "Theft": "💰", "Mobile Snatching": "📱",
        "Car Theft": "🚗", "Motorcycle Theft": "🏍️", "Assault": "👊",
        "Kidnapping": "🚨", "Harassment": "⚠️", "Drug Activity": "💊",
        "Vandalism": "🔨", "Accident": "💥", "Other": "📋"
    }
    icon = icons.get(category, "📋")

    st.markdown(f"""
    <div class="glass-card">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
            <div style="display:flex; align-items:center; gap:10px;">
                <span style="font-size:1.4rem;">{icon}</span>
                <span style="font-family:'Syne',sans-serif; font-weight:700; font-size:1rem;
                             background:linear-gradient(135deg,#a78bfa,#06b6d4);
                             -webkit-background-clip:text; -webkit-text-fill-color:transparent;">
                    {category}
                </span>
            </div>
            <div style="display:flex; gap:8px;">
                <span class="badge badge-{p_word}">{priority}</span>
            </div>
        </div>
        <p style="color:#c4c9e8; font-size:0.88rem; margin:0 0 12px 0; line-height:1.6;">{desc_short}</p>
        <div style="display:flex; gap:20px; flex-wrap:wrap;">
            {"<span style='color:#4a5080; font-size:0.75rem;'>📍 " + loc + "</span>" if loc else ""}
            <span style="color:#4a5080; font-size:0.75rem;">🕐 {ts}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
