from datetime import timedelta
from temporalio.common import RetryPolicy
from temporalio import workflow
from activities import (
    reservar_estoque,
    processar_pagamento,
    confirmar_entrega,
    estornar_pagamento,
    libertar_estoque,
)

@workflow.defn
class SagaPedidoWorkflow:
    @workflow.run
    async def run(self, pedido_id: str):
        try:
            await workflow.execute_activity(
                reservar_estoque,
                pedido_id,
                start_to_close_timeout=timedelta(seconds=10)
            )
            await workflow.execute_activity(
                processar_pagamento,
                pedido_id,
                start_to_close_timeout=timedelta(seconds=10),
                retry_policy=RetryPolicy(maximum_attempts=1)            )

            await workflow.execute_activity(
                confirmar_entrega,
                pedido_id,
                start_to_close_timeout=timedelta(seconds=10)
            )
        except Exception:
            await workflow.execute_activity(
                estornar_pagamento,
                pedido_id,
                start_to_close_timeout=timedelta(seconds=10)
            )
            await workflow.execute_activity(
                libertar_estoque,
                pedido_id,
                start_to_close_timeout=timedelta(seconds=10)
            )
            raise
