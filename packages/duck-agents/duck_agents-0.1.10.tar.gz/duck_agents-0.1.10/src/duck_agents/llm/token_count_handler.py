import logging
from typing import Any, Optional
from uuid import UUID, uuid4

from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.messages import AIMessage
from langchain_core.outputs import LLMResult, ChatGeneration
from langsmith.schemas import UsageMetadata

_logger = logging.getLogger(__name__)

class TokenCountHandler(BaseCallbackHandler):
    def __init__(self, identifier: Optional[str] = None):
        super().__init__()
        self.identifier = identifier if identifier else uuid4()
        self._input_token_count = 0
        self._output_token_count = 0
        self._call_count = 0
        TokenCountHandler._instances.append(self)

    _input_token_count = 0
    _output_token_count = 0
    _call_count = 0
    _instances = []

    @staticmethod
    def log_usage_overview() -> None:
        _logger.info(f"Total input token count: {TokenCountHandler.get_total_input_token_count()}")
        _logger.info(f"Total output token count: {TokenCountHandler.get_total_output_token_count()}")
        _logger.info(f"Total token count: {TokenCountHandler.get_total_token_count()}")
        _logger.info(f"Total call count: {TokenCountHandler.get_total_call_count()}\n")
        _logger.info("Session token counts:")
        for instance in TokenCountHandler._instances:
            _logger.info(f"Session {instance.identifier}:")
            _logger.info(f"\tInput token count: {instance.get_input_token_count()}")
            _logger.info(f"\tOutput token count: {instance.get_output_token_count()}")
            _logger.info(f"\tToken count: {instance.get_token_count()}")
            _logger.info(f"\tCall count: {instance.get_call_count()}")

    @staticmethod
    def remove_instance(instance: "TokenCountHandler") -> None:
        TokenCountHandler._instances.remove(instance)

    @staticmethod
    def get_total_token_count() -> int:
        return TokenCountHandler._input_token_count + TokenCountHandler._output_token_count

    @staticmethod
    def add_total_input_token_count(count: int) -> int:
        TokenCountHandler._input_token_count += count
        return TokenCountHandler._input_token_count

    @staticmethod
    def reset_total_input_token_count() -> int:
        TokenCountHandler._input_token_count = 0
        for instance in TokenCountHandler._instances:
            instance.reset_input_token_count()
        return TokenCountHandler._input_token_count

    @staticmethod
    def get_total_input_token_count() -> int:
        return TokenCountHandler._input_token_count

    @staticmethod
    def add_total_output_token_count(count: int) -> int:
        TokenCountHandler._output_token_count += count
        return TokenCountHandler._output_token_count

    @staticmethod
    def reset_total_output_token_count() -> int:
        TokenCountHandler._output_token_count = 0
        for instance in TokenCountHandler._instances:
            instance.reset_output_token_count()
        return TokenCountHandler._output_token_count

    @staticmethod
    def get_total_output_token_count() -> int:
        return TokenCountHandler._output_token_count

    @staticmethod
    def increment_total_call_count() -> int:
        TokenCountHandler._call_count += 1
        return TokenCountHandler._call_count

    @staticmethod
    def reset_total_call_count() -> int:
        TokenCountHandler._call_count = 0
        for instance in TokenCountHandler._instances:
            instance.reset_call_count()
        return TokenCountHandler._call_count

    @staticmethod
    def get_total_call_count() -> int:
        return TokenCountHandler._call_count

    def get_token_count(self) -> int:
        return self._input_token_count + self._output_token_count

    def add_input_token_count(self, count: int) -> int:
        self._input_token_count += count
        TokenCountHandler.add_total_input_token_count(count)
        return self._input_token_count

    def reset_input_token_count(self) -> int:
        self._input_token_count = 0
        return self._input_token_count

    def get_input_token_count(self) -> int:
        return self._input_token_count

    def add_output_token_count(self, count: int) -> int:
        self._output_token_count += count
        TokenCountHandler.add_total_output_token_count(count)
        return self._output_token_count

    def reset_output_token_count(self) -> int:
        self._output_token_count = 0
        return self._output_token_count

    def get_output_token_count(self) -> int:
        return self._output_token_count

    def increment_call_count(self) -> int:
        self._call_count += 1
        TokenCountHandler.increment_total_call_count()
        return self._call_count

    def reset_call_count(self) -> int:
        self._call_count = 0
        return self._call_count

    def get_call_count(self) -> int:
        return self._call_count

    def on_llm_end(
            self,
            response: LLMResult,
            *,
            run_id: UUID,
            parent_run_id: Optional[UUID] = None,
            **kwargs: Any,
    ) -> Any:
        for generation_candidates in response.generations:
            if len(generation_candidates) > 1:
                _logger.info("Multiple generation candidates. Including all token counts.")
            for generation_candidate in generation_candidates:
                if not isinstance(generation_candidate, ChatGeneration):
                    _logger.warning("Generation is not a ChatGeneration. Skipping token count.")
                    continue
                if not isinstance(generation_candidate.message, AIMessage):
                    _logger.warning("Generation message is not an AIMessage. Skipping token count.")
                    continue
                if generation_candidate.message.usage_metadata is None:
                    _logger.warning("Generation message usage metadata is None. Skipping token count.")
                    continue
                usage_metadata : UsageMetadata = generation_candidate.message.usage_metadata
                self.add_input_token_count(usage_metadata["input_tokens"])
                self.add_output_token_count(usage_metadata["output_tokens"])
            self.increment_call_count()