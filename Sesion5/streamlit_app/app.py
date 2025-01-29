import streamlit as st
import pandas as pd
import sqlalchemy

# Configuración inicial de Streamlit
st.set_page_config(page_title="Explorador de Datos", layout="wide")

# Título de la aplicación
st.title("Explorador de Datos - MySQL")

# Sidebar para ingresar configuración de la base de datos
st.sidebar.header("Configuración de la Base de Datos")
db_host = st.sidebar.text_input("Host", value="mysql")
db_user = st.sidebar.text_input("Usuario", value="root")
db_password = st.sidebar.text_input("Contraseña", value="root", type="password")
db_name = st.sidebar.text_input("Base de Datos", value="retail_db")
db_port = st.sidebar.text_input("Puerto", value="3306")

# Función para conectarse a la base de datos
@st.cache_resource
def create_connection():
    try:
        engine = sqlalchemy.create_engine(
            f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        )
        return engine
    except Exception as e:
        st.error(f"Error al conectarse a la base de datos: {e}")
        return None

# Conexión a la base de datos
engine = create_connection()

if engine:
    st.success("Conexión establecida con la base de datos.")

    # Input para consultar datos
    st.subheader("Consulta SQL")
    query = st.text_area("Escribe tu consulta SQL aquí", value="SELECT * FROM departments LIMIT 10")

    # Ejecutar consulta y mostrar resultados
    if st.button("Ejecutar Consulta"):
        try:
            with engine.connect() as conn:
                result = pd.read_sql(query, conn)
                st.write("Resultados:")
                st.dataframe(result)

                # Descarga de resultados
                csv = result.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="Descargar Resultados en CSV",
                    data=csv,
                    file_name="resultados.csv",
                    mime="text/csv",
                )
        except Exception as e:
            st.error(f"Error al ejecutar la consulta: {e}")
else:
    st.warning("Conexión no establecida. Revisa la configuración.")

# Pie de página
st.sidebar.markdown("---")
st.sidebar.info("Desarrollado con ❤️ usando Streamlit.")
