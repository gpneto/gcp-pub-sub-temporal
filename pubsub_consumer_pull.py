from google.cloud import pubsub_v1
import base64
import asyncio
from temporalio.client import Client

async def iniciar_workflow(pedido_id: str):
    client = await Client.connect("localhost:7233")
    await client.start_workflow(
        workflow="SagaPedidoWorkflow",
        id=f"pedido-{pedido_id}",
        task_queue="saga-pedidos",
        args=[pedido_id],
    )

def consumir_mensagens():
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path("smart-school-egalite", "temporal-pull")

    def callback(message):
        pedido_id = base64.b64decode(message.data).decode()
        print(f"Evento recebido: {pedido_id}")
        asyncio.run(iniciar_workflow(pedido_id))
        message.ack()

    subscriber.subscribe(subscription_path, callback=callback)
    print("Aguardando mensagens...")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Encerrado.")

if __name__ == "__main__":
    consumir_mensagens()
