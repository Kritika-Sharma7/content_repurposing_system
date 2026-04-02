"""
Multi-Agent Content Repurposing System
Production-quality Streamlit application

A professional multi-agent system that transforms long-form content into
optimized LinkedIn posts, Twitter threads, and newsletters using AI agents
with built-in feedback loops and quality refinement.
"""

import sys
import os
import time
import json
import base64
import html
import difflib
from pathlib import Path
from datetime import datetime
from typing import Optional

sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# =============================================================================
# CONFIGURATION
# =============================================================================

def get_api_key() -> Optional[str]:
    """Get API key from environment or session state."""
    # First check environment variable
    env_key = os.getenv("OPENAI_API_KEY")
    if env_key and not env_key.startswith("sk-your"):
        return env_key
    
    # Then check session state (user input)
    if "api_key" in st.session_state and st.session_state.api_key:
        return st.session_state.api_key
    
    return None

# =============================================================================
# PAGE CONFIG
# =============================================================================

st.set_page_config(
    page_title="ContentForge AI | Multi-Agent Content System",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com',
        'Report a bug': 'https://github.com',
        'About': "# ContentForge AI\nA multi-agent content repurposing system."
    }
)

# =============================================================================
# PROFESSIONAL STYLES - PRODUCTION QUALITY
# =============================================================================

