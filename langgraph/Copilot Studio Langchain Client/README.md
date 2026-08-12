# LangChain connected to Copilot Studio Agent

## 1.  Create a Copilot Studio Agent
Add a knowledge Source:<br/>
<img width="1799" height="584" alt="image" src="https://github.com/user-attachments/assets/71c79ae1-da68-4008-a57a-7bfac8d87928" /><br/>

Copy the Connection String from:<br/>
<img width="2421" height="1272" alt="image" src="https://github.com/user-attachments/assets/d5b41b7a-83f2-4874-bd40-1f556a06bf86" /><br/>

## 2.  Create App Registration from Azure Portal
<img width="2239" height="1049" alt="image" src="https://github.com/user-attachments/assets/9b848a3c-4298-4d76-bfe4-9321147bbd39" /><br/>
Add these API Permission:<br/>
<img width="2252" height="1277" alt="image" src="https://github.com/user-attachments/assets/df3c4511-5784-461b-8114-1640710bf8f3" /><br/>

## 3. Implement LangChain connected to Copilot Studio Agent 
.env file is like:
```
# Copilot Studio > Channels > Native app > Microsoft 365 Agents SDK
COPILOT_STUDIO_DIRECT_CONNECT_URL=https://example.environment.api.powerplatform.com/copilotstudio/dataverse-backed/authenticated/bots/your-agent/conversations?api-version=2022-03-01-preview
COPILOT_STUDIO_TENANT_ID=your-microsoft-entra-tenant-id
COPILOT_STUDIO_CLIENT_ID=your-public-client-application-id
```
Python code
```py
import asyncio
import os
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Coroutine, TypeVar

from dotenv import load_dotenv
from langchain_core.callbacks import (
    AsyncCallbackManagerForLLMRun,
    CallbackManagerForLLMRun,
)
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from microsoft_agents.activity import ActivityTypes
from microsoft_agents.copilotstudio.client import ConnectionSettings, CopilotClient
from msal import PublicClientApplication
from pydantic import PrivateAttr


ResultType = TypeVar("ResultType")


class CopilotStudioChatModel(BaseChatModel):
    """LangChain chat model backed by the Copilot Studio Native app channel."""

    direct_connect_url: str
    tenant_id: str
    client_id: str

    _client: CopilotClient | None = PrivateAttr(default=None)
    _conversation_id: str | None = PrivateAttr(default=None)
    _msal_app: PublicClientApplication | None = PrivateAttr(default=None)

    def model_post_init(self, context: Any, /) -> None:
        del context

    @property
    def _llm_type(self) -> str:
        return "copilot-studio-native-app"

    @property
    def _identifying_params(self) -> dict[str, Any]:
        return {"direct_connect_url": self.direct_connect_url}

    def _generate(
        self,
        messages: list[BaseMessage],
        stop: list[str] | None = None,
        run_manager: CallbackManagerForLLMRun | None = None,
        **kwargs: Any,
    ) -> ChatResult:
        del stop, run_manager, kwargs
        return self._run_sync(self._agenerate_response(messages))

    async def _agenerate(
        self,
        messages: list[BaseMessage],
        stop: list[str] | None = None,
        run_manager: AsyncCallbackManagerForLLMRun | None = None,
        **kwargs: Any,
    ) -> ChatResult:
        del stop, run_manager, kwargs
        return await self._agenerate_response(messages)

    def reset_conversation(self) -> None:
        """Start a new Copilot Studio conversation on the next invocation."""
        self._conversation_id = None

    async def _agenerate_response(self, messages: list[BaseMessage]) -> ChatResult:
        prompt = self._latest_user_text(messages)
        client = self._ensure_client()
        await self._ensure_conversation(client)

        activities = [
            activity
            async for activity in client.ask_question(
                prompt,
                conversation_id=self._conversation_id,
            )
        ]
        text = "\n".join(
            activity.text or ""
            for activity in activities
            if activity.type == ActivityTypes.message and activity.text
        )
        if not text:
            raise RuntimeError("Copilot Studio returned no text message")

        message = AIMessage(
            content=text,
            additional_kwargs={
                "copilot_studio_activities": [
                    activity.model_dump(mode="json", exclude_none=True)
                    for activity in activities
                ]
            },
        )
        return ChatResult(generations=[ChatGeneration(message=message)])

    def _ensure_client(self) -> CopilotClient:
        if self._client is not None:
            return self._client

        settings = ConnectionSettings(
            environment_id="",
            agent_identifier="",
            direct_connect_url=self.direct_connect_url,
        )
        scopes = [CopilotClient.scope_from_settings(settings)]
        if self._msal_app is None:
            self._msal_app = PublicClientApplication(
                client_id=self.client_id,
                authority=f"https://login.microsoftonline.com/{self.tenant_id}",
            )
        accounts = self._msal_app.get_accounts()
        token_result = None
        if accounts:
            token_result = self._msal_app.acquire_token_silent(
                scopes,
                account=accounts[0],
            )
        if not token_result or "access_token" not in token_result:
            token_result = self._msal_app.acquire_token_interactive(scopes=scopes)
        if "access_token" not in token_result:
            description = token_result.get(
                "error_description",
                token_result.get("error", "unknown authentication error"),
            )
            raise RuntimeError(f"Microsoft sign-in failed: {description}")

        self._client = CopilotClient(settings, token_result["access_token"])
        return self._client

    async def _ensure_conversation(self, client: CopilotClient) -> None:
        if self._conversation_id:
            return

        async for activity in client.start_conversation(True):
            conversation = activity.conversation
            if conversation and conversation.id:
                self._conversation_id = conversation.id
        if not self._conversation_id:
            raise RuntimeError("Copilot Studio did not return a conversation ID")

    @staticmethod
    def _latest_user_text(messages: list[BaseMessage]) -> str:
        for message in reversed(messages):
            if isinstance(message, HumanMessage):
                return CopilotStudioChatModel._content_to_text(message.content)
        if messages:
            return CopilotStudioChatModel._content_to_text(messages[-1].content)
        raise ValueError("At least one message is required")

    @staticmethod
    def _content_to_text(content: str | list[str | dict[str, Any]]) -> str:
        if isinstance(content, str):
            return content
        return "\n".join(
            item if isinstance(item, str) else str(item.get("text", item))
            for item in content
        )

    @staticmethod
    def _run_sync(coroutine: Coroutine[Any, Any, ResultType]) -> ResultType:
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            return asyncio.run(coroutine)

        with ThreadPoolExecutor(max_workers=1) as executor:
            return executor.submit(asyncio.run, coroutine).result()


def main() -> None:
    load_dotenv()
    model = CopilotStudioChatModel(
        direct_connect_url=os.environ["COPILOT_STUDIO_DIRECT_CONNECT_URL"],
        tenant_id=os.environ["COPILOT_STUDIO_TENANT_ID"],
        client_id=os.environ["COPILOT_STUDIO_CLIENT_ID"],
    )

    while prompt := input("You: ").strip():
        response = model.invoke(prompt)
        print(f"Copilot: {response.content}")


if __name__ == "__main__":
    main()
```

