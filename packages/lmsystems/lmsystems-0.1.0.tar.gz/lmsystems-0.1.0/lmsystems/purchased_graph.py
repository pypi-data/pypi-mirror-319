import jwt
from typing import Any, Optional, Union, Iterator, AsyncIterator, Sequence
from langgraph.pregel.remote import RemoteGraph
from langchain_core.runnables import RunnableConfig
from langgraph.pregel.protocol import PregelProtocol
from langgraph_sdk.client import LangGraphClient, SyncLangGraphClient
import requests
from .exceptions import (
    LmsystemsError,
    AuthenticationError,
    GraphError,
    InputError,
    APIError
)
import os
from lmsystems.config import Config
from langgraph.errors import GraphInterrupt
from langgraph_sdk.schema import StreamPart
from langgraph.pregel.types import All

class PurchasedGraph(PregelProtocol):
    """
    A wrapper class for RemoteGraph that handles marketplace authentication and graph purchasing.

    This class provides a simplified interface for working with purchased graphs from the marketplace,
    while maintaining full compatibility with LangGraph's RemoteGraph functionality.

    Attributes:
        graph_name (str): Name of the purchased graph
        api_key (str): Marketplace API key for authentication
        config (Optional[RunnableConfig]): Configuration for the graph
        default_state_values (dict): Default values to inject into graph state
        base_url (str): Marketplace API base URL
        development_mode (bool): Whether to run in development mode
        graph_info (dict): Cached graph information from marketplace
        remote_graph (RemoteGraph): Internal RemoteGraph instance

    Example:
        ```python
        graph = PurchasedGraph(
            graph_name="my-agent",
            api_key="api_key_123",
            default_state_values={
                "system_prompt": "You are a helpful assistant"
            }
        )

        result = graph.invoke({
            "messages": [{"role": "user", "content": "Hello"}]
        })
        ```
    """

    def __init__(
        self,
        graph_name: str,
        api_key: str,
        config: Optional[RunnableConfig] = None,
        default_state_values: Optional[dict[str, Any]] = None,
        base_url: str = Config.DEFAULT_BASE_URL,
        development_mode: bool = False,
    ):
        """
        Initialize a PurchasedGraph instance.

        Args:
            graph_name: The name of the purchased graph.
            api_key: The buyer's lmsystems API key.
            config: Optional RunnableConfig for additional configuration.
            default_state_values: Optional default values for required state parameters.
            base_url: The base URL of the marketplace backend.
            development_mode: Whether to run in development mode.

        Raises:
            AuthenticationError: If the API key is invalid
            GraphError: If the graph doesn't exist or hasn't been purchased
            InputError: If required configuration is invalid
            APIError: If there are backend communication issues
        """
        if not api_key:
            raise AuthenticationError("API key is required.")
        if not graph_name:
            raise InputError("Graph name is required")

        self.graph_name = graph_name
        self.api_key = api_key
        self.config = config
        self.default_state_values = default_state_values or {}
        self.base_url = base_url
        self.development_mode = development_mode

        try:
            # Authenticate and retrieve graph details
            self.graph_info = self._get_graph_info()

            # Merge stored configurables with any user-provided config
            stored_config = self.graph_info.get('configurables', {})
            merged_config = stored_config.copy()
            if config:
                if 'configurable' in config and 'configurable' in stored_config:
                    merged_config['configurable'].update(config['configurable'])
                else:
                    merged_config.update(config)

            # Get the LangGraph API key directly from response
            lgraph_api_key = self.graph_info.get('lgraph_api_key')
            if not lgraph_api_key:
                raise GraphError("LangGraph API key not found in response")

            # Create internal RemoteGraph instance with merged config
            self.remote_graph = RemoteGraph(
                self.graph_info['graph_name'],
                url=self.graph_info['graph_url'],
                api_key=lgraph_api_key,
                config=merged_config,
            )
        except Exception as e:
            raise APIError(f"Failed to initialize graph: {str(e)}")

    def _get_graph_info(self) -> dict:
        """
        Authenticate with the marketplace backend and retrieve graph details.

        This method handles the initial authentication and graph validation process.
        It verifies the API key, checks if the graph exists and has been purchased,
        and retrieves necessary configuration details.

        Returns:
            dict: Graph information including:
                - graph_name: Name of the graph
                - graph_url: URL for the graph deployment
                - lgraph_api_key: LangGraph API key for authentication
                - configurables: Default configuration values

        Raises:
            AuthenticationError: If the API key is invalid
            GraphError: If the graph doesn't exist or hasn't been purchased
            APIError: If there are backend communication issues
        """
        try:
            endpoint = f"{self.base_url}/api/get_graph_info"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }
            payload = {"graph_name": self.graph_name}

            response = requests.post(endpoint, json=payload, headers=headers)

            if response.status_code == 401:
                raise AuthenticationError("Invalid API key.")
            elif response.status_code == 403:
                raise GraphError(f"Graph '{self.graph_name}' has not been purchased")
            elif response.status_code == 404:
                raise GraphError(f"Graph '{self.graph_name}' not found")
            elif response.status_code != 200:
                raise APIError(f"Backend API error: {response.text}")

            return response.json()
        except requests.RequestException as e:
            raise APIError(f"Failed to communicate with backend: {str(e)}")

    def _extract_api_key(self, access_token: str) -> str:
        """Extract the LangGraph API key from the JWT token without verification."""
        try:
            decoded_token = jwt.decode(access_token, options={"verify_signature": False})
            lgraph_api_key = decoded_token.get("lgraph_api_key")
            if not lgraph_api_key:
                raise GraphAuthenticationError("LangGraph API key not found in token payload")
            return lgraph_api_key
        except jwt.InvalidTokenError as e:
            raise GraphAuthenticationError(f"Invalid access token: {str(e)}")
        except Exception as e:
            raise GraphAuthenticationError(f"Failed to decode token: {str(e)}")

    def _prepare_input(self, input: Union[dict[str, Any], Any]) -> dict[str, Any]:
        """
        Merge input with default state values.

        This method ensures that any default values specified during initialization
        are properly merged with the input for each graph invocation.

        Args:
            input: The input to prepare. Can be either a dict or any other type.
                  If dict, it will be merged with default_state_values.

        Returns:
            The prepared input with default values merged in if applicable

        Raises:
            ValidationError: If input preparation fails
        """
        try:
            if isinstance(input, dict):
                return {**self.default_state_values, **input}
            return input
        except Exception as e:
            raise ValidationError(f"Failed to prepare input: {str(e)}")

    def invoke(
        self,
        input: Union[dict[str, Any], Any],
        config: Optional[RunnableConfig] = None,
        *,
        interrupt_before: Optional[Union[All, Sequence[str]]] = None,
        interrupt_after: Optional[Union[All, Sequence[str]]] = None,
        **kwargs: Any
    ) -> Union[dict[str, Any], Any]:
        """
        Invoke the purchased graph synchronously.

        This method handles the synchronous execution of the graph, including input
        preparation and error handling. It automatically injects default state values
        and handles stream mode configuration.

        Args:
            input: The input to the graph. If dict, merged with default_state_values
            config: Optional configuration for this specific invocation
            interrupt_before: Optional node names to interrupt before execution
            interrupt_after: Optional node names to interrupt after execution
            **kwargs: Additional arguments passed to RemoteGraph

        Returns:
            The final output from the graph execution

        Raises:
            GraphInterrupt: If graph execution was interrupted
            GraphError: If graph execution failed
            LmsystemsError: For any marketplace-specific errors
        """
        try:
            prepared_input = self._prepare_input(input)

            # Remove stream_mode if present in kwargs since invoke() doesn't accept it
            kwargs.pop('stream_mode', None)

            return self.remote_graph.invoke(
                prepared_input,
                config=config,
                interrupt_before=interrupt_before,
                interrupt_after=interrupt_after,
                **kwargs
            )
        except GraphInterrupt as e:
            raise GraphInterrupt(e.args[0])
        except Exception as e:
            if isinstance(e, LmsystemsError):
                raise
            raise GraphError(f"Failed to execute graph: {str(e)}")

    def stream(
        self,
        input: Union[dict[str, Any], Any],
        config: Optional[RunnableConfig] = None,
        *,
        stream_mode: Optional[Union[str, list[str]]] = None,
        interrupt_before: Optional[Union[All, Sequence[str]]] = None,
        interrupt_after: Optional[Union[All, Sequence[str]]] = None,
        subgraphs: bool = False,
        **kwargs: Any
    ) -> Iterator[Any]:
        """
        Stream results from the purchased graph synchronously.

        This method provides streaming access to graph execution results,
        allowing for real-time processing of outputs.

        Args:
            input: The input to the graph. If dict, merged with default_state_values
            config: Optional configuration for this specific stream
            stream_mode: What to stream ("messages", "values", etc)
            interrupt_before: Optional node names to interrupt before execution
            interrupt_after: Optional node names to interrupt after execution
            subgraphs: Whether to include subgraph outputs in stream
            **kwargs: Additional arguments passed to RemoteGraph

        Yields:
            Chunks of the graph execution output based on stream_mode

        Raises:
            GraphInterrupt: If graph execution was interrupted
            GraphError: If streaming failed
            LmsystemsError: For any marketplace-specific errors
        """
        try:
            prepared_input = self._prepare_input(input)
            return self.remote_graph.stream(
                prepared_input,
                config=config,
                stream_mode=stream_mode,
                interrupt_before=interrupt_before,
                interrupt_after=interrupt_after,
                subgraphs=subgraphs,
                **kwargs
            )
        except GraphInterrupt as e:
            raise GraphInterrupt(e.args[0])
        except Exception as e:
            if isinstance(e, LmsystemsError):
                raise
            raise GraphError(f"Failed to stream from graph: {str(e)}")

    async def ainvoke(
        self,
        input: Union[dict[str, Any], Any],
        config: Optional[RunnableConfig] = None,
        *,
        interrupt_before: Optional[Union[All, Sequence[str]]] = None,
        interrupt_after: Optional[Union[All, Sequence[str]]] = None,
        **kwargs: Any
    ) -> Union[dict[str, Any], Any]:
        """
        Invoke the purchased graph asynchronously.

        Async version of invoke() that provides the same functionality but returns
        a coroutine for use with async/await syntax.

        Args:
            input: The input to the graph. If dict, merged with default_state_values
            config: Optional configuration for this specific invocation
            interrupt_before: Optional node names to interrupt before execution
            interrupt_after: Optional node names to interrupt after execution
            **kwargs: Additional arguments passed to RemoteGraph

        Returns:
            The final output from the graph execution

        Raises:
            GraphInterrupt: If graph execution was interrupted
            GraphError: If graph execution failed
            LmsystemsError: For any marketplace-specific errors
        """
        try:
            prepared_input = self._prepare_input(input)
            return await self.remote_graph.ainvoke(
                prepared_input,
                config=config,
                interrupt_before=interrupt_before,
                interrupt_after=interrupt_after,
                **kwargs,
            )
        except GraphInterrupt as e:
            raise GraphInterrupt(e.args[0])
        except Exception as e:
            if isinstance(e, LmsystemsError):
                raise
            raise GraphError(f"Failed to execute graph: {str(e)}")

    async def astream(
        self,
        input: Union[dict[str, Any], Any],
        config: Optional[RunnableConfig] = None,
        *,
        stream_mode: Optional[Union[str, list[str]]] = None,
        interrupt_before: Optional[Union[All, Sequence[str]]] = None,
        interrupt_after: Optional[Union[All, Sequence[str]]] = None,
        subgraphs: bool = False,
        **kwargs: Any
    ) -> AsyncIterator[Any]:
        """
        Stream results from the purchased graph asynchronously.

        Async version of stream() that provides the same functionality but returns
        an async iterator for use with async for syntax.

        Args:
            input: The input to the graph. If dict, merged with default_state_values
            config: Optional configuration for this specific stream
            stream_mode: What to stream ("messages", "values", etc)
            interrupt_before: Optional node names to interrupt before execution
            interrupt_after: Optional node names to interrupt after execution
            subgraphs: Whether to include subgraph outputs in stream
            **kwargs: Additional arguments passed to RemoteGraph

        Yields:
            Chunks of the graph execution output based on stream_mode

        Raises:
            GraphInterrupt: If graph execution was interrupted
            GraphError: If streaming failed
            LmsystemsError: For any marketplace-specific errors
        """
        try:
            prepared_input = self._prepare_input(input)
            async for chunk in self.remote_graph.astream(
                prepared_input,
                config=config,
                interrupt_before=interrupt_before,
                interrupt_after=interrupt_after,
                stream_mode=stream_mode,
                subgraphs=subgraphs,
                **kwargs,
            ):
                yield chunk
        except GraphInterrupt as e:
            raise GraphInterrupt(e.args[0])
        except Exception as e:
            if isinstance(e, LmsystemsError):
                raise
            raise GraphError(f"Failed to stream from graph: {str(e)}")
    def with_config(self, config: Optional[RunnableConfig] = None, **kwargs: Any) -> Any:
        """
        Return a modified copy of the 'PurchasedGraph' or its underlying
        RemoteGraph with merged config, so advanced usage can be done
        (e.g. setting thread_id).
        """
        # Option 1: just return remote_graph.with_config(...)
        #     which effectively returns a RemoteGraph.
        # Option 2: re-initialize a new PurchasedGraph if you
        #     want to preserve the same class type.
        # For simplicity, we keep returning RemoteGraph itself:
        return self.remote_graph.with_config(config, **kwargs)

    def get_graph(self, config: Optional[RunnableConfig] = None, *, xray: Union[int, bool] = False) -> Any:
        return self.remote_graph.get_graph(config=config, xray=xray)

    async def aget_graph(self, config: Optional[RunnableConfig] = None, *, xray: Union[int, bool] = False) -> Any:
        return await self.remote_graph.aget_graph(config=config, xray=xray)

    def get_state(self, config: RunnableConfig, *, subgraphs: bool = False) -> Any:
        return self.remote_graph.get_state(config=config, subgraphs=subgraphs)

    async def aget_state(self, config: RunnableConfig, *, subgraphs: bool = False) -> Any:
        return await self.remote_graph.aget_state(config=config, subgraphs=subgraphs)

    def get_state_history(self, config: RunnableConfig, *, filter: Optional[dict[str, Any]] = None, before: Optional[RunnableConfig] = None, limit: Optional[int] = None) -> Any:
        return self.remote_graph.get_state_history(config=config, filter=filter, before=before, limit=limit)

    async def aget_state_history(self, config: RunnableConfig, *, filter: Optional[dict[str, Any]] = None, before: Optional[RunnableConfig] = None, limit: Optional[int] = None) -> Any:
        return await self.remote_graph.aget_state_history(config=config, filter=filter, before=before, limit=limit)

    def update_state(self, config: RunnableConfig, values: Optional[Union[dict[str, Any], Any]], as_node: Optional[str] = None) -> RunnableConfig:
        return self.remote_graph.update_state(config=config, values=values, as_node=as_node)

    async def aupdate_state(self, config: RunnableConfig, values: Optional[Union[dict[str, Any], Any]], as_node: Optional[str] = None) -> RunnableConfig:
        return await self.remote_graph.aupdate_state(config=config, values=values, as_node=as_node)

