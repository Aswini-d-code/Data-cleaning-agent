import streamlit as st
import pandas as pd
import google.generativeai as genai
import io

# --- 1. INITIALIZATION ---
# This keeps your data and chat history from disappearing when you click buttons
if "df" not in st.session_state:
    st.session_state.df = None
if "cleaned_df" not in st.session_state:
    st.session_state.cleaned_df = None
if "messages" not in st.session_state:
    st.session_state.messages = []

st.set_page_config(page_title="Data Clean Hub", layout="wide")

# --- 2. API SETUP ---
try:
    # Looks for GEMINI_API_KEY in your Streamlit Cloud Secrets
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    # Using the full model path to avoid the 404 error
    model = genai.GenerativeModel('models/gemini-1.5-flash')
except Exception:
    st.sidebar.error("⚠️ API Key missing! Add 'GEMINI_API_KEY' to your Secrets.")

# --- 3. SIDEBAR ---
with st.sidebar:
    st.header("📂 Data Input")
    uploaded_file = st.file_uploader("Upload Messy CSV", type="csv")
    if uploaded_file:
        st.session_state.df = pd.read_csv(uploaded_file)

st.title("🚀 Data Quality & Cleaning Center")

# Check if data is uploaded
if st.session_state.df is not None:
    df = st.session_state.df
    tab1, tab2, tab3 = st.tabs(["📋 Data Dashboard", "🧹 AI Deep Clean", "💬 Data Assistant"])

    # --- TAB 1: DASHBOARD ---
    with tab1:
        st.subheader("Data Summary Details")
        col1, col2, col3 = st.columns(3)
        total_cells = df.size
        null_cells = df.isnull().sum().sum()
        duplicate_rows = df.duplicated().sum()
        
        col1.metric("Total Records", len(df), border=True)
        col2.metric("Total Data Points", total_cells, border=True)
        col3.metric("Duplicate Rows", duplicate_rows, border=True)

        col4, col5, col6 = st.columns(3)
        health_score = ((total_cells - null_cells) / total_cells) * 100
        col4.metric("Data Health Score", f"{health_score:.1f}%", border=True)
        col5.metric("Total Missing Values", null_cells, delta="Needs Cleaning", delta_color="inverse", border=True)
        col6.metric("Total Columns", len(df.columns), border=True)

        st.divider()
        st.write("### 🔍 Column-wise Missing Values")
        null_details = df.isnull().sum().reset_index()
        null_details.columns = ['Column Name', 'Missing Count']
        st.table(null_details)

    # --- TAB 2: CLEANING ---
    with tab2:
        st.subheader("Automated Data Refinement")
        st.write("This tool removes all nulls and duplicate rows instantly.")
        
        if st.button("✨ Execute Deep Clean"):
            # The cleaning logic
            clean_df = df.dropna().drop_duplicates().reset_index(drop=True)
            st.session_state.cleaned_df = clean_df
            st.success(f"Cleaned! Kept {len(clean_df)} out of {len(df)} rows.")

        if st.session_state.cleaned_df is not None:
            st.write("### 📥 Download Cleaned CSV")
            csv_buffer = io.BytesIO()
            st.session_state.cleaned_df.to_csv(csv_buffer, index=False)
            
            st.download_button(
                label="Download Cleaned File",
                data=csv_buffer.getvalue(),
                file_name="fully_cleaned_data.csv",
                mime="text/csv"
            )
            st.dataframe(st.session_state.cleaned_df.head(20))

    # --- TAB 3: DATA ASSISTANT ---
    with tab3:
        st.subheader("💬 AI Data Consultant")
        
        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Ask me about your data..."):
            # Save user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.spinner("Analyzing data..."):
                try:
                    # Context for the AI
                    context = f"The dataset has {len(df)} rows and {len(df.columns)} columns: {list(df.columns)}."
                    response = model.generate_content(f"{context}\n\nUser Question: {prompt}")
                    answer = response.text
                    
                    # Save AI message
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                    with st.chat_message("assistant"):
                        st.markdown(answer)
                        
                        # --- VOICE SCRIPT ---
                        # This triggers the browser to speak the answer out loud
                        clean_answer = answer.replace("'", "").replace("\n", " ")
                        st.components.v1.html(f"""
                            <script>
                                var msg = new SpeechSynthesisUtterance('{clean_answer}');
                                window.speechSynthesis.speak(msg);
                            </script>
                        """, height=0)
                except Exception as e:
                    st.error(f"⚠️ Error: {str(e)}")
                    if "429" in str(e):
                        st.warning("Limit reached. Please wait 60 seconds.")
else:
    st.info("👈 Please upload a CSV file in the sidebar to start.")