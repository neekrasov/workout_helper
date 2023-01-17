import time
from celery import Celery


def test_nearest_grounds(celery_app: Celery):

    response = celery_app.send_task(
        "get_nearest_grounds", args=(55.743755580823, 37.621502218329, 10)
    )

    task_id = response.id

    time.sleep(1)

    result = celery_app.AsyncResult(task_id).result

    assert result is not None
    assert result.get("1062") is not None
    assert len(result) == 10


def test_search_grounds(celery_app: Celery):

    response = celery_app.send_task("search_grounds", args=("Лужники", 3))

    task_id = response.id

    time.sleep(1)

    result = celery_app.AsyncResult(task_id).result

    assert result is not None
    assert len(result) == 3


def test_recommendations(celery_app: Celery):

    response = celery_app.send_task("get_recommendations", args=(406671453, 5))

    task_id = response.id

    time.sleep(1)

    result = celery_app.AsyncResult(task_id).result

    assert result is not None
    assert len(result) == 5
