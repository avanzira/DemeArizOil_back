# src/app/tests/test_full_flow.py
import pytest
from httpx import AsyncClient
from src.app.main import app


@pytest.mark.asyncio
async def test_full_flow_simplified():

    async with AsyncClient(app=app, base_url="http://test") as client:

        # 1) LOGIN
        login = await client.post(
            "/auth/login",
            json={"username": "Amadou", "password": "123456"}
        )
        assert login.status_code == 200
        headers = {"Authorization": f"Bearer {login.json()['access_token']}"}

        # ------------------------------------------
        # 2) CREAR O RECUPERAR PRODUCTO
        # ------------------------------------------
        product_payload = {
            "name": "Gasoil Premium",
            "unit_measure": "litros",
            "is_inventory": True
        }

        # Intentar crearlo
        res = await client.post("/products/", json=product_payload, headers=headers)

        if res.status_code == 400:
            # Ya existe → obtenerlo
            list_res = await client.get("/products/", headers=headers)
            assert list_res.status_code == 200
            product = next(p for p in list_res.json() if p["name"] == "Gasoil Premium")
            product_id = product["id"]
        else:
            assert res.status_code == 200
            product_id = res.json()["id"]

        # ------------------------------------------
        # 3) CREAR O RECUPERAR SUPPLIER
        # ------------------------------------------
        supplier_payload = {
            "name": "Proveedor Dakar Oil",
            "phone": "22177000000",
            "email": "info@dakaroil.com",
            "address": "Dakar"
        }

        res = await client.post("/suppliers/", json=supplier_payload, headers=headers)

        if res.status_code == 400:
            list_res = await client.get("/suppliers/", headers=headers)
            assert list_res.status_code == 200
            supplier = next(s for s in list_res.json() if s["name"] == "Proveedor Dakar Oil")
            supplier_id = supplier["id"]
        else:
            assert res.status_code == 200
            supplier_id = res.json()["id"]

        # ------------------------------------------
        # 4) CREAR O RECUPERAR CUSTOMER
        # ------------------------------------------
        customer_payload = {
            "name": "Cliente Moussa",
            "phone": "22178000000",
            "email": "cliente@moussa.com",
            "address": "Dakar"
        }

        res = await client.post("/customers/", json=customer_payload, headers=headers)

        if res.status_code == 400:
            list_res = await client.get("/customers/", headers=headers)
            assert list_res.status_code == 200
            customer = next(c for c in list_res.json() if c["name"] == "Cliente Moussa")
            customer_id = customer["id"]
        else:
            assert res.status_code == 200
            customer_id = res.json()["id"]

        # ------------------------------------------
        # 5) CREAR PURCHASE
        # ------------------------------------------
        purchase_payload = {
            "supplier_id": supplier_id,
            "account_id": 1,
            "lines": [
                {"product_id": product_id, "quantity": 260, "unit_price": 400}
            ],
            "paid": 54000
        }

        res = await client.post("/purchase-notes/", json=purchase_payload, headers=headers)
        assert res.status_code == 200 or res.status_code == 400

        if res.status_code == 200:
            print(res.status_code, res.json())
            purchase_id = res.json()["id"]
        else:
            # Ya existe → coger la última
            list_res = await client.get("/purchase-notes/", headers=headers)
            purchase_id = list_res.json()[-1]["id"]

        # ------------------------------------------
        # 6) CREAR SALES NOTE
        # ------------------------------------------
        sale_payload = {
            "customer_id": customer_id,
            "account_id": 1,
            "lines": [
                {"product_id": product_id, "quantity": 100, "unit_price": 600}
            ]
        }

        res = await client.post("/sales-notes/", json=sale_payload, headers=headers)
        assert res.status_code == 200 or res.status_code == 400

        if res.status_code == 200:
            sale_id = res.json()["id"]
        else:
            list_res = await client.get("/sales-notes/", headers=headers)
            sale_id = list_res.json()[-1]["id"]

        # 7) PAGAR DEUDA (compatible con backend real)
        pay_payload = {
            "account_from_id": 1,
            "account_to_id": None,
            "amount": 50000,
            "purchase_id": purchase_id,
            "sales_id": None
        }

        res = await client.post("/cash/movement", json=pay_payload, headers=headers)
        assert res.status_code == 200

        # ------------------------------------------
        # 8) RENOMBRAR ENTIDADES (idempotente)
        # ------------------------------------------
        await client.put(f"/products/{product_id}", json={"name": "Gasoil Azul"}, headers=headers)
        await client.put(f"/suppliers/{supplier_id}", json={"name": "Dakar Oil SA"}, headers=headers)
        await client.put(f"/customers/{customer_id}", json={"name": "Moussa Ndiaye"}, headers=headers)

        # ------------------------------------------
        # 9) CONSULTAR LISTADOS
        # ------------------------------------------
        assert (await client.get("/purchase-notes/", headers=headers)).status_code == 200
        assert (await client.get("/sales-notes/", headers=headers)).status_code == 200
        assert (await client.get("/customers/", headers=headers)).status_code == 200
        assert (await client.get("/products/", headers=headers)).status_code == 200
        assert (await client.get("/suppliers/", headers=headers)).status_code == 200
