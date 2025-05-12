from flask import Flask,request, jsonify
from flask_cors import CORS
from openai import OpenAI
from supabase import create_client, Client
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
CORS(app)#enables CORS for all routes

URL = os.getenv("SUPABASE_URL")
KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(URL, KEY)
client = OpenAI(api_key=os.getenv("LLM_KEY"))

update = supabase.table("productos").select("*").execute()
data = update.data

#Se crea la ruta para la API, seguido de la función que se ejecutará al entrar en la ruta

@app.route('/')
def home():
    return "Hola mundo!"

@app.route('/api/ask', methods=['POST'])
def ask_ai():
    data_received = request.form.get('question')
    # Se verifica si se recibió una pregunta
    if not data_received:
        return jsonify({'error': 'No se proporcionó ninguna pregunta'}), 400
    # Se envía la pregunta al modelo de IA y se obtiene una respuesta
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": f"eres un asistente que ayuda a los usuarios a crear listas de compras {data}"},
                {"role": "user", "content": data_received}
            ]
        )
        ai_answer = response.choices[0].message.content
        return jsonify({'answer': ai_answer}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)





# from flask import Flask, request, jsonify, render_template
# from flask_cors import CORS
# from openai import OpenAI
# from supabase import create_client, Client
# from dotenv import load_dotenv
# import os

# load_dotenv()
# app = Flask(__name__)
# CORS(app, resources={r"/api/*": {"origins": "*"}})  # Permitir solicitudes desde cualquier origen

# URL = os.getenv("SUPABASE_URL")
# KEY = os.getenv("SUPABASE_KEY")

# supabase: Client = create_client(URL, KEY)
# client = OpenAI(api_key=os.getenv("LLM_KEY"))

# update = supabase.table("productos").select("*").execute()
# data = update.data

# @app.route('/')
# def home():
#     return render_template('index.html')  # Renderizar el archivo HTML

# @app.route('/api/ask', methods=['POST'])
# def ask_ai():
#     data_received = request.form.get('question')
#     if not data_received:
#         return jsonify({'error': 'No se proporcionó ninguna pregunta'}), 400
#     try:
#         response = client.chat.completions.create(
#             model="gpt-4",
#             messages=[
#                 {"role": "system", "content": f"eres un asistente que ayuda a los usuarios a crear listas de compras {data}"},
#                 {"role": "user", "content": data_received}
#             ]
#         )
#         ai_answer = response.choices[0].message.content
#         return jsonify({'answer': ai_answer}), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True)