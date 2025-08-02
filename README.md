# Exemplo: Pub/Sub + Temporal + Saga (Python)

Este projeto demonstra como integrar Google Cloud Pub/Sub com Temporal.io para orquestrar uma transação distribuída com rollback usando o padrão Saga.

## Requisitos

- Conta no GCP com Pub/Sub habilitado
- Python 3.10+
- Docker (para rodar o Temporal localmente)
- gcloud SDK

## Passos

1. Crie o tópico e a subscrição:

```bash
gcloud pubsub topics create pedidos
gcloud pubsub subscriptions create temporal-trigger \
  --topic=pedidos \
  --push-endpoint=http://localhost:8080/pubsub \
  --ack-deadline=60
```

2. Suba o Temporal localmente:

```bash
git clone https://github.com/temporalio/docker-compose.git
cd docker-compose
docker-compose up
```

3. Instale as dependências e execute:

```bash
pip install -r requirements.txt
python worker.py
```

4. Em outro terminal:

```bash
python server.py
```

5. Publique um evento:

```bash
gcloud pubsub topics publish pedidos --message="12345"
```

Acompanhe a execução em http://localhost:8233
