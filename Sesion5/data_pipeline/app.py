import pandas as pd 
from sqlalchemy import create_engine
import logging
import sys 
from config import DATABASE_CONFIG,CSV_FILES,LOG_FILE

# configuracion de logging
# 2025-'1-25 10.29 - info -hay duplicados

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,  # O el nivel deseado
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def create_db_engine(config):
    """
    Crea uan conexion a la base de datos mysql
    """
    try:
        engine = create_engine(
            f"mysql+mysqlconnector://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}")
        logging.info("conexion establecido correctamente")
        return engine
    except Exception as e:
        logging.error(f"error al conectarse a la base de datos. {e}")   
        sys.exit(1) 

def read_csv(file_path):
    """
    Valida Carga de archivo csv
    """    
    try:
        df =pd.read_csv(file_path)
        logging.info(f"archivo {file_path} leido correctamente")
        return df

    except Exception as e: 
        logging.error(f"error  al leer el archivo {file_path}")     
        sys.exit(1) 

def transform_department(df):
    """
    Validacion de departamentos duplicados
    """
    if df['department_name'].duplicated().any():
        logging.warning(f"hay departamentos duplicados")  

    return df                   

def transform_customers(df):
    """
    Valida inconsistencia de data en el df customers_df
    """
    df['customer_email']=df['customer_email'].str.lower()

    if df[['customer_fname','customer_lname']].isnull().any().any():
        logging.error('Datos faltantes en el dataframe')
        sys.exit(1) 
    return df  

def transform_categories(df,departments_df):
    """
    Valida inconsistencia de data entre los df  category_df y depatments_df
    """
    valid_ids=set(departments_df['department_id'])
    if not df['category_department_id'].isin(valid_ids).all():
        logging.error('hay category_department_id  que no existen en los departamentos ')
        sys.exit(1) 
    return df    

def transform_products(df,category_df):
    """
    Valida inconsistencia de data entre los df  products_df y category_df
    """
    valid_ids=set(category_df['category_id'])
    if not df['product_category_id'].isin(valid_ids).all():
        logging.error('hay product_category_id  que no existen en los categoria ')
        sys.exit(1) 
    return df   


def transform_order_items(df,orders_df,products_df):
    """
    Valida inconsistencia de data entre los df products y order_items
    """
    valida_order_ids= set(orders_df['order_id'])
    if not df['order_item_order_id'].isin(valida_order_ids).all():
        logging.error('hay order_item_order_id  que no existen en las ordenes ')
        sys.exit(1)

    valid_product_ids=set(products_df['product_id'])
    if not df['order_item_product_id'].isin(valid_product_ids).all():
        logging.error('hay order_item_product_id  que no existen en los producto ')
        sys.exit(1) 

    calculated_subtotal= df['order_item_quantity']*df['order_item_product_price']
    if not (df['order_item_subtotal']==calculated_subtotal).all():
        logging.info('Recalculando order_item_subtotal ')
        df['order_item_subtotal']=calculated_subtotal


    return df   

def transform_orders(df, customers_df):
    """
    Valida inconsistencia de data entre los df order_df y customers_df
    """

    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
    if df['order_date'].isnull().any():
        logging.error("Hay valores invalidos en order_date")
        sys.exit(1)
    
    valid_ids = set(customers_df['customer_id'])
    if not df['order_customer_id'].isin(valid_ids).all():
        logging.error("Hay order_customer_id que no existen en customers")
        sys.exit(1)
    
    return df

def load_data(engine,table_name, df , if_exists='append'):
    """
    Carga de DataFrame de pandas a una tabla de Mysql
    """
    try:
        df.to_sql(name=table_name , con= engine ,if_exists= if_exists , index=False)
        logging.info(f"Datos cargados exitosamente a la tabla {table_name}")

    except Exception as e:
        logging.error(f"error al cargar a la tabla {table_name}: {e}")
        sys.exit(1)

def main():
    # Crear conexión a la base de datos
    engine = create_db_engine(DATABASE_CONFIG)
    
    # Orden de carga para respetar las dependencias de claves foráneas
    load_order = ['departments', 'categories', 'customers', 'products', 'orders', 'order_items']
    
    # Diccionario para almacenar DataFrames transformados
    dataframes = {}
    
    # Leer y transformar cada tabla
    # 1. Departments
    departments_df = read_csv(CSV_FILES['departments'])
    departments_df = transform_department(departments_df)
    dataframes['departments'] = departments_df
    
    # 2. Categories
    categories_df = read_csv(CSV_FILES['categories'])
    categories_df = transform_categories(categories_df, departments_df)
    dataframes['categories'] = categories_df
    
    # 3. Customers
    customers_df = read_csv(CSV_FILES['customers'])
    customers_df = transform_customers(customers_df)
    dataframes['customers'] = customers_df
    
    # 4. Products
    products_df = read_csv(CSV_FILES['products'])
    products_df = transform_products(products_df, categories_df)
    dataframes['products'] = products_df
    
    # 5. Orders
    orders_df = read_csv(CSV_FILES['orders'])
    orders_df = transform_orders(orders_df, customers_df)
    dataframes['orders'] = orders_df
    
    # 6. Order Items
    order_items_df = read_csv(CSV_FILES['order_items'])
    order_items_df = transform_order_items(order_items_df, orders_df, products_df)
    dataframes['order_items'] = order_items_df
    
    # Cargar datos en MySQL en el orden correcto
    for table in load_order:
        load_data(engine, table, dataframes[table], if_exists='append')
    
    logging.info("Pipeline de datos ejecutado exitosamente.")


if __name__ == "__main__":
    main()       