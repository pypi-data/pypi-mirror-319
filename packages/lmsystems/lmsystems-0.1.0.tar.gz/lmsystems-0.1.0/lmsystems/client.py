import httpx
from typing import Optional, Any, AsyncIterator, Union, Iterator, List
import jwt
from langgraph_sdk import get_client, get_sync_client
from .exceptions import AuthenticationError, GraphError, APIError
from .config import Config
from enum import Enum
import time
import asyncio

class StreamMode(str, Enum):
    """Enum defining available stream modes for run execution.

    Attributes:
        MESSAGES: Stream message updates from the graph
        VALUES: Stream value updates from graph nodes
        UPDATES: Stream general state updates
        CUSTOM: Stream custom-defined updates
    """
    MESSAGES = "messages"
    VALUES = "values"
    UPDATES = "updates"
    CUSTOM = "custom"

class MultitaskStrategy(str, Enum):
    """Enum defining strategies for handling concurrent tasks on a thread.

    Attributes:
        REJECT: Reject new tasks if thread is busy
        ROLLBACK: Roll back current task and start new one
        INTERRUPT: Pause current task for human interaction
        ENQUEUE: Queue new tasks to run after current one
    """
    REJECT = "reject"
    ROLLBACK = "rollback"
    INTERRUPT = "interrupt"
    ENQUEUE = "enqueue"

class ThreadStatus(str, Enum):
    """Enum representing possible thread states.

    Attributes:
        IDLE: Thread is available for new tasks
        BUSY: Thread is currently processing a task
        INTERRUPTED: Thread is paused waiting for human input
    """
    IDLE = "idle"
    BUSY = "busy"
    INTERRUPTED = "interrupted"

