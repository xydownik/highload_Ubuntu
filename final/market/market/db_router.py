class PrimaryReplicaRouter:
    def db_for_read(self, model, **hints):
        """
        Route read operations:
        - Products to replica1.
        - Payments to my_keyspace.
        - Orders and OrderItems to replica2.
        - Others to default.
        """
        if model._meta.app_label == 'api' and model._meta.model_name ==  ['product','category']:
            return 'replica1'
        elif model._meta.app_label == 'payments' and model._meta.model_name == 'payment':
            return 'my_keyspace'
        return 'default'

    def db_for_write(self, model, **hints):
        """
        Route write operations:
        - Products to replica1.
        - Payments to my_keyspace.
        - Orders and OrderItems to replica2.
        - Others to default.
        """
        if model._meta.app_label == 'api' and model._meta.model_name == ['product','category']:
            return 'replica1'
        elif model._meta.app_label == 'payments' and model._meta.model_name == 'payment':
            return 'my_keyspace'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relationships if both objects belong to the same database.
        """
        if obj1._state.db == obj2._state.db:
            return True
        return False

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Control migrations:
        - Allow migrations for products and categories on replica1.
        - Allow migrations for payments on my_keyspace.
        - Allow migrations for orders and order items on replica2.
        - Allow others on default.
        """
        if db == 'replica1':
            return app_label == 'api' and model_name in ['product',
                                                         'category']  # Allow migrations for product and category
        if db == 'my_keyspace':
            return app_label == 'payments' and model_name == 'payment'
        return db == 'default'
