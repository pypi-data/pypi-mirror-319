from typing import Optional, Any, Dict, List
import asyncio
import psutil
import wrapt
import functools
from datetime import datetime
import uuid
import contextvars
import traceback

from .unique_decorator import generate_unique_hash_simple   
from .utils.trace_utils import load_model_costs
from .utils.llm_utils import extract_llm_output
from .file_name_tracker import TrackName


class LLMTracerMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file_tracker = TrackName()
        self.patches = []
        try:
            self.model_costs = load_model_costs()
        except Exception as e:
            self.model_costs = {
                # TODO: Default cost handling needs to be improved
                "default": {
                    "input_cost_per_token": 0.0,
                    "output_cost_per_token": 0.0
                }
            }
        self.current_llm_call_name = contextvars.ContextVar("llm_call_name", default=None)
        self.component_network_calls = {}  
        self.component_user_interaction = {}
        self.current_component_id = None  
        self.total_tokens = 0
        self.total_cost = 0.0
        self.llm_data = {}

    def instrument_llm_calls(self):
        # Handle modules that are already imported
        import sys
        
        if "vertexai" in sys.modules:
            self.patch_vertex_ai_methods(sys.modules["vertexai"])
        if "vertexai.generative_models" in sys.modules:
            self.patch_vertex_ai_methods(sys.modules["vertexai.generative_models"])
            
        if "openai" in sys.modules:
            self.patch_openai_methods(sys.modules["openai"])
        if "litellm" in sys.modules:
            self.patch_litellm_methods(sys.modules["litellm"])
        if "anthropic" in sys.modules:
            self.patch_anthropic_methods(sys.modules["anthropic"])
        if "google.generativeai" in sys.modules:
            self.patch_google_genai_methods(sys.modules["google.generativeai"])
        if "langchain_google_vertexai" in sys.modules:
            self.patch_langchain_google_methods(sys.modules["langchain_google_vertexai"])
        if "langchain_google_genai" in sys.modules:
            self.patch_langchain_google_methods(sys.modules["langchain_google_genai"])

        # Register hooks for future imports
        wrapt.register_post_import_hook(self.patch_vertex_ai_methods, "vertexai")
        wrapt.register_post_import_hook(self.patch_vertex_ai_methods, "vertexai.generative_models")
        wrapt.register_post_import_hook(self.patch_openai_methods, "openai")
        wrapt.register_post_import_hook(self.patch_litellm_methods, "litellm")
        wrapt.register_post_import_hook(self.patch_anthropic_methods, "anthropic")
        wrapt.register_post_import_hook(self.patch_google_genai_methods, "google.generativeai")
        
        # Add hooks for LangChain integrations
        wrapt.register_post_import_hook(self.patch_langchain_google_methods, "langchain_google_vertexai")
        wrapt.register_post_import_hook(self.patch_langchain_google_methods, "langchain_google_genai")

    def patch_openai_methods(self, module):
        try:
            if hasattr(module, "OpenAI"):
                client_class = getattr(module, "OpenAI")
                self.wrap_openai_client_methods(client_class)
            if hasattr(module, "AsyncOpenAI"):
                async_client_class = getattr(module, "AsyncOpenAI")
                self.wrap_openai_client_methods(async_client_class)
        except Exception as e:
            # Log the error but continue execution
            print(f"Warning: Failed to patch OpenAI methods: {str(e)}")

    def patch_anthropic_methods(self, module):
        if hasattr(module, "Anthropic"):
            client_class = getattr(module, "Anthropic")
            self.wrap_anthropic_client_methods(client_class)

    def patch_google_genai_methods(self, module):
        # Patch direct Google GenerativeAI usage
        if hasattr(module, "GenerativeModel"):
            model_class = getattr(module, "GenerativeModel")
            self.wrap_genai_model_methods(model_class)
        
        # Patch LangChain integration
        if hasattr(module, "ChatGoogleGenerativeAI"):
            chat_class = getattr(module, "ChatGoogleGenerativeAI")
            # Wrap invoke method to capture messages
            original_invoke = chat_class.invoke
            
            def patched_invoke(self, messages, *args, **kwargs):
                # Store messages in the instance for later use
                self._last_messages = messages
                return original_invoke(self, messages, *args, **kwargs)
            
            chat_class.invoke = patched_invoke
            
            # LangChain v0.2+ uses invoke/ainvoke
            self.wrap_method(chat_class, "_generate")
            if hasattr(chat_class, "_agenerate"):
                self.wrap_method(chat_class, "_agenerate")
            # Fallback for completion methods
            if hasattr(chat_class, "complete"):
                self.wrap_method(chat_class, "complete")
            if hasattr(chat_class, "acomplete"):
                self.wrap_method(chat_class, "acomplete")

    def patch_vertex_ai_methods(self, module):
        # Patch the GenerativeModel class
        if hasattr(module, "generative_models"):
            gen_models = getattr(module, "generative_models")
            if hasattr(gen_models, "GenerativeModel"):
                model_class = getattr(gen_models, "GenerativeModel")
                self.wrap_vertex_model_methods(model_class)
        
        # Also patch the class directly if available
        if hasattr(module, "GenerativeModel"):
            model_class = getattr(module, "GenerativeModel")
            self.wrap_vertex_model_methods(model_class)

    def wrap_vertex_model_methods(self, model_class):
        # Patch both sync and async methods
        self.wrap_method(model_class, "generate_content")
        if hasattr(model_class, "generate_content_async"):
            self.wrap_method(model_class, "generate_content_async")

    def patch_litellm_methods(self, module):
        self.wrap_method(module, "completion")
        self.wrap_method(module, "acompletion")

    def patch_langchain_google_methods(self, module):
        """Patch LangChain's Google integration methods"""
        if hasattr(module, "ChatVertexAI"):
            chat_class = getattr(module, "ChatVertexAI")
            # LangChain v0.2+ uses invoke/ainvoke
            self.wrap_method(chat_class, "_generate")
            if hasattr(chat_class, "_agenerate"):
                self.wrap_method(chat_class, "_agenerate")
            # Fallback for completion methods
            if hasattr(chat_class, "complete"):
                self.wrap_method(chat_class, "complete")
            if hasattr(chat_class, "acomplete"):
                self.wrap_method(chat_class, "acomplete")

        if hasattr(module, "ChatGoogleGenerativeAI"):
            chat_class = getattr(module, "ChatGoogleGenerativeAI")
            # LangChain v0.2+ uses invoke/ainvoke
            self.wrap_method(chat_class, "_generate")
            if hasattr(chat_class, "_agenerate"):
                self.wrap_method(chat_class, "_agenerate")
            # Fallback for completion methods
            if hasattr(chat_class, "complete"):
                self.wrap_method(chat_class, "complete")
            if hasattr(chat_class, "acomplete"):
                self.wrap_method(chat_class, "acomplete")

    def wrap_openai_client_methods(self, client_class):
        original_init = client_class.__init__

        @functools.wraps(original_init)
        def patched_init(client_self, *args, **kwargs):
            original_init(client_self, *args, **kwargs)
            self.wrap_method(client_self.chat.completions, "create")
            if hasattr(client_self.chat.completions, "acreate"):
                self.wrap_method(client_self.chat.completions, "acreate")

        setattr(client_class, "__init__", patched_init)

    def wrap_anthropic_client_methods(self, client_class):
        original_init = client_class.__init__

        @functools.wraps(original_init)
        def patched_init(client_self, *args, **kwargs):
            original_init(client_self, *args, **kwargs)
            self.wrap_method(client_self.messages, "create")
            if hasattr(client_self.messages, "acreate"):
                self.wrap_method(client_self.messages, "acreate")

        setattr(client_class, "__init__", patched_init)

    def wrap_genai_model_methods(self, model_class):
        original_init = model_class.__init__

        @functools.wraps(original_init)
        def patched_init(model_self, *args, **kwargs):
            original_init(model_self, *args, **kwargs)
            self.wrap_method(model_self, "generate_content")
            if hasattr(model_self, "generate_content_async"):
                self.wrap_method(model_self, "generate_content_async")

        setattr(model_class, "__init__", patched_init)

    def wrap_method(self, obj, method_name):
        """
        Wrap a method with tracing functionality.
        Works for both class methods and instance methods.
        """
        # If obj is a class, we need to patch both the class and any existing instances
        if isinstance(obj, type):
            # Store the original class method
            original_method = getattr(obj, method_name)
            
            @wrapt.decorator
            def wrapper(wrapped, instance, args, kwargs):
                if asyncio.iscoroutinefunction(wrapped):
                    return self.trace_llm_call(wrapped, *args, **kwargs)
                return self.trace_llm_call_sync(wrapped, *args, **kwargs)
            
            # Wrap the class method
            wrapped_method = wrapper(original_method)
            setattr(obj, method_name, wrapped_method)
            self.patches.append((obj, method_name, original_method))
            
        else:
            # For instance methods
            original_method = getattr(obj, method_name)
            
            @wrapt.decorator
            def wrapper(wrapped, instance, args, kwargs):
                if asyncio.iscoroutinefunction(wrapped):
                    return self.trace_llm_call(wrapped, *args, **kwargs)
                return self.trace_llm_call_sync(wrapped, *args, **kwargs)
            
            wrapped_method = wrapper(original_method)
            setattr(obj, method_name, wrapped_method)
            self.patches.append((obj, method_name, original_method))

    def _extract_model_name(self, args, kwargs, result):
        """Extract model name from kwargs or result"""
        # First try direct model parameter
        model = kwargs.get("model", "")
        
        if not model:
            # Try to get from instance
            instance = kwargs.get("self", None)
            if instance:
                # Try model_name first (Google format)
                if hasattr(instance, "model_name"):
                    model = instance.model_name
                # Try model attribute
                elif hasattr(instance, "model"):
                    model = instance.model
        
        # TODO: This way isn't scalable. The necessity for normalising model names needs to be fixed. We shouldn't have to do this
        # Normalize Google model names
        if model and isinstance(model, str):
            model = model.lower()
            if "gemini-1.5-flash" in model:
                return "gemini-1.5-flash"
            if "gemini-1.5-pro" in model:
                return "gemini-1.5-pro"
            if "gemini-pro" in model:
                return "gemini-pro"

        if 'to_dict' in dir(result):
            result = result.to_dict()
            if 'model_version' in result:
                model = result['model_version']
        
        return model or "default"

    def _extract_parameters(self, kwargs):
        """Extract all non-null parameters from kwargs"""
        parameters = {k: v for k, v in kwargs.items() if v is not None}

        # Remove contents key in parameters (Google LLM Response)
        if 'contents' in parameters:
            del parameters['contents']

        # Remove messages key in parameters (OpenAI message)
        if 'messages' in parameters:
            del parameters['messages']

        if 'generation_config' in parameters:
            generation_config = parameters['generation_config']
            # If generation_config is already a dict, use it directly
            if isinstance(generation_config, dict):
                config_dict = generation_config
            else:
                # Convert GenerationConfig to dictionary if it has a to_dict method, otherwise try to get its __dict__
                config_dict = getattr(generation_config, 'to_dict', lambda: generation_config.__dict__)()
            parameters.update(config_dict)
            del parameters['generation_config']
            
        return parameters

    def _extract_token_usage(self, result):
        """Extract token usage from result"""
        # Handle coroutines
        if asyncio.iscoroutine(result):
            # Get the current event loop
            loop = asyncio.get_event_loop()
            # Run the coroutine in the current event loop
            result = loop.run_until_complete(result)


        # Handle standard OpenAI/Anthropic format
        if hasattr(result, "usage"):
            usage = result.usage
            return {
                "prompt_tokens": getattr(usage, "prompt_tokens", 0),
                "completion_tokens": getattr(usage, "completion_tokens", 0),
                "total_tokens": getattr(usage, "total_tokens", 0)
            }
        
        # Handle Google GenerativeAI format with usage_metadata
        if hasattr(result, "usage_metadata"):
            metadata = result.usage_metadata
            return {
                "prompt_tokens": getattr(metadata, "prompt_token_count", 0),
                "completion_tokens": getattr(metadata, "candidates_token_count", 0),
                "total_tokens": getattr(metadata, "total_token_count", 0)
            }
        
        # Handle Vertex AI format
        if hasattr(result, "text"):
            # For LangChain ChatVertexAI
            total_tokens = getattr(result, "token_count", 0)
            if not total_tokens and hasattr(result, "_raw_response"):
                # Try to get from raw response
                total_tokens = getattr(result._raw_response, "token_count", 0)
            return {
                # TODO: This implementation is incorrect. Vertex AI does provide this breakdown    
                "prompt_tokens": 0,  # Vertex AI doesn't provide this breakdown
                "completion_tokens": total_tokens,
                "total_tokens": total_tokens
            }
        
        return {    # TODO: Passing 0 in case of not recorded is not correct. This needs to be fixes. Discuss before making changes to this
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0
        }

    def _extract_input_data(self, args, kwargs, result):
        return {
            'args': args,
            'kwargs': kwargs
        }

    def _calculate_cost(self, token_usage, model_name):
        # TODO: Passing default cost is a faulty logic & implementation and should be fixed
        """Calculate cost based on token usage and model"""
        if not isinstance(token_usage, dict):
            token_usage = {
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": token_usage if isinstance(token_usage, (int, float)) else 0
            }

        # TODO: This is a temporary fix. This needs to be fixed

        # Get model costs, defaulting to Vertex AI PaLM2 costs if unknown
        model_cost = self.model_costs.get(model_name, {
            "input_cost_per_token": 0.0,   
            "output_cost_per_token": 0.0   
        })

        input_cost = (token_usage.get("prompt_tokens", 0)) * model_cost.get("input_cost_per_token", 0.0)
        output_cost = (token_usage.get("completion_tokens", 0)) * model_cost.get("output_cost_per_token", 0.0)
        total_cost = input_cost + output_cost

        # TODO: Return the value as it is, no need to round
        return {
            "input_cost": round(input_cost, 10),
            "output_cost": round(output_cost, 10),
            "total_cost": round(total_cost, 10)
        }

    def create_llm_component(self, component_id, hash_id, name, llm_type, version, memory_used, start_time, end_time, input_data, output_data, cost={}, usage={}, error=None, parameters={}):
        # Update total metrics
        self.total_tokens += usage.get("total_tokens", 0)
        self.total_cost += cost.get("total_cost", 0)

        component = {
            "id": component_id,
            "hash_id": hash_id,
            "source_hash_id": None,
            "type": "llm",
            "name": name,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "error": error,
            "parent_id": self.current_agent_id.get(),
            "info": {
                "model": llm_type,
                "version": version,
                "memory_used": memory_used,
                "cost": cost,
                "tokens": usage,
                **parameters
            },
            "data": {
                "input": input_data['args'] if hasattr(input_data, 'args') else input_data,
                "output": output_data.output_response if output_data else None,
                "memory_used": memory_used
            },
            "network_calls": self.component_network_calls.get(component_id, []),
            "interactions": self.component_user_interaction.get(component_id, [])
        }

        if self.gt: 
            component["data"]["gt"] = self.gt

        return component
    
    def start_component(self, component_id):
        """Start tracking network calls for a component"""
        self.component_network_calls[component_id] = []
        self.current_component_id = component_id

    def end_component(self, component_id):
        """Stop tracking network calls for a component"""
        self.current_component_id = None


    async def trace_llm_call(self, original_func, *args, **kwargs):
        """Trace an LLM API call"""
        if not self.is_active:
            return await original_func(*args, **kwargs)

        start_time = datetime.now().astimezone()
        start_memory = psutil.Process().memory_info().rss
        component_id = str(uuid.uuid4())
        hash_id = generate_unique_hash_simple(original_func) 

        # Start tracking network calls for this component
        self.start_component(component_id)

        try:
            # Execute the LLM call
            result = await original_func(*args, **kwargs)

            # Calculate resource usage
            end_time = datetime.now().astimezone()
            end_memory = psutil.Process().memory_info().rss
            memory_used = max(0, end_memory - start_memory)

            # Extract token usage and calculate cost
            token_usage = self._extract_token_usage(result)
            model_name = self._extract_model_name(args, kwargs, result)
            cost = self._calculate_cost(token_usage, model_name)
            parameters = self._extract_parameters(kwargs)

            # End tracking network calls for this component
            self.end_component(component_id)

            name = self.current_llm_call_name.get()
            if name is None:
                name = original_func.__name__
            
            # Create input data with ground truth
            input_data = self._extract_input_data(args, kwargs, result)
            
            # Create LLM component
            llm_component = self.create_llm_component(
                component_id=component_id,
                hash_id=hash_id,
                name=name,
                llm_type=model_name,
                version="1.0.0",
                memory_used=memory_used,
                start_time=start_time,
                end_time=end_time,
                input_data=input_data,
                output_data=extract_llm_output(result),
                cost=cost,
                usage=token_usage,
                parameters=parameters
            )
                
            # self.add_component(llm_component)
            self.llm_data = llm_component
            return result

        except Exception as e:
            error_component = {
                "code": 500,
                "type": type(e).__name__,
                "message": str(e),
                "details": {}
            }
            
            # End tracking network calls for this component
            self.end_component(component_id)
            
            end_time = datetime.now().astimezone()

            name = self.current_llm_call_name.get()
            if name is None:
                name = original_func.__name__
            
            llm_component = self.create_llm_component(
                component_id=component_id,
                hash_id=hash_id,
                name=name,
                llm_type="unknown",
                version="1.0.0",
                memory_used=0,
                start_time=start_time,
                end_time=end_time,
                input_data=self._extract_input_data(args, kwargs, None),
                output_data=None,
                error=error_component
            )
    
            self.add_component(llm_component)
            raise

    def trace_llm_call_sync(self, original_func, *args, **kwargs):
        """Sync version of trace_llm_call"""
        if not self.is_active:
            if asyncio.iscoroutinefunction(original_func):
                return asyncio.run(original_func(*args, **kwargs))
            return original_func(*args, **kwargs)

        start_time = datetime.now().astimezone()
        component_id = str(uuid.uuid4())
        hash_id = generate_unique_hash_simple(original_func)

        # Start tracking network calls for this component
        self.start_component(component_id)

        # Calculate resource usage
        end_time = datetime.now().astimezone()
        start_memory = psutil.Process().memory_info().rss

        try:
            # Execute the function
            if asyncio.iscoroutinefunction(original_func):
                result = asyncio.run(original_func(*args, **kwargs))
            else:
                result = original_func(*args, **kwargs)

            end_memory = psutil.Process().memory_info().rss
            memory_used = max(0, end_memory - start_memory)

            # Extract token usage and calculate cost
            token_usage = self._extract_token_usage(result)
            model_name = self._extract_model_name(args, kwargs, result)
            cost = self._calculate_cost(token_usage, model_name)
            parameters = self._extract_parameters(kwargs)

            # End tracking network calls for this component
            self.end_component(component_id)

            name = self.current_llm_call_name.get()
            if name is None:
                name = original_func.__name__

            # Create input data with ground truth
            input_data = self._extract_input_data(args, kwargs, result)
            
            # Create LLM component
            llm_component = self.create_llm_component(
                component_id=component_id,
                hash_id=hash_id,
                name=name,
                llm_type=model_name,
                version="1.0.0",
                memory_used=memory_used,
                start_time=start_time,
                end_time=end_time,
                input_data=input_data,
                output_data=extract_llm_output(result),
                cost=cost,
                usage=token_usage,
                parameters=parameters
            )
            
            self.add_component(llm_component)
            return result

        except Exception as e:
            error_component = {
                "code": 500,
                "type": type(e).__name__,
                "message": str(e),
                "details": {}
            }
            
            # End tracking network calls for this component
            self.end_component(component_id)
            
            end_time = datetime.now().astimezone()

            name = self.current_llm_call_name.get()
            if name is None:
                name = original_func.__name__

            end_memory = psutil.Process().memory_info().rss
            memory_used = max(0, end_memory - start_memory)
            
            llm_component = self.create_llm_component(
                component_id=component_id,
                hash_id=hash_id,
                name=name,
                llm_type="unknown",
                version="1.0.0",
                memory_used=memory_used,
                start_time=start_time,
                end_time=end_time,
                input_data=self._extract_input_data(args, kwargs, None),
                output_data=None,
                error=error_component
            )
    
            self.add_component(llm_component)
            raise

    def trace_llm(self, name: str = None):
        def decorator(func):
            @self.file_tracker.trace_decorator
            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs):
                self.gt = kwargs.get('gt', None) if kwargs else None
                if not self.is_active:
                    return await func(*args, **kwargs)
                
                hash_id = generate_unique_hash_simple(func)                
                component_id = str(uuid.uuid4())
                parent_agent_id = self.current_agent_id.get()
                self.start_component(component_id)
                
                start_time = datetime.now()
                error_info = None
                result = None
                
                try:
                    result = await func(*args, **kwargs)
                    return result
                except Exception as e:
                    error_info = {
                        "error": {
                            "type": type(e).__name__,
                            "message": str(e),
                            "traceback": traceback.format_exc(),
                            "timestamp": datetime.now().isoformat()
                        }
                    }
                    raise
                finally:

                    llm_component = self.llm_data
                    llm_component['name'] = name

                    if self.gt:
                        llm_component["data"]["gt"] = self.gt

                    if error_info:
                        llm_component["error"] = error_info["error"]
                    
                    if parent_agent_id:
                        children = self.agent_children.get()
                        children.append(llm_component)
                        self.agent_children.set(children)
                    else:
                        self.add_component(llm_component)
                    
                    self.end_component(component_id)

            @self.file_tracker.trace_decorator
            @functools.wraps(func)
            def sync_wrapper(*args, **kwargs):
                self.gt = kwargs.get('gt', None) if kwargs else None
                if not self.is_active:
                    return func(*args, **kwargs)
                
                hash_id = generate_unique_hash_simple(func)

                component_id = str(uuid.uuid4())
                parent_agent_id = self.current_agent_id.get()
                self.start_component(component_id)
                
                start_time = datetime.now()
                error_info = None
                result = None
                
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    error_info = {
                        "error": {
                            "type": type(e).__name__,
                            "message": str(e),
                            "traceback": traceback.format_exc(),
                            "timestamp": datetime.now().isoformat()
                        }
                    }
                    raise
                finally:

                    llm_component = self.llm_data

                    if error_info:
                        llm_component["error"] = error_info["error"]
                    
                    if parent_agent_id:
                        children = self.agent_children.get()
                        children.append(llm_component)
                        self.agent_children.set(children)
                    else:
                        self.add_component(llm_component)
                    
                    self.end_component(component_id)

            return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
        return decorator

    def unpatch_llm_calls(self):
        # Remove all patches
        for obj, method_name, original_method in self.patches:
            try:
                setattr(obj, method_name, original_method)
            except Exception as e:
                print(f"Error unpatching {method_name}: {str(e)}")
        self.patches = []

    def _sanitize_api_keys(self, data):
        """Remove sensitive information from data"""
        if isinstance(data, dict):
            return {k: self._sanitize_api_keys(v) for k, v in data.items() 
                    if not any(sensitive in k.lower() for sensitive in ['key', 'token', 'secret', 'password'])}
        elif isinstance(data, list):
            return [self._sanitize_api_keys(item) for item in data]
        elif isinstance(data, tuple):
            return tuple(self._sanitize_api_keys(item) for item in data)
        return data

    def _sanitize_input(self, args, kwargs):
        """Convert input arguments to text format.
        
        Args:
            args: Input arguments that may contain nested dictionaries
            
        Returns:
            str: Text representation of the input arguments
        """
        if isinstance(args, dict):
            return str({k: self._sanitize_input(v, {}) for k, v in args.items()})
        elif isinstance(args, (list, tuple)):
            return str([self._sanitize_input(item, {}) for item in args])
        return str(args)

