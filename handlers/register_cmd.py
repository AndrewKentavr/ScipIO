"""
Распределяйте всё по блокам, чтобы не запутаться
"""

# ------main-------
from handlers.cart import register_handlers_cart
from handlers.cmd import register_handlers_start

# ------math-------
from handlers.math.math import register_handlers_math
from handlers.math.math_formulas import register_handlers_math_formulas
from handlers.math.mentally_math import register_handlers_math_mentally
from handlers.math.tasks_category_math import register_handlers_tasks_math_category

# ------flashcards-------
from handlers.flashcards.flashcard import register_handlers_flashcard
from handlers.flashcards.flashcards_managing import register_handlers_flashcards_managing
from handlers.flashcards.flashcards_training import register_handlers_flashcards_training

# ------logic-------
from handlers.logic.logic import register_handlers_logic
from handlers.logic.tasks_category_logic import register_handlers_tasks_logic_category

# ------timer-------
from handlers.timer.timer import register_handlers_timer
from handlers.timer.timer_managing import register_handlers_timer_managing


def reg_cmd(dp):
    # ------main-------
    register_handlers_start(dp)
    register_handlers_cart(dp)

    # ------math-------
    register_handlers_math(dp)
    register_handlers_math_mentally(dp)
    register_handlers_math_formulas(dp)
    register_handlers_tasks_math_category(dp)

    # ------flashcards-------
    register_handlers_flashcard(dp)
    register_handlers_flashcards_managing(dp)
    register_handlers_flashcards_training(dp)

    # ------logic-------
    register_handlers_tasks_logic_category(dp)
    register_handlers_logic(dp)

    # ------timer-------
    register_handlers_timer(dp)
    register_handlers_timer_managing(dp)