st.markdown("""
<style>
    /* === BASE LAYOUT === */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

    :root {
        --primary: #111827;
        --primary-dark: #0b1220;
        --primary-light: #1f2937;
        --secondary: #2563eb;
        --success: #10b981;
        --warning: #f59e0b;
        --danger: #ef4444;
        --dark: #0f172a;
        --dark-secondary: #1e293b;
        --gray-50: #f8fafc;
        --gray-100: #f1f5f9;
        --gray-200: #e2e8f0;
        --gray-300: #cbd5e1;
        --gray-400: #94a3b8;
        --gray-500: #64748b;
        --gray-600: #475569;
        --gray-700: #334155;
        --gray-800: #1e293b;
        --gray-900: #0f172a;
        --gradient-primary: linear-gradient(135deg, #111827 0%, #1f2937 100%);
        --gradient-dark: linear-gradient(135deg, #111827 0%, #0f172a 100%);
        --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
        --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
        --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
        --shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
    }

    .stApp {
        background: #ffffff;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }

    .block-container {
        max-width: 1200px;
        padding: 1rem 2rem 4rem;
    }

    .top-nav {
        position: sticky;
        top: 0;
        z-index: 99;
        background: #ffffff;
        border-bottom: 1px solid #e5e7eb;
        padding: 0.75rem 0;
        margin: -1rem -2rem 1.25rem;
    }

    .top-nav-inner {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .brand-wrap {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        font-weight: 800;
        color: #111827;
        letter-spacing: -0.02em;
    }

    .brand-dot {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: #2563eb;
        box-shadow: 0 0 0 6px rgba(37, 99, 235, 0.12);
    }

    .nav-cta {
        background: #111827;
        color: white;
        border-radius: 12px;
        padding: 0.45rem 0.85rem;
        font-size: 0.8rem;
        font-weight: 700;
    }

    /* === ANIMATED HERO SECTION === */
    .hero-section {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 24px;
        padding: 2.6rem 2.2rem;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
        box-shadow: var(--shadow-sm);
    }

    .hero-section::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(37, 99, 235, 0.06) 0%, transparent 60%);
        animation: rotate 20s linear infinite;
    }

    .hero-section::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        opacity: 0;
    }

    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }

    .hero-content {
        position: relative;
        z-index: 1;
    }

    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(37, 99, 235, 0.12);
        backdrop-filter: blur(8px);
        color: #1e40af;
        padding: 0.5rem 1rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 1.25rem;
        border: 1px solid rgba(37, 99, 235, 0.2);
        animation: fadeInDown 0.6s ease-out 0.1s both;
    }

    .hero-badge::before {
        content: '';
        width: 8px;
        height: 8px;
        background: #2563eb;
        border-radius: 50%;
        animation: pulse-dot 2s infinite;
        box-shadow: 0 0 12px var(--primary-light);
    }

    .hero-title {
        font-size: 3rem;
        font-weight: 900;
        color: #111827;
        line-height: 1.1;
        margin-bottom: 1rem;
        letter-spacing: -0.03em;
        animation: fadeInUp 0.6s ease-out 0.2s both;
        background: none;
    }

    .hero-subtitle {
        font-size: 1.125rem;
        color: var(--gray-600);
        max-width: 640px;
        line-height: 1.7;
        animation: fadeInUp 0.6s ease-out 0.3s both;
    }

    .hero-stats {
        display: flex;
        gap: 3rem;
        margin-top: 2.5rem;
        animation: fadeInUp 0.6s ease-out 0.4s both;
    }

    .hero-stat {
        text-align: left;
        padding: 1rem 1.5rem;
        background: #f9fafb;
        border-radius: 16px;
        border: 1px solid #e5e7eb;
        backdrop-filter: blur(8px);
        transition: all 0.3s ease;
    }

    .hero-stat:hover {
        background: #ffffff;
        transform: translateY(-4px);
        box-shadow: var(--shadow-md);
    }

    .hero-stat-value {
        font-size: 2rem;
        font-weight: 800;
        color: #111827;
    }

    .hero-stat-label {
        font-size: 0.8125rem;
        color: var(--gray-600);
        margin-top: 0.25rem;
    }

    /* === ANIMATIONS === */
    @keyframes pulse-dot {
        0%, 100% { opacity: 1; transform: scale(1); box-shadow: 0 0 12px var(--primary-light); }
        50% { opacity: 0.6; transform: scale(1.3); box-shadow: 0 0 20px var(--primary-light); }
    }

    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-30px); }
        to { opacity: 1; transform: translateX(0); }
    }

    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(30px); }
        to { opacity: 1; transform: translateX(0); }
    }

    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }

    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
        40% { transform: translateY(6px); }
        60% { transform: translateY(3px); }
    }

    @keyframes spin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }

    /* === TYPOGRAPHY === */
    h1 {
        font-size: 1.875rem !important;
        font-weight: 800 !important;
        color: var(--dark) !important;
        letter-spacing: -0.03em;
        margin-bottom: 0.5rem !important;
    }

    h2 {
        font-size: 1.25rem !important;
        font-weight: 700 !important;
        color: var(--dark-secondary) !important;
        margin-top: 2rem !important;
        margin-bottom: 1rem !important;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    h3 {
        font-size: 1rem !important;
        font-weight: 600 !important;
        color: var(--gray-700) !important;
        margin-bottom: 0.75rem !important;
    }

    p, li, .stMarkdown {
        color: var(--gray-600);
        font-size: 0.9375rem;
        line-height: 1.7;
    }

    /* === SIDEBAR === */
    [data-testid="stSidebar"] {
        background: white;
        border-right: 1px solid var(--gray-200);
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: 2rem;
    }

    .sidebar-logo {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 0 1rem 1.5rem;
        border-bottom: 1px solid var(--gray-100);
        margin-bottom: 1rem;
    }

    .sidebar-logo-icon {
        width: 44px;
        height: 44px;
        background: var(--gradient-primary);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        box-shadow: var(--shadow-md);
    }

    .sidebar-logo-text {
        font-weight: 800;
        font-size: 1.25rem;
        color: var(--dark);
        letter-spacing: -0.02em;
    }

    .sidebar-logo-sub {
        font-size: 0.6875rem;
        color: var(--gray-500);
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* === PIPELINE TRACKER === */
    .pipeline-tracker {
        background: white;
        border: 1px solid var(--gray-200);
        border-radius: 16px;
        padding: 1.5rem 2rem;
        margin: 1rem 0 2rem;
        box-shadow: var(--shadow-sm);
    }

    .pipeline-steps {
        display: flex;
        align-items: center;
        justify-content: space-between;
        position: relative;
    }

    .pipeline-step {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.625rem;
        z-index: 1;
        flex: 1;
    }

    .step-circle {
        width: 48px;
        height: 48px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 1rem;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
    }

    .step-circle.pending {
        background: var(--gray-100);
        color: var(--gray-400);
        border: 2px solid var(--gray-200);
    }

    .step-circle.active {
        background: var(--gradient-primary);
        color: white;
        border: none;
        box-shadow: 0 0 0 6px rgba(99, 102, 241, 0.2), var(--shadow-lg);
        animation: pulse-active 2s infinite;
    }

    .step-circle.active::after {
        content: '';
        position: absolute;
        width: 100%;
        height: 100%;
        border-radius: 50%;
        background: var(--gradient-primary);
        animation: ping 1.5s cubic-bezier(0, 0, 0.2, 1) infinite;
        z-index: -1;
    }

    @keyframes pulse-active {
        0%, 100% { box-shadow: 0 0 0 6px rgba(99, 102, 241, 0.2), var(--shadow-lg); }
        50% { box-shadow: 0 0 0 10px rgba(99, 102, 241, 0.1), var(--shadow-lg); }
    }

    @keyframes ping {
        75%, 100% { transform: scale(1.5); opacity: 0; }
    }

    .step-circle.complete {
        background: linear-gradient(135deg, var(--success) 0%, #059669 100%);
        color: white;
        border: none;
        box-shadow: var(--shadow-md);
    }

    .step-label {
        font-size: 0.8125rem;
        font-weight: 600;
        color: var(--gray-500);
        text-align: center;
    }

    .step-label.active {
        color: var(--primary);
    }

    .step-label.complete {
        color: var(--success);
    }

    .pipeline-line {
        position: absolute;
        top: 24px;
        left: 12%;
        right: 12%;
        height: 3px;
        background: var(--gray-200);
        z-index: 0;
        border-radius: 2px;
    }

    .pipeline-line-progress {
        height: 100%;
        background: var(--gradient-primary);
        border-radius: 2px;
        transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    }

    /* === CARDS === */
    .card {
        background: white;
        border: 1px solid var(--gray-200);
        border-radius: 20px;
        padding: 1.75rem;
        margin-bottom: 1.25rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: var(--shadow-sm);
        animation: fadeInUp 0.5s ease-out both;
    }

    .card:hover {
        border-color: var(--gray-300);
        box-shadow: var(--shadow-lg);
        transform: translateY(-4px);
    }

    .card-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 1.25rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid var(--gray-100);
    }

    .card-title {
        font-size: 1rem;
        font-weight: 700;
        color: var(--dark);
        display: flex;
        align-items: center;
        gap: 0.625rem;
    }

    .card-badge {
        font-size: 0.6875rem;
        font-weight: 700;
        padding: 0.375rem 0.75rem;
        border-radius: 9999px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .badge-primary { background: #eef2ff; color: var(--primary); }
    .badge-success { background: #f0fdf4; color: var(--success); }
    .badge-warning { background: #fffbeb; color: var(--warning); }
    .badge-gray { background: var(--gray-100); color: var(--gray-600); }

    /* === AGENT CARDS === */
    .agent-card {
        background: white;
        border: 1px solid var(--gray-200);
        border-radius: 20px;
        padding: 1.75rem;
        margin-bottom: 1rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: var(--shadow-sm);
        animation: fadeInUp 0.5s ease-out both;
        position: relative;
        overflow: hidden;
    }

    .agent-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: var(--gradient-primary);
        opacity: 0;
        transition: opacity 0.3s ease;
    }

    .agent-card:hover::before {
        opacity: 1;
    }

    .agent-card:hover {
        border-color: var(--primary-light);
        box-shadow: var(--shadow-xl);
        transform: translateY(-6px);
    }

    .agent-header {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1rem;
    }

    .agent-icon {
        width: 52px;
        height: 52px;
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        box-shadow: var(--shadow-md);
    }

    .agent-icon.summarizer { background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); }
    .agent-icon.formatter { background: linear-gradient(135deg, #f3e8ff 0%, #e9d5ff 100%); }
    .agent-icon.reviewer { background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); }
    .agent-icon.refiner { background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%); }

    .agent-name {
        font-weight: 700;
        font-size: 1.0625rem;
        color: var(--dark);
    }

    .agent-role {
        font-size: 0.8125rem;
        color: var(--gray-500);
    }

    .agent-details {
        background: var(--gray-50);
        border-radius: 12px;
        padding: 1.25rem;
        margin-top: 1rem;
        border: 1px solid var(--gray-100);
    }

    /* === INSIGHT CARDS === */
    .insight-item {
        display: flex;
        gap: 1rem;
        padding: 1rem 1.25rem;
        background: var(--gray-50);
        border-radius: 12px;
        margin-bottom: 0.625rem;
        border-left: 4px solid var(--gray-300);
        transition: all 0.2s ease;
    }

    .insight-item:hover {
        background: white;
        box-shadow: var(--shadow-md);
        transform: translateX(4px);
    }

    .insight-item.high { border-left-color: var(--primary); }
    .insight-item.medium { border-left-color: var(--warning); }
    .insight-item.low { border-left-color: var(--gray-400); }

    .insight-topic {
        font-weight: 700;
        font-size: 0.9375rem;
        color: var(--dark);
        margin-bottom: 0.375rem;
    }

    .insight-text {
        font-size: 0.8125rem;
        color: var(--gray-600);
        line-height: 1.6;
    }

    .insight-tag {
        font-size: 0.625rem;
        font-weight: 700;
        padding: 0.25rem 0.625rem;
        border-radius: 6px;
        text-transform: uppercase;
        margin-left: 0.5rem;
    }

    .tag-high { background: #dbeafe; color: #1d4ed8; }
    .tag-medium { background: #fef3c7; color: #b45309; }
    .tag-low { background: var(--gray-200); color: var(--gray-600); }

    /* === CONTENT DISPLAY === */
    .content-section {
        background: var(--gray-50);
        border-radius: 12px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        border: 1px solid var(--gray-100);
        position: relative;
    }

    .content-label {
        font-size: 0.6875rem;
        font-weight: 700;
        color: var(--gray-500);
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.625rem;
    }

    .content-text {
        font-size: 0.9375rem;
        color: var(--gray-700);
        line-height: 1.8;
        white-space: pre-wrap;
    }

    .copy-btn {
        position: absolute;
        top: 0.75rem;
        right: 0.75rem;
        background: white;
        border: 1px solid var(--gray-200);
        border-radius: 8px;
        padding: 0.5rem;
        cursor: pointer;
        opacity: 0;
        transition: all 0.2s ease;
        color: var(--gray-500);
    }

    .content-section:hover .copy-btn {
        opacity: 1;
    }

    .copy-btn:hover {
        background: var(--gray-100);
        color: var(--primary);
    }

    /* === TWEET DISPLAY === */
    .tweet-container {
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
    }

    .tweet-item {
        background: white;
        border: 1px solid var(--gray-200);
        border-radius: 16px;
        padding: 1rem 1.25rem;
        position: relative;
        transition: all 0.2s ease;
    }

    .tweet-item:hover {
        border-color: var(--secondary);
        box-shadow: var(--shadow-md);
    }

    .tweet-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 0.625rem;
    }

    .tweet-number {
        font-weight: 800;
        font-size: 0.75rem;
        color: var(--secondary);
        background: #e0f2fe;
        padding: 0.25rem 0.625rem;
        border-radius: 6px;
    }

    .tweet-chars {
        font-size: 0.6875rem;
        font-weight: 600;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
    }

    .tweet-chars.ok { color: var(--success); background: #f0fdf4; }
    .tweet-chars.over { color: var(--danger); background: #fef2f2; }

    .tweet-text {
        font-size: 0.9375rem;
        color: var(--gray-700);
        line-height: 1.6;
    }

    /* === METRICS === */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1.25rem;
        margin-bottom: 2rem;
    }

    .metric-card {
        background: white;
        border: 1px solid var(--gray-200);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: var(--shadow-sm);
    }

    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-lg);
    }

    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: var(--dark);
        line-height: 1;
        margin-bottom: 0.5rem;
    }

    .metric-value.good { color: var(--success); }
    .metric-value.medium { color: var(--warning); }
    .metric-value.low { color: var(--danger); }

    .metric-label {
        font-size: 0.8125rem;
        font-weight: 600;
        color: var(--gray-500);
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* === STATUS ITEMS === */
    .status-item {
        display: flex;
        align-items: flex-start;
        gap: 0.875rem;
        padding: 1rem 1.25rem;
        border-radius: 12px;
        margin-bottom: 0.625rem;
        font-size: 0.9375rem;
        transition: all 0.2s ease;
    }

    .status-item:hover {
        transform: translateX(4px);
    }

    .status-item.critical {
        background: #fef2f2;
        border-left: 4px solid var(--danger);
        color: #991b1b;
    }

    .status-item.warning {
        background: #fffbeb;
        border-left: 4px solid var(--warning);
        color: #92400e;
    }

    .status-item.success {
        background: #f0fdf4;
        border-left: 4px solid var(--success);
        color: #166534;
    }

    .status-icon {
        width: 20px;
        height: 20px;
        flex-shrink: 0;
        margin-top: 2px;
    }

    /* === COMPARISON === */
    .compare-container {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1.5rem;
    }

    .compare-panel {
        border-radius: 16px;
        padding: 1.5rem;
        transition: all 0.3s ease;
    }

    .compare-panel:hover {
        transform: scale(1.02);
    }

    .compare-panel.v1 {
        background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
        border: 2px solid #fde68a;
    }

    .compare-panel.v2 {
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        border: 2px solid #86efac;
    }

    .compare-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1.25rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid rgba(0,0,0,0.08);
    }

    .compare-badge {
        font-size: 0.75rem;
        font-weight: 800;
        padding: 0.375rem 0.875rem;
        border-radius: 9999px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .compare-badge.v1 { background: #fde68a; color: #92400e; }
    .compare-badge.v2 { background: #86efac; color: #166534; }

    /* === TABS === */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: var(--gray-100);
        padding: 6px;
        border-radius: 14px;
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 10px;
        padding: 0.625rem 1.5rem;
        font-size: 0.9375rem;
        font-weight: 600;
        color: var(--gray-500);
    }

    .stTabs [aria-selected="true"] {
        background: white;
        color: var(--dark);
        box-shadow: var(--shadow-sm);
    }

    /* === BUTTONS === */
    .stButton > button {
        background: var(--gradient-primary);
        color: white;
        border: none;
        padding: 0.875rem 2.5rem;
        font-weight: 700;
        font-size: 1rem;
        border-radius: 14px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 14px rgba(99, 102, 241, 0.4);
        letter-spacing: -0.01em;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(99, 102, 241, 0.5);
    }

    .stButton > button:active {
        transform: translateY(0);
    }

    /* === INPUTS === */
    .stTextInput input, .stTextArea textarea {
        border: 2px solid var(--gray-200);
        border-radius: 14px;
        font-size: 1rem;
        padding: 0.875rem 1.25rem;
        transition: all 0.2s ease;
    }

    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: var(--primary);
        box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.1);
    }

    /* === LOADING STATES === */
    .loading-skeleton {
        background: linear-gradient(90deg, var(--gray-200) 25%, var(--gray-100) 50%, var(--gray-200) 75%);
        background-size: 200% 100%;
        animation: shimmer 1.5s infinite;
        border-radius: 8px;
    }

    .loading-spinner {
        width: 48px;
        height: 48px;
        border: 4px solid var(--gray-200);
        border-top-color: var(--primary);
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }

    /* === EXPORT BUTTONS === */
    .export-btn-group {
        display: flex;
        gap: 0.5rem;
        flex-wrap: wrap;
        margin-top: 1rem;
    }

    .export-btn {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: white;
        color: var(--gray-600);
        padding: 0.5rem 1rem;
        border-radius: 10px;
        font-size: 0.8125rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s ease;
        border: 1px solid var(--gray-200);
    }

    .export-btn:hover {
        background: var(--primary);
        color: white;
        border-color: var(--primary);
    }

    /* === FLOWCHART === */
    .flowchart-container {
        background: linear-gradient(135deg, white 0%, var(--gray-50) 100%);
        border: 1px solid var(--gray-200);
        border-radius: 20px;
        padding: 2.5rem;
        margin: 2rem 0;
        overflow: hidden;
        box-shadow: var(--shadow-sm);
    }

    .flowchart-title {
        font-size: 0.8125rem;
        font-weight: 700;
        color: var(--gray-500);
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 2rem;
        text-align: center;
    }

    .flow-row {
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0.75rem 0;
    }

    .flow-node {
        padding: 1.25rem 2rem;
        border-radius: 14px;
        font-weight: 700;
        font-size: 0.9375rem;
        text-align: center;
        min-width: 160px;
        transition: all 0.3s ease;
        animation: fadeInUp 0.6s ease-out both;
        box-shadow: var(--shadow-md);
    }

    .flow-node:hover {
        transform: translateY(-6px);
        box-shadow: var(--shadow-xl);
    }

    .flow-node.input { background: linear-gradient(135deg, var(--gray-100) 0%, var(--gray-200) 100%); border: 2px solid var(--gray-300); }
    .flow-node.summarizer { background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); border: 2px solid #93c5fd; color: #1e40af; }
    .flow-node.formatter { background: linear-gradient(135deg, #f3e8ff 0%, #e9d5ff 100%); border: 2px solid #c4b5fd; color: #6b21a8; }
    .flow-node.reviewer { background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); border: 2px solid #fcd34d; color: #92400e; }
    .flow-node.refiner { background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%); border: 2px solid #6ee7b7; color: #065f46; }
    .flow-node.output { background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%); border: 2px solid #86efac; color: #166534; }

    .flow-arrow {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 0.75rem 0;
        color: var(--gray-400);
    }

    .flow-arrow svg {
        width: 28px;
        height: 28px;
        animation: bounce 2.5s infinite;
    }

    .flow-arrow-label {
        font-size: 0.6875rem;
        color: var(--gray-400);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 0.375rem;
        font-weight: 600;
    }

    /* === API KEY INPUT === */
    .api-key-section {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border: 2px solid #fcd34d;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
    }

    .api-key-title {
        font-weight: 700;
        color: #92400e;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .api-key-text {
        font-size: 0.875rem;
        color: #78350f;
        margin-bottom: 1rem;
    }

    /* === SUCCESS TOAST === */
    .success-toast {
        position: fixed;
        bottom: 2rem;
        right: 2rem;
        background: var(--success);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        font-weight: 600;
        box-shadow: var(--shadow-lg);
        animation: slideInRight 0.3s ease-out;
        z-index: 9999;
    }

    /* === HISTORY PANEL === */
    .history-item {
        background: white;
        border: 1px solid var(--gray-200);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.75rem;
        cursor: pointer;
        transition: all 0.2s ease;
    }

    .history-item:hover {
        border-color: var(--primary);
        box-shadow: var(--shadow-md);
    }

    .history-title {
        font-weight: 600;
        color: var(--dark);
        margin-bottom: 0.25rem;
    }

    .history-meta {
        font-size: 0.75rem;
        color: var(--gray-500);
    }

    /* === HIDE STREAMLIT DEFAULTS === */
    #MainMenu, footer, header {visibility: hidden;}

    hr {
        border: none;
        border-top: 1px solid var(--gray-200);
        margin: 2rem 0;
    }

    /* === PLATFORM PREVIEWS === */
    .platform-shell {
        background: white;
        border: 1px solid var(--gray-200);
        border-radius: 16px;
        box-shadow: var(--shadow-md);
        overflow: hidden;
        margin-bottom: 1rem;
    }

    .platform-head {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.85rem 1rem;
        border-bottom: 1px solid var(--gray-200);
        background: var(--gray-50);
    }

    .platform-brand {
        font-size: 0.82rem;
        font-weight: 700;
        color: var(--gray-700);
        letter-spacing: 0.03em;
        text-transform: uppercase;
    }

    .platform-tag {
        font-size: 0.72rem;
        font-weight: 700;
        color: white;
        border-radius: 999px;
        padding: 0.2rem 0.6rem;
    }

    .platform-body {
        padding: 1rem;
    }

    .platform-meta {
        font-size: 0.78rem;
        color: var(--gray-500);
        margin-bottom: 0.8rem;
    }

    .linkedin-tag { background: #0a66c2; }
    .twitter-tag { background: #0f1419; }
    .newsletter-tag { background: #059669; }

    .platform-title {
        font-size: 1rem;
        font-weight: 800;
        color: var(--dark);
        margin-bottom: 0.5rem;
    }

    .platform-text {
        font-size: 0.94rem;
        color: var(--gray-700);
        line-height: 1.6;
        white-space: normal;
    }

    .platform-actions {
        display: flex;
        gap: 1rem;
        font-size: 0.78rem;
        color: var(--gray-500);
        margin-top: 0.9rem;
        padding-top: 0.75rem;
        border-top: 1px solid var(--gray-100);
    }

    .trace-box {
        border: 1px solid var(--gray-200);
        border-radius: 14px;
        padding: 1rem;
        background: white;
        margin-bottom: 0.85rem;
    }

    .loop-panel {
        border: 1px solid #86efac;
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        border-radius: 14px;
        padding: 1rem;
        margin: 1rem 0;
    }

    .loop-title {
        font-size: 0.9rem;
        font-weight: 800;
        color: #166534;
        margin-bottom: 0.6rem;
    }

    .loop-flow {
        display: flex;
        gap: 0.5rem;
        align-items: center;
        flex-wrap: wrap;
        color: #166534;
        font-weight: 600;
        font-size: 0.85rem;
    }

    .loop-node {
        background: rgba(22, 101, 52, 0.12);
        border: 1px solid rgba(22, 101, 52, 0.2);
        border-radius: 10px;
        padding: 0.35rem 0.6rem;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# SAMPLE CONTENT
# =============================================================================

SAMPLE_CONTENT = """The Future of Remote Work: Lessons from Five Years of Distributed Teams

After leading distributed engineering teams for five years, I've learned that remote work success isn't about tools or policies—it's about trust and intentional communication.

The biggest mistake companies make is trying to replicate office culture online. Forcing 9-to-5 schedules across time zones destroys productivity. Instead, focus on async-first communication where possible. We reduced meetings by 60% by switching to written proposals with comment-based discussions.

Key insight: Documentation becomes your office. When we mandated that every decision must be documented, onboarding time dropped from 3 months to 3 weeks. New hires could trace the "why" behind every system.

However, some synchronous time is crucial. We found that 2 hours of overlapping time daily was the sweet spot—enough for real-time collaboration without forcing anyone into awkward hours.

The productivity data surprised us: Our remote team shipped 40% more features than our previous co-located team. The secret? Fewer interruptions and more deep work time. We tracked focus blocks and found remote workers averaged 4.2 hours of uninterrupted work daily, versus 2.1 hours in office.

One counterintuitive finding: Random social interactions matter more than we thought. We created "virtual water cooler" channels and short, optional daily standups focused on personal updates. Team cohesion scores improved 25% after implementing these.

The tools that made the biggest difference weren't fancy collaboration platforms—they were simple shared documents, async video messages (Loom became essential), and a well-organized knowledge base.

For managers transitioning to remote: Stop measuring hours worked. Start measuring outcomes. Trust your team until they give you a reason not to. And over-communicate context—people need to understand the "why" more than ever when they can't absorb it through office osmosis.

The future isn't fully remote or fully in-office. It's about giving people autonomy to do their best work, wherever that happens to be."""

# =============================================================================
# COMPONENTS
# =============================================================================

def render_header(title: str, subtitle: str):
    st.markdown(f"""
    <div class="header-bar">
        <div class="header-title">{title}</div>
        <div class="header-subtitle">{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)


def render_pipeline_tracker(current_step: int = 0, status: str = "pending"):
    """Render pipeline progress tracker. Steps: 0=none, 1=summarizer, 2=formatter, 3=reviewer, 4=refiner, 5=complete"""
    steps = [
        ("1", "Summarizer", "Extract insights"),
        ("2", "Formatter", "Generate content"),
        ("3", "Reviewer", "Quality check"),
        ("4", "Refiner", "Apply feedback"),
    ]

    progress_width = min(100, (current_step / 4) * 100) if current_step > 0 else 0

    html = f'''
    <div class="pipeline-tracker">
        <div class="pipeline-steps">
            <div class="pipeline-line">
                <div class="pipeline-line-progress" style="width: {progress_width}%"></div>
            </div>
    '''

    for i, (num, name, desc) in enumerate(steps):
        step_num = i + 1
        if step_num < current_step:
            circle_class = "complete"
            label_class = "complete"
            icon = "✓"
        elif step_num == current_step:
            circle_class = "active"
            label_class = "active"
            icon = num
        else:
            circle_class = "pending"
            label_class = ""
            icon = num

        html += f'''
            <div class="pipeline-step">
                <div class="step-circle {circle_class}">{icon}</div>
                <div class="step-label {label_class}">{name}</div>
            </div>
        '''

    html += '</div></div>'
    st.markdown(html, unsafe_allow_html=True)


def render_metric_card(value, label, status="neutral"):
    status_class = ""
    if isinstance(value, (int, float)):
        if value >= 8:
            status_class = "good"
        elif value >= 5:
            status_class = "medium"
        else:
            status_class = "low"

    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value {status_class}">{value}</div>
        <div class="metric-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)


def render_insight(topic: str, text: str, importance: str):
    imp = importance.lower()
    st.markdown(f"""
    <div class="insight-item {imp}">
        <div class="insight-content">
            <div class="insight-topic">{topic} <span class="insight-tag tag-{imp}">{importance}</span></div>
            <div class="insight-text">{text}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_content_block(label: str, text: str):
    st.markdown(f"""
    <div class="content-section">
        <div class="content-label">{label}</div>
        <div class="content-text">{text}</div>
    </div>
    """, unsafe_allow_html=True)


def render_tweet(number: int, text: str):
    count = len(text)
    char_class = "ok" if count <= 280 else "over"
    st.markdown(f"""
    <div class="tweet-item">
        <div class="tweet-header">
            <span class="tweet-number">{number}</span>
            <span class="tweet-chars {char_class}">{count}/280</span>
        </div>
        <div class="tweet-text">{text}</div>
    </div>
    """, unsafe_allow_html=True)


def render_status_item(text: str, status: str = "success"):
    icons = {
        "critical": '<svg class="status-icon" viewBox="0 0 20 20" fill="#ef4444"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/></svg>',
        "warning": '<svg class="status-icon" viewBox="0 0 20 20" fill="#f59e0b"><path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/></svg>',
        "success": '<svg class="status-icon" viewBox="0 0 20 20" fill="#10b981"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/></svg>',
    }
    st.markdown(f"""
    <div class="status-item {status}">
        {icons.get(status, '')}
        <span>{text}</span>
    </div>
    """, unsafe_allow_html=True)


def _to_html_text(text: str) -> str:
    return html.escape(text or "").replace("\n", "<br>")


def render_linkedin_preview(linkedin, version_label: str):
    hashtags = " ".join(f"#{h}" for h in linkedin.hashtags)
    body = _to_html_text(linkedin.body)
    hook = _to_html_text(linkedin.hook)
    cta = _to_html_text(linkedin.call_to_action)
    st.markdown(f"""
    <div class="platform-shell">
        <div class="platform-head">
            <span class="platform-brand">LinkedIn Preview</span>
            <span class="platform-tag linkedin-tag">{html.escape(version_label)}</span>
        </div>
        <div class="platform-body">
            <div class="platform-meta">ContentForge AI · 1st · Just now</div>
            <div class="platform-title">{hook}</div>
            <div class="platform-text">{body}<br><br><strong>{cta}</strong><br><br>{html.escape(hashtags)}</div>
            <div class="platform-actions"><span>Like</span><span>Comment</span><span>Repost</span><span>Send</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_twitter_preview(twitter, version_label: str):
    tweets = "".join(
        f"<li style='margin-bottom:0.6rem;'><strong>{i+1}.</strong> {_to_html_text(tweet)}</li>"
        for i, tweet in enumerate(twitter.tweets)
    )
    st.markdown(f"""
    <div class="platform-shell">
        <div class="platform-head">
            <span class="platform-brand">Twitter/X Thread Preview</span>
            <span class="platform-tag twitter-tag">{html.escape(version_label)}</span>
        </div>
        <div class="platform-body">
            <div class="platform-meta">@contentforgeai · Now</div>
            <div class="platform-title">{_to_html_text(twitter.thread_hook)}</div>
            <ol class="platform-text" style="padding-left: 1.1rem; margin-top:0.75rem;">{tweets}</ol>
            <div class="platform-actions"><span>Reply</span><span>Repost</span><span>Like</span><span>Bookmark</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_newsletter_preview(newsletter, version_label: str):
    sections = "".join(f"<li>{_to_html_text(sec)}</li>" for sec in newsletter.body_sections)
    st.markdown(f"""
    <div class="platform-shell">
        <div class="platform-head">
            <span class="platform-brand">Newsletter Preview</span>
            <span class="platform-tag newsletter-tag">{html.escape(version_label)}</span>
        </div>
        <div class="platform-body">
            <div class="platform-meta">Subject: {_to_html_text(newsletter.subject_line)}</div>
            <div class="platform-title">{_to_html_text(newsletter.preview_text)}</div>
            <div class="platform-text">
                {_to_html_text(newsletter.intro)}
                <ul style="margin-top:0.7rem; padding-left:1rem;">{sections}</ul>
                <br>{_to_html_text(newsletter.closing)}
            </div>
            <div class="platform-actions"><span>Open</span><span>Forward</span><span>Archive</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_navbar():
    st.markdown(
        """
        <div class="top-nav">
            <div class="top-nav-inner">
                <div class="brand-wrap"><span class="brand-dot"></span><span>MultiAgent Studio</span></div>
                <div style="font-size:0.78rem; color:#6b7280;">Home · Demo · Architecture</div>
                <div class="nav-cta">Try Demo</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns([1, 1, 1, 1])
    with c1:
        if st.button("Home", use_container_width=True):
            st.session_state.current_page = "🏠 Overview"
            st.rerun()
    with c2:
        if st.button("Demo", use_container_width=True):
            st.session_state.current_page = "🚀 Run Pipeline"
            st.rerun()
    with c3:
        if st.button("Architecture", use_container_width=True):
            st.session_state.current_page = "🏗️ Architecture"
            st.rerun()
    with c4:
        if st.button("Try Demo", type="primary", use_container_width=True):
            st.session_state.current_page = "🚀 Run Pipeline"
            st.rerun()


def render_hero_flow_diagram():
    st.markdown(
        """
        <div class="trace-box" style="height:100%;">
            <div style="font-size:0.8rem; font-weight:700; text-transform:uppercase; color:#6b7280; letter-spacing:0.08em; margin-bottom:0.6rem;">System Flow</div>
            <div class="loop-flow" style="justify-content:flex-start; gap:0.45rem;">
                <span class="loop-node">Input</span><span>↓</span>
                <span class="loop-node">Summarizer</span><span>↓</span>
                <span class="loop-node">Formatter</span><span>↓</span>
                <span class="loop-node">Reviewer</span><span>↓</span>
                <span class="loop-node">Refiner</span><span>↓</span>
                <span class="loop-node">Final Output</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_diff_view(before_text: str, after_text: str):
    diff_lines = difflib.ndiff((before_text or "").splitlines(), (after_text or "").splitlines())
    rows = []
    for line in diff_lines:
        if line.startswith("+ "):
            rows.append(f"<div style='background:#ecfdf5; border-left:3px solid #22c55e; padding:0.35rem 0.55rem; margin-bottom:0.2rem;'>+ {_to_html_text(line[2:])}</div>")
        elif line.startswith("- "):
            rows.append(f"<div style='background:#eff6ff; border-left:3px solid #2563eb; padding:0.35rem 0.55rem; margin-bottom:0.2rem;'>~ {_to_html_text(line[2:])}</div>")
    if not rows:
        rows.append("<div style='color:#6b7280; font-size:0.85rem;'>No line-level textual differences detected.</div>")
    st.markdown("".join(rows), unsafe_allow_html=True)


# =============================================================================
# PAGES
# =============================================================================

def page_overview():
    left, right = st.columns([1.2, 1])
    with left:
        st.markdown("""
        <div class="hero-section">
            <div class="hero-content">
                <div class="hero-badge">Production SaaS Interface</div>
                <div class="hero-title">Multi-Agent Content Repurposing System</div>
                <div class="hero-subtitle">
                    Transform long-form content into platform-ready outputs using structured AI agents with feedback, review, and refinement.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        btn1, btn2 = st.columns(2)
        with btn1:
            if st.button("Try Demo", type="primary", use_container_width=True):
                st.session_state.current_page = "🚀 Run Pipeline"
                st.rerun()
        with btn2:
            if st.button("View Architecture", use_container_width=True):
                st.session_state.current_page = "🏗️ Architecture"
                st.rerun()
    with right:
        render_hero_flow_diagram()

    st.markdown("## Features")
    f1, f2, f3, f4 = st.columns(4)
    with f1:
        st.markdown('<div class="trace-box"><strong>Structured Multi-Agent Workflow</strong><div style="font-size:0.84rem;color:#6b7280;margin-top:0.45rem;">Explicit orchestrator and typed handoffs across all agents.</div></div>', unsafe_allow_html=True)
    with f2:
        st.markdown('<div class="trace-box"><strong>Feedback-Driven Refinement Loop</strong><div style="font-size:0.84rem;color:#6b7280;margin-top:0.45rem;">Reviewer output is fed directly into Refiner to produce V2.</div></div>', unsafe_allow_html=True)
    with f3:
        st.markdown('<div class="trace-box"><strong>Platform-Specific Rendering</strong><div style="font-size:0.84rem;color:#6b7280;margin-top:0.45rem;">Native previews for LinkedIn, Twitter/X, and newsletter format.</div></div>', unsafe_allow_html=True)
    with f4:
        st.markdown('<div class="trace-box"><strong>Transparent Data + Versioning</strong><div style="font-size:0.84rem;color:#6b7280;margin-top:0.45rem;">Track V1, review, and V2 with clear change logs.</div></div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="trace-box" style="text-align:center; padding:1.15rem;">
      <div style="font-size:1.1rem; font-weight:800; color:#111827; margin-bottom:0.7rem;">Start Repurposing Content</div>
      <div style="font-size:0.86rem; color:#6b7280;">Run a full agent workflow and inspect each stage end-to-end.</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Start Repurposing Content", type="primary", use_container_width=True):
        st.session_state.current_page = "🚀 Run Pipeline"
        st.rerun()

    st.markdown("## Pipeline Architecture")
    render_pipeline_tracker(0)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="agent-card">
            <div class="agent-header">
                <div class="agent-icon summarizer">📝</div>
                <div>
                    <div class="agent-name">Summarizer Agent</div>
                    <div class="agent-role">Extracts key insights from content</div>
                </div>
            </div>
            <div class="agent-details">
                <strong>Input:</strong> Raw text content<br>
                <strong>Output:</strong> Structured summary with key insights, theme, audience
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="agent-card">
            <div class="agent-header">
                <div class="agent-icon reviewer">🔍</div>
                <div>
                    <div class="agent-name">Reviewer Agent</div>
                    <div class="agent-role">Evaluates quality and identifies issues</div>
                </div>
            </div>
            <div class="agent-details">
                <strong>Checks:</strong> Clarity, consistency, missing insights<br>
                <strong>Output:</strong> Scores, issues, improvement suggestions
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="agent-card">
            <div class="agent-header">
                <div class="agent-icon formatter">✨</div>
                <div>
                    <div class="agent-name">Formatter Agent</div>
                    <div class="agent-role">Creates platform-specific content</div>
                </div>
            </div>
            <div class="agent-details">
                <strong>Formats:</strong> LinkedIn post, Twitter thread, Newsletter<br>
                <strong>Output:</strong> Version 1 of all formats
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="agent-card">
            <div class="agent-header">
                <div class="agent-icon refiner">🔧</div>
                <div>
                    <div class="agent-name">Refiner Agent</div>
                    <div class="agent-role">Improves content based on feedback</div>
                </div>
            </div>
            <div class="agent-details">
                <strong>Uses:</strong> Review feedback to fix issues<br>
                <strong>Output:</strong> Version 2 with documented changes
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Key Features
    st.markdown("## Key Features")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="card">
            <div class="card-title">📊 Structured Data Flow</div>
            <p style="margin-top: 0.5rem; font-size: 0.875rem;">
                All agents communicate via typed Pydantic schemas—never raw text.
                This ensures type safety and validated outputs.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
            <div class="card-title">🔄 Feedback Loop</div>
            <p style="margin-top: 0.5rem; font-size: 0.875rem;">
                The Reviewer evaluates V1 content and provides actionable feedback
                that the Refiner uses to produce improved V2.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="card">
            <div class="card-title">📋 Version Tracking</div>
            <p style="margin-top: 0.5rem; font-size: 0.875rem;">
                Clear before/after versioning with documented changes.
                See exactly what improved and why.
            </p>
        </div>
        """, unsafe_allow_html=True)


def page_run():
    render_header(
        "Demo Workspace",
        "Run a transparent multi-agent workflow with traceable inputs, outputs, feedback, and versioning"
    )

    # Check for API key
    api_key = get_api_key()
    if not api_key:
        st.markdown("""
        <div class="api-key-section">
            <div class="api-key-title">🔑 API Key Required</div>
            <div class="api-key-text">
                To run the pipeline, you need an OpenAI API key. You can either:
                <ul style="margin: 0.5rem 0; padding-left: 1.25rem;">
                    <li>Set the <code>OPENAI_API_KEY</code> environment variable</li>
                    <li>Enter your API key below (stored for this session only)</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        user_key = st.text_input(
            "OpenAI API Key",
            type="password",
            placeholder="sk-...",
            help="Your API key is only stored for this session and never saved to disk."
        )
        
        if user_key:
            st.session_state.api_key = user_key
            st.rerun()
        
        st.stop()

    # Input section
    st.markdown("## 📝 Input Content")

    use_sample = st.checkbox("Use sample article", value=True, help="Try the pipeline with a pre-loaded sample article")

    if use_sample:
        content = st.text_area("Content", value=SAMPLE_CONTENT, height=180, label_visibility="collapsed")
    else:
        content = st.text_area("Content", placeholder="Paste your article, blog post, or long-form content here...", height=180, label_visibility="collapsed")

    # Stats row
    words = len(content.split()) if content else 0
    chars = len(content) if content else 0
    st.markdown(f'''
    <div style="display: flex; gap: 2rem; margin: 1rem 0;">
        <div style="display: flex; align-items: baseline; gap: 0.375rem;">
            <span style="font-weight: 700; font-size: 1.25rem; color: var(--dark);">{words}</span>
            <span style="font-size: 0.8125rem; color: var(--gray-500);">words</span>
        </div>
        <div style="display: flex; align-items: baseline; gap: 0.375rem;">
            <span style="font-weight: 700; font-size: 1.25rem; color: var(--dark);">{chars:,}</span>
            <span style="font-size: 0.8125rem; color: var(--gray-500);">characters</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    ctl1, ctl2, ctl3 = st.columns([2, 1, 1])
    with ctl1:
        tone = st.selectbox("Tone", ["Professional", "Analytical", "Friendly", "Bold"], index=0)
        st.caption(f"Selected tone: {tone} (optional, for demo context)")

    col1, col2 = st.columns([3, 1])
    with col1:
        run = st.button("🚀 Run Pipeline", use_container_width=True, type="primary")
    with col2:
        clear = st.button("🗑️ Clear Results", use_container_width=True)
    
    if clear:
        st.session_state.result = None
        st.rerun()

    # Session state
    if "result" not in st.session_state:
        st.session_state.result = None
    if "pipeline_step" not in st.session_state:
        st.session_state.pipeline_step = 0
    if "history" not in st.session_state:
        st.session_state.history = []

    # Execute
    if run:
        if not content or len(content) < 100:
            st.error("⚠️ Please enter at least 100 characters of content to process.")
            st.stop()

        # Pipeline execution with visual feedback
        progress_placeholder = st.empty()
        status_placeholder = st.empty()
        time_placeholder = st.empty()

        try:
            from pipeline.orchestrator import PipelineOrchestrator
            from utils.llm import LLMClient
            from schemas.schemas import PipelineResult
            import time

            start_time = time.time()
            
            llm = LLMClient(api_key=api_key)
            orch = PipelineOrchestrator(llm_client=llm, verbose=False)

            # Step 1
            with progress_placeholder.container():
                render_pipeline_tracker(1)
            status_placeholder.info("🔍 **Summarizer Agent**: Analyzing content and extracting key insights...")
            step_start = time.time()
            summary = orch.summarizer.run(content)
            time_placeholder.caption(f"Step 1 completed in {time.time() - step_start:.1f}s")

            # Step 2
            with progress_placeholder.container():
                render_pipeline_tracker(2)
            status_placeholder.info("✨ **Formatter Agent**: Creating LinkedIn, Twitter, and Newsletter content...")
            step_start = time.time()
            v1 = orch.formatter.run(summary)
            time_placeholder.caption(f"Step 2 completed in {time.time() - step_start:.1f}s")

            # Step 3
            with progress_placeholder.container():
                render_pipeline_tracker(3)
            status_placeholder.info("🔍 **Reviewer Agent**: Evaluating content quality and consistency...")
            step_start = time.time()
            review = orch.reviewer.run(summary, v1)
            time_placeholder.caption(f"Step 3 completed in {time.time() - step_start:.1f}s")

            # Step 4
            with progress_placeholder.container():
                render_pipeline_tracker(4)
            status_placeholder.info("🔧 **Refiner Agent**: Applying feedback and enhancing content...")
            step_start = time.time()
            v2 = orch.refiner.run(summary, v1, review)
            time_placeholder.caption(f"Step 4 completed in {time.time() - step_start:.1f}s")

            # Complete
            total_time = time.time() - start_time
            with progress_placeholder.container():
                render_pipeline_tracker(5)
            status_placeholder.success(f"✅ **Pipeline complete!** Total time: {total_time:.1f} seconds")
            time_placeholder.empty()

            st.session_state.result = PipelineResult(
                input_summary=summary,
                version_1=v1,
                review=review,
                version_2=v2,
            )

            # Save to history
            st.session_state.history.append({
                "timestamp": datetime.now().isoformat(),
                "title": summary.title,
                "result": st.session_state.result
            })

            orch.save_results(st.session_state.result, "outputs")
            
            # Trigger confetti effect
            st.balloons()

        except Exception as e:
            status_placeholder.error(f"❌ **Error**: {str(e)}")
            st.markdown("""
            <div style="background: #fef2f2; border: 1px solid #fecaca; border-radius: 12px; padding: 1rem; margin-top: 1rem;">
                <strong style="color: #991b1b;">Troubleshooting Tips:</strong>
                <ul style="color: #7f1d1d; margin: 0.5rem 0; padding-left: 1.25rem; font-size: 0.875rem;">
                    <li>Check that your API key is valid and has credits</li>
                    <li>Ensure you have internet connectivity</li>
                    <li>Try with a shorter piece of content</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            st.stop()

    # Display results
    if st.session_state.result:
        r = st.session_state.result

        st.divider()
        
        # Export buttons at the top
        st.markdown("## 📊 Results")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            # Export as JSON
            json_data = json.dumps(r.model_dump(), indent=2, ensure_ascii=False)
            st.download_button(
                "📥 Export JSON",
                data=json_data,
                file_name=f"content_output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
        with col2:
            # Export LinkedIn
            linkedin_text = f"{r.version_2.linkedin.hook}\n\n{r.version_2.linkedin.body}\n\n{r.version_2.linkedin.call_to_action}\n\n{' '.join(['#' + h for h in r.version_2.linkedin.hashtags])}"
            st.download_button(
                "📋 LinkedIn Post",
                data=linkedin_text,
                file_name="linkedin_post.txt",
                mime="text/plain",
                use_container_width=True
            )
        with col3:
            # Export Twitter
            twitter_text = "\n\n---\n\n".join([f"Tweet {i+1}:\n{tweet}" for i, tweet in enumerate(r.version_2.twitter.tweets)])
            st.download_button(
                "🐦 Twitter Thread",
                data=twitter_text,
                file_name="twitter_thread.txt",
                mime="text/plain",
                use_container_width=True
            )
        with col4:
            # Export Newsletter
            newsletter_text = f"Subject: {r.version_2.newsletter.subject_line}\nPreview: {r.version_2.newsletter.preview_text}\n\n{r.version_2.newsletter.intro}\n\n" + "\n\n".join(r.version_2.newsletter.body_sections) + f"\n\n{r.version_2.newsletter.closing}"
            st.download_button(
                "📧 Newsletter",
                data=newsletter_text,
                file_name="newsletter.txt",
                mime="text/plain",
                use_container_width=True
            )

        st.divider()

        # Summary Section
        st.markdown("## 📄 Content Summary")

        st.markdown(f"""
        <div class="card">
            <div class="card-header">
                <div class="card-title">📄 {r.input_summary.title}</div>
                <span class="card-badge badge-primary">{r.input_summary.word_count_original} words</span>
            </div>
            <p style="font-style: italic; color: var(--gray-500); margin-bottom: 1.25rem; font-size: 1rem;">{r.input_summary.one_liner}</p>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                <div style="background: var(--gray-50); padding: 1rem; border-radius: 12px;">
                    <div style="font-size: 0.6875rem; font-weight: 700; color: var(--gray-500); text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.375rem;">Target Audience</div>
                    <div style="color: var(--dark); font-weight: 500;">{r.input_summary.target_audience}</div>
                </div>
                <div style="background: var(--gray-50); padding: 1rem; border-radius: 12px;">
                    <div style="font-size: 0.6875rem; font-weight: 700; color: var(--gray-500); text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.375rem;">Main Theme</div>
                    <div style="color: var(--dark); font-weight: 500;">{r.input_summary.main_theme}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 💡 Key Insights")
        for insight in r.input_summary.key_insights:
            render_insight(insight.topic, insight.insight, insight.importance)

        st.divider()

        st.markdown("## Agent-by-Agent Execution Trace")
        st.markdown("Each panel shows exactly what went into an agent and what came out, so reviewers can audit the workflow clearly.")

        with st.expander("Agent 1 · Summarizer (Input -> Structured Summary)", expanded=True):
            in_col, out_col = st.columns(2)
            with in_col:
                st.markdown("**Input to Summarizer**")
                st.text_area("Raw Long-form Input", content, height=180, key="trace_input_a1")
            with out_col:
                st.markdown("**Output from Summarizer**")
                st.markdown(f"**Title:** {r.input_summary.title}")
                st.markdown(f"**One-liner:** {r.input_summary.one_liner}")
                st.markdown(f"**Theme:** {r.input_summary.main_theme}")
                st.markdown(f"**Target Audience:** {r.input_summary.target_audience}")
                st.markdown(f"**Key Insights Extracted:** {len(r.input_summary.key_insights)}")

        with st.expander("Agent 2 · Formatter (Summary -> Multi-Format V1)"):
            in_col, out_col = st.columns(2)
            with in_col:
                st.markdown("**Input to Formatter**")
                st.markdown(f"- Summary title: {r.input_summary.title}")
                st.markdown(f"- Theme: {r.input_summary.main_theme}")
                st.markdown(f"- Insights count: {len(r.input_summary.key_insights)}")
            with out_col:
                st.markdown("**Output from Formatter (V1)**")
                st.markdown(f"- LinkedIn post fields: hook/body/CTA/hashtags")
                st.markdown(f"- Twitter thread tweets: {len(r.version_1.twitter.tweets)}")
                st.markdown(f"- Newsletter sections: {len(r.version_1.newsletter.body_sections)}")
                st.markdown(f"- Version flag: {r.version_1.version}")

        with st.expander("Agent 3 · Reviewer (Quality Check)"):
            in_col, out_col = st.columns(2)
            with in_col:
                st.markdown("**Input to Reviewer**")
                st.markdown("- Structured summary")
                st.markdown("- Formatter V1 outputs for all 3 platforms")
            with out_col:
                st.markdown("**Output from Reviewer**")
                st.markdown(f"- Alignment score: {r.review.overall_alignment_score}/10")
                st.markdown(f"- Consistency score: {r.review.consistency_score}/10")
                st.markdown(f"- Critical issues: {len(r.review.critical_issues)}")
                st.markdown(f"- Priority improvements: {len(r.review.priority_improvements)}")

        with st.expander("Agent 4 · Refiner (Feedback -> V2)"):
            in_col, out_col = st.columns(2)
            with in_col:
                st.markdown("**Input to Refiner**")
                st.markdown("- Summary output")
                st.markdown("- V1 formatted content")
                st.markdown("- Reviewer critical issues and improvements")
            with out_col:
                st.markdown("**Output from Refiner (V2)**")
                st.markdown(f"- Version flag: {r.version_2.version}")
                st.markdown(f"- Changes made: {len(r.version_2.changes_made)}")
                st.markdown(f"- Addressed issues: {len(r.version_2.addressed_issues)}")

        st.markdown(f"""
        <div class="loop-panel">
            <div class="loop-title">Feedback Loop Confirmed</div>
            <div class="loop-flow">
                <span class="loop-node">Formatter V1</span>
                <span>-></span>
                <span class="loop-node">Reviewer Feedback ({len(r.review.critical_issues)} critical)</span>
                <span>-></span>
                <span class="loop-node">Refiner V2 ({len(r.version_2.changes_made)} improvements)</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("## Platform Experience Preview")
        st.markdown("What the generated content looks like in real destination surfaces.")

        version_choice = st.radio(
            "Preview version",
            ["Version 1 (before refinement)", "Version 2 (final refined)"],
            horizontal=True,
            key="platform_preview_version"
        )
        selected = r.version_1 if "Version 1" in version_choice else r.version_2
        selected_label = "V1" if "Version 1" in version_choice else "V2"

        preview_tabs = st.tabs(["LinkedIn UI", "Twitter/X UI", "Newsletter UI"])
        with preview_tabs[0]:
            render_linkedin_preview(selected.linkedin, selected_label)
        with preview_tabs[1]:
            render_twitter_preview(selected.twitter, selected_label)
        with preview_tabs[2]:
            render_newsletter_preview(selected.newsletter, selected_label)

        st.divider()

        # Version 1
        st.markdown("## 📝 Version 1 — Initial Content")

        tabs = st.tabs(["💼 LinkedIn", "🐦 Twitter/X", "📧 Newsletter"])

        with tabs[0]:
            render_content_block("Hook", r.version_1.linkedin.hook)
            render_content_block("Body", r.version_1.linkedin.body)
            render_content_block("Call to Action", r.version_1.linkedin.call_to_action)
            st.markdown("**Hashtags:** " + " ".join([f"`#{t}`" for t in r.version_1.linkedin.hashtags]))

        with tabs[1]:
            st.caption(f"Thread with {len(r.version_1.twitter.tweets)} tweets")
            for i, tweet in enumerate(r.version_1.twitter.tweets, 1):
                render_tweet(i, tweet)

        with tabs[2]:
            render_content_block("Subject Line", r.version_1.newsletter.subject_line)
            render_content_block("Preview Text", r.version_1.newsletter.preview_text)
            render_content_block("Introduction", r.version_1.newsletter.intro)
            st.markdown("**Body Sections:**")
            for i, sec in enumerate(r.version_1.newsletter.body_sections, 1):
                with st.expander(f"📌 Section {i}", expanded=i==1):
                    st.markdown(sec)
            render_content_block("Closing", r.version_1.newsletter.closing)

        st.divider()

        # Review
        st.markdown("## 🔍 Review Feedback")

        st.markdown(f"""
        <div class="metric-grid">
            <div class="metric-card">
                <div class="metric-value {'good' if r.review.overall_alignment_score >= 8 else 'medium' if r.review.overall_alignment_score >= 5 else 'low'}">{r.review.overall_alignment_score}/10</div>
                <div class="metric-label">Alignment Score</div>
            </div>
            <div class="metric-card">
                <div class="metric-value {'good' if r.review.consistency_score >= 8 else 'medium' if r.review.consistency_score >= 5 else 'low'}">{r.review.consistency_score}/10</div>
                <div class="metric-label">Consistency Score</div>
            </div>
            <div class="metric-card">
                <div class="metric-value {'low' if len(r.review.critical_issues) > 2 else 'medium' if len(r.review.critical_issues) > 0 else 'good'}">{len(r.review.critical_issues)}</div>
                <div class="metric-label">Critical Issues</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if r.review.critical_issues:
            st.markdown("### ⚠️ Critical Issues")
            for issue in r.review.critical_issues:
                render_status_item(issue, "critical")

        if r.review.priority_improvements:
            st.markdown("### 📋 Priority Improvements")
            for imp in r.review.priority_improvements:
                render_status_item(imp, "warning")

        st.markdown("### Reviewer Scores")
        st.progress(r.review.overall_alignment_score / 10.0, text=f"Clarity & Alignment: {r.review.overall_alignment_score * 10}%")
        st.progress(r.review.consistency_score / 10.0, text=f"Consistency Across Formats: {r.review.consistency_score * 10}%")

        st.divider()

        # Version 2 - Highlighted as the FINAL output
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%); border: 2px solid #86efac; border-radius: 16px; padding: 1.25rem; margin-bottom: 1rem;">
            <div style="display: flex; align-items: center; gap: 0.75rem;">
                <span style="font-size: 1.5rem;">✨</span>
                <div>
                    <div style="font-weight: 700; color: #166534; font-size: 1.125rem;">Version 2 — Refined Final Content</div>
                    <div style="font-size: 0.875rem; color: #15803d;">After applying reviewer feedback</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        tabs2 = st.tabs(["💼 LinkedIn", "🐦 Twitter/X", "📧 Newsletter"])

        with tabs2[0]:
            render_content_block("Hook", r.version_2.linkedin.hook)
            render_content_block("Body", r.version_2.linkedin.body)
            render_content_block("Call to Action", r.version_2.linkedin.call_to_action)
            st.markdown("**Hashtags:** " + " ".join([f"`#{t}`" for t in r.version_2.linkedin.hashtags]))
            
            # Quick copy button
            linkedin_full = f"{r.version_2.linkedin.hook}\n\n{r.version_2.linkedin.body}\n\n{r.version_2.linkedin.call_to_action}\n\n{' '.join(['#' + h for h in r.version_2.linkedin.hashtags])}"
            st.text_area("Copy-ready LinkedIn post:", linkedin_full, height=200, key="linkedin_copy")

        with tabs2[1]:
            st.caption(f"Thread with {len(r.version_2.twitter.tweets)} tweets")
            for i, tweet in enumerate(r.version_2.twitter.tweets, 1):
                render_tweet(i, tweet)

        with tabs2[2]:
            render_content_block("Subject Line", r.version_2.newsletter.subject_line)
            render_content_block("Preview Text", r.version_2.newsletter.preview_text)
            render_content_block("Introduction", r.version_2.newsletter.intro)
            st.markdown("**Body Sections:**")
            for i, sec in enumerate(r.version_2.newsletter.body_sections, 1):
                with st.expander(f"📌 Section {i}", expanded=i==1):
                    st.markdown(sec)
            render_content_block("Closing", r.version_2.newsletter.closing)

        st.divider()

        # Improvements Made
        st.markdown("## ✅ Improvements Made")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 🔧 Changes Applied")
            for change in r.version_2.changes_made:
                render_status_item(change, "success")

        with col2:
            st.markdown("### ✔️ Issues Addressed")
            for issue in r.version_2.addressed_issues:
                render_status_item(issue, "success")

        st.divider()
        st.markdown("## Refiner: Before vs After")
        before_col, after_col = st.columns(2)
        with before_col:
            st.markdown("### Version 1")
            st.markdown(r.version_1.linkedin.body)
        with after_col:
            st.markdown("### Version 2")
            st.markdown(r.version_2.linkedin.body)

        st.markdown("### Line-Level Changes (LinkedIn Body)")
        render_diff_view(r.version_1.linkedin.body, r.version_2.linkedin.body)

        st.markdown("## Version History")
        if st.session_state.history:
            for i, item in enumerate(reversed(st.session_state.history[-5:]), start=1):
                ts = datetime.fromisoformat(item["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
                with st.expander(f"v{i}: {item['title']} ({ts})"):
                    ri = item["result"]
                    st.markdown(f"- V1 score: {ri.review.overall_alignment_score}/10")
                    st.markdown(f"- V2 changes: {len(ri.version_2.changes_made)}")
                    st.markdown(f"- Critical issues: {len(ri.review.critical_issues)}")


def page_comparison():
    render_header(
        "Version Comparison",
        "Side-by-side view of V1 vs V2 with improvements highlighted"
    )

    if "result" not in st.session_state or not st.session_state.result:
        st.info("Run the pipeline first to see the comparison.")
        if st.button("Go to Run Pipeline"):
            st.session_state.current_page = "Run Pipeline"
            st.rerun()
        return

    r = st.session_state.result

    format_choice = st.selectbox("Select format:", ["LinkedIn", "Twitter", "Newsletter"])

    st.divider()

    col1, col2 = st.columns(2)

    if format_choice == "LinkedIn":
        with col1:
            st.markdown(f"""
            <div class="compare-panel v1">
                <div class="compare-header">
                    <span class="compare-badge v1">Version 1</span>
                    <span style="color: #92400e; font-size: 0.875rem;">Before Refinement</span>
                </div>
                <div class="compare-field">
                    <div class="compare-field-label">Hook</div>
                    <div class="compare-field-value">{r.version_1.linkedin.hook}</div>
                </div>
                <div class="compare-field">
                    <div class="compare-field-label">Body Preview</div>
                    <div class="compare-field-value">{r.version_1.linkedin.body[:300]}...</div>
                </div>
                <div class="compare-field">
                    <div class="compare-field-label">CTA</div>
                    <div class="compare-field-value">{r.version_1.linkedin.call_to_action}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="compare-panel v2">
                <div class="compare-header">
                    <span class="compare-badge v2">Version 2</span>
                    <span style="color: #166534; font-size: 0.875rem;">After Refinement</span>
                </div>
                <div class="compare-field">
                    <div class="compare-field-label">Hook</div>
                    <div class="compare-field-value">{r.version_2.linkedin.hook}</div>
                </div>
                <div class="compare-field">
                    <div class="compare-field-label">Body Preview</div>
                    <div class="compare-field-value">{r.version_2.linkedin.body[:300]}...</div>
                </div>
                <div class="compare-field">
                    <div class="compare-field-label">CTA</div>
                    <div class="compare-field-value">{r.version_2.linkedin.call_to_action}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Scores
        st.markdown("### Review Scores")
        c1, c2 = st.columns(2)
        c1.metric("Clarity", f"{r.review.linkedin_review.clarity_score}/10")
        c2.metric("Engagement", f"{r.review.linkedin_review.engagement_score}/10")

    elif format_choice == "Twitter":
        with col1:
            v1t = r.version_1.twitter.tweets
            st.markdown(f"""
            <div class="compare-panel v1">
                <div class="compare-header">
                    <span class="compare-badge v1">Version 1</span>
                </div>
                <div class="compare-field">
                    <div class="compare-field-label">Thread Length</div>
                    <div class="compare-field-value">{len(v1t)} tweets</div>
                </div>
                <div class="compare-field">
                    <div class="compare-field-label">First Tweet</div>
                    <div class="compare-field-value">{v1t[0] if v1t else 'N/A'}</div>
                </div>
                <div class="compare-field">
                    <div class="compare-field-label">Last Tweet</div>
                    <div class="compare-field-value">{v1t[-1] if len(v1t) > 1 else 'N/A'}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            v2t = r.version_2.twitter.tweets
            st.markdown(f"""
            <div class="compare-panel v2">
                <div class="compare-header">
                    <span class="compare-badge v2">Version 2</span>
                </div>
                <div class="compare-field">
                    <div class="compare-field-label">Thread Length</div>
                    <div class="compare-field-value">{len(v2t)} tweets</div>
                </div>
                <div class="compare-field">
                    <div class="compare-field-label">First Tweet</div>
                    <div class="compare-field-value">{v2t[0] if v2t else 'N/A'}</div>
                </div>
                <div class="compare-field">
                    <div class="compare-field-label">Last Tweet</div>
                    <div class="compare-field-value">{v2t[-1] if len(v2t) > 1 else 'N/A'}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("### Review Scores")
        c1, c2 = st.columns(2)
        c1.metric("Clarity", f"{r.review.twitter_review.clarity_score}/10")
        c2.metric("Engagement", f"{r.review.twitter_review.engagement_score}/10")

    else:
        with col1:
            st.markdown(f"""
            <div class="compare-panel v1">
                <div class="compare-header">
                    <span class="compare-badge v1">Version 1</span>
                </div>
                <div class="compare-field">
                    <div class="compare-field-label">Subject Line</div>
                    <div class="compare-field-value">{r.version_1.newsletter.subject_line}</div>
                </div>
                <div class="compare-field">
                    <div class="compare-field-label">Preview</div>
                    <div class="compare-field-value">{r.version_1.newsletter.preview_text}</div>
                </div>
                <div class="compare-field">
                    <div class="compare-field-label">Sections</div>
                    <div class="compare-field-value">{len(r.version_1.newsletter.body_sections)}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="compare-panel v2">
                <div class="compare-header">
                    <span class="compare-badge v2">Version 2</span>
                </div>
                <div class="compare-field">
                    <div class="compare-field-label">Subject Line</div>
                    <div class="compare-field-value">{r.version_2.newsletter.subject_line}</div>
                </div>
                <div class="compare-field">
                    <div class="compare-field-label">Preview</div>
                    <div class="compare-field-value">{r.version_2.newsletter.preview_text}</div>
                </div>
                <div class="compare-field">
                    <div class="compare-field-label">Sections</div>
                    <div class="compare-field-value">{len(r.version_2.newsletter.body_sections)}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("### Review Scores")
        c1, c2 = st.columns(2)
        c1.metric("Clarity", f"{r.review.newsletter_review.clarity_score}/10")
        c2.metric("Engagement", f"{r.review.newsletter_review.engagement_score}/10")

    st.divider()

    # Changes summary
    st.markdown("### What Changed")
    for change in r.version_2.changes_made:
        render_status_item(change, "success")


def page_architecture():
    # Architecture page hero
    st.markdown("""
    <div class="hero-section" style="padding: 2rem 2.5rem;">
        <div class="hero-content">
            <div class="hero-badge">Technical Documentation</div>
            <div class="hero-title" style="font-size: 2rem;">System Architecture</div>
            <div class="hero-subtitle">
                Deep dive into the multi-agent pipeline design, data schemas, and orchestration patterns.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## Pipeline Overview")
    render_pipeline_tracker(0)

    st.markdown("""
    The system uses **explicit orchestration** with no black-box frameworks.
    Each agent is a separate Python class with a `run()` method that takes
    structured input and returns structured output via Pydantic schemas.
    """)

    st.divider()

    st.markdown("## Agent Specifications")

    # Summarizer
    st.markdown("""
    <div class="agent-card">
        <div class="agent-header">
            <div class="agent-icon summarizer">📝</div>
            <div>
                <div class="agent-name">SummarizerAgent</div>
                <div class="agent-role">agents/summarizer.py</div>
            </div>
        </div>
        <p style="font-size: 0.875rem; color: #64748b; margin: 0.5rem 0;">
            Extracts structured insights from raw long-form content. Uses lower temperature (0.5) for consistent analysis.
        </p>
        <div class="agent-details">
            <strong>Input:</strong> <code>str</code> (raw text)<br>
            <strong>Output:</strong> <code>SummaryOutput</code>
            <div class="agent-schema">
{
  "title": str,
  "one_liner": str,
  "key_insights": [{"topic": str, "insight": str, "importance": "high|medium|low"}],
  "target_audience": str,
  "main_theme": str,
  "word_count_original": int
}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Formatter
    st.markdown("""
    <div class="agent-card">
        <div class="agent-header">
            <div class="agent-icon formatter">✨</div>
            <div>
                <div class="agent-name">FormatterAgent</div>
                <div class="agent-role">agents/formatter.py</div>
            </div>
        </div>
        <p style="font-size: 0.875rem; color: #64748b; margin: 0.5rem 0;">
            Transforms structured summary into platform-specific content. Higher temperature (0.7) for creative output.
        </p>
        <div class="agent-details">
            <strong>Input:</strong> <code>SummaryOutput</code><br>
            <strong>Output:</strong> <code>FormattedOutput</code> (version=1)
            <div class="agent-schema">
{
  "version": 1,
  "linkedin": {"hook": str, "body": str, "call_to_action": str, "hashtags": [str]},
  "twitter": {"thread_hook": str, "tweets": [str]},
  "newsletter": {"subject_line": str, "preview_text": str, "intro": str, "body_sections": [str], "closing": str}
}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Reviewer
    st.markdown("""
    <div class="agent-card">
        <div class="agent-header">
            <div class="agent-icon reviewer">🔍</div>
            <div>
                <div class="agent-name">ReviewerAgent</div>
                <div class="agent-role">agents/reviewer.py</div>
            </div>
        </div>
        <p style="font-size: 0.875rem; color: #64748b; margin: 0.5rem 0;">
            Critical evaluation comparing formatted content against source summary. Low temperature (0.3) for consistent scoring.
        </p>
        <div class="agent-details">
            <strong>Input:</strong> <code>SummaryOutput</code> + <code>FormattedOutput</code><br>
            <strong>Output:</strong> <code>ReviewOutput</code>
            <div class="agent-schema">
{
  "overall_alignment_score": int (1-10),
  "consistency_score": int (1-10),
  "linkedin_review": FormatReview,
  "twitter_review": FormatReview,
  "newsletter_review": FormatReview,
  "critical_issues": [str],
  "priority_improvements": [str]
}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Refiner
    st.markdown("""
    <div class="agent-card">
        <div class="agent-header">
            <div class="agent-icon refiner">🔧</div>
            <div>
                <div class="agent-name">RefinerAgent</div>
                <div class="agent-role">agents/refiner.py</div>
            </div>
        </div>
        <p style="font-size: 0.875rem; color: #64748b; margin: 0.5rem 0;">
            Applies review feedback to improve V1 content. Documents all changes made. Temperature 0.6 for balanced improvement.
        </p>
        <div class="agent-details">
            <strong>Input:</strong> <code>SummaryOutput</code> + <code>FormattedOutput</code> + <code>ReviewOutput</code><br>
            <strong>Output:</strong> <code>RefinedOutput</code> (version=2)
            <div class="agent-schema">
{
  "version": 2,
  "linkedin": LinkedInPost,
  "twitter": TwitterThread,
  "newsletter": NewsletterSection,
  "changes_made": [str],
  "addressed_issues": [str]
}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("## Data Flow")

    # Animated Visual Flowchart
    st.markdown("""
    <div class="flowchart-container">
        <div class="flowchart-title">Pipeline Architecture Flow</div>

        <!-- Input -->
        <div class="flow-row">
            <div class="flow-node input">
                <span style="margin-right: 0.5rem;">&#128196;</span> Raw Text Input
            </div>
        </div>

        <div class="flow-arrow">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 5v14M19 12l-7 7-7-7"/>
            </svg>
        </div>

        <!-- Summarizer -->
        <div class="flow-row">
            <div class="flow-node summarizer">
                <span style="margin-right: 0.5rem;">&#128221;</span> Summarizer Agent
            </div>
        </div>

        <div class="flow-arrow">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 5v14M19 12l-7 7-7-7"/>
            </svg>
            <div class="flow-arrow-label">SummaryOutput</div>
        </div>

        <!-- Formatter -->
        <div class="flow-row">
            <div class="flow-node formatter">
                <span style="margin-right: 0.5rem;">&#10024;</span> Formatter Agent
            </div>
        </div>

        <div class="flow-arrow">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 5v14M19 12l-7 7-7-7"/>
            </svg>
            <div class="flow-arrow-label">FormattedOutput (V1)</div>
        </div>

        <!-- Reviewer and Refiner Split -->
        <div class="flow-split">
            <div class="flow-branch">
                <div class="flow-node reviewer">
                    <span style="margin-right: 0.5rem;">&#128269;</span> Reviewer Agent
                </div>
                <div class="flow-arrow">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="transform: rotate(45deg);">
                        <path d="M12 5v14M19 12l-7 7-7-7"/>
                    </svg>
                    <div class="flow-arrow-label">ReviewOutput</div>
                </div>
            </div>

            <div class="flow-branch" style="margin-top: 3rem;">
                <div class="flow-feedback-loop">
                    <svg viewBox="0 0 24 24" fill="none" stroke="#059669" stroke-width="2" style="width: 20px; height: 20px; margin-right: 0.5rem;">
                        <path d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
                    </svg>
                    <span>Feedback Loop</span>
                </div>
            </div>

            <div class="flow-branch">
                <div class="flow-node refiner">
                    <span style="margin-right: 0.5rem;">&#128295;</span> Refiner Agent
                </div>
                <div class="flow-arrow">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M12 5v14M19 12l-7 7-7-7"/>
                    </svg>
                    <div class="flow-arrow-label">RefinedOutput (V2)</div>
                </div>
            </div>
        </div>

        <!-- Output -->
        <div class="flow-row">
            <div class="flow-node output">
                <span style="margin-right: 0.5rem;">&#9989;</span> Final Content
            </div>
        </div>

        <!-- Version Comparison -->
        <div class="flow-versions">
            <div class="flow-version v1">
                <div class="flow-version-num">V1</div>
                <div class="flow-version-label">Initial Draft</div>
            </div>
            <div style="display: flex; align-items: center; color: #94a3b8;">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width: 32px; height: 24px;">
                    <path d="M5 12h14M12 5l7 7-7 7"/>
                </svg>
            </div>
            <div class="flow-version v2">
                <div class="flow-version-num">V2</div>
                <div class="flow-version-label">Refined Final</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# =============================================================================
# SIDEBAR & MAIN
# =============================================================================

def main():
    # Initialize session state
    if "history" not in st.session_state:
        st.session_state.history = []
    if "result" not in st.session_state:
        st.session_state.result = None
    if "current_page" not in st.session_state:
        st.session_state.current_page = "🏠 Overview"

    render_navbar()
        
    with st.sidebar:
        # Logo and branding
        st.markdown("""
        <div class="sidebar-logo">
            <div class="sidebar-logo-icon">🔮</div>
            <div>
                <div class="sidebar-logo-text">ContentForge</div>
                <div class="sidebar-logo-sub">AI Content System</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### Workspace Status")
        st.divider()

        # Status indicator
        if st.session_state.get("result"):
            st.markdown("""
            <div style="background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%); border: 1px solid #86efac; border-radius: 12px; padding: 1rem; margin-bottom: 1rem;">
                <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.25rem;">
                    <span style="font-size: 1rem;">✅</span>
                    <span style="font-size: 0.8125rem; font-weight: 700; color: #166534;">Pipeline Complete</span>
                </div>
                <div style="font-size: 0.75rem; color: #15803d;">Results ready to view</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: var(--gray-100); border-radius: 12px; padding: 1rem; margin-bottom: 1rem;">
                <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.25rem;">
                    <span style="font-size: 1rem;">⏳</span>
                    <span style="font-size: 0.8125rem; font-weight: 600; color: var(--gray-600);">Ready to Process</span>
                </div>
                <div style="font-size: 0.75rem; color: var(--gray-500);">Go to Run Pipeline to start</div>
            </div>
            """, unsafe_allow_html=True)
        
        # History section
        if st.session_state.history:
            st.markdown("### 📜 Recent Runs")
            for i, item in enumerate(reversed(st.session_state.history[-5:])):
                timestamp = datetime.fromisoformat(item["timestamp"]).strftime("%H:%M")
                if st.button(f"📄 {item['title'][:30]}... ({timestamp})", key=f"history_{i}", use_container_width=True):
                    st.session_state.result = item["result"]
                    st.rerun()
            
            st.divider()
        
        # API Key status
        api_key = get_api_key()
        if api_key:
            st.markdown("""
            <div style="display: flex; align-items: center; gap: 0.5rem; padding: 0.5rem; background: #f0fdf4; border-radius: 8px; margin-bottom: 1rem;">
                <span style="color: #16a34a;">🔑</span>
                <span style="font-size: 0.75rem; color: #166534;">API Key configured</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="display: flex; align-items: center; gap: 0.5rem; padding: 0.5rem; background: #fef3c7; border-radius: 8px; margin-bottom: 1rem;">
                <span style="color: #d97706;">⚠️</span>
                <span style="font-size: 0.75rem; color: #92400e;">API Key needed</span>
            </div>
            """, unsafe_allow_html=True)

        # Tech stack info
        st.markdown("""
        <div style="font-size: 0.75rem; color: var(--gray-400); margin-top: 2rem; padding-top: 1rem; border-top: 1px solid var(--gray-200);">
            <div style="font-weight: 600; color: var(--gray-500); margin-bottom: 0.5rem;">Tech Stack</div>
            <div>Python • Pydantic • OpenAI</div>
            <div>Streamlit • Explicit Orchestration</div>
            <div style="margin-top: 0.75rem; color: var(--gray-300);">v1.0.0</div>
        </div>
        """, unsafe_allow_html=True)

    # Page routing
    page = st.session_state.current_page
    page_name = page.split(" ", 1)[1] if " " in page else page
    
    if page_name == "Overview":
        page_overview()
    elif page_name == "Run Pipeline":
        page_run()
    elif page_name == "Comparison":
        page_comparison()
    elif page_name == "Architecture":
        page_architecture()


if __name__ == "__main__":
    main()
