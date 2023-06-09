import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError


########################## start
streamlit.title('My Parents New Healthy Dinner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔Hard-boiled Free Range Egg')
streamlit.text('🥑🍞Avocado Toast')

########################## pandas
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
# Display the table on the page.
streamlit.dataframe(fruits_to_show)

# 1U7YhSzv4V7EpS0pAqF-8TIiGfuxBtIM3gMpEnO8uCVo


########################## requests
streamlit.header("Fruityvice Fruit Advice!")

#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
#streamlit.text(fruityvice_response) #just writes data to the screen
#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + "kiwi")


def get_fruityvice_data(this_fruit_choice):
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
        fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
        return fruityvice_normalized

try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?') #,'Kiwi')
    if not fruit_choice:
        streamlit.error("Please select a fruit to get information.")
    else:
        # streamlit.write('The user entered ', fruit_choice)
        # fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
        # # fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
        back_from_function = get_fruityvice_data(fruit_choice)
        streamlit.dataframe(back_from_function)  

except URLError as e:
    streamlit.error()

########################### secrets file in the app
# [snowflake]
# user = "asydmr"
# password = "xyz"
# account = "TR12345.eu-west-1" 
# warehouse = "pc_rivery_wh" 
# database = "pc_rivery_db" 
# schema = "public"
# role = "pc_rivery_role"


########################## snowflake.connector
# my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
# my_cur = my_cnx.cursor()
# my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
# my_cur.execute("use warehouse compute_wh") 
#my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
# my_data_row = my_cur.fetchone()
# streamlit.text("Hello from Snowflake:")

##########################
streamlit.header("View Our Fruit List - Add Your Favorites!")

def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("select * from fruit_load_list")
        return my_cur.fetchall()
# add a button to load the fruit
if streamlit.button('Get Fruit List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    my_cnx.close()
    streamlit.dataframe(my_data_rows)
# streamlit.text(my_data_row)my_data_row = my_cur.fetchone()
# my_data_rows = my_cur.fetchall()
# streamlit.dataframe(my_data_rows)



# streamlit.stop()
def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into  pc_rivery_db.public.fruit_load_list values('"+new_fruit+"')")
        streamlit.write('Thanks for adding ', new_fruit)

add_my_fruit = streamlit.text_input('What fruit would you like to add?') #,'jackfruit')
if streamlit.button('Add a Fruit to the List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    insert_row_snowflake(add_my_fruit)



