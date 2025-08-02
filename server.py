from flask import Flask, request
from temporalio.client import Client
import asyncio

app = Flask(__name__)
client = None

@app.route("/pubsub", methods=["POST"])
def trigger_temporal():
    data = request.json.get("message", {}).get("data")
    pedido_id = data  # base64, mas aqui deixamos simples
    asyncio.run(iniciar_workflow(pedido_id))
    return "", 204

async def iniciar_workflow(pedido_id: str):
    global client
    if not client:
        client = await Client.connect("localhost:7233")
    await client.start_workflow(
        workflow="SagaPedidoWorkflow",
        id=f"pedido-{pedido_id}",
        task_queue="saga-pedidos",
        args=[pedido_id],
    )

if __name__ == "__main__":
    app.run(port=8080)
