from mag_tools.log.logger import Logger
from mag_tools.model.log_type import LogType


class TransactionCache:
    def __init__(self):
        self.tx_cache = []

    @property
    def current(self):
        if not self.tx_cache:
            return None
        tx = self.tx_cache[-1]
        if tx is None:
            Logger.throw(LogType.DAO, "Cached transaction is null")
        return tx

    def remove(self, tx):
        self.tx_cache.remove(tx)

    def add(self, tx):
        self.tx_cache.append(tx)
