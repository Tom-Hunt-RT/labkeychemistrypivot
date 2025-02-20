import streamlit as st
import pandas as pd

# Set up Streamlit configuration
st.set_page_config(layout="wide")

# Pivot the chemistry tall table
def pivot_chemistry_csv(data):
    data['Analyte_Units_Scheme'] = data['Analyte'] + '_' + data['Units'] + '_' + data['Scheme']
    data = data.drop(columns=['Analyte', 'Units', 'Scheme', 'Detection Limit', 'Warning', 'Ranking'])
    pivot_data = data.pivot_table(index='Sample ID', columns='Analyte_Units_Scheme', values='Result', aggfunc='first')
    pivot_data = pivot_data.reset_index()
    pivot_data["Sample ID"] = pivot_data["Sample ID"].astype(str)
    return pivot_data

def display_uploaded_chemistry_data(chemistry, labkeychemistry):
    if chemistry is not None:
        if st.button(f"Pivot Uploaded Chemistry Data ({labkeychemistry.name})"):
            st.write(pivot_chemistry_csv(chemistry))
    else:
        st.text("This section will remain blank until you upload a .csv file (LabKey Chemistry Assay export) in the sidebar.")

def main():
    st.title("Pivot LabKey Chemistry App")
    st.sidebar.title("Upload Files")
    st.sidebar.write("Upload a .csv file (LabKey Chemistry Assay export) to pivot the data.")
    
    with st.sidebar:
        labkeychemistry = st.file_uploader("Upload Mineral Chemistry File", type=['csv'])
        chemistry = pd.read_csv(labkeychemistry) if labkeychemistry else None

    display_uploaded_chemistry_data(chemistry, labkeychemistry)

if __name__ == "__main__":
    main()
