"""
Connect to the Google Gemini API to their LLMs. See more `Gemini <https://ai.google.dev>`_.
"""

# Copyright © 2024- Frello Technology Private Limited
# https://ai.google.dev/gemini-api/docs/function-calling

import httpx
import requests
from pydantic import BaseModel
from typing import get_args, get_origin, List, Optional, Dict, Any, Union

import tuneapi.utils as tu
import tuneapi.types as tt
from tuneapi.apis.turbo import distributed_chat, distributed_chat_async


class Gemini(tt.ModelInterface):

    def __init__(
        self,
        id: Optional[str] = "gemini-1.5-flash",
        base_url: str = "https://generativelanguage.googleapis.com/v1beta/models/{id}:{rpc}",
        extra_headers: Optional[Dict[str, str]] = None,
    ):
        self.model_id = id
        self.base_url = base_url
        self.api_token = tu.ENV.GEMINI_TOKEN("")
        self.extra_headers = extra_headers

    def set_api_token(self, token: str) -> None:
        self.api_token = token

    def _process_input(self, chats, token: Optional[str] = None):
        if not token and not self.api_token:  # type: ignore
            raise Exception(
                "Gemini API key not found. Please set GEMINI_TOKEN environment variable or pass through function"
            )
        if isinstance(chats, tt.Thread):
            thread = chats
        elif isinstance(chats, str):
            thread = tt.Thread(tt.human(chats))
        else:
            raise Exception("Invalid input")

        system = ""
        if thread.chats[0].role == tt.Message.SYSTEM:
            system = thread.chats[0].value

        messages = []
        prev_fn_name = ""
        for m in thread.chats[int(system != "") :]:
            if m.role == tt.Message.HUMAN:
                inline_objects = []
                for img in m.images:
                    inline_objects.append({"mime_type": "image/png", "data": img})
                if len(inline_objects) > 1:
                    inline_objects.append({"text": m.value})
                else:
                    inline_objects.insert(0, {"text": m.value})
                messages.append({"role": "user", "parts": inline_objects})
            elif m.role == tt.Message.GPT:
                inline_objects = []
                for img in m.images:
                    inline_objects.append({"mime_type": "image/png", "data": img})
                if len(inline_objects) > 1:
                    inline_objects.append({"text": m.value})
                else:
                    inline_objects.insert(0, {"text": m.value})
                messages.append({"role": "model", "parts": inline_objects})
            elif m.role == tt.Message.FUNCTION_CALL:
                _m = tu.from_json(m.value) if isinstance(m.value, str) else m.value
                prev_fn_name = _m["name"]
                messages.append(
                    {
                        "role": "model",
                        "parts": [
                            {
                                "functionCall": {
                                    "name": _m["name"],
                                    "args": _m["arguments"],
                                }
                            }
                        ],
                    }
                )
            elif m.role == tt.Message.FUNCTION_RESP:
                # _m = tu.from_json(m.value) if isinstance(m.value, str) else m.value
                messages.append(
                    {
                        "role": "function",
                        "parts": [
                            {
                                "functionResponse": {
                                    "name": prev_fn_name,
                                    "response": {
                                        "name": prev_fn_name,
                                        "content": m.value,
                                    },
                                }
                            }
                        ],
                    }
                )
            else:
                raise Exception(f"Unknown role: {m.role}")

        # create headers
        headers = self._process_header()
        params = {"key": self.api_token}
        return headers, system.strip(), messages, params

    def _process_header(self):
        return {
            "Content-Type": "application/json",
        }

    @staticmethod
    def get_structured_schema(model: type[BaseModel]) -> Dict[str, Any]:
        """
        Converts a Pydantic BaseModel to a JSON schema compatible with Gemini API,
        including `anyOf` for optional or union types and handling nested structures correctly.

        Args:
            model: The Pydantic BaseModel class to convert.

        Returns:
            A dictionary representing the JSON schema.
        """

        def _process_field(
            field_name: str, field_type: Any, field_description: str = None
        ) -> dict:
            """Helper function to process a single field."""
            schema = {}
            origin = get_origin(field_type)
            args = get_args(field_type)

            if origin is list:
                schema["type"] = "array"
                if args:
                    item_schema = _process_field_type(args[0])
                    schema["items"] = item_schema
                    if "type" not in item_schema and "anyOf" not in item_schema:
                        schema["items"]["type"] = "object"  # default item type for list
                else:
                    schema["items"] = {}
            elif origin is Optional:
                if args:
                    inner_schema = _process_field_type(args[0])
                    schema["anyOf"] = [inner_schema, {"type": "null"}]
                else:
                    schema = {"type": "null"}
            elif origin is dict:
                schema["type"] = "object"
                if len(args) == 2:
                    schema["additionalProperties"] = _process_field_type(args[1])
            else:
                schema = _process_field_type(field_type)

            if field_description:
                schema["description"] = field_description
            return schema

        def _process_field_type(field_type: Any) -> dict:
            """Helper function to process the type of a field."""

            origin = get_origin(field_type)
            args = get_args(field_type)

            if field_type is str:
                return {"type": "string"}
            elif field_type is int:
                return {"type": "integer"}
            elif field_type is float:
                return {"type": "number"}
            elif field_type is bool:
                return {"type": "boolean"}
            elif isinstance(field_type, type) and issubclass(field_type, BaseModel):
                return Gemini.get_structured_schema(
                    field_type
                )  # Recursive call for nested models
            elif origin is list:
                schema = {"type": "array"}
                if args:
                    item_schema = _process_field_type(args[0])
                    schema["items"] = item_schema
                    if "type" not in item_schema and "anyOf" not in item_schema:
                        schema["items"]["type"] = "object"
                return schema
            elif origin is Optional:
                return _process_field_type(args[0])
            elif origin is dict:
                schema = {"type": "object"}
                if len(args) == 2:
                    schema["additionalProperties"] = _process_field_type(args[1])
                return schema
            elif origin is Union:
                return _process_field_type(args[0])
            else:
                return {"type": "string"}  # default any object to string

        schema = {"type": "object", "properties": {}, "required": []}

        for field_name, field in model.model_fields.items():
            field_description = field.description
            if field.is_required():
                schema["required"].append(field_name)

            schema["properties"][field_name] = _process_field(
                field_name, field.annotation, field_description
            )

        if model.__doc__:
            schema["description"] = model.__doc__.strip()
        return schema

    def chat(
        self,
        chats: tt.Thread | str,
        model: Optional[str] = None,
        max_tokens: int = 4096,
        temperature: float = 1,
        token: Optional[str] = None,
        timeout=None,
        extra_headers: Optional[Dict[str, str]] = None,
        **kwargs,
    ) -> Any:
        output = ""
        x = None
        try:
            for x in self.stream_chat(
                chats=chats,
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                token=token,
                timeout=timeout,
                extra_headers=extra_headers,
                raw=False,
                **kwargs,
            ):
                if isinstance(x, dict):
                    output = x
                else:
                    output += x
        except requests.HTTPError as e:
            print(e.response.text)
            raise e

        if isinstance(chats, tt.Thread) and chats.schema:
            output = chats.schema(**tu.from_json(output))
            return output
        return output

    def stream_chat(
        self,
        chats: tt.Thread | str,
        model: Optional[str] = None,
        max_tokens: int = 4096,
        temperature: float = 1,
        token: Optional[str] = None,
        timeout=(5, 60),
        raw: bool = False,
        debug: bool = False,
        extra_headers: Optional[Dict[str, str]] = None,
        **kwargs,
    ):
        tools = []
        if isinstance(chats, tt.Thread):
            tools = [x.to_dict() for x in chats.tools]
        headers, system, messages, params = self._process_input(chats, token)
        extra_headers = extra_headers or self.extra_headers
        if extra_headers:
            headers.update(extra_headers)

        data = {
            "systemInstruction": {
                "parts": [{"text": system}],
            },
            "contents": messages,
            "safetySettings": [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
                },
            ],
        }

        generation_config = {
            "temperature": temperature,
            "maxOutputTokens": max_tokens,
            "stopSequences": [],
        }

        if isinstance(chats, tt.Thread) and chats.schema:
            generation_config.update(
                {
                    "response_mime_type": "application/json",
                    "response_schema": self.get_structured_schema(chats.schema),
                }
            )
        data["generationConfig"] = generation_config

        if tools:
            data["tool_config"] = {
                "function_calling_config": {
                    "mode": "ANY",
                }
            }
            std_tools = []
            for i, t in enumerate(tools):
                props = t["parameters"]["properties"]
                t_copy = t.copy()
                if not props:
                    t_copy.pop("parameters")
                std_tools.append(t_copy)
            data["tools"] = [{"function_declarations": std_tools}]
        data.update(kwargs)

        if debug:
            fp = "sample_gemini.json"
            print("Saving at path " + fp)
            tu.to_json(data, fp=fp)

        response = requests.post(
            self.base_url.format(
                id=model or self.model_id,
                rpc="streamGenerateContent",
            ),
            headers=headers,
            params=params,
            json=data,
            stream=True,
            timeout=timeout,
        )
        try:
            response.raise_for_status()
        except Exception as e:
            yield response.text
            raise e

        block_lines = ""
        done = False
        for lno, line in enumerate(response.iter_lines()):
            line = line.decode("utf-8")
            # print(f"[{lno:03d}] {line}")

            # get the clean line for block
            if line == ("[{"):  # first line
                line = line[1:]
            elif line == "," or line == "]":  # intermediate or last line
                continue
            block_lines += line

            done = False
            try:
                tu.from_json(block_lines)
                done = True
            except Exception as e:
                pass

            # print(f"{block_lines=}")
            if done:
                part_data = tu.from_json(block_lines)["candidates"][0]["content"][
                    "parts"
                ][0]
                if "text" in part_data:
                    if raw:
                        yield b"data: " + tu.to_json(
                            {
                                "object": "gemini_text",
                                "choices": [{"delta": {"content": part_data["text"]}}],
                            },
                            tight=True,
                        ).encode()
                        yield b""
                    else:
                        yield part_data["text"]
                elif "functionCall" in part_data:
                    fn_call = part_data["functionCall"]
                    fn_call["arguments"] = fn_call.pop("args")
                    yield fn_call
                block_lines = ""

    async def chat_async(
        self,
        chats: tt.Thread | str,
        model: Optional[str] = None,
        max_tokens: int = None,
        temperature: float = 1,
        token: Optional[str] = None,
        timeout=None,
        extra_headers: Optional[Dict[str, str]] = None,
        **kwargs,
    ) -> Any:
        output = ""
        x = None
        try:
            async for x in self.stream_chat_async(
                chats=chats,
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                token=token,
                timeout=timeout,
                extra_headers=extra_headers,
                raw=False,
                **kwargs,
            ):
                if isinstance(x, dict):
                    output = x
                else:
                    output += x
        except Exception as e:
            if not x:
                raise e
            else:
                raise ValueError(x)

        if isinstance(chats, tt.Thread) and chats.schema:
            output = chats.schema(**tu.from_json(output))
            return output
        return output

    async def stream_chat_async(
        self,
        chats: tt.Thread | str,
        model: Optional[str] = None,
        max_tokens: int = 4096,
        temperature: float = 1,
        token: Optional[str] = None,
        timeout=(5, 60),
        raw: bool = False,
        debug: bool = False,
        extra_headers: Optional[Dict[str, str]] = None,
        **kwargs,
    ):
        tools = []
        if isinstance(chats, tt.Thread):
            tools = [x.to_dict() for x in chats.tools]
        headers, system, messages, params = self._process_input(chats, token)
        extra_headers = extra_headers or self.extra_headers
        if extra_headers:
            headers.update(extra_headers)

        data = {
            "systemInstruction": {
                "parts": [{"text": system}],
            },
            "contents": messages,
            "safetySettings": [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
                },
            ],
        }

        generation_config = {
            "temperature": temperature,
            "maxOutputTokens": max_tokens,
            "stopSequences": [],
        }

        if isinstance(chats, tt.Thread) and chats.schema:
            generation_config.update(
                {
                    "response_mime_type": "application/json",
                    "response_schema": chats.schema,
                }
            )
        data["generationConfig"] = generation_config

        if tools:
            data["tool_config"] = {
                "function_calling_config": {
                    "mode": "ANY",
                }
            }
            std_tools = []
            for i, t in enumerate(tools):
                props = t["parameters"]["properties"]
                t_copy = t.copy()
                if not props:
                    t_copy.pop("parameters")
                std_tools.append(t_copy)
            data["tools"] = [{"function_declarations": std_tools}]
        data.update(kwargs)

        if debug:
            fp = "sample_gemini.json"
            print("Saving at path " + fp)
            tu.to_json(data, fp=fp)

        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.base_url.format(
                    id=model or self.model_id,
                    rpc="streamGenerateContent",
                ),
                headers=headers,
                params=params,
                json=data,
                timeout=timeout,
            )
            try:
                response.raise_for_status()
            except Exception as e:
                yield str(e)
                return

            block_lines = ""
            done = False

        async for chunk in response.aiter_bytes():
            for line in chunk.decode("utf-8").splitlines():
                # print(f"[{lno:03d}] {line}")

                # get the clean line for block
                if line == ("[{"):  # first line
                    line = line[1:]
                elif line == "," or line == "]":  # intermediate or last line
                    continue
                block_lines += line

                done = False
                try:
                    tu.from_json(block_lines)
                    done = True
                except Exception as e:
                    pass

                # print(f"{block_lines=}")
                if done:
                    part_data = tu.from_json(block_lines)["candidates"][0]["content"][
                        "parts"
                    ][0]
                    if "text" in part_data:
                        if raw:
                            yield b"data: " + tu.to_json(
                                {
                                    "object": "gemini_text",
                                    "choices": [
                                        {"delta": {"content": part_data["text"]}}
                                    ],
                                },
                                tight=True,
                            ).encode()
                            yield b""
                        else:
                            yield part_data["text"]
                    elif "functionCall" in part_data:
                        fn_call = part_data["functionCall"]
                        fn_call["arguments"] = fn_call.pop("args")
                        yield fn_call
                    block_lines = ""

    def distributed_chat(
        self,
        prompts: List[tt.Thread],
        post_logic: Optional[callable] = None,
        max_threads: int = 10,
        retry: int = 3,
        pbar=True,
        debug=False,
        **kwargs,
    ):
        return distributed_chat(
            self,
            prompts=prompts,
            post_logic=post_logic,
            max_threads=max_threads,
            retry=retry,
            pbar=pbar,
            debug=debug,
            **kwargs,
        )

    async def distributed_chat_async(
        self,
        prompts: List[tt.Thread],
        post_logic: Optional[callable] = None,
        max_threads: int = 10,
        retry: int = 3,
        pbar=True,
        debug=False,
        **kwargs,
    ):
        return await distributed_chat_async(
            self,
            prompts=prompts,
            post_logic=post_logic,
            max_threads=max_threads,
            retry=retry,
            pbar=pbar,
            debug=debug,
            **kwargs,
        )
