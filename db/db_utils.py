from decimal import Decimal
from typing import Iterable

import db
from sqlalchemy.orm.session import Session
from sqlalchemy import update, delete, select, DECIMAL
from sqlalchemy.sql.functions import func
from sqlalchemy.exc import IntegrityError


from .models import Users, Categories, Cart, Finally_carts, Products, engine

with Session(engine) as session:
    db_session = session


def db_register_user(chat_id: int, full_name: str) -> bool:
    # Первая регистрация пользователя с доступными данными
    try:
        query = Users(name=full_name, telegram=chat_id)
        db_session.add(query)
        db_session.commit()
        return True
    except IntegrityError:
        db_session.rollback()
        return False


def db_update_user(chat_id: int, phone: str):
    # Дополняем данные пользователя телефоном
    query = update(Users).where(Users.telegram == chat_id).values(phone=phone)
    db_session.execute(query)
    db_session.commit()


def db_create_user_cart(chat_id: int):
    # Создание временной корзинки
    try:
        subquery = db_session.scalar(select(Users).where(Users.telegram == chat_id))
        query = Cart(user_id=subquery.id)
        db_session.add(query)
        db_session.commit()
        return True
    except IntegrityError:
        # если уже есть
        db_session.rollback()
        return False
    except AttributeError:
        # если отправил контакт анонимный пользователь
        db_session.rollback()
        return False


def db_get_user_by_telegram(chat_id) -> Users | None:
    return db_session.scalar(select(Users).where(Users.telegram == chat_id))


def db_get_all_category() -> Iterable[Categories]:
    # Получаем все категории
    query = select(Categories)
    return db_session.scalars(query).all()


def db_get_products(category_id) -> Iterable[Products] | None:
    # Получаем все продукты
    query = select(Products).where(Products.category_id == category_id)
    return db_session.scalars(query).all()


def db_get_product_by_id(product_id: int) -> Products | None:
    query = select(Products).where(Products.id == product_id)
    return db_session.scalar(query)


def db_get_user_cart(chat_id: int) -> Cart | None:
    # Получение корзины
    query = select(Cart).join(Users).where(Users.telegram == chat_id)
    return db_session.scalar(query)


def db_update_to_cart(price: DECIMAL, cart_id: int, quantity=1) -> None:
    # Добавление товаров в корзину
    query = (
        update(Cart)
        .where(Cart.id == cart_id)
        .values(
            total_price=price,
            total_product=quantity,
        )
    )
    db_session.execute(query)
    db_session.commit()
    return None


def db_get_product_by_name(product_name) -> Products | None:
    query = select(Products).where(Products.product_name == product_name)
    return db_session.scalar(query)


def db_insert_or_upd_finally_cart(
    cart_id,
    product_name,
    total_products,
    total_price,
) -> bool:
    # Постоянная корзина
    try:
        query = Finally_carts(
            card_id=cart_id,
            product_name=product_name,
            quantity=total_products,
            finally_price=total_price,
        )
        db_session.add(query)
        db_session.commit()
        return True
    except IntegrityError:
        db_session.rollback()
        query = (
            update(Finally_carts)
            .where(Finally_carts.product_name == product_name)
            .where(Finally_carts.card_id == cart_id)
            .values(
                quantity=total_products,
                finally_price=total_price,
            )
        )
        db_session.execute(query)
        db_session.commit()
        return False


def db_get_total_price(chat_id: int) -> DECIMAL:
    # Получение общей суммы пользователя из корзины
    query = (
        select(func.sum(Finally_carts.finally_price))
        .join(Finally_carts.user_carts)
        .join(Cart.user_cart)
        .where(Users.telegram == chat_id)
    )
    result = db_session.scalar(query)
    return result or Decimal(0)


def db_get_cart_products(chat_id: int) -> Iterable | None:
    query = (
        select(
            Finally_carts.product_name,
            Finally_carts.quantity,
            Finally_carts.finally_price,
            Finally_carts.card_id,
        )
        .join(Finally_carts.user_carts)
        .join(Cart.user_cart)
        .where(Users.telegram == chat_id)
    )

    result = db_session.execute(query).all()
    return result
