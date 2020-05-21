from joplin.apps import JoplinConfig

JOPLIN_DATABASE_CONF_KEY = 'joplin'


class JoplinRouter:
    route_app_labels = {JoplinConfig.name}

    def db_for_read(self, model, **kwargs):
        if model._meta.app_label in self.route_app_labels:
            return JOPLIN_DATABASE_CONF_KEY
        return None

    def db_for_write(self, model, **kwargs):
        if model._meta.app_label in self.route_app_labels:
            return JOPLIN_DATABASE_CONF_KEY
        return None

    def allow_relation(self, obj1, obj2, **kwargs):
        return None

    def allow_migrate(self, db, app_label, model_name=None, **kwargs):
        """
        Ban migrate
        """
        if app_label in self.route_app_labels:
            return False
        return None