def extract_llm_output(result):
    """Extract output from LLM response"""
    class OutputResponse:
        def __init__(self, output_response):
            self.output_response = output_response

    # Handle coroutines
    if asyncio.iscoroutine(result):
        # For sync context, run the coroutine
        if not asyncio.get_event_loop().is_running():
            result = asyncio.run(result)
        else:
            # We're in an async context, but this function is called synchronously
            # Return a placeholder and let the caller handle the coroutine
            return OutputResponse("Coroutine result pending")

    # Handle Google GenerativeAI format
    if hasattr(result, "result"):
        candidates = getattr(result.result, "candidates", [])
        output = []
        for candidate in candidates:
            content = getattr(candidate, "content", None)
            if content and hasattr(content, "parts"):
                for part in content.parts:
                    if hasattr(part, "text"):
                        output.append({
                            "content": part.text,
                            "role": getattr(content, "role", "assistant"),
                            "finish_reason": getattr(candidate, "finish_reason", None)
                        })
        return OutputResponse(output)
    
    # Handle Vertex AI format
    if hasattr(result, "text"):
        return OutputResponse([{
            "content": result.text,
            "role": "assistant"
        }])
    
    # Handle OpenAI format
    if hasattr(result, "choices"):
        return OutputResponse([{
            "content": choice.message.content,
            "role": choice.message.role
        } for choice in result.choices])
    
    # Handle Anthropic format
    if hasattr(result, "completion"):
        return OutputResponse([{
            "content": result.completion,
            "role": "assistant"
        }])
    
    # Default case
    return OutputResponse(str(result))
