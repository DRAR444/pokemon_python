import hug
import mysql.connector, json

# Connection à la BDD
conn = mysql.connector.Connect(host="localhost", user="root", password="", database="pokemon")

# Première méthode qui retourne les pokemons
@hug.get('/', output=hug.output_format.json)
def getPokemon():
    cursor = conn.cursor()
    cursor.execute("""SELECT t.*, p.*
    FROM pokemon AS p
    LEFT JOIN pokemon_type AS pt ON pt.pokemon_id  = p.id
    LEFT JOIN type AS t ON pt.type_id  = t.id""")
    result = cursor.fetchall()
    return json.dumps(result)

# Deuxième méthode qui ajoute un pokemon
@hug.post('/', output=hug.output_format.json)
def postPokemon(body):
    values = []
    for element in body.values():
        values.append(element)

    cursor = conn.cursor()
    try:
        cursor.execute("""INSERT INTO pokemon (attack, defense, hp, name, pokemon_id, sp_atk, sp_def, speed, total) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""", sorted(values))
        conn.commit()
    except:
        return "ERROR"

    return json.dumps("it work")

# Troisième méthode qui modifie un pokemon existant
@hug.put('/', output=hug.output_format.json)
def putPokemon(body):
    query = ""
    for key, val in body.items():
        if key != 'id':
            query = query + ", " + str(key) + " = " + "'" + str(val.decode('utf-8').splitlines()[0]) + "'"
    query = query[1:]
    cursor = conn.cursor()
    try:
        cursor.execute("""UPDATE pokemon SET name = %s WHERE id = %s""", [query, body.get("id")])
        conn.commit()
    except:
        return "ERROR"

    return json.dumps("it work")

# Quatrième méthode qui supprime un pokemon
@hug.delete('/', output=hug.output_format.json)
def deletePokemon(body):
    cursor = conn.cursor()
    print(body.get("id"))
    try:
        cursor.execute("""DELETE FROM pokemon WHERE pokemon.id = %s""", [str(body.get("id"))])
        conn.commit()
    except:
        return "ERROR"

    return json.dumps("it work")