# tests/test_models.py

import pytest
from src.models import TaskCreate

def test_valid_task_create():
    task = TaskCreate(title="Teste de tarefa", completed=False)
    assert task.title == "Teste de tarefa"
    assert task.completed is False

def test_invalid_task_create_empty_title():
    with pytest.raises(ValueError):
        TaskCreate(title="", completed=False)
