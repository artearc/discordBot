import discord
from discord.ext import commands
import datetime
import json  # Para manejar el almacenamiento en archivo JSON
import os    # Para verificar si el archivo existe

# Crear los intents
intents = discord.Intents.default()
intents.message_content = True  # Permitir que el bot lea el contenido de los mensajes

# Crear el bot con los intents
bot = commands.Bot(command_prefix="!", intents=intents)

# Archivo donde se guardará el historial
archivo_historial = 'historial_partidos.json'

# Variable global para almacenar el histórico
historico_partidos = []

# Función para cargar el historial desde un archivo JSON
def cargar_historial():
    global historico_partidos
    if os.path.exists(archivo_historial):
        with open(archivo_historial, 'r') as f:
            historico_partidos = json.load(f)
    else:
        historico_partidos = []

# Función para guardar el historial en un archivo JSON
def guardar_historial():
    with open(archivo_historial, 'w') as f:
        json.dump(historico_partidos, f, indent=4)

# Evento que se ejecuta cuando el bot se conecta
@bot.event
async def on_ready():
    cargar_historial()  # Cargar el historial cuando el bot se conecta
    print(f'Bot conectado como {bot.user}')

# Comando para registrar un partido de fútbol y frase (anteriormente !partido)
@bot.command()
async def racistada(ctx, equipo1: str, equipo2: str, *, frase: str):
    # Obtener el timestamp actual
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Guardar el enfrentamiento en el historial
    historico_partidos.append({
        'equipo1': equipo1,
        'equipo2': equipo2,
        'frase': frase,
        'timestamp': timestamp
    })

    # Guardar el historial actualizado en el archivo
    guardar_historial()

    # Responder en el chat con la confirmación
    await ctx.send(f"Partido registrado: {equipo1} vs {equipo2}. Frase: '{frase}' (Registrado en: {timestamp})")

# Comando para mostrar el histórico de partidos registrados (anteriormente !mostrar_historial)
@bot.command()
async def historial(ctx):
    if not historico_partidos:
        await ctx.send("No hay partidos registrados aún.")
    else:
        historial = "\n".join([f"{p['equipo1']} vs {p['equipo2']} - '{p['frase']}' (Registrado en: {p['timestamp']})" for p in historico_partidos])
        await ctx.send(f"Histórico de partidos:\n{historial}")

# Comando para borrar un partido por frase, con confirmación
@bot.command()
async def borrar(ctx, *, frase: str):
    # Buscar la frase en el historial
    partido_a_borrar = next((p for p in historico_partidos if p['frase'] == frase), None)

    if partido_a_borrar:
        # Preguntar confirmación
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        await ctx.send(f"¿Estás seguro de que deseas borrar el partido: {partido_a_borrar['equipo1']} vs {partido_a_borrar['equipo2']} con la frase '{partido_a_borrar['frase']}'? Responde con 'sí' o 'no'.")

        try:
            respuesta = await bot.wait_for('message', check=check, timeout=30.0)  # 30 segundos para responder

            if respuesta.content.lower() == 'si':
                # Borrar el partido
                historico_partidos.remove(partido_a_borrar)
                guardar_historial()  # Guardar el historial actualizado
                await ctx.send("El partido ha sido eliminado del historial.")
            else:
                await ctx.send("Operación cancelada, el partido no ha sido eliminado.")
        except:
            await ctx.send("No se recibió confirmación a tiempo. Operación cancelada.")
    else:
        await ctx.send(f"No se encontró ningún partido con la frase '{frase}'.")

# Comando que envía una imagen (anteriormente !mono)
@bot.command()
async def mono(ctx):
    # URL de la imagen que se quiere enviar
    url_imagen = "https://e00-elmundo.uecdn.es/assets/multimedia/imagenes/2023/05/22/16847456869289.jpg"
    await ctx.send(url_imagen)

# Manejo de errores para los comandos
@bot.event
async def on_command_error(ctx, error):
    await ctx.send(f"Ocurrió un error: {error}")
    print(f"Error: {error}")

# Reemplaza 'TU_TOKEN_AQUI' con tu token real de bot de Discord
bot.run('MTI5OTA1ODAwODAyNTk5MzI5OQ.Ga6txd.vU74LgzhI4IEYkBLe3uf3TQAplr1Qkn21j6qp4')
