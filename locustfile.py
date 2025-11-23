from locust import HttpUser, task, between
import uuid
import json
import requests

# Your GA4 credentials
MEASUREMENT_ID = "G-BDEF2MYY8F"
API_SECRET = "5kVYOJJiSPurqL8UoxRhFA"  # MUST BE FILLED

# Sends event to Google Analytics 4
def send_ga4_event(path):
    client_id = str(uuid.uuid4())  # unique fake visitor

    payload = {
        "client_id": client_id,
        "events": [{
            "name": "page_view",
            "params": {
                "page_title": f"Locust Load Test: {path}",
                "page_location": f"http://localhost:3000{path}",
                "engagement_time_msec": 1
            }
        }]
    }

    # GA4 Measurement Protocol endpoint
    mp_url = (
        f"https://www.google-analytics.com/mp/collect"
        f"?measurement_id={MEASUREMENT_ID}&api_secret={API_SECRET}"
    )

    # Send the event
    requests.post(mp_url, json=payload)


class WebsiteUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def visit_fast_page(self):
        path = "/fast"
        self.client.get(path)
        send_ga4_event(path)

    @task(2)
    def visit_medium_page(self):
        path = "/medium"
        self.client.get(path)
        send_ga4_event(path)

    @task(1)
    def visit_slow_page(self):
        path = "/slow"
        self.client.get(path)
        send_ga4_event(path)


# Funktsioon määratud pikkusega juhusliku stringi genereerimiseks
#def random_string(length=8):
#    return ''.join(random.choices(string.ascii_letters, k=length))


# 1. Suure kasutajate arvu registreerimise test
#class RegisterUserTest(HttpUser):
#    # Viivitus päringute vahel 1 kuni 2 sekundit
#    wait_time = between(1, 2)

#    @task
#    def register_user(self):
        # Genereerime juhusliku kasutajanime
#        username = random_string()
        # Saadame POST-päringu registreerimiseks
#        self.client.post("/api/register", json={"username": username, "password": "password123"})


# 2. Kasutajate massilise sisselogimise test
#class LoginTest(HttpUser):
#    wait_time = between(1, 2)

#    @task
#    def login_user(self):
        # Saadame POST-päringu olemasoleva kasutaja sisselogimiseks
#        self.client.post("/api/login", json={"username": "testuser", "password": "password123"})


# 3. Ülesannete loendi lugemise test
#class GetTodosTest(HttpUser):
#    wait_time = between(0.5, 1.5)

#    @task
#    def get_todos(self):
        # Saadame GET-päringu, et saada kõik ülesanded
#        self.client.get("/api/todos")


# 4. Ülesannete loomise test
#class CreateTodoTest(HttpUser):
#    wait_time = between(1, 2)

#    @task
#    def create_todo(self):
        # Saadame POST-päringu uue ülesande loomiseks juhusliku nimega
#        self.client.post("/api/todos", json={
#            "title": random_string(),
#            "description": "Load Test Task",
#            "priority": "high"
#        })


# 5. Ülesannete uuendamise test koormuse all
#class UpdateTodoTest(HttpUser):
#    wait_time = between(1, 3)

#    @task
#    def update_todo(self):
        # Uuendame ülesannet id=1 juhuslike andmetega
#        todo_id = 1
#        self.client.put(f"/api/todos/{todo_id}", json={
#            "title": random_string(),
#            "description": "Updated Task",
#            "priority": "medium"
#        })


# 6. Ülesannete massilise kustutamise test
#class DeleteTodoTest(HttpUser):
#    wait_time = between(1, 3)

#    @task
#    def delete_todo(self):
        # Valime juhuslikult ülesande id 1 kuni 5 ja kustutame selle
#        todo_id = random.randint(1, 5)
#        self.client.delete(f"/api/todos/{todo_id}")


# 7. Bulk-operatsioonide test (nt massiline kustutamine)
#class BulkActionTest(HttpUser):
#    wait_time = between(1, 3)

#    @task
#    def bulk_delete(self):
        # Saadame POST-päringu ülesannete massiliseks kustutamiseks koos määratud id-dega
#        ids = [1, 2, 3, 4, 5]
#        self.client.post("/api/todos/bulk", json={"action": "delete", "ids": ids})


# 8. Kasutaja parooli muutmise test
#class ChangePasswordTest(HttpUser):
#    wait_time = between(1, 3)

#    @task
#    def change_password(self):
        # Saadame POST-päringu parooli muutmiseks
#        self.client.post("/api/change-password", json={
#            "old_password": "password123",
#            "new_password": "newpassword123"
#        })


# 9. Kasutaja andmete ekspordi test
#class ExportDataTest(HttpUser):
#    wait_time = between(1, 3)

#    @task
#    def export_data(self):
        # Saadame GET-päringu kasutaja andmete eksportimiseks
#        self.client.get("/api/export")


# 10. Kasutajakonto kustutamise test
#class DeleteAccountTest(HttpUser):
#    wait_time = between(1, 3)

#    @task
#    def delete_account(self):
        # Saadame DELETE-päringu konto kustutamiseks
#        self.client.delete("/api/user")
