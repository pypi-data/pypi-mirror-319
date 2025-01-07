import os
import requests
import json
import datetime

# https://packaging.python.org/en/latest/tutorials/packaging-projects/

class Recording:
    WAYFOUND_HOST = "https://app.wayfound.ai"
    WAYFOUND_RECORDINGS_URL = WAYFOUND_HOST + "/api/v1/recordings/active"
    WAYFOUND_RECORDING_COMPLETED_URL = WAYFOUND_HOST + "/api/v1/recordings/completed"

    def __init__(self, wayfound_api_key=None, agent_id=None, recording_id=None, visitor_id=None):
        super().__init__()

        self.wayfound_api_key = wayfound_api_key or os.getenv("WAYFOUND_API_KEY")
        self.agent_id = agent_id or os.getenv("WAYFOUND_AGENT_ID")
        self.recording_id = recording_id
        self.visitor_id = visitor_id
        
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.wayfound_api_key}",
            "X-SDK-Language": "Python",
            "X-SDK-Version": "0.1.0"
        }

    def new_recording(self, messages=[]):
        self.recording_id = None

        payload = {
            "agentId": self.agent_id,
            "recordingId": self.recording_id,
            "messages": messages,
        }

        if self.visitor_id:
            payload["visitorId"] = self.visitor_id

        if not self.recording_id:
            try:
                response = requests.post(self.WAYFOUND_RECORDINGS_URL, headers=self.headers, data=json.dumps(payload))
                response.raise_for_status()
                response_data = response.json()
                self.recording_id = response_data['id']
                return self.recording_id
            except requests.exceptions.RequestException as e:
                print(f"Error during POST request: {e}")
                self.recording_id = None


    def record_messages(self, messages, visitor_id=None):
        if not self.recording_id:
            self.new_recording(messages)
            print(f"Recording ID: {self.recording_id}")
            return

        payload = {
            "agentId": self.agent_id,
            "recordingId": self.recording_id,
            "messages": messages,
        }

        if visitor_id:
            self.visitor_id = visitor_id
            payload["visitorId"] = visitor_id

        try:
            response = requests.put(self.WAYFOUND_RECORDINGS_URL, headers=self.headers, data=json.dumps(payload))
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error during PUT request: {e}")

    def completed_recording(self, messages=None, first_message_at=None, last_message_at=None, visitor_id=None):
        if messages is None:
            messages = []

        if not first_message_at:
            first_message_at = datetime.datetime.now(datetime.timezone.utc).isoformat()

        if not last_message_at:
            last_message_at = datetime.datetime.now(datetime.timezone.utc).isoformat()

        recording_url = self.WAYFOUND_RECORDING_COMPLETED_URL
        payload = {
            "agentId": self.agent_id,
            "messages": messages,
            "firstMessageAt": first_message_at,
            "lastMessageAt": last_message_at,
        }

        if visitor_id:
            payload["visitorId"] = visitor_id

        try:
            response = requests.post(recording_url, headers=self.headers, data=json.dumps(payload))
            if response.status_code == 200:
                self.recording_id = None
            else:
                print(f"The request failed with status code: {response.status_code} and response: {response.text}")
                raise Exception(f"Error completing recording request: {response.status_code}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error completing recording request: {e}")


    def record_messages_from_langchain_memory(self, memory):
        formatted_messages = []
        for message in memory.chat_memory.messages:
            if message.type == 'ai':
                formatted_messages.append({'role': 'assistant', 'content': message.content})
            elif message.type == 'human':
                formatted_messages.append({'role': 'user', 'content': message.content})

        self.record_messages(formatted_messages)
