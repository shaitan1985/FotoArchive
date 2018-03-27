"""
    создает файлы лога и дебаг лога
    логгер пишет все важные события, такие,
    как сообщения наблюдателю, действия с файлами
    запись производится либо в базу, либо в файлы через внутренние модули

"""

import logging
import os.path

with open('debug.log', 'w') as f:
    pass


def log_debug(*args):


    formatt = '[%(levelname)s] %(asctime).19s [%(filename)s_Line:%(lineno)d] %(message)s'

    logging.basicConfig(
        level=logging.DEBUG,
        format=formatt,
        filename = 'debug.log'
    )

    logger = logging.getLogger()

    logger.debug(args)





