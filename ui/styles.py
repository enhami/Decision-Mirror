import streamlit as st

def apply_styles():
    st.markdown(
        """
        <style>
        /* Main application background */
        .stApp {
            background: linear-gradient(
                135deg,
                #0b1120 0%,
                #111827 55%,
                #17152e 100%
            );
            color: #f8fafc;
        }

        /* Make top header bar match dark theme */
        [data-testid="stHeader"] {
            background: rgba(11, 17, 32, 0.85) !important;
            backdrop-filter: blur(8px);
        }

        /* Main content spacing */
        .block-container {
            max-width: 1150px;
            padding-top: 2rem;
            padding-bottom: 3.5rem;
        }

        /* Headings */
        h1, h2, h3, h4 {
            color: #f8fafc !important;
            font-weight: 700 !important;
        }

        /* Normal text */
        p, label, .stMarkdown, span {
            color: #cbd5e1;
        }

        /* Metric cards */
        [data-testid="stMetric"] {
            background: rgba(30, 41, 59, 0.85);
            border: 1px solid #334155;
            padding: 18px;
            border-radius: 14px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
        }

        [data-testid="stMetricLabel"] p {
            color: #94a3b8 !important;
            font-weight: 600 !important;
        }

        [data-testid="stMetricValue"] {
            color: #a5b4fc !important;
        }

        /* Buttons */
        .stButton > button {
            background: linear-gradient(90deg, #6366f1, #8b5cf6);
            color: #ffffff !important;
            border: none;
            border-radius: 10px;
            padding: 0.6rem 1.3rem;
            font-weight: 600;
            transition: 0.2s ease;
        }

        .stButton > button:hover {
            background: linear-gradient(90deg, #4f46e5, #7c3aed);
            color: #ffffff !important;
            transform: translateY(-1px);
            box-shadow: 0 6px 16px rgba(99, 102, 241, 0.35);
        }

        /* File uploader outer & inner dropzone */
        [data-testid="stFileUploader"] {
            background: rgba(30, 41, 59, 0.65);
            border: 1px dashed #6366f1;
            border-radius: 14px;
            padding: 15px;
        }

        [data-testid="stFileUploaderDropzone"] {
            background-color: rgba(15, 23, 42, 0.7) !important;
            color: #e2e8f0 !important;
        }

        /* Data tables */
        [data-testid="stDataFrame"] {
            border: 1px solid #334155;
            border-radius: 12px;
            overflow: hidden;
        }

        /* Dividers */
        hr {
            border-color: #334155 !important;
            margin: 2rem 0 !important;
        }

        /* Select boxes and dropdown menus */
        [data-baseweb="select"] > div {
            background-color: #1e293b !important;
            border-color: #475569 !important;
            color: #f8fafc !important;
            border-radius: 10px !important;
        }

        [data-baseweb="popover"] ul {
            background-color: #1e293b !important;
            color: #f8fafc !important;
        }

        /* Hero section */
        .hero-card {
            background: linear-gradient(120deg, #1e1b4b, #312e81, #4338ca);
            border: 1px solid #6366f1;
            border-radius: 18px;
            padding: 32px;
            margin-bottom: 24px;
            box-shadow: 0 10px 25px rgba(30, 27, 75, 0.5);
        }

        .hero-tag {
            color: #c4b5fd;
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 2px;
            text-transform: uppercase;
        }

        .hero-title {
            color: #ffffff;
            font-size: 38px;
            font-weight: 800;
            margin: 10px 0;
        }

        .hero-description {
            color: #e0e7ff;
            font-size: 16px;
            max-width: 780px;
            line-height: 1.6;
        }

        /* Section cards */
        .section-card {
            background: rgba(30, 41, 59, 0.75);
            border: 1px solid #334155;
            border-radius: 16px;
            padding: 22px 24px;
            margin: 14px 0 20px 0;
        }

        .section-label {
            color: #a5b4fc;
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            margin-bottom: 6px;
        }

        .section-title {
            color: #f8fafc;
            font-size: 22px;
            font-weight: 700;
            margin-bottom: 6px;
        }

        .section-description {
            color: #94a3b8;
            font-size: 14px;
            line-height: 1.6;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

