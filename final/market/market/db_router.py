# allMart/db_router.py
import random


class PrimaryReplicaRouter:
    def db_for_read(self, model, **hints):
        """
        Route read operations for the Payment model to the Cassandra database.
        Other models use replica databases.
        """
        if model._meta.app_label == 'payments' and model._meta.model_name == 'payment':
            return 'my_keyspace'
        return random.choice(['replica1', 'replica2'])

    def db_for_write(self, model, **hints):
        """
        Route write operations for the Payment model to the Cassandra database.
        Other models use the default database.
        """
        if model._meta.app_label == 'payments' and model._meta.model_name == 'payment':
            return 'my_keyspace'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relationships if both objects belong to the same database.
        """
        if obj1._state.db == obj2._state.db:
            return True
        # Optionally, allow relations across databases if needed
        return False

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Prevent migrations for the Cassandra database.
        """
        if db == 'my_keyspace':
            return app_label == 'payments' and model_name == 'payment'
        return True
