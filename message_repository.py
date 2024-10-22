import psycopg2
from psycopg2 import sql

from utils_files import generate_uuid

# Configurações de conexão
conn = psycopg2.connect(
    dbname="demo_db",
    user="demo",
    password="demo@2024",
    host="localhost",
    port="5432"
)


# Função para criar uma nova mensagem
def create_message(role, content):
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO message (role, content, chat_id) VALUES (%s, %s, %s) RETURNING id",
            (role, content, str(generate_uuid())))
        conn.commit()
        return cur.fetchone()[0]


# Função para adicionar uma mensagem pelo id_conversa
def create_message_by_chat_id(chat_id, role, content):
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO message (role, content, chat_id) VALUES (%s, %s, %s) RETURNING id",
            (role, content, chat_id))
        conn.commit()
        return cur.fetchone()[0]


# Função para ler mensagens
def read_messages():
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM message order by id")
        messages = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]
        return [dict(zip(column_names, message)) for message in messages]


def read_messages():
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM message order by id")
        messages = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]
        return [dict(zip(column_names, message)) for message in messages]


def read_distinct_chats():
    with conn.cursor() as cur:
        cur.execute("select distinct message.chat_id from message")
        messages = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]
        return [dict(zip(column_names, message)) for message in messages]


# Função para buscar mensagens por id
def get_message_by_id(id):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM message WHERE id = %s", (id,))
        message = cur.fetchone()
        if message:
            column_names = [desc[0] for desc in cur.description]
            return dict(zip(column_names, message))
        return None


# Função para buscar mensagens por id_conversa
def get_message_by_chat_id(chat_id):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM message WHERE chat_id = %s", (chat_id,))
        message = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]
        return [dict(zip(column_names, message)) for message in message]


# Função para atualizar uma mensagem
def update_message(chat_id, role=None, content=None):
    with conn.cursor() as cur:
        query = sql.SQL("UPDATE message SET {fields} WHERE chat_id = %s").format(
            fields=sql.SQL(", ").join(
                sql.Composed([sql.Identifier(k), sql.SQL(" = "), sql.Placeholder(k)]) for k in
                ["role", "content"] if locals()[k] is not None
            )
        )
        cur.execute(query,
                    {k: v for k, v in locals().items() if k in ["role", "content"] and v is not None})
        conn.commit()


# Função para deletar uma mensagem
def delete_message(id):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM message WHERE id = %s", (id,))
        conn.commit()


# Obter chats distintos
chat_ids = read_distinct_chats()
print(chat_ids)
