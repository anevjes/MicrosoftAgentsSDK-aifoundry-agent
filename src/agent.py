from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import ListSortOrder
import json

def run_weather_forecast_agent(user_message: str) -> None:
    """
    Sends a message to the Azure AI Foundry agent and prints the response.
    """
    project = AIProjectClient(
        credential=DefaultAzureCredential(),
        endpoint="https://anevjes-ai-f-001.services.ai.azure.com/api/projects/firstProject"
    )

    agent = project.agents.get_agent("asst_FzNBH2H6sydxiULj6poD1CTz__")

    thread = project.agents.threads.create()
    print(f"Created thread, ID: {thread.id}")

    message = project.agents.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_message
    )

    run = project.agents.runs.create_and_process(
        thread_id=thread.id,
        agent_id=agent.id
    )

    if run.status == "failed":
        print(f"Run failed: {run.last_error}")
    else:
        messages = project.agents.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)
        for message in messages:
            if message.text_messages:
                print(f"{message.role}: {message.text_messages[-1].text.value}")
        return str(message.text_messages[0].text.value)
