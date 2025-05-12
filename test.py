from openai import OpenAI
from supabase import create_client, Client
from dotenv import load_dotenv
import os

load_dotenv()

URL = os.getenv("SUPABASE_URL")
KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(URL, KEY)
client = OpenAI(api_key=os.getenv("LLM_KEY"))

#para agregar datos  a la base de datos
supabase.table("productos").insert({"product": "pan","price":2000, "quantity": 2}).execute()

update = supabase.table("productos").select("*").execute()
data = update.data

while True:
    preg_user = str(input("ingrese su pregunta:"))
    if preg_user == "salir":
        break
    response = client.chat.completions.create(
    model="gpt-4o-mini",

    messages=[
        {"role": "system", "content": f"eres un asistente que ayuda a los usuarios a crear listas de compras{data}"},
        {"role": "user", "content": preg_user}
    ]
    )
    print(response.choices[0].message.content)