import streamlit as st
import pandas as pd
from pycaret.regression import RegressionExperiment

# Cargar el dataset
datos = pd.read_csv('/mnt/data/heart-disease.csv')

# Inicializar PyCaret
ExperimentoRegresion = RegressionExperiment()
ExperimentoRegresion.setup(datos, target='target', session_id=123, silent=True)

# Entrenar el modelo Bayesian Ridge
modelo_br = ExperimentoRegresion.create_model('br')

# Título de la App
st.title("Predicción de Enfermedad Cardíaca 🫀")

# Ingresar valores para la predicción
st.sidebar.header("Ingrese los datos del paciente")

# Crear campos para cada característica (ajustar según el dataset)
input_data = {}
for col in datos.columns:
    if col != 'target':  # No pedimos el target porque queremos predecirlo
        input_data[col] = st.sidebar.number_input(f"{col}", value=float(datos[col].mean()))

# Convertir entrada en DataFrame
input_df = pd.DataFrame([input_data])

# Botón para predecir
if st.sidebar.button("Predecir"):
    prediccion = ExperimentoRegresion.predict_model(modelo_br, data=input_df)
    st.subheader("Resultado de la Predicción:")
    st.write(f"Probabilidad de enfermedad cardíaca: **{prediccion['Label'][0]:.2f}**")

# Mostrar información adicional
st.write("Este modelo usa **Bayesian Ridge Regression** para predecir el riesgo de enfermedad cardíaca basado en datos históricos.")