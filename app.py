from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os

def get_secret(key):
    return os.getenv(key) or st.secrets.get(key)
import os
import time
from crew import research_crew


# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [data-testid="stAppViewContainer"], .main, .block-container {
    background-color: #f0f2f8 !important;
    font-family: 'Inter', sans-serif !important;
    color: #0f1120 !important;
}
.block-container { padding: 2.2rem 2.8rem !important; max-width: 100% !important; }
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
[data-testid="stToolbar"] { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }
[data-testid="stSidebarCollapseButton"] { display: none !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #0f1120 !important;
    border-right: none !important;
}
[data-testid="stSidebar"] > div:first-child { padding: 1.8rem 1.2rem !important; }

/* ── Text input ── */
[data-testid="stTextInput"] input {
    background-color: #ffffff !important;
    border: 2px solid #e2e5f0 !important;
    border-radius: 12px !important;
    color: #0f1120 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 16px !important;
    font-weight: 400 !important;
    height: 52px !important;
    padding: 12px 18px !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: #4f46e5 !important;
    box-shadow: 0 0 0 4px rgba(79,70,229,0.12) !important;
}
[data-testid="stTextInput"] input::placeholder { color: #a0a8c0 !important; }

/* ── Primary button ── */
[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    height: 52px !important;
    letter-spacing: 0.01em !important;
    transition: opacity 0.2s, transform 0.1s !important;
}
[data-testid="stButton"] > button[kind="primary"]:hover {
    opacity: 0.9 !important;
    transform: translateY(-1px) !important;
}
[data-testid="stButton"] > button[kind="primary"]:active {
    transform: translateY(0) scale(0.98) !important;
}
[data-testid="stButton"] > button[kind="primary"]:disabled {
    background: #c4c9e2 !important;
    cursor: not-allowed !important;
}

/* ── Tabs ── */
[data-testid="stTabs"] [role="tablist"] {
    background: #e8eaf5 !important;
    border-radius: 12px !important;
    padding: 5px !important;
    gap: 3px !important;
    border-bottom: none !important;
}
[data-testid="stTabs"] [role="tab"] {
    background: transparent !important;
    color: #7880a0 !important;
    border-radius: 9px !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    font-family: 'Inter', sans-serif !important;
    border: none !important;
    padding: 9px 20px !important;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    background: #ffffff !important;
    color: #4f46e5 !important;
    font-weight: 600 !important;
    box-shadow: 0 2px 8px rgba(79,70,229,0.15) !important;
}
[data-testid="stTabs"] [role="tabpanel"] { padding-top: 1.2rem !important; }

/* ── Progress ── */
[data-testid="stProgress"] > div > div {
    background-color: #dde0f0 !important;
    border-radius: 99px !important;
    height: 5px !important;
}

/* ── Metrics ── */
[data-testid="stMetric"] {
    background: #ffffff !important;
    border: 1.5px solid #e2e5f0 !important;
    border-radius: 14px !important;
    padding: 18px 16px !important;
    text-align: center !important;
}
[data-testid="stMetricLabel"] {
    font-size: 11px !important;
    color: #7880a0 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Syne', sans-serif !important;
    font-size: 26px !important;
    font-weight: 800 !important;
    color: #0f1120 !important;
}

/* ── Download button ── */
[data-testid="stDownloadButton"] > button {
    background: #f0f0ff !important;
    color: #4f46e5 !important;
    border: 1.5px solid #c7c4f6 !important;
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
    font-weight: 500 !important;
}
[data-testid="stDownloadButton"] > button:hover {
    background: #e0dfff !important;
}

.stAlert { border-radius: 12px !important; }
hr { border-color: #e2e5f0 !important; }
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #f0f2f8; }
::-webkit-scrollbar-thumb { background: #d0d4e8; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)


# ── Helpers ────────────────────────────────────────────────────────────────────

def check_api_keys():
    required = ['SERPER_API_KEY', 'GROQ_API_KEY']
    return [v for v in required if not os.getenv(v)]


def sb_label(text):
    st.markdown(
        f'<div style="font-size:10px;font-weight:600;letter-spacing:0.14em;'
        f'text-transform:uppercase;color:#4a5070;margin:0 0 10px;'
        f'font-family:\'Inter\',sans-serif;">{text}</div>',
        unsafe_allow_html=True,
    )


def sb_agent(dot_color, name, desc, active=False):
    bg  = "#1a1d35" if active else "transparent"
    bdr = "1px solid #2e3260" if active else "1px solid transparent"
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:10px;padding:10px 12px;
                border-radius:10px;background:{bg};border:{bdr};margin-bottom:3px;">
        <div style="width:8px;height:8px;border-radius:50%;background:{dot_color};
                    flex-shrink:0;box-shadow:0 0 6px {dot_color}88;"></div>
        <div>
            <div style="font-size:13px;font-weight:500;color:#e8eaf8;
                        font-family:'Inter',sans-serif;">{name}</div>
            <div style="font-size:11px;color:#4a5070;font-family:'Inter',sans-serif;
                        margin-top:1px;">{desc}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def step_row(num, label, done=True):
    n_bg  = "#eef9f4" if done else "#f3f4f8"
    n_col = "#059669" if done else "#9ca3af"
    l_col = "#065f46" if done else "#9ca3af"
    bdr   = "#a7f3d0" if done else "#e2e5f0"
    bg    = "#f0fdf8" if done else "#fafafa"
    check = """
    <svg width="20" height="20" viewBox="0 0 20 20" fill="none" style="flex-shrink:0;">
        <circle cx="10" cy="10" r="9" fill="#059669"/>
        <path d="M6 10l3 3 5-5" stroke="white" stroke-width="2"
              stroke-linecap="round" stroke-linejoin="round"/>
    </svg>""" if done else \
    '<div style="width:20px;height:20px;border-radius:50%;border:2px solid #dde0f0;flex-shrink:0;"></div>'

    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:14px;padding:14px 18px;
                border-radius:12px;border:1.5px solid {bdr};background:{bg};margin-bottom:8px;">
        <div style="width:28px;height:28px;border-radius:8px;background:{n_bg};flex-shrink:0;
                    display:flex;align-items:center;justify-content:center;font-size:12px;
                    font-weight:700;color:{n_col};font-family:'JetBrains Mono',monospace;">{num}</div>
        <span style="font-size:15px;color:{l_col};font-family:'Inter',sans-serif;
                     font-weight:500;flex:1;">{label}</span>
        {check}
    </div>
    """, unsafe_allow_html=True)


def live_step(label):
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:14px;padding:14px 18px;border-radius:12px;
                border:1.5px solid #c7c4f6;background:#f5f4ff;margin-bottom:8px;">
        <div style="width:10px;height:10px;border-radius:50%;background:#4f46e5;flex-shrink:0;
             animation:livepulse 1s ease-in-out infinite;"></div>
        <span style="font-size:15px;color:#3730a3;font-family:'Inter',sans-serif;font-weight:500;">
            {label}</span>
    </div>
    <style>@keyframes livepulse{{0%,100%{{opacity:1;transform:scale(1)}}
    50%{{opacity:.4;transform:scale(.7)}}}}</style>
    """, unsafe_allow_html=True)


def tag_pill(text):
    return (
        f'<span style="display:inline-block;background:#ede9fe;border:1.5px solid #c4b5fd;'
        f'border-radius:20px;padding:4px 12px;font-size:12px;color:#5b21b6;'
        f'margin-right:7px;margin-bottom:7px;font-family:\'JetBrains Mono\',monospace;'
        f'font-weight:500;">{text}</span>'
    )


def card(content_html, padding="24px 26px", border_color="#e2e5f0", bg="#ffffff"):
    st.markdown(
        f'<div style="background:{bg};border:1.5px solid {border_color};'
        f'border-radius:16px;padding:{padding};">{content_html}</div>',
        unsafe_allow_html=True,
    )


# ── Session state ──────────────────────────────────────────────────────────────
for k, v in dict(
    research_completed=False,
    research_result=None,
    research_error=None,
    run_time=0.0,
    topic_saved="",
).items():
    st.session_state.setdefault(k, v)

missing = check_api_keys()


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR  —  dark navy theme
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    # Logo block
    st.markdown("""
    <div style="padding-bottom:22px;border-bottom:1px solid #1e2240;margin-bottom:22px;">
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;">
            <div style="width:36px;height:36px;background:linear-gradient(135deg,#4f46e5,#7c3aed);
                        border-radius:10px;display:flex;align-items:center;justify-content:center;
                        flex-shrink:0;">
                <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
                    <circle cx="9" cy="9" r="6" stroke="white" stroke-width="1.8"/>
                    <path d="M9 5v4l3 2" stroke="white" stroke-width="1.8" stroke-linecap="round"/>
                </svg>
            </div>
            <div>
                <div style="font-family:'Syne',sans-serif;font-size:16px;font-weight:800;
                            color:#f0f2ff;letter-spacing:-0.3px;">ResearchAI</div>
                <div style="font-family:'JetBrains Mono',monospace;font-size:10px;
                            color:#3a4070;margin-top:1px;">powered by CrewAI</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # API status
    sb_label("Configuration")
    
    if missing:
        st.markdown("""
        <div style="background:#2a1a0a;border:1px solid #7c3a0a;border-radius:10px;
                    padding:10px 14px;display:flex;align-items:center;gap:8px;margin-bottom:10px;">
            <div style="width:8px;height:8px;border-radius:50%;background:#f59e0b;flex-shrink:0;"></div>
            <span style="font-size:12px;font-weight:600;color:#fbbf24;
                         font-family:'Inter',sans-serif;">Missing API keys</span>
        </div>
        """, unsafe_allow_html=True)
        for var in missing:
            st.code(f"{var}=your_key")
        st.info("Create a `.env` file with your API keys.")
    else:
        st.markdown("""
        <div style="background:#0a1f14;border:1px solid #166534;border-radius:10px;
                    padding:10px 14px;display:flex;align-items:center;gap:8px;margin-bottom:4px;">
            <div style="width:8px;height:8px;border-radius:50%;background:#22c55e;flex-shrink:0;
                        box-shadow:0 0 7px #22c55e99;"></div>
            <span style="font-size:12px;font-weight:600;color:#4ade80;
                         font-family:'Inter',sans-serif;">All systems active</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    sb_label("Agent Pipeline")

    sb_agent("#818cf8", "Research Specialist", "Searches & gathers data", active=True)
    sb_agent("#34d399", "Data Analyst",        "Structures & analyzes findings")
    sb_agent("#fb923c", "Content Writer",      "Writes the final report")

    st.markdown("""
    <div style="margin-top:28px;border-top:1px solid #1e2240;padding-top:18px;">
        <div style="background:#141728;border:1px solid #1e2240;border-radius:10px;
                    padding:10px 14px;">
            <div style="font-family:'JetBrains Mono',monospace;font-size:10px;color:#3a4070;
                        margin-bottom:6px;">runtime</div>
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <span style="font-family:'JetBrains Mono',monospace;font-size:11px;
                             color:#818cf8;">Groq / llama3</span>
                <span style="font-family:'JetBrains Mono',monospace;font-size:10px;
                             color:#3a4070;">llm</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# MAIN + RIGHT PANEL
# ══════════════════════════════════════════════════════════════════════════════
col_main, col_right = st.columns([5, 1.5])

with col_main:

    # ── Hero header ──────────────────────────────────────────────────────────
    hcol1, hcol2 = st.columns([3, 1])
    with hcol1:
        st.markdown("""
        <div style="margin-bottom:6px;">
            <h1 style="font-family:'Syne',sans-serif;font-size:34px;font-weight:800;
                       color:#0f1120;letter-spacing:-1px;margin:0;line-height:1.1;">
                AI Research
                <span style="background:linear-gradient(135deg,#4f46e5,#7c3aed);
                             -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                             background-clip:text;">Assistant</span>
            </h1>
            <p style="font-size:15px;color:#5a6080;margin:8px 0 0;font-weight:400;
                      font-family:'Inter',sans-serif;line-height:1.5;">
                Paste any topic and three AI agents will search the web, analyse the data,
                and hand you a polished research report — in seconds.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with hcol2:
        if st.session_state.research_completed and not st.session_state.research_error:
            st.markdown("""
            <div style="display:flex;align-items:center;gap:8px;
                        background:linear-gradient(135deg,#ecfdf5,#d1fae5);
                        border:1.5px solid #6ee7b7;border-radius:24px;
                        padding:9px 16px;width:fit-content;margin-top:10px;">
                <div style="width:8px;height:8px;border-radius:50%;background:#059669;
                            box-shadow:0 0 7px #059669aa;"></div>
                <span style="font-size:13px;font-weight:600;color:#065f46;
                             font-family:'Inter',sans-serif;">Research complete</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:22px'></div>", unsafe_allow_html=True)

    # ── Input card ───────────────────────────────────────────────────────────
    st.markdown("""
    <div style="background:#ffffff;border:1.5px solid #e2e5f0;border-radius:16px;
                padding:24px 26px 20px;">
        <div style="margin-bottom:6px;">
            <span style="font-family:'Syne',sans-serif;font-size:18px;font-weight:700;
                         color:#0f1120;">What do you want to research?</span>
        </div>
        <p style="font-size:13px;color:#7880a0;font-family:'Inter',sans-serif;
                  margin:0 0 16px;">
            Try a company, technology, market trend, scientific topic, or anything you're curious about.
        </p>
    """, unsafe_allow_html=True)

    ic1, ic2 = st.columns([5, 1])
    with ic1:
        topic = st.text_input(
            "",
            placeholder="e.g.  OpenAI o3 model capabilities, EV market in India 2025…",
            label_visibility="collapsed",
        )
    with ic2:
        start = st.button(
            "▶  Research",
            type="primary",
            disabled=bool(missing),
            use_container_width=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # ── Run research ─────────────────────────────────────────────────────────
    if start:
        if not topic.strip():
            st.error("Please enter a research topic first.")
        else:
            st.session_state.research_completed = False
            st.session_state.research_result    = None
            st.session_state.research_error     = None
            st.session_state.topic_saved        = topic.strip()

            st.markdown("""
            <div style="background:#ffffff;border:1.5px solid #e2e5f0;border-radius:16px;
                        padding:24px 26px;">
            <div style="display:flex;align-items:center;justify-content:space-between;
                        margin-bottom:16px;">
                <span style="font-family:'Syne',sans-serif;font-size:16px;font-weight:700;
                             color:#0f1120;">Running Agent Pipeline</span>
                <span style="font-family:'JetBrains Mono',monospace;font-size:12px;
                             color:#4f46e5;">in progress…</span>
            </div>
            """, unsafe_allow_html=True)

            prog     = st.progress(0)
            live_box = st.empty()
            t_start  = time.time()

            with live_box.container():
                live_step("Research Specialist is searching the web…")
            prog.progress(10)

            try:
                result = research_crew.kickoff({"topic": topic.strip()})
                prog.progress(80)
                with live_box.container():
                    live_step("Data Analyst is structuring findings…")
                time.sleep(0.4)
                prog.progress(93)
                with live_box.container():
                    live_step("Content Writer is polishing the report…")
                time.sleep(0.4)
                prog.progress(100)

                st.session_state.research_result    = result
                st.session_state.research_completed = True
                st.session_state.research_error     = None

            except Exception as e:
                st.session_state.research_error     = str(e)
                st.session_state.research_completed = True

            st.session_state.run_time = round(time.time() - t_start, 1)
            live_box.empty()
            st.markdown("</div>", unsafe_allow_html=True)
            st.rerun()

    # ── Post-run pipeline ─────────────────────────────────────────────────────
    if st.session_state.research_completed:
        pct_col = "#059669" if not st.session_state.research_error else "#ef4444"
        pct_txt = "100% complete" if not st.session_state.research_error else "Failed"

        st.markdown(f"""
        <div style="background:#ffffff;border:1.5px solid #e2e5f0;border-radius:16px;
                    padding:24px 26px;">
        <div style="display:flex;align-items:center;justify-content:space-between;
                    margin-bottom:18px;">
            <span style="font-family:'Syne',sans-serif;font-size:16px;font-weight:700;
                         color:#0f1120;">Agent Pipeline</span>
            <span style="font-family:'JetBrains Mono',monospace;font-size:13px;
                         font-weight:500;color:{pct_col};">{pct_txt}</span>
        </div>
        """, unsafe_allow_html=True)

        st.progress(1.0)
        st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

        if st.session_state.research_error:
            st.error(f"Pipeline error: {st.session_state.research_error}")
        else:
            step_row("01", "Research Specialist gathered data from the web")
            step_row("02", "Data Analyst structured and interpreted findings")
            step_row("03", "Content Writer produced the final report")

        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # ── Results ───────────────────────────────────────────────────────────────
    if st.session_state.research_completed and not st.session_state.research_error:

        output_files = {
            "research_findings.md": (
                "🔍  Raw Findings",
                ["web-scraped", "real-time", "multi-source"],
            ),
            "analysis_report.md": (
                "📊  Analysis",
                ["structured", "data-driven", "comparative"],
            ),
            "final_report.md": (
                "📝  Final Report",
                ["executive summary", "actionable", "AI-written"],
            ),
        }

        st.markdown(f"""
        <div style="background:#ffffff;border:1.5px solid #e2e5f0;border-radius:16px;
                    padding:24px 26px 8px;">
        <div style="margin-bottom:4px;">
            <span style="font-family:'Syne',sans-serif;font-size:18px;font-weight:700;
                         color:#0f1120;">Your Research Report</span>
        </div>
        <p style="font-size:13px;color:#7880a0;font-family:'Inter',sans-serif;
                  margin:4px 0 16px;">
            Topic: <strong style="color:#4f46e5;">{st.session_state.topic_saved}</strong>
        </p>
        """, unsafe_allow_html=True)

        tabs = st.tabs([v[0] for v in output_files.values()])

        for i, (filename, (title, pills)) in enumerate(output_files.items()):
            with tabs[i]:
                label = title.split(None, 1)[1]
                st.markdown(f"""
                <div style="font-family:'Syne',sans-serif;font-size:20px;font-weight:700;
                            color:#0f1120;margin-bottom:4px;">{label}</div>
                <p style="font-size:13px;color:#7880a0;font-family:'Inter',sans-serif;
                           margin:0 0 14px;">
                    {st.session_state.topic_saved}
                </p>
                """, unsafe_allow_html=True)

                if os.path.exists(filename):
                    with open(filename, "r", encoding="utf-8") as f:
                        content = f.read()
                    st.markdown(content)
                    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
                    st.markdown("".join(tag_pill(p) for p in pills), unsafe_allow_html=True)
                    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
                    st.download_button(
                        label=f"⬇  Download {label}",
                        data=content,
                        file_name=filename,
                        mime="text/markdown",
                        key=f"dl_{filename}",
                    )
                else:
                    st.warning(f"`{filename}` not found. The agent may not have written it yet.")

        st.markdown("</div>", unsafe_allow_html=True)

        # ── Stats ──
        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
        m1, m2, m3 = st.columns(3)
        m1.metric("⏱  Run Time",    f"{st.session_state.run_time}s")
        m2.metric("🤖  Agents Used", 3)
        m3.metric("📄  Reports",     len(output_files))

    # Footer
    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
    st.markdown("""
    <hr style="border-color:#e2e5f0;margin-bottom:10px;">
    <p style="font-family:'JetBrains Mono',monospace;font-size:11px;color:#b0b8d0;
              text-align:center;">
        Built with CrewAI · Streamlit · Groq · Serper
    </p>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# RIGHT PANEL
# ══════════════════════════════════════════════════════════════════════════════
with col_right:
    st.markdown("<div style='height:72px'></div>", unsafe_allow_html=True)

    # Run status
    done = st.session_state.research_completed
    err  = st.session_state.research_error

    if done and err:
        s_text = "Failed"
        s_dot  = "#ef4444"; s_col = "#991b1b"
        s_bg   = "#fff5f5"; s_bdr = "#fecaca"
    elif done:
        s_text = "Completed"
        s_dot  = "#059669"; s_col = "#065f46"
        s_bg   = "linear-gradient(135deg,#ecfdf5,#d1fae5)"; s_bdr = "#6ee7b7"
    else:
        s_text = "Waiting…"
        s_dot  = "#a0a8c0"; s_col = "#5a6080"
        s_bg   = "#f8f9fc"; s_bdr = "#e2e5f0"

    st.markdown(f"""
    <div style="background:#ffffff;border:1.5px solid #e2e5f0;border-radius:16px;
                padding:18px;margin-bottom:14px;">
        <div style="font-size:10px;font-weight:700;letter-spacing:0.12em;
                    text-transform:uppercase;color:#a0a8c0;margin-bottom:12px;
                    font-family:'Inter',sans-serif;">Run Status</div>
        <div style="display:flex;align-items:center;gap:8px;background:{s_bg};
                    border:1.5px solid {s_bdr};border-radius:10px;padding:10px 12px;">
            <div style="width:8px;height:8px;border-radius:50%;background:{s_dot};
                        flex-shrink:0;box-shadow:0 0 6px {s_dot}88;"></div>
            <span style="font-size:13px;font-weight:600;color:{s_col};
                         font-family:'Inter',sans-serif;">{s_text}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Session info
    api_ok  = not missing
    api_col = "#059669" if api_ok else "#ef4444"
    api_val = "Active"  if api_ok else "Missing"

    st.markdown(f"""
    <div style="background:#ffffff;border:1.5px solid #e2e5f0;border-radius:16px;padding:18px;">
        <div style="font-size:10px;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;
                    color:#a0a8c0;margin-bottom:14px;font-family:'Inter',sans-serif;">
            Session Info
        </div>
        <div style="display:flex;flex-direction:column;gap:13px;">
            <div>
                <div style="font-size:11px;color:#a0a8c0;font-family:'Inter',sans-serif;
                            font-weight:600;text-transform:uppercase;letter-spacing:0.08em;">
                    Framework</div>
                <div style="font-size:14px;font-weight:600;color:#0f1120;
                            font-family:'JetBrains Mono',monospace;margin-top:3px;">CrewAI</div>
            </div>
            <div>
                <div style="font-size:11px;color:#a0a8c0;font-family:'Inter',sans-serif;
                            font-weight:600;text-transform:uppercase;letter-spacing:0.08em;">
                    LLM</div>
                <div style="font-size:14px;font-weight:600;color:#0f1120;
                            font-family:'JetBrains Mono',monospace;margin-top:3px;">
                    Groq / llama3</div>
            </div>
            <div>
                <div style="font-size:11px;color:#a0a8c0;font-family:'Inter',sans-serif;
                            font-weight:600;text-transform:uppercase;letter-spacing:0.08em;">
                    API Keys</div>
                <div style="font-size:14px;font-weight:600;
                            font-family:'JetBrains Mono',monospace;margin-top:3px;
                            color:{api_col};">{api_val}</div>
            </div>
            <div>
                <div style="font-size:11px;color:#a0a8c0;font-family:'Inter',sans-serif;
                            font-weight:600;text-transform:uppercase;letter-spacing:0.08em;">
                    Run Time</div>
                <div style="font-size:14px;font-weight:600;color:#0f1120;
                            font-family:'JetBrains Mono',monospace;margin-top:3px;">
                    {st.session_state.run_time}s</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
