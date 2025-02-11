import telebot
from telebot import types
import requests

TOKEN = "7646905313:AAEMMC26UQSzeyigKKvanKnYpfV7lyiunP0"
bot = telebot.TeleBot(TOKEN)



""" INICIO COMANDOS """
# Función para manejar el comando /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Hola Dave, ¿En qué puedo ayudarte?\n\nOpciones:\n🍕 /pizza\n🎬 /recopeli Te recominedo una peli\n🔍 /buscapelis Buscador de películas\n📸 /foto cheeeeese\n👾 /help")

# Función para manejar el comando /help
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(
        message.chat.id, "Prueba alguno de mis comandos:/start, /help, /pizza, /peliculas, /buscapelis, /foto"
        )

# Función para manejar el comando /pizza
@bot.message_handler(commands=['pizza'])
def send_options(message):
    markup = types.InlineKeyboardMarkup(row_width=2)

    btnSi = types.InlineKeyboardButton('Si', callback_data='pizza_si')
    btnNo = types.InlineKeyboardButton('No', callback_data='pizza_no')

    markup.add(btnSi, btnNo)

    bot.send_message(
        message.chat.id, "¿Te gusta la pizza?", reply_markup=markup
        )

# Función para manejar el comando /recopeli
#@bot.message_handler(commands=['recopeli'])
@bot.message_handler(func=lambda message: message.text == '🎬 Recomendar Película')
def send_options_movie(message):
    markup = types.InlineKeyboardMarkup(row_width=3)

    btnDrama = types.InlineKeyboardButton('🎭 Drama', callback_data='drama')
    btnComedia = types.InlineKeyboardButton('😂 Comedia', callback_data='comedia')
    btnAccion = types.InlineKeyboardButton('💥 Acción', callback_data='accion')

    markup.add(btnDrama, btnComedia, btnAccion)

    bot.send_message(
        message.chat.id, "¿Qué tipo de película te gusta?", reply_markup=markup
        )

# Función para manejar el comando /buscapelis
@bot.message_handler(commands=['buscapelis'])
def send_movie(message):
    movie = message.text.split()[1] if len(message.text.split()) > 1 else None
    if movie:
        peliculas = get_movie(movie)
        if peliculas:
            bot.send_message(message.chat.id, "Estas son las primeras 5 películas que encontré:")
            for title, year, poster, imdbID in peliculas:
                bot.send_photo(
                    chat_id=message.chat.id,
                    photo=poster,
                    caption=f"Título: {title} - Año: {year}",
                    reply_markup=types.InlineKeyboardMarkup().add(
                        types.InlineKeyboardButton(
                            text="Ver más",
                            url=f"https://www.imdb.com/title/{imdbID}/"
                        )
                    )
                )
        else:
            bot.send_message(message.chat.id, "No encontré ninguna película con ese nombre")
    else:
        bot.send_message(message.chat.id, "Por favor, escribe el nombre de la película que quieres buscar después del comando.\n\nEjemplo: /buscapelis batman")    

# Función para manejar el comando /foto
@bot.message_handler(commands=['foto'])
def send_photo(message):
    imgUrl = "https://i.namu.wiki/i/pPOtKyvbPzc-cysHyks0Q-fDYoDj1nynmlhdbRyTmpoqKyZ7W8MV3VCg-dgeGFbW9zNgB335Z2InmtIQcyU3F4An4vt3WliszK_J_RJAs-qoSqdghst3G0ZSr9QWU0wGoqoOJ4MqHq7LbBayVQ8u_w.webp"
    bot.send_photo(chat_id=message.chat.id,
                   photo=imgUrl,
                   caption="Este soy yo, Dave"
    )

""" FIN COMANDOS """


""" INICIO CALLBACKS """

# Función para manejar los callbacks de los botones
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'pizza_si':
        bot.send_message(call.message.chat.id, "¡Genial! ¿De qué sabor?")
    elif call.data == 'pizza_no':
        bot.send_message(call.message.chat.id, "¡Qué lástima!")
    elif call.data == 'drama':
        bot.send_message(call.message.chat.id, "🎭 Te recomiendo 'El Padrino'")
    elif call.data == 'comedia':
        bot.send_message(call.message.chat.id, "😂 Te recomiendo 'Mi pobre angelito'")
    elif call.data == 'accion':
        bot.send_message(call.message.chat.id, "💥 Te recomiendo 'John Wick'")    

# Función para manejar cualquier mensaje
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if "hola" in message.text.lower():
        bot.reply_to(message, "Hola, ¿En qué puedo ayudarte?")

""" FIN CALLBACKS """


""" IMPLEMENTACIÓN API DE PELIS """

def get_movie(movie):
    url = f"http://www.omdbapi.com/?i=tt3896198&apikey=76146b9f&s={movie}&page=1"
    response = requests.get(url)
    dataMovie = response.json()

    pelis_info = []
    
    if dataMovie['Response'] == 'True':
       for movie in dataMovie['Search'][:5]:
           title = movie['Title']
           year = movie['Year']
           poster = movie['Poster']
           imdbID = movie['imdbID']
           pelis_info.append((title, year, poster, imdbID))
           
    return pelis_info


print("Bot is running")

if __name__ == "__main__":
    bot.polling(none_stop=True)