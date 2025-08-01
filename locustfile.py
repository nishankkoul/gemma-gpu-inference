from locust import HttpUser, task, constant

class ChatLLMUser(HttpUser):
    wait_time = constant(0)  # No wait between tasks

    @task
    def send_prompt(self):
        self.client.post(
            "/v1/chat/completions",
            json={
                "model": "gemma-3-1b-it",
                "messages": [
                    {"role": "user", "content": "Explain cloud computing in simple terms."}
                ],
                "max_tokens": 100
            },
            headers={"Content-Type": "application/json"}
        )
