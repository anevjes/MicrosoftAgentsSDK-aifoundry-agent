from os import environ

from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from .agent import run_weather_forecast_agent

from microsoft.agents.hosting.core import (
    Authorization,
    AgentApplication,
    TurnState,
    TurnContext,
    MessageFactory,
    MemoryStorage,
)

from microsoft.agents.hosting.aiohttp import CloudAdapter
from microsoft.agents.authentication.msal import MsalConnectionManager

from microsoft.agents.activity import Attachment, load_configuration_from_env

load_dotenv()
agents_sdk_config = load_configuration_from_env(environ)

STORAGE = MemoryStorage()
CONNECTION_MANAGER = MsalConnectionManager(**agents_sdk_config)
ADAPTER = CloudAdapter(connection_manager=CONNECTION_MANAGER)
AUTHORIZATION = Authorization(STORAGE, CONNECTION_MANAGER, **agents_sdk_config)


# token_provider = get_bearer_token_provider(
#     DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
# )

print("WeatherForecastAgent replaced with Azure AI Foundry agent.")

AGENT_APP = AgentApplication[TurnState](
    storage=STORAGE, adapter=ADAPTER, authorization=AUTHORIZATION, **agents_sdk_config
)

@AGENT_APP.conversation_update("membersAdded")
async def on_members_added(context: TurnContext, _state: TurnState):
    members_added = context.activity.members_added
    for member in members_added:
        if member.id != context.activity.recipient.id:
            await context.send_activity("Hello and welcome!")


# @AGENT_APP.activity("message")
# async def on_message(context: TurnContext, state: TurnState):
#     print(f"Received message: {context.activity.text}")
#     # Directly call the Azure AI Foundry agent function
#     run_weather_forecast_agent(context.activity.text)


@AGENT_APP.activity("message")
async def on_message(context: TurnContext, state: TurnState):
    user_message = context.activity.text

    # Get the agent response (capture output as a variable)
    response = run_weather_forecast_agent(user_message)
    print(f"Agent response: {response}")
    print(f"Response type: {type(response)}")

    # If response is text, send as message
    if isinstance(response, str):
        await context.send_activity(response)
    # If response is a dict with adaptive card
    # elif isinstance(response, dict) and response.get("contentType") == "AdaptiveCard":
    #     await context.send_activity(
    #         Activity(
    #             type="message",
    #             attachments=[
    #                 Attachment(
    #                     content_type="application/vnd.microsoft.card.adaptive",
    #                     content=response["content"]
    #                 )
    #             ]
    #         )
    #     )
    else:
        await context.send_activity("Sorry, I couldn't get the weather forecast at the moment.")