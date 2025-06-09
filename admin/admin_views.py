from sqladmin import ModelView
from db.models import Users, Cart, Finally_carts, Categories, Products, Order, OrderItem


class UserAdmin(ModelView, model=Users):
    column_list = [Users.id, Users.name, Users.telegram, Users.phone]
    name = "User"
    name_plural = "Users"


class CartAdmin(ModelView, model=Cart):
    column_list = [Cart.id, Cart.total_price, Cart.total_product, Cart.user_id]
    name = "Cart"
    name_plural = "Carts"


class FinallyCartAdmin(ModelView, model=Finally_carts):
    column_list = [
        Finally_carts.id,
        Finally_carts.product_name,
        Finally_carts.finally_price,
        Finally_carts.quantity,
        Finally_carts.card_id,
    ]
    name = "Final Cart Item"
    name_plural = "Final Cart Items"


class CategoryAdmin(ModelView, model=Categories):
    column_list = [Categories.id, Categories.category_name]
    name = "Category"
    name_plural = "Categories"


class ProductAdmin(ModelView, model=Products):
    column_list = [
        Products.id,
        Products.product_name,
        Products.description,
        Products.image,
        Products.price,
        Products.category_id,
    ]
    name = "Product"
    name_plural = "Products"


class OrderAdmin(ModelView, model=Order):
    column_list = [
        Order.id,
        Order.user_id,
        Order.total_price,
        Order.status,
        Order.created_at,
    ]
    name = "Order"
    name_plural = "Orders"


class OrderItemAdmin(ModelView, model=OrderItem):
    column_list = [
        OrderItem.id,
        OrderItem.order_id,
        OrderItem.product_name,
        OrderItem.price,
        OrderItem.quantity,
    ]
    name = "Order Item"
    name_plural = "Order Items"
