import streamlit as st
import pandas as pd
import joblib

# Load trained model and label encoder
model = joblib.load("C:/Users/user/Desktop/STATISTICAL METHODS/thyroid_model.pkl")
label_encoder = joblib.load("C:/Users/user/Desktop/STATISTICAL METHODS/label_encoder.pkl")

# Mapping of numerical predictions to labels
class_labels = {
    0: "Hyperthyroidism",
    1: "Normal",
    2: "Primary Hypothyroidism",
    3: "Secondary Hyperthyroidism",
    4: "Secondary Hypothyroidism",
    5: "Subclinical Hyperthyroidism",
    6: "Subclinical Hypothyroidism",
    7: "Unclassified"
}

# Streamlit UI
st.title("Thyroid Classification Web App")
st.write("Upload an Excel file or enter patient data manually to predict thyroid condition.")

# Upload Excel file
uploaded_file = st.file_uploader("Upload an Excel file with TSH, FT3, FT4 values", type=["xlsx"])

if uploaded_file:
    # Load the Excel file
    df = pd.read_excel(uploaded_file)
    
    # Check if required columns exist
    if set(["TSH", "FT3", "FT4"]).issubset(df.columns):
        # Make predictions
        predictions = model.predict(df[["TSH", "FT3", "FT4"]])
        
        # Convert predictions to labels
        df["Diagnosis"] = [class_labels[pred] for pred in predictions]
        
        # Show results
        st.write("### Prediction Results:")
        st.dataframe(df)
        
        # Download button
        st.download_button(
            label="Download Results as Excel",
            data=df.to_csv(index=False),
            file_name="thyroid_predictions.csv",
            mime="text/csv"
        )
    else:
        st.error("Uploaded file is missing required columns: 'TSH', 'FT3', 'FT4'")

# Manual Input Section
st.write("---")
st.write("### Manual Input for a Single Patient")

# Input fields
tsh = st.number_input("TSH Level", min_value=0.0, format="%.2f")
ft3 = st.number_input("FT3 Level", min_value=0.0, format="%.2f")
ft4 = st.number_input("FT4 Level", min_value=0.0, format="%.2f")

if st.button("Predict Diagnosis"):
    input_data = pd.DataFrame([[tsh, ft3, ft4]], columns=["TSH", "FT3", "FT4"])
    prediction = model.predict(input_data)[0]
    diagnosis = class_labels[prediction]
    
    st.success(f"The model predicts: **{diagnosis}**")
