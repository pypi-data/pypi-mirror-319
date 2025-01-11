from mag_db.core.transaction_cache import TransactionCache


class TransactionCacheMgr:
    """
    数据库事务缓存管理类
    """
    transaction_caches = {}

    @classmethod
    def get_tx_cache_by_name(cls, ds_name):
        if ds_name not in cls.transaction_caches:
            cls.transaction_caches[ds_name] = TransactionCache()
        return cls.transaction_caches[ds_name]

    @classmethod
    def get_current_tx(cls, ds_name):
        cache = cls.get_tx_cache_by_name(ds_name)
        return cache.current

    @classmethod
    def close(cls):
        cls.transaction_caches.clear()

if __name__ == '__main__':
    # 示例用法
    try:
        tx_cache = TransactionCacheMgr.get_tx_cache_by_name("my_datasource")
        tx_cache.add("my_transaction")
        current_tx = TransactionCacheMgr.get_current_tx("my_datasource")
        print(current_tx)  # 输出: my_transaction
    finally:
        TransactionCacheMgr.close()
