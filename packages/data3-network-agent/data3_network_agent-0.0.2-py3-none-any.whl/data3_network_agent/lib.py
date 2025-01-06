
from typing import List
from dotenv import load_dotenv
import requests
load_dotenv()

class Data3AgentUtils:
    '''
    Class to fetch environment variables for the agent backend
    Methods:
    fetch_agent_env_variables: Fetch Single or all ([]) agent env
    '''
    def __init__(self):
        print("RAG_BACKEND_URL", self.rag_backend_url)

    def fetch_agent_env_variables(self,docker_service_name: str, field_names: List[str] = []):
        """Fetch a value from Redis and handle errors."""
        try:
            base_url = f"{self.rag_backend_url}:7000/get-tools-env"
            params = {"docker_service_name": docker_service_name}

            # Add `env_vars` only if the list is not empty
            if field_names:
                params["env_vars"] = field_names

            # Perform the GET request
            get_envs = requests.get(base_url, params=params)
            get_envs.raise_for_status()  # Raise an exception for HTTP errors

            # Print the response JSON
            print("Get Env Vars Response:", get_envs.json())
            return get_envs.json()

        except requests.exceptions.RequestException as e:
            return f"Error: {e}"

    def fetch_base_url(self):
        """Fetch a value from Redis and handle errors."""
        try:
            return "http://host.docker.internal"
        except Exception as e:
            return f"Error: {e}"        