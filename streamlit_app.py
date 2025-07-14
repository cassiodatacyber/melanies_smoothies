import streamlit as st
from snowflake.snowpark.functions import col

# Título do app
st.title("Smoothie!")
st.write("Choose the fruits you want in your custom Smoothie!")

# Entrada de nome do pedido
name_on_order = st.text_input("Name on Smoothie:")
st.write('The name on your Smoothie will be:', name_on_order)

# Obter a sessão ativa do Snowflake
cnx = st.connection('snowflake')
session = cnx.session()

# Buscar a lista de frutas disponíveis
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))
fruit_list = [row['FRUIT_NAME'] for row in my_dataframe.collect()]

# Multiselect para escolher até 5 frutas
ingredients_List = st.multiselect(
    'Choose up to 5 ingredients:',
    fruit_list,
    max_selections=5
)

# Mostrar botão e processar inserção
if ingredients_List and name_on_order:
    ingredients_string = ' '.join(ingredients_List)
    my_insert_stmt = f"""
        insert into smoothies.public.orders (ingredients, name_on_order)
        values ('{ingredients_string}', '{name_on_order}')
    """

    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

 #New section to display smoothiefroot nutrition information
import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon" )
#st.text(smoothiefroot_response.json())
sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)


