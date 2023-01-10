from .models.user import map_user_table
from .models import mapper_registry


def start_mappers():

    map_user_table(mapper_registry)