class LmsystemsClient:
    """Asynchronous client for the Lmsystems API that wraps LangGraph functionality.

    This client provides high-level access to graph execution with proper error handling,
    state management, and streaming support. It handles authentication and provides
    a simpler interface compared to direct LangGraph usage.

    Example:
        ```python
        # Initialize client
        client = await LmsystemsClient.create(
            graph_name="github-agentz-6",
            api_key="your-api-key"
        )

        # Create thread and stream run
        thread = await client.create_thread()
        async for chunk in client.stream_run(
            thread=thread,
            input={
                "messages": [{"role": "user", "content": "What's this repo about?"}],
                "repo_url": "https://github.com/user/repo",
                "chat_mode": "ask"
            },
            stream_mode=["messages"]
        ):
            print(chunk)
        ```

    Attributes:
        graph_name: Name of the purchased graph
        api_key: API key for authentication
        base_url: Base URL for the API
        client: Underlying LangGraph client instance
        default_assistant_id: Default assistant ID from graph info
    """

    def __init__(
        self,
        graph_name: str,
        api_key: str,
        base_url: str = Config.DEFAULT_BASE_URL,
    ) -> None:
        """
        Initialize the Lmsystems client.

        Args:
            graph_name: The name of the purchased graph
            api_key: The Lmsystems API key
            base_url: Base URL for the Lmsystems API
        """
        self.graph_name = graph_name
        self.api_key = api_key

        # Validate and set base URL
        if not base_url:
            base_url = "https://api.lmsystems.ai"
        if not base_url.startswith(("http://", "https://")):
            base_url = f"https://{base_url}"
        self.base_url = base_url.rstrip('/')  # Remove trailing slash if present

        self.client = None
        self.default_assistant_id = None

    @classmethod
    async def create(
        cls,
        graph_name: str,
        api_key: str,
        base_url: str = Config.DEFAULT_BASE_URL,
    ) -> "LmsystemsClient":
        """Async factory method to create and initialize the client."""
        client = cls(graph_name, api_key, base_url)
        await client.setup()
        return client

    async def setup(self) -> None:
        """Initialize the client asynchronously."""
        try:
            # Store graph info for later use of configurables
            self.graph_info = await self._get_graph_info()

            # Store default assistant_id and use lgraph_api_key directly
            self.default_assistant_id = self.graph_info.get('assistant_id')

            self.client = get_client(
                url=self.graph_info['graph_url'],
                api_key=self.graph_info['lgraph_api_key']
            )
        except Exception as e:
            raise APIError(f"Failed to initialize client: {str(e)}")

    async def _get_graph_info(self) -> dict:
        """Authenticate and retrieve graph connection details."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/api/get_graph_info",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={"graph_name": self.graph_name}
                )

                if response.status_code == 401:
                    raise AuthenticationError("Invalid API key")
                elif response.status_code == 403:
                    raise GraphError(f"Graph '{self.graph_name}' has not been purchased")
                elif response.status_code == 404:
                    raise GraphError(f"Graph '{self.graph_name}' not found")
                elif response.status_code != 200:
                    raise APIError(f"Backend API error: {response.text}")

                return response.json()
        except httpx.RequestError as e:
            raise APIError(f"Failed to communicate with server: {str(e)}")

    def _extract_api_key(self, access_token: str) -> str:
        """Extract LangGraph API key from JWT token."""
        try:
            decoded = jwt.decode(access_token, options={"verify_signature": False})
            lgraph_api_key = decoded.get("lgraph_api_key")
            if not lgraph_api_key:
                raise AuthenticationError("LangGraph API key not found in token")
            return lgraph_api_key
        except jwt.InvalidTokenError as e:
            raise AuthenticationError(f"Invalid access token: {str(e)}")

    # Helper method to handle thread ID format
    def _get_thread_id(self, thread: dict) -> str:
        """Extract thread ID from response, handling both formats."""
        if "thread_id" in thread:
            return thread["thread_id"]
        elif "id" in thread:
            return thread["id"]
        raise APIError("Invalid thread response format")

    # Delegate methods with improved error handling
    async def create_thread(self, **kwargs) -> dict:
        """Create a new thread with error handling."""
        try:
            return await self.client.threads.create(**kwargs)
        except Exception as e:
            raise APIError(f"Failed to create thread: {str(e)}")

    async def create_run(
        self,
        thread: dict,
        *,
        input: dict,
        assistant_id: Optional[str] = None,
        multitask_strategy: Optional[str] = MultitaskStrategy.REJECT,
        wait_for_idle: bool = True,
        timeout: int = 30,
    ) -> dict:
        """Create a run with proper thread state handling."""
        try:
            thread_id = thread.get("thread_id") or thread.get("id")
            if not thread_id:
                raise APIError("Invalid thread format")

            # Check thread status if we're not using REJECT strategy
            if multitask_strategy != MultitaskStrategy.REJECT:
                status = await self.get_thread_status(thread)
                if status == ThreadStatus.BUSY:
                    if wait_for_idle:
                        if not await self.wait_for_thread(thread, timeout):
                            raise APIError(f"Thread still busy after {timeout} seconds")
                    else:
                        raise APIError("Thread is busy. Set wait_for_idle=True to wait")

            # Use provided assistant_id or fall back to default
            assistant_id = assistant_id or self.default_assistant_id
            if not assistant_id:
                raise APIError("No assistant_id provided and no default available")

            return await self.client.runs.create(
                thread_id=thread_id,
                assistant_id=assistant_id,
                input=input,
                multitask_strategy=multitask_strategy
            )

        except Exception as e:
            raise APIError(f"Failed to create run: {str(e)}")

    async def stream_run(
        self,
        thread: dict,
        input: dict,
        *,
        assistant_id: Optional[str] = None,
        stream_mode: Union[str, List[str]] = ["messages"],
        multitask_strategy: Optional[str] = MultitaskStrategy.REJECT,
        wait_for_idle: bool = True,
        timeout: int = 30,
        interrupt_before: Optional[List[str]] = None,
    ) -> AsyncIterator[dict]:
        """Stream a run with proper thread state handling.

        This is the recommended way to execute graph runs as it handles thread state
        management and provides real-time streaming of results.

        Example:
            ```python
            async for chunk in client.stream_run(
                thread=thread,
                input={
                    "messages": [{"role": "user", "content": "Analyze this repo"}],
                    "repo_url": "https://github.com/user/repo",
                    "chat_mode": "ask"
                },
                stream_mode=["messages", "updates"],
                multitask_strategy=MultitaskStrategy.INTERRUPT
            ):
                print(chunk)
            ```

        Args:
            thread: Thread dict containing thread_id
            input: Input data for the run
            assistant_id: Optional assistant ID (defaults to self.default_assistant_id)
            stream_mode: What to stream (default: ["messages"])
            multitask_strategy: How to handle concurrent tasks
            wait_for_idle: Whether to wait for thread to become idle if busy
            timeout: Maximum time to wait for thread to become idle
            interrupt_before: Optional list of node names to interrupt before

        Returns:
            AsyncIterator yielding streamed responses

        Raises:
            APIError: If thread is busy and wait_for_idle is False, or other API errors
        """
        try:
            thread_id = thread.get("thread_id") or thread.get("id")
            if not thread_id:
                raise APIError("Invalid thread format")

            # Check thread status if we're not using REJECT strategy
            if multitask_strategy != MultitaskStrategy.REJECT:
                status = await self.get_thread_status(thread)
                if status == ThreadStatus.BUSY:
                    if wait_for_idle:
                        if not await self.wait_for_thread(thread, timeout):
                            raise APIError(f"Thread still busy after {timeout} seconds")
                    else:
                        raise APIError("Thread is busy. Set wait_for_idle=True to wait")

            # Use the assistant_id from the run or fall back to default
            assistant_id = assistant_id or self.default_assistant_id
            if not assistant_id:
                raise APIError("No assistant_id available")

            # Always ensure stream_mode is a list
            if isinstance(stream_mode, str):
                stream_mode = [stream_mode]

            # Use client.runs.stream directly with all parameters
            async for chunk in self.client.runs.stream(
                thread_id,
                assistant_id,
                input=input,
                stream_mode=stream_mode,
                multitask_strategy=multitask_strategy,
                interrupt_before=interrupt_before
            ):
                yield chunk

        except Exception as e:
            raise APIError(f"Failed to stream run: {str(e)}")

    async def stream_run_events(
        self,
        thread: dict,
        run: dict,
        *,
        version: str = "v1"
    ) -> AsyncIterator[dict]:
        """Stream individual events from a run.

        Args:
            thread: Thread object containing thread_id
            run: Run object containing run_id
            version: Event format version ("v1" or "v2")

        Returns:
            AsyncIterator yielding event objects
        """
        try:
            thread_id = self._get_thread_id(thread)
            run_id = run.get("run_id") or run.get("id")

            if not run_id:
                raise APIError("Invalid run response format")

            async for event in self.client.runs.stream_events(
                thread_id=thread_id,
                run_id=run_id,
                version=version
            ):
                yield event

        except Exception as e:
            raise APIError(f"Failed to stream run events: {str(e)}")

    @property
    def assistants(self):
        """Access the assistants API."""
        return self.client.assistants

    @property
    def threads(self):
        """Access the threads API."""
        return self.client.threads

    @property
    def runs(self):
        """Access the runs API."""
        return self.client.runs

    @property
    def crons(self):
        """Access the crons API."""
        return self.client.crons

    @property
    def store(self):
        """Access the store API."""
        return self.client.store

    async def get_thread_status(self, thread: dict) -> str:
        """Get the current status of a thread."""
        thread_id = thread.get("thread_id") or thread.get("id")
        if not thread_id:
            raise APIError("Invalid thread format")

        thread_info = await self.threads.get(thread_id)
        return thread_info.get("status", ThreadStatus.IDLE)

    async def wait_for_thread(self, thread: dict, timeout: int = 30) -> bool:
        """Wait for thread to become idle, with timeout."""
        thread_id = thread.get("thread_id") or thread.get("id")
        start_time = time.time()

        while time.time() - start_time < timeout:
            status = await self.get_thread_status(thread)
            if status == ThreadStatus.IDLE:
                return True
            await asyncio.sleep(1)
        return False

    def get_thread_state(self, thread: dict) -> dict:
        """Get the current state of a thread."""
        thread_id = thread.get("thread_id") or thread.get("id")
        if not thread_id:
            raise APIError("Invalid thread format")
        return self.client.threads.get_state(thread_id)

    def update_thread_state(self, thread: dict, state_update: dict, *, as_node: str = None) -> dict:
        """Update the state of a thread."""
        thread_id = thread.get("thread_id") or thread.get("id")
        if not thread_id:
            raise APIError("Invalid thread format")

        # Pass state_update directly as first argument after thread_id
        if as_node:
            return self.client.threads.update_state(thread_id, state_update, as_node=as_node)
        return self.client.threads.update_state(thread_id, state_update)

    def stream_run(
        self,
        thread: dict,
        input: Optional[dict] = None,
        *,
        assistant_id: Optional[str] = None,
        checkpoint_id: Optional[str] = None,
        stream_mode: Optional[List[str]] = None,
        multitask_strategy: Optional[str] = MultitaskStrategy.REJECT,
    ) -> Iterator[dict]:
        """Stream a run with proper thread state handling.

        Args:
            thread: Thread dict containing thread_id
            input: Optional input for the run
            assistant_id: Optional assistant ID (defaults to self.default_assistant_id)
            checkpoint_id: Optional checkpoint ID to resume from
            stream_mode: What to stream (default: ["messages", "updates"])
            multitask_strategy: Strategy for handling multiple tasks
        """
        thread_id = thread.get("thread_id") or thread.get("id")
        if not thread_id:
            raise APIError("Invalid thread format")

        # Use provided assistant_id or fall back to default
        assistant_id = assistant_id or self.default_assistant_id
        if not assistant_id:
            raise APIError("No assistant_id provided and no default available")

        # Set default stream_mode if not provided
        if stream_mode is None:
            stream_mode = ["messages", "updates"]

        return self.client.runs.stream(
            thread_id=thread_id,
            assistant_id=assistant_id,
            input=input,
            checkpoint_id=checkpoint_id,
            stream_mode=stream_mode,
            multitask_strategy=multitask_strategy
        )


class SyncLmsystemsClient:
    """Synchronous client for the Lmsystems API that wraps LangGraph functionality.

    This provides the same interface as LmsystemsClient but in a synchronous form,
    suitable for scripts and applications that don't use async/await.

    Example:
        ```python
        # Initialize client
        client = SyncLmsystemsClient(
            graph_name="github-agentz-6",
            api_key="your-api-key"
        )

        # Create thread and stream run
        thread = client.threads.create()
        for chunk in client.stream_run(
            thread=thread,
            input={
                "messages": [{"role": "user", "content": "What's this repo about?"}],
                "repo_url": "https://github.com/user/repo",
                "chat_mode": "ask"
            },
            stream_mode=["messages"]
        ):
            print(chunk)
        ```

    Example (Resuming Interrupted Graph):
        ```python
        # Resume from interrupted state
        thread = {"thread_id": "existing-thread-id"}

        # Update state at specific node
        client.update_thread_state(
            thread=thread,
            state_update={
                "messages": [{"role": "user", "content": "continue"}],
                "accepted": True
            },
            as_node="human_interaction"
        )

        # Resume with checkpoint
        for chunk in client.stream_run(
            thread=thread,
            input=None,
            checkpoint_id=checkpoint_id
        ):
            print(chunk)
        ```

    Attributes:
        graph_name: Name of the purchased graph
        api_key: API key for authentication
        base_url: Base URL for the API
        client: Underlying LangGraph sync client instance
        default_assistant_id: Default assistant ID from graph info
    """

    def __init__(
        self,
        graph_name: str,
        api_key: str,
        base_url: str = Config.DEFAULT_BASE_URL,
    ) -> None:
        """Initialize the synchronous client."""
        self.graph_name = graph_name
        self.api_key = api_key
        self.base_url = base_url

        # Initialize these in setup
        self.client = None
        self.default_assistant_id = None
        self.graph_info = None

        # Call setup immediately for sync client
        self.setup()

    def setup(self) -> None:
        """Initialize the client synchronously."""
        try:
            # Get graph info first
            self.graph_info = self._get_graph_info()

            # Store assistant_id from graph info
            self.default_assistant_id = self.graph_info.get('assistant_id')
            if not self.default_assistant_id:
                raise APIError("No assistant_id found in graph info")

            # Initialize LangGraph client
            self.client = get_sync_client(
                url=self.graph_info['graph_url'],
                api_key=self.graph_info['lgraph_api_key']
            )
        except Exception as e:
            raise APIError(f"Failed to initialize client: {str(e)}")

    def _get_graph_info(self) -> dict:
        """Synchronous version of getting graph info."""
        try:
            with httpx.Client() as client:
                response = client.post(
                    f"{self.base_url}/api/get_graph_info",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={"graph_name": self.graph_name}
                )

                if response.status_code == 401:
                    raise AuthenticationError("Invalid API key")
                elif response.status_code == 403:
                    raise GraphError(f"Graph '{self.graph_name}' has not been purchased")
                elif response.status_code == 404:
                    raise GraphError(f"Graph '{self.graph_name}' not found")
                elif response.status_code != 200:
                    raise APIError(f"Backend API error: {response.text}")

                return response.json()
        except httpx.RequestError as e:
            raise APIError(f"Failed to connect to backend: {str(e)}")

    def _extract_api_key(self, access_token: str) -> str:
        """Extract LangGraph API key from JWT token."""
        try:
            decoded = jwt.decode(access_token, options={"verify_signature": False})
            if 'lgraph_api_key' not in decoded:
                raise AuthenticationError("Invalid token format")
            return decoded['lgraph_api_key']
        except jwt.InvalidTokenError as e:
            raise AuthenticationError(f"Invalid access token: {str(e)}")

    @property
    def assistants(self):
        """Access the assistants API."""
        return self.client.assistants

    @property
    def threads(self):
        """Access the threads API."""
        return self.client.threads

    @property
    def runs(self):
        """Access the runs API."""
        return self.client.runs

    @property
    def crons(self):
        """Access the crons API."""
        return self.client.crons

    @property
    def store(self):
        """Access the store API."""
        return self.client.store

    def create_run(
        self,
        thread: dict,
        *,
        input: dict,
        assistant_id: Optional[str] = None,
        multitask_strategy: Optional[str] = MultitaskStrategy.REJECT,
        wait_for_idle: bool = True,
        timeout: int = 30,
    ) -> dict:
        """Create a run with proper thread state handling."""
        try:
            thread_id = thread.get("thread_id") or thread.get("id")
            if not thread_id:
                raise APIError("Invalid thread format")

            # Check thread status if we're not using REJECT strategy
            if multitask_strategy != MultitaskStrategy.REJECT:
                status = self.get_thread_status(thread)
                if status == ThreadStatus.BUSY:
                    if wait_for_idle:
                        if not self.wait_for_thread(thread, timeout):
                            raise APIError(f"Thread still busy after {timeout} seconds")
                    else:
                        raise APIError("Thread is busy. Set wait_for_idle=True to wait")

            # Use provided assistant_id or fall back to default
            assistant_id = assistant_id or self.default_assistant_id
            if not assistant_id:
                raise APIError("No assistant_id provided and no default available")

            return self.client.runs.create(
                thread_id=thread_id,
                assistant_id=assistant_id,
                input=input,
                multitask_strategy=multitask_strategy
            )

        except Exception as e:
            raise APIError(f"Failed to create run: {str(e)}")

    def stream_run(
        self,
        thread: dict,
        input: dict,
        *,
        assistant_id: Optional[str] = None,
        checkpoint_id: Optional[str] = None,
        stream_mode: Optional[List[str]] = None,
        multitask_strategy: Optional[str] = MultitaskStrategy.REJECT,
    ) -> Iterator[dict]:
        """Stream a run with proper thread state handling.

        Args:
            thread: Thread dict containing thread_id
            input: Optional input for the run
            assistant_id: Optional assistant ID (defaults to self.default_assistant_id)
            checkpoint_id: Optional checkpoint ID to resume from
            stream_mode: What to stream (default: ["messages", "updates"])
            multitask_strategy: Strategy for handling multiple tasks
        """
        thread_id = thread.get("thread_id") or thread.get("id")
        if not thread_id:
            raise APIError("Invalid thread format")

        # Use provided assistant_id or fall back to default
        assistant_id = assistant_id or self.default_assistant_id
        if not assistant_id:
            raise APIError("No assistant_id provided and no default available")

        # Set default stream_mode if not provided
        if stream_mode is None:
            stream_mode = ["messages", "updates"]

        return self.client.runs.stream(
            thread_id=thread_id,
            assistant_id=assistant_id,
            input=input,
            checkpoint_id=checkpoint_id,
            stream_mode=stream_mode,
            multitask_strategy=multitask_strategy
        )

    def stream_run_events(
        self,
        thread: dict,
        run: dict,
        *,
        version: str = "v1"
    ) -> Iterator[dict]:
        """Synchronous version of stream_run_events."""
        try:
            thread_id = thread.get("thread_id") or thread.get("id")
            run_id = run.get("run_id") or run.get("id")

            if not thread_id or not run_id:
                raise APIError("Invalid thread or run format")

            # Note the positional args here too
            for event in self.client.runs.stream_events(
                thread_id,  # Changed: removed keyword argument
                run_id,    # Changed: removed keyword argument
                version=version
            ):
                yield event

        except Exception as e:
            raise APIError(f"Failed to stream run events: {str(e)}")

    def get_thread_status(self, thread: dict) -> str:
        """Get the current status of a thread."""
        thread_id = thread.get("thread_id") or thread.get("id")
        if not thread_id:
            raise APIError("Invalid thread format")

        thread_info = self.threads.get(thread_id)
        return thread_info.get("status", ThreadStatus.IDLE)

    def wait_for_thread(self, thread: dict, timeout: int = 30) -> bool:
        """Wait for thread to become idle, with timeout."""
        thread_id = thread.get("thread_id") or thread.get("id")
        start_time = time.time()

        while time.time() - start_time < timeout:
            status = self.get_thread_status(thread)
            if status == ThreadStatus.IDLE:
                return True
            time.sleep(1)
        return False

    def get_thread_state(self, thread: dict) -> dict:
        """Get the current state of a thread."""
        thread_id = thread.get("thread_id") or thread.get("id")
        if not thread_id:
            raise APIError("Invalid thread format")
        return self.client.threads.get_state(thread_id)

    def update_thread_state(self, thread: dict, state_update: dict, *, as_node: str = None) -> dict:
        """Update the state of a thread."""
        thread_id = thread.get("thread_id") or thread.get("id")
        if not thread_id:
            raise APIError("Invalid thread format")

        # Pass state_update directly as first argument after thread_id
        if as_node:
            return self.client.threads.update_state(thread_id, state_update, as_node=as_node)
        return self.client.threads.update_state(thread_id, state_update)
