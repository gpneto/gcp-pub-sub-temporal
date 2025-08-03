from google.cloud import pubsub_v1
import asyncio
import uuid
from temporalio.client import Client

async def iniciar_workflow(pedido_id: str):
    client = await Client.connect("localhost:7233")
    workflow_id = f"pedido-{pedido_id}-{uuid.uuid4().hex[:6]}"
    await client.start_workflow(
        workflow="SagaPedidoWorkflow",
        id=workflow_id,
        task_queue="saga-pedidos",
        args=[pedido_id],
    )

def consumir_mensagens():
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path("projet-exemple", "temporal-pull")

    def callback(message):
        try:
            pedido_id = message.data.decode()
            print(f"Evento recebido: {pedido_id}")
            asyncio.run(iniciar_workflow(pedido_id))
            message.ack()
        except Exception as e:
            print(f"Erro ao processar mensagem: {e}")
            message.nack()

    subscriber.subscribe(subscription_path, callback=callback)
    print("Aguardando mensagens...")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Encerrado.")

if __name__ == "__main__":
    consumir_mensagens()
