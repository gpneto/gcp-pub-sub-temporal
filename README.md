# Exemplo: Pub/Sub + Temporal + Saga (Python)

Este projeto demonstra como integrar Google Cloud Pub/Sub com Temporal.io para orquestrar uma transação distribuída com rollback usando o padrão Saga.

## Requisitos

- Conta no GCP com Pub/Sub habilitado
- Python 3.10+
- Docker (para rodar o Temporal localmente)
- gcloud SDK

## Passos

### 1. Crie o tópico e a subscrição Pull:

```bash
gcloud pubsub topics create pedidos

gcloud pubsub subscriptions create temporal-pull --topic=pedidos
```

### 2. Suba o Temporal localmente:

```bash
git clone https://github.com/temporalio/docker-compose.git
cd docker-compose
docker-compose up
```

Interface Web: http://localhost:8233  
Servidor: localhost:7233

### 3. Instale as dependências e ative o ambiente virtual:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 4. Em um terminal, execute o Worker do Temporal:

```bash
python worker.py
```

### 5. Em outro terminal, execute o consumidor Pub/Sub Pull:

```bash
python pubsub_consumer_pull.py
```

### 6. Publique um evento:

```bash
gcloud pubsub topics publish pedidos --message="12345"
```

### 7. Verifique a execução

- O worker processa o pedido
- A etapa `processar_pagamento` falha de propósito
- O workflow executa `estornar_pagamento` e `libertar_estoque`
- Acompanhe a execução via http://localhost:8233

