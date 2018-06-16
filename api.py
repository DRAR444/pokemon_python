import requests
import mysql.connector
from bs4 import BeautifulSoup

# Connection � la BDD
cnx = mysql.connector.Connect(host="localhost", user="root", password="", database="pokemon")
cursor = cnx.cursor()

url = "https://pokemondb.net/pokedex/all"

response = requests.get(url)
html = str(response.content)
soup = BeautifulSoup(html, "html.parser")

#Cr�ation de la table type:
cursor.execute("""CREATE TABLE IF NOT EXISTS type (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, name VARCHAR(100) UNIQUE KEY);""")
#Cr�ation de la table type_pokemon :
cursor.execute("""CREATE TABLE IF NOT EXISTS pokemon (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, pokemon_id int(11), name VARCHAR(100), total VARCHAR(100), hp VARCHAR(100), attack VARCHAR(100), defense VARCHAR(100), sp_atk VARCHAR(100), sp_def VARCHAR(100), speed VARCHAR(100));""")
#Cr�ation de la table pokemon_type :
cursor.execute("""CREATE TABLE IF NOT EXISTS pokemon_type (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, pokemon_id INT(11), type_id INT(11));""")


cursor.execute("""SET FOREIGN_KEY_CHECKS=0""")
cursor.execute("""TRUNCATE TABLE pokemon""")
cursor.execute("""TRUNCATE TABLE type""")
cursor.execute("""TRUNCATE TABLE pokemon_type""")
cursor.execute("""SET FOREIGN_KEY_CHECKS=1""")


tab = soup.find(id="pokedex")
for link in tab.find_all("tr"):
    tab = []
    for l in link.find_all("td"):
        tab.append(l.text)
    if len(tab) > 0:
        types = re.findall('[A-Z][^A-Z]*', tab[2])
        del tab[2]
        cursor.execute("""INSERT INTO pokemon (pokemon_id, name, total, hp, attack, defense, sp_atk, sp_def, speed) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""", tab)
        lastPokemonId = cursor.lastrowid
        for t in types:
            try:
                cursor.execute("""INSERT INTO type (name) VALUES (%s)""", [t])
                typeId = cursor.lastrowid
            except:
                cursor.execute("""SELECT id FROM type WHERE name = %s LIMIT 1""", (t,))
                typeId = cursor.fetchall()[0][0]
            cursor.execute("""INSERT INTO pokemon_type (pokemon_id, type_id) VALUES (%s, %s)""", [lastPokemonId, typeId])

cnx.commit()
cnx.close()