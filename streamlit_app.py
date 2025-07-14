import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas

# Título do app
st.title("Customize Your Smoothie!")
st.write("Choose the fruits you want in your custom Smoothie!")

# Entrada de nome do pedido
name_on_order = st.text_input("Name on Smoothie:")
st.write('The name on your Smoothie will be:', name_on_order)

# Obter a sessão ativa do Snowflake
cnx = st.connection('snowflake')
session = cnx.session()

# Buscar as colunas FRUIT_NAME e SEARCH_ON
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))

# Converter para DataFrame do Pandas para facilitar a busca
pd_df = my_dataframe.to_pandas()

# Criar a lista de frutas para o usuário a partir da coluna 'FRUIT_NAME'
fruit_list = pd_df['FRUIT_NAME'].tolist()

# Multiselect para escolher até 5 frutas
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    fruit_list,
    max_selections=5
)

# Se o usuário escolheu ingredientes, processar
if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        # Adiciona a fruta à string de ingredientes
        ingredients_string += fruit_chosen + ' '

        # Usa o Pandas para encontrar o valor de busca correto na coluna SEARCH_ON
        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]

        st.subheader(fruit_chosen + ' Nutrition Information')
        
        # --- MODIFICAÇÃO PRINCIPAL: Atualizar a URL da API ---
        # A chamada agora é feita para a API da Fruityvice, usando o valor de 'search_on'.
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + search_on )
        
        # Exibe os dados nutricionais retornados pela nova API
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)

    # Prepara a declaração SQL para inserir o pedido
    my_insert_stmt = """
        INSERT INTO smoothies.public.orders(ingredients, name_on_order)
        VALUES ('{}', '{}')
    """.format(ingredients_string, name_on_order)

    # Cria o botão para enviar o pedido
    time_to_insert = st.button('Submit Order')

    # Se o botão for clicado, executa a inserção e mostra a mensagem de sucesso
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")


