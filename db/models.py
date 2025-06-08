from sqlalchemy.orm import DeclarativeBase, Mapped, relationship, Session, mapped_column
from sqlalchemy import (
    String,
    Integer,
    BigInteger,
    DECIMAL,
    ForeignKey,
    UniqueConstraint,
    create_engine,
)
from sqlalchemy import DateTime, Enum
from datetime import datetime
import enum

from config import settings

engine = create_engine(settings.db_url)


class Base(DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    telegram: Mapped[int] = mapped_column(BigInteger, unique=True)
    phone: Mapped[str] = mapped_column(String(30), nullable=True)

    carts: Mapped[list["Cart"]] = relationship("Cart", back_populates="user_cart")

    def __str__(self):
        return self.name


class Cart(Base):
    __tablename__ = "carts"

    id: Mapped[int] = mapped_column(primary_key=True)
    total_price: Mapped[DECIMAL] = mapped_column(DECIMAL(12, 2), default=0)
    total_product: Mapped[int] = mapped_column(default=0)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), unique=True
    )

    user_cart: Mapped[Users] = relationship(back_populates="carts")
    finally_id: Mapped[list["Finally_carts"]] = relationship(
        "Finally_carts", back_populates="user_carts"
    )

    def __str__(self):
        return str(self.id)


class Finally_carts(Base):
    __tablename__ = "finally_carts"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_name: Mapped[str] = mapped_column(String(50))
    finally_price: Mapped[DECIMAL] = mapped_column(DECIMAL(12, 2), default=0)
    quantity: Mapped[int]
    card_id: Mapped[int] = mapped_column(ForeignKey("carts.id", ondelete="CASCADE"))

    user_carts: Mapped[Cart] = relationship(back_populates="finally_id")

    __table_args__ = (UniqueConstraint("card_id", "product_name"),)

    def __str__(self):
        return self.id


class Categories(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    category_name: Mapped[str] = mapped_column(String(50), unique=True)

    products: Mapped[list["Products"]] = relationship(
        "Products", back_populates="product_category"
    )

    def __str__(self):
        return self.category_name


class Products(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_name: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[str] = mapped_column(nullable=True)
    image: Mapped[str] = mapped_column(String(100))
    price: Mapped[int] = mapped_column(DECIMAL(12, 2), default=0)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="CASCADE")
    )

    product_category: Mapped["Categories"] = relationship(
        "Categories", back_populates="products"
    )


class OrderStatusEnum(enum.Enum):
    pending = "pending"
    paid = "paid"
    cancelled = "cancelled"


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    total_price: Mapped[DECIMAL] = mapped_column(DECIMAL(12, 2))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    status: Mapped[OrderStatusEnum] = mapped_column(
        Enum(OrderStatusEnum), default=OrderStatusEnum.pending
    )

    user: Mapped[Users] = relationship("Users")
    items: Mapped[list["OrderItem"]] = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"))
    product_name: Mapped[str] = mapped_column(String(50))
    price: Mapped[DECIMAL] = mapped_column(DECIMAL(12, 2))
    quantity: Mapped[int]

    order: Mapped[Order] = relationship("Order", back_populates="items")
