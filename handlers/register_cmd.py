from handlers.cart import register_handlers_cart
from handlers.cmd import register_handlers_start
from handlers.math.math import register_handlers_math
from handlers.math.mentally_math import register_handlers_math_mentally


def reg_cmd(dp):
    register_handlers_start(dp)
    register_handlers_cart(dp)
    register_handlers_math(dp)
    register_handlers_math_mentally(dp)