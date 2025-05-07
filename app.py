import streamlit as st
import pandas as pd
import joblib
from io import BytesIO

model = joblib.load("stunting_classification_model.pkl")
label_encoder_gender = joblib.load("label_encoder_gender.pkl")
label_encoder_status = joblib.load("label_encoder_status.pkl")

def predict_status_gizi(row):
    jenis_kelamin_encoded = label_encoder_gender.transform([row['Jenis Kelamin']])[0]

    input_data = pd.DataFrame([[row['Umur (bulan)'], jenis_kelamin_encoded, row['Tinggi Badan (cm)']]],
                              columns=["Umur (bulan)", "Jenis Kelamin", "Tinggi Badan (cm)"])

    hasil_prediksi = model.predict(input_data)[0]
    label_prediksi = label_encoder_status.inverse_transform([hasil_prediksi])[0].title()

    return label_prediksi

st.title("Prediksi Status Gizi Balita")

uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])
if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.subheader("Data Balita")
    st.dataframe(df)

    if st.button("Prediksi Status Gizi"):
        df['Status Gizi'] = df.apply(predict_status_gizi, axis=1)

        st.subheader("Hasil Prediksi Status Gizi")
        st.dataframe(df)

        def to_excel(df):
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Sheet1')
            return output.getvalue()

        excel_data = to_excel(df)

        st.download_button(
            label="Download File Hasil Prediksi",
            data=excel_data,
            file_name='data_status_gizi_balita.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
