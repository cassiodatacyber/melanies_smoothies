import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Título do app
st.title(" Smoothie!")
st.write("Choose the fruits you want in your custom Smoothie!")

# Entrada de nome do pedido
name_on_order = st.text_input("Name on Smoothie:")
st.write('The name on your Smoothie Will be:', name_on_order)

# Obter a sessão ativa do Snowflake
session = get_active_session()

# Buscar a lista de frutas disponíveis
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))
fruit_list = [row['FRUIT_NAME'] for row in my_dataframe.collect()]

# Multiselect para escolher até 5 frutas
ingredients_List = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
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
        # Opcional: mostrar SQL apenas quando o botão for clicado
        # st.write("Preview SQL:", my_insert_stmt)
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
