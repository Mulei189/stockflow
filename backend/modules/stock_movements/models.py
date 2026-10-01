from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from core.database import Base

class StockMovement(Base):
    __tablename__ = "stock_movements"
    
    id = Column(Integer, primary_key=True, index=True)
    
    product_id = Column(
        Integer,
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False
    )
    
    movement_type = Column(
        String,
        nullable=False
    )
    
    quantity = Column(
        Integer,
        nullable=False
    )
    
    reference_type = Column(
        String,
        nullable=False
    )
    
    reference_id = Column(
        Integer,
        nullable=False
    )
    
    notes = Column(
        String(255),
        nullable=True
    )
    
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    
    product = relationship("Product")