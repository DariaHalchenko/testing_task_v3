import pytest
import tempfile
import os
import importlib

# Pytest-fixture testikliendi loomiseks ajutise andmebaasiga
@pytest.fixture
def client():
    # Loome ajutise faili, mida kasutatakse andmebaasina
    db = tempfile.NamedTemporaryFile(delete=False)
    db_path = db.name  
    db.close() 

    # Määrame andmebaasi asukoha muutuja abil
    os.environ['DB_PATH'] = db_path
    # Importime rakenduse mooduli
    app_module = importlib.import_module('app')
    # Laadime mooduli uuesti
    importlib.reload(app_module)
    app = app_module.app
    # Initsialiseerime andmebaasi (loome tabelid ja algandmed)
    app_module.init_db()
    app.testing = True
    yield app.test_client()

    # Pärast testide lõpetamist kustutame ajutise andmebaasi faili
    os.remove(db_path)


# 1. Kasutaja registreerimise ja sisselogimise test
def test_login(client):
    # Uue kasutaja registreerimine
    r = client.post('/api/register', json={'username': 'daria', 'password': '123456'})
    assert r.get_json()['success'] is True

    # Logi sisse õige parooliga
    r = client.post('/api/login', json={'username': 'daria', 'password': '123456'})
    assert r.get_json()['success'] is True

    # Sisselogimine vale andmetega
    r = client.post('/api/login', json={'username': 'valeUsername', 'password': 'valePassword'})
    assert r.get_json()['success'] is False

    # muuta parooli vale vana parooliga
    r = client.post('/api/change-password', json={'old_password': 'qwerty', 'new_password': 'newpassword123'})
    assert r.get_json()['success'] is False


# 2. Uue kasutaja registreerimise test
def test_register(client):
    # Uue kasutaja registreerimine
    r = client.post('/api/register', json={'username': 'daria1', 'password': 'password123'})
    assert r.get_json()['success'] is True

    # registreerida olemasolev kasutaja
    r = client.post('/api/register', json={'username': 'daria1', 'password': 'password123'})
    assert r.get_json()['success'] is False
    # Vigade kontrollimine
    assert r.get_json()['message'] == 'Kasutajanimi on juba kasutusel'


# 3. Parooli muutmise test
def test_change_password(client):
    # Uue kasutaja registreerimine
    r = client.post('/api/register', json={'username': 'daria2', 'password': '123456'})
    assert r.get_json()['success'] is True

    # Kasutaja autoriseerimine algse parooliga
    r = client.post('/api/login', json={'username': 'daria2', 'password': '123456'})
    assert r.get_json()['success'] is True

    # Kasutaja parooli muutmine
    r = client.post('/api/change-password', json={'old_password': '123456', 'new_password': 'newpassword123'})
    assert r.get_json()['success'] is True

    # Uue parooliga sisselogimise võimaluse kontrollimine
    r = client.post('/api/login', json={'username': 'daria2', 'password': 'newpassword123'})
    assert r.get_json()['success'] is True

    # Kontrollige, et vana parool enam ei kehti
    r = client.post('/api/login', json={'username': 'daria2', 'password': '123456'})
    assert r.get_json()['success'] is False


# 4. Ülesande loomise test
def test_create_todo(client):
    # Uue kasutaja registreerimine
    r = client.post('/api/register', json={'username': 'daria3', 'password': '123456'})
    assert r.get_json()['success'] is True

    # Kasutaja autoriseerimine 
    r = client.post('/api/login', json={'username': 'daria3', 'password': '123456'})
    assert r.get_json()['success'] is True

    # Uue ülesande loomine 
    r = client.post('/api/todos', json={
        'title': 'New Task',
        'description': 'Task description',
        'priority': 'medium',
        'due_date': '10.10.2025',
        'tags': 'work'
    })
    data = r.get_json()
    # Ülesande edukat loomist kontrollimine
    assert data['success'] is True
    # Ülesande loomise teate õigsuse kontrollimine
    assert 'Ülesanne loodud edukalt' in data['message']


# 5. Ülesannete nimekirja saamise test
def test_get_todos(client):
    # Uue kasutaja registreerimine
    r = client.post('/api/register', json={'username': 'daria4', 'password': '123456'})
    assert r.get_json()['success'] is True

    # Sisselogimine
    r = client.post('/api/login', json={'username': 'daria4', 'password': '123456'})
    assert r.get_json()['success'] is True

    # Kahe testülesande loomine
    client.post('/api/todos', json={
        'title': 'Task 1',
        'description': 'Description 1',
        'priority': 'low',
        'due_date': '12.12.2025',
        'tags': 'home'
    })
    client.post('/api/todos', json={
        'title': 'Task 2',
        'description': 'Description 2',
        'priority': 'high',
        'due_date': '01.01.2026',
        'tags': 'work'
    })

    # Kõigi kasutaja ülesannete loendi saamine
    r = client.get('/api/todos')
    data = r.get_json()
    # Ülesannete edukate vastuvõtmiste kontrollimine
    assert data['success'] is True
    # Kontrollige, et nimekiri sisaldab kahte loodud ülesannet.
    assert len(data['todos']) == 2


# 6. Ülesande kustutamise test
def test_delete_todo(client):
    # Uue kasutaja registreerimine
    r = client.post('/api/register', json={'username': 'daria5', 'password': '123456'})
    assert r.get_json()['success'] is True

    # Sisselogimine
    r = client.post('/api/login', json={'username': 'daria5', 'password': '123456'})
    assert r.get_json()['success'] is True

    # Loome ülesande, mille me kustutame
    r = client.post('/api/todos', json={
        'title': 'Task to delete',
        'description': 'This task will be deleted',
        'priority': 'medium',
        'due_date': '14.04.2026',
        'tags': 'test'
    })
    data = r.get_json()
    assert data['success'] is True

    # Ülesannete loendi saamine, et teada saada loodud ülesande ID
    r = client.get('/api/todos')
    todos = r.get_json()['todos']
    todo_id = todos[0]['id']

    # Ülesande kustutamine selle ID järgi
    r = client.delete(f'/api/todos/{todo_id}')
    # Eemaldamise edukuse kontrollimine
    assert r.get_json()['success'] is True
