from temporalio import activity

@activity.defn
async def reservar_estoque(pedido_id: str):
    print(f"[OK] Estoque reservado para pedido {pedido_id}")

@activity.defn
async def processar_pagamento(pedido_id: str):
    print(f"[!] Simulando falha no pagamento do pedido {pedido_id}")
    raise Exception("Pagamento recusado")

@activity.defn
async def confirmar_entrega(pedido_id: str):
    print(f"[OK] Entrega confirmada para pedido {pedido_id}")

@activity.defn
async def estornar_pagamento(pedido_id: str):
    print(f"[ROLLBACK] Estorno do pagamento do pedido {pedido_id}")

@activity.defn
async def libertar_estoque(pedido_id: str):
    print(f"[ROLLBACK] Estoque liberado para pedido {pedido_id}")
