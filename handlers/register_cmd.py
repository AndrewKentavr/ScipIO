from handlers.cart import register_handlers_cart
from handlers.cmd import register_handlers_start
from handlers.math import register_handlers_math


def reg_cmd(dp):
    register_handlers_start(dp)
    register_handlers_cart(dp)
    register_handlers_math(dp)
