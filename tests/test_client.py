import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from client.client import LLMClient
from client.response import EventType, StreamEvent, TextDelta, TokenUsage


@pytest.fixture
def mock_openai_client():
    """Fixture za mockovanje AsyncOpenAI client-a."""
    with patch("client.client.AsyncOpenAI") as mock:
        yield mock


@pytest.fixture
def llm_client():
    """Fixture za LLMClient instancu."""
    client = LLMClient()
    yield client
    # Cleanup
    import asyncio

    asyncio.run(client.close())


class TestLLMClient:
    """Testovi za LLMClient klasu."""

    def test_initialization(self):
        """Testira inicijalizaciju LLMClient-a."""
        client = LLMClient()
        assert client._client is None

    @patch("client.client.os.getenv")
    def test_get_client_creates_client_once(
        self, mock_getenv, mock_openai_client
    ):
        """Testira da se klijent kreira samo jednom."""
        mock_getenv.return_value = "test-key"

        client = LLMClient()
        client1 = client.get_client()
        client2 = client.get_client()

        # Treba da vrati istu instancu
        assert client1 is client2
        # AsyncOpenAI treba da bude pozvan samo jednom
        mock_openai_client.assert_called_once()

    @patch("client.client.os.getenv")
    def test_get_client_passes_correct_params(
        self, mock_getenv, mock_openai_client
    ):
        """Testira da se prosleđuju ispravni parametri."""
        mock_getenv.side_effect = lambda key: {
            "OPENAI_API_KEY": "test-key",
            "OPENAI_BASE_URL": "http://test.com",
        }.get(key)

        client = LLMClient()
        client.get_client()

        mock_openai_client.assert_called_once_with(
            api_key="test-key",
            base_url="http://test.com",
        )

    @pytest.mark.asyncio
    async def test_close(self, mock_openai_client):
        """Testira close metod."""
        mock_client_instance = AsyncMock()
        mock_openai_client.return_value = mock_client_instance

        client = LLMClient()
        _ = client.get_client()
        await client.close()

        assert client._client is None
        mock_client_instance.close.assert_called_once()


class TestChatCompletion:
    """Testovi za chat_completition metod."""

    @pytest.mark.asyncio
    async def test_chat_completion_non_streaming(self, mock_openai_client):
        """Testira chat_completion u non-streaming modu."""
        # Mockovanje odgovora
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Test response"
        mock_response.choices[0].finish_reason = "stop"
        mock_response.usage = MagicMock()
        mock_response.usage.prompt_tokens = 10
        mock_response.usage.completion_tokens = 5
        mock_response.usage.total_tokens = 15
        mock_response.usage.prompt_tokens_details.cached_tokens = 2

        mock_openai_client.return_value.chat.completions.create = AsyncMock(
            return_value=mock_response
        )

        client = LLMClient()
        messages = [{"role": "user", "content": "Hello"}]

        events = []
        async for event in client.chat_completition(messages, stream=False):
            events.append(event)

        assert len(events) == 1
        event = events[0]
        assert event.type == EventType.MESSAGE_COMPLETE
        assert event.text_delta.content == "Test response"
        assert event.finish_reason == "stop"
        assert event.usage.prompt_tokens == 10
        assert event.usage.completion_tokens == 5
        assert event.usage.total_tokens == 15

    @pytest.mark.asyncio
    async def test_chat_completion_passes_correct_kwargs(
        self, mock_openai_client
    ):
        """Testira da se prosleđuju ispravni parametri API-u."""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Response"
        mock_response.choices[0].finish_reason = "stop"
        mock_response.usage = MagicMock()
        mock_response.usage.prompt_tokens = 10
        mock_response.usage.completion_tokens = 5
        mock_response.usage.total_tokens = 15
        mock_response.usage.prompt_tokens_details.cached_tokens = 0

        mock_openai_client.return_value.chat.completions.create = AsyncMock(
            return_value=mock_response
        )

        client = LLMClient()
        messages = [{"role": "user", "content": "Test"}]

        async for _ in client.chat_completition(messages, stream=False):
            pass

        # Proveri da li je pozvan sa ispravnim parametrima
        mock_openai_client.return_value.chat.completions.create.assert_called_once()
        call_kwargs = (
            mock_openai_client.return_value.chat.completions.create.call_args[1]
        )
        assert call_kwargs["model"] == "glm-4.7"
        assert call_kwargs["messages"] == messages
        assert call_kwargs["stream"] is False

    @pytest.mark.asyncio
    async def test_chat_completion_handles_empty_content(
        self, mock_openai_client
    ):
        """Testira scenario kada je content None."""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = None
        mock_response.choices[0].finish_reason = "stop"
        mock_response.usage = None

        mock_openai_client.return_value.chat.completions.create = AsyncMock(
            return_value=mock_response
        )

        client = LLMClient()
        messages = [{"role": "user", "content": "Test"}]

        events = []
        async for event in client.chat_completition(messages, stream=False):
            events.append(event)

        assert len(events) == 1
        assert events[0].text_delta is None
        assert events[0].usage is None

    @pytest.mark.asyncio
    async def test_chat_completion_handles_no_usage(self, mock_openai_client):
        """Testira scenario kada usage nije prisutan."""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Test"
        mock_response.choices[0].finish_reason = "stop"
        mock_response.usage = None

        mock_openai_client.return_value.chat.completions.create = AsyncMock(
            return_value=mock_response
        )

        client = LLMClient()
        messages = [{"role": "user", "content": "Test"}]

        events = []
        async for event in client.chat_completition(messages, stream=False):
            events.append(event)

        assert len(events) == 1
        assert events[0].usage is None


class TestNonStreamResponse:
    """Testovi za _non_stream_response metod."""

    @pytest.mark.asyncio
    async def test_non_stream_response_returns_stream_event(
        self, mock_openai_client
    ):
        """Testira da _non_stream_response vraća StreamEvent."""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Test response"
        mock_response.choices[0].finish_reason = "stop"
        mock_response.usage = MagicMock()
        mock_response.usage.prompt_tokens = 10
        mock_response.usage.completion_tokens = 5
        mock_response.usage.total_tokens = 15
        mock_response.usage.prompt_tokens_details.cached_tokens = 0

        mock_openai_client.return_value.chat.completions.create = AsyncMock(
            return_value=mock_response
        )

        client = LLMClient()
        kwargs = {
            "model": "glm-4.7",
            "messages": [{"role": "user", "content": "Test"}],
            "stream": False,
        }

        result = await client._non_stream_response(
            mock_openai_client.return_value, kwargs
        )

        assert isinstance(result, StreamEvent)
        assert result.type == EventType.MESSAGE_COMPLETE
        assert result.text_delta.content == "Test response"
