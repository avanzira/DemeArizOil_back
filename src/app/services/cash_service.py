# file: src/app/services/cash_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException
from decimal import Decimal

from app.core.config.database import get_session
from app.repositories.cash_account_repository import CashAccountRepository
from app.repositories.cash_movement_repository import CashMovementRepository


class CashService:
    """
    Servicio interno para registrar movimientos de efectivo.
    Incluye:
        - list_accounts()
        - list_movements() (orden descendente)
        - register_movement()
    """

    def __init__(self, db: Session | None = None):
        self.db = db or get_session()
        self.accounts = CashAccountRepository(self.db)
        self.movements = CashMovementRepository(self.db)

        # --- NUEVO ---
        self.ensure_default_accounts()


    # ------------------------------------------------------------
    # NUEVO: Crear cuentas DEME obligatorias si no existen
    # ------------------------------------------------------------
    def ensure_default_accounts(self):
        required = [
            "DEME_CASH",
            "DEME_BANK_1",
            "DEME_BANK_2",
            "DEME_BANK_3"
        ]

        existing = {acc.name for acc in self.accounts.list()}

        for name in required:
            if name not in existing:
                self.accounts.create({
                    "name": name,
                    "is_active": True
                })

    # -----------------------------
    # NUEVO → listar cuentas
    # -----------------------------
    def list_accounts(self):
        return self.accounts.list()

    # -----------------------------
    # NUEVO → listar movimientos
    # -----------------------------
    def list_movements(self):
        return (
            self.db.query(self.movements.model)
            .order_by(self.movements.model.created_at.desc())
            .all()
        )

    # -----------------------------
    # Helpers
    # -----------------------------
    def _validate_account(self, account_id: int | None):
        if account_id is None:
            return None
        acc = self.accounts.get(account_id)
        if not acc:
            raise HTTPException(404, "Cash account not found")
        return acc

    def _compute_balance(self, account_id: int) -> float:
        incoming = sum(
            m.amount for m in self.db.query(self.movements.model)
            .filter_by(account_to_id=account_id)
            .all()
        )
        outgoing = sum(
            m.amount for m in self.db.query(self.movements.model)
            .filter_by(account_from_id=account_id)
            .all()
        )
        return incoming - outgoing

    # -----------------------------
    # Registrar movimiento
    # -----------------------------
    def register_movement(
        self,
        *,
        account_from_id: int | None,
        account_to_id: int | None,
        amount: float,
        purchase_id: int | None = None,
        sales_id: int | None = None
    ):
        amount = Decimal(str(amount))
        if amount <= 0:
            raise HTTPException(400, "Amount must be > 0")

        acc_from = self._validate_account(account_from_id)
        acc_to = self._validate_account(account_to_id)

        if acc_from:
            balance = self._compute_balance(acc_from.id)
            if balance - amount < 0:
                raise HTTPException(400, f"Account {acc_from.name} cannot go negative")

        self.movements.create({
            "account_from_id": account_from_id,
            "account_to_id": account_to_id,
            "amount": amount,
            "purchase_id": purchase_id,
            "sales_id": sales_id
        })

        self.db.commit()
        return True
