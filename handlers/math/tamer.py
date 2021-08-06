# from asyncio import sleep as async_sleep
# from datetime import datetime
#
# from aiogram.types import message
#
#
# class Timer:
#     def __init__(self, hour, min):
#         self.hour = hour
#         self.min = min
#         self.check = False
#
#     def wait_timer_func(self):
#         while not self.check:
#             now = datetime.now()
#             if now.hour == self.hour and now.minute == self.min:
#                 return
#             else:
#                 await async_sleep(10)
