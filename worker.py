import asyncio
from temporalio.worker import Worker
from workflows import SagaPedidoWorkflow
import activities

async def main():
    from temporalio.client import Client
    client = await Client.connect("localhost:7233")
    worker = Worker(
        client,
        task_queue="saga-pedidos",
        workflows=[SagaPedidoWorkflow],
        activities=[
            activities.reservar_estoque,
            activities.processar_pagamento,
            activities.confirmar_entrega,
            activities.estornar_pagamento,
            activities.libertar_estoque,
        ],
    )
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())
