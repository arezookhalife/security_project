from locust import HttpUser, between, task

TEST_TOKEN = "dummy_token_for_local"

USERNAME = "load_test_user"
PASSWORD = "testpass"


class WebsiteUser(HttpUser):
    wait_time = between(1, 2)

    def on_start(self):
        try:
            with self.client.post(
                "/accounts/test-login-no-otp/",
                json={"username": USERNAME, "password": PASSWORD},
                headers={"X-TEST-TOKEN": TEST_TOKEN},
                catch_response=True,
            ) as resp:
                if resp.status_code != 200:
                    resp.failure(f"Test-login failed: {resp.status_code} - {resp.text}")
                else:
                    resp.success()
        except Exception as e:
            print(f"Exception on login: {e}")

    @task(3)
    def home_page(self):

        with self.client.get("/home/", catch_response=True) as resp:
            if resp.status_code != 200:
                resp.failure(f"Home page failed: {resp.status_code}")
            else:
                resp.success()

