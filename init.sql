-- Criação da tabela
CREATE TABLE message
(
    id      SERIAL PRIMARY KEY,
    role    TEXT NOT NULL,
    content TEXT NOT NULL,
    chat_id TEXT NOT NULL
);

-- Inserção de dados na tabela
INSERT INTO message (role, content, chat_id)
VALUES ('human', 'Olá', '5fe36eaf-5c06-4e12-bd70-bbd8c897c491'),
       ('ai', 'Olá, tudo bem?', '5fe36eaf-5c06-4e12-bd70-bbd8c897c491')