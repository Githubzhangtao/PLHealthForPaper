from django.conf import settings
DATABASE_MAPPING = settings.DATABASE_APPS_MAPPING
class DBRouter(object):
    """
        A router to control all database operations on models in the app02 application.
        """

    def db_for_read(self, model, **hints):
        """
        Attempts to read app02 models go to hvdb DB.
        """
        if model._meta.app_label in DATABASE_MAPPING:  # app name（如果该app不存在，则无法同步成功）
            return DATABASE_MAPPING[model._meta.app_label]  # cache_db为settings中配置的database节点名称，并非db name。dbname为testdjango
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write app02 models go to hvdb DB.
        """
        if model._meta.app_label in DATABASE_MAPPING:  # app name（如果该app不存在，则无法同步成功）
            return DATABASE_MAPPING[model._meta.app_label]
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the app02 app is involved.
        当 obj1 和 obj2 之间允许有关系时返回 True ，不允许时返回 False ，或者没有 意见时返回 None 。
        """
        db_obj1 = DATABASE_MAPPING.get(obj1._meta.app_label)
        db_obj2 = DATABASE_MAPPING.get(obj2._meta.app_label)
        if db_obj1 and db_obj2:
            if db_obj1 == db_obj2:
                return True
            else:
                return False
        return None
    #
    # def allow_migrate(self, db, model):
    #     """
    #     Make sure the app02 app only appears in the hvdb database.
    #     """
    #     if db == 'cache_db':
    #         return model._meta.app_label == 'app02'
    #     elif model._meta.app_label == 'app02':
    #         return False
    #
    # def allow_syncdb(self, db, model):  # 决定 model 是否可以和 db 为别名的数据库同步
    #     if db == 'hvdb' or model._meta.app_label == "app02":
    #         return False  # we're not using syncdb on our hvdb database
    #     else:  # but all other models/databases are fine
    #         return True
    #     return None