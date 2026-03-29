import streamlit as st
import pandas as pd
import io
import base64
import matplotlib.pyplot as plt
import sys
import os
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
from backend.src.pipeline import NameMatchingPipeline

st.set_page_config(layout="wide", page_title="Name Matching System", page_icon="🔍")

def sidebar():
    st.sidebar.title("About the App")
    st.sidebar.info(
        """
        This Name Matching System helps you detect duplicate or similar names across two CSV datasets.\n\n
        **Steps to use:**
        1. Upload two CSV files (with headers).
        2. Select a similarity threshold and blocking strategy.
        3. Click **Find Matches** to view results.
        4. Download the matches as a CSV file.
        """
    )
    st.sidebar.markdown("---")
    st.sidebar.write("Developed as a Final Year Project")

sidebar()

def main():
    st.markdown(
        """
        <h1 style='text-align: center; color: #0072C6;'>🔍 Name Matching System</h1>
        <p style='text-align: center; font-size:18px;'>Upload two CSV files to find matching names and other data across datasets.</p>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("ℹ️ Instructions", expanded=False):
        st.write("""
        - Both CSV files should have headers.
        - Choose a similarity threshold: Higher values = stricter matching.
        - Select a blocking strategy for faster matching.
        - Results will be shown in a table and can be downloaded.
        """)

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            db1_file = st.file_uploader("Upload the first CSV file", type=["csv"], key="db1")
        with col2:
            db2_file = st.file_uploader("Upload the second CSV file", type=["csv"], key="db2")

    st.markdown("---")
    col3, col4 = st.columns([2, 1])
    with col3:
        threshold = st.slider("Similarity Threshold", min_value=0.0, max_value=100.0, value=80.0, step=1.0, help="Higher values mean stricter matching.")
    with col4:
        blocking = st.selectbox("Blocking Strategy", ["metaphone", "soundex"], index=0)

    st.markdown("---")
    btn_col1, btn_col2, btn_col3 = st.columns([2,1,2])
    with btn_col2:
        find_btn = st.button("🔎 Find Matches", use_container_width=True)

    if find_btn:
        if db1_file and db2_file:
            find_matches(db1_file, db2_file, threshold, blocking)
        else:
            st.warning("Please upload both CSV files.", icon="⚠️")

def get_table_download_link(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="matches.csv">📥 Download Results as CSV</a>'
    return href

def find_matches(db1_file, db2_file, threshold, blocking):
    with st.spinner("Processing files and finding matches..."):
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".csv", mode='wb') as temp1, \
                 tempfile.NamedTemporaryFile(delete=False, suffix=".csv", mode='wb') as temp2:
                
                temp1.write(db1_file.getvalue())
                temp2.write(db2_file.getvalue())
                
                temp1_name = temp1.name
                temp2_name = temp2.name

            pipeline = NameMatchingPipeline(
                blocking_strategy=blocking,
                threshold=threshold
            )
            results_df = pipeline.process_csv_files([temp1_name, temp2_name])
            
            if len(results_df) > 0:
                total_matches = len(results_df)
                avg_score = results_df['similarity_score'].mean() if 'similarity_score' in results_df.columns else None
                
                summary_data = {
                    "Total Matches": [total_matches],
                }
                if avg_score is not None:
                    summary_data["Average Similarity (%)"] = [f"{avg_score:.2f}"]
                summary_df = pd.DataFrame(summary_data)
                st.table(summary_df)

                if 'similarity_score' in results_df.columns:
                    fig, ax = plt.subplots()
                    results_df['similarity_score'].plot(kind='hist', bins=10, color='#1976D2', edgecolor='white', ax=ax)
                    ax.set_title('Distribution of Similarity Scores')
                    ax.set_xlabel('Similarity Score')
                    ax.set_ylabel('Frequency')
                    st.pyplot(fig)

                if 'similarity_score' in results_df.columns:
                    min_score = float(results_df['similarity_score'].min())
                    max_score = float(results_df['similarity_score'].max())
                    filter_score = st.slider(
                        "Filter matches by minimum similarity score", min_value=min_score, max_value=max_score, value=min_score, step=1.0
                    )
                    filtered_df = results_df[results_df['similarity_score'] >= filter_score]
                else:
                    filtered_df = results_df

                st.dataframe(
                    filtered_df.style.apply(
                        lambda x: [
                            'background-color: #C8E6C9' if v >= threshold else '' if pd.notnull(v) else ''
                            for v in x
                        ] if x.name == 'similarity_score' else ['']*len(x),
                        axis=0
                    ),
                    use_container_width=True,
                    hide_index=True
                )

                with st.expander("📥 Download Options & Insights"):
                    st.markdown(get_table_download_link(filtered_df), unsafe_allow_html=True)
                    st.write("You can download the matched results as a CSV file.")
                st.success(f"✅ Found {total_matches} matches!", icon="✅")
            else:
                st.info("No matches found.", icon="ℹ️")
                
            os.unlink(temp1_name)
            os.unlink(temp2_name)
            
        except Exception as e:
            st.error(f"❌ An error occurred: {e}")
            import traceback
            st.error(traceback.format_exc())

if __name__ == "__main__":
    main()
