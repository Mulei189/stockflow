from sqlalchemy import Column, Integer, Numeric, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from core.database import Base


class Purchase(Base):
    __tablename__ = "purchases"

    id = Column(Integer, primary_key=True, index=True)

    supplier_id = Column(
        Integer,
        ForeignKey("suppliers.id"),
        nullable=False
    )

    total_amount = Column(
        Numeric(12, 2),
        nullable=False,
        default=0
    )

    status = Column(
        String(50),
        nullable=False,
        default="received"
    )

    purchase_date = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now()
    )

    supplier = relationship(
        "Supplier",
        back_populates="purchases"
    )

    items = relationship(
        "PurchaseItem",
        back_populates="purchase",
        cascade="all, delete-orphan"
    )


class PurchaseItem(Base):
    __tablename__ = "purchase_items"

    id = Column(Integer, primary_key=True, index=True)

    purchase_id = Column(
        Integer,
        ForeignKey("purchases.id"),
        nullable=False
    )

    product_id = Column(
        Integer,
        ForeignKey("products.id"),
        nullable=False
    )

    quantity = Column(
        Integer,
        nullable=False
    )

    unit_cost = Column(
        Numeric(12, 2),
        nullable=False
    )

    subtotal = Column(
        Numeric(12, 2),
        nullable=False
    )

    purchase = relationship(
        "Purchase",
        back_populates="items"
    )

    product = relationship(
        "Product"
    )