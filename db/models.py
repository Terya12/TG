from os import getenv


from sqlalchemy.orm import DeclarativeBase, Mapped, relationship, Session
from sqlalchemy.orm import mapped_column
from sqlalchemy import (
    String,
    Integer,
    BigInteger,
    DECIMAL,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy import create_engine

from dotenv import load_dotenv

load_dotenv()

DB_USER = getenv("DB_USER")
DB_PASS = getenv("DB_PASS")
DB_ADDRESS = getenv("DB_ADDRESS")
DB_NAME = getenv("DB_NAME")
DB_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_ADDRESS}/{DB_NAME}"

engine = create_engine(DB_URL)


class Base(DeclarativeBase):
    pass


class Users(Base):
    # Таблица пользователей
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    telegram: Mapped[int] = mapped_column(BigInteger, unique=True)
    phone: Mapped[str] = mapped_column(String(30), nullable=True)

    carts: Mapped[list["Cart"]] = relationship("Cart", back_populates="user_cart")

    def __str__(self):
        return self.name


class Cart(Base):
    # Временная корзика покупателя, используется до кассы
    __tablename__ = "carts"

    id: Mapped[int] = mapped_column(primary_key=True)
    total_price: Mapped[DECIMAL] = mapped_column(
        DECIMAL(12, 2),
        default=0,
    )
    total_product: Mapped[int] = mapped_column(default=0)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        unique=True,
    )

    user_cart: Mapped[Users] = relationship(back_populates="carts")
    finally_id: Mapped[list["Finally_carts"]] = relationship(
        "Finally_carts", back_populates="user_carts"
    )

    def __str__(self):
        return str(self.id)


class Finally_carts(Base):
    # Окончательная корзина пользователя, возле кассы
    __tablename__ = "finally_carts"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_name: Mapped[str] = mapped_column(String(50))
    finally_price: Mapped[DECIMAL] = mapped_column(
        DECIMAL(12, 2),
        default=0,
    )
    quantity: Mapped[int]

    card_id: Mapped[int] = mapped_column(
        ForeignKey("carts.id"),
        unique=True,
    )
    user_carts: Mapped[Cart] = relationship(back_populates="finally_id")

    __table_args__ = (UniqueConstraint("card_id", "product_name"),)

    def __str__(self):
        return self.id


class Categories(Base):
    # Категории продуктов
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    category_name: Mapped[str] = mapped_column(
        String(50),
        unique=True,
    )
    products: Mapped[list["Products"]] = relationship(
        "Products", back_populates="product_category"
    )

    def __str__(self):
        return self.category_name


class Products(Base):
    # Продукты
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_name: Mapped[str] = mapped_column(
        String(50),
        unique=True,
    )
    description: Mapped[str] = mapped_column(nullable=True)
    image: Mapped[str] = mapped_column(String(100))
    price: Mapped[int] = mapped_column(DECIMAL(12, 2), default=0)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    product_category: Mapped["Categories"] = relationship(
        "Categories", back_populates="products"
    )


def main():
    Base.metadata.create_all(engine)
    categories = ("Лаваши", "Донары", "Хот-доги", "Десерты", "Соусы")
    products = (
        (1, "Мини Лаваш", 100, "Мясо, тесто, помидоры", "media/lavash/lavash_1.jpg"),
        (1, "Мини Говяжий", 120, "Мясо, тесто, помидоры", "media/lavash/lavash_2.jpg"),
        (
            1,
            "Мини с сыром",
            110,
            "Мясо, тесто, помидоры, сыр",
            "media/lavash/lavash_3.jpg",
        ),
        (2, "Гамбургер", 80, "Мясо, тесто, помидоры", "media/donar/donar_1.jpg"),
        (2, "Дамбургер", 110, "Мясо, тесто, помидоры", "media/lavash/donar_2.jpg"),
        (2, "Чисбургер", 130, "Мясо, тесто, помидоры", "media/lavash/donar_3.jpg"),
    )

    with Session(engine) as session:
        for category in categories:
            query = Categories(category_name=category)
            session.add(query)
            session.commit()

        for product in products:
            query = Products(
                category_id=product[0],
                product_name=product[1],
                price=product[2],
                description=product[3],
                image=product[4],
            )
            session.add(query)
            session.commit()


if __name__ == "__main__":
    main()
