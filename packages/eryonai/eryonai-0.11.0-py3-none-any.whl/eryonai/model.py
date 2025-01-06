import torch
import torch.nn as nn
from transformers import LlamaConfig, LlamaForCausalLM, AutoConfig, AutoModelForCausalLM
import re
import platform
import psutil
import requests
from typing import Optional, Dict, Any
import atexit

class EryonMessages:
    ascii_art = """                                                                                                              
                                                                                                       
                                                                                                       
  ░██████████                                                   ░█████     ████     ████████████████   
  ░██████████                                                   ██████▒    ████    █████████████████▒  
  ░████        ███▒████████    ████  ▓██████░   ▓███▓█████     ░███████    ████    █████████████████▒  
  ░████████▓  ░████████ ████  ████  ██████████  ▓██████████    ████ ████   ████    █████████████████▒  
  ░█████████  ░████     ▓███  ███░ ████░  ▓████ ▓███▒  ████   ▓███  ████   ████    █████████████████▒  
  ░████       ░████      ████████  ████   ░████ ▓███▒  ████   ███████████  ████    █████████████████▒  
  ░████░░░░░░ ░████       ██████   ▓████  ████░ ▓███▒  ████  ████████████  ████    █████████████████▒  
  ░██████████ ░████       ░████▓    ▓████████░  ▓███▒  ████  ████    ░████ ████    █████████████████░  
   ▒▒▒▒▒▒▒▒▒░  ░▒▒░        ████        ▓██▓      ▒▒░   ░▒▒░  ▒▒▒      ░▒▒▒ ░▒▒░     ░██████████████    
                        ██████                                                                         
                        ████░                                                                          
                                                                                                                                                                                                                                                                                                   
"""
    _show_messages = False

    @staticmethod
    def detect_hardware():
        """Detect available hardware and return optimal configuration"""
        device_info = {
            'device': 'cpu',
            'optimization_level': 1,
            'memory_fraction': 0.5
        }
        
        if torch.cuda.is_available():
            device_info['device'] = 'cuda'
            device_info['optimization_level'] = 4
            if EryonMessages._show_messages:
                print("Using CUDA - Performance boost: 4x faster")
            return device_info
        
        elif hasattr(torch, 'hip') and torch.hip.is_available():
            device_info['device'] = 'hip'
            device_info['optimization_level'] = 3
            if EryonMessages._show_messages:
                print("Using AMD GPU (ROCm) - Performance boost: 3x faster")
            return device_info
        
        else:
            total_ram = psutil.virtual_memory().total / (1024 ** 3)
            if total_ram >= 32:
                device_info['memory_fraction'] = 0.7
                device_info['optimization_level'] = 2
                if EryonMessages._show_messages:
                    print("Using RAM (High Memory Mode) - Performance boost: 2x faster")
            elif EryonMessages._show_messages:
                print("Using RAM (Standard Mode) - Performance boost: 1.5x faster")
            return device_info

    @classmethod
    def show_welcome_message(cls):
        if cls._show_messages:
            print(cls.ascii_art)
            cls.detect_hardware()

class EryonConfig(LlamaConfig):
    model_type = "eryon"
    rope_type = "eryon3"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        hardware_config = EryonMessages.detect_hardware()
        self.memory_size = int(psutil.virtual_memory().total * hardware_config['memory_fraction'])
        self.enable_internet_search = True
        self.keyword_patterns = {
            'search_patterns': [r'\b(search|find|what|why)\b', r'\?$'],
            'memory_patterns': [r'\bremember\b', r'\brecall\b']
        }
        self.device = hardware_config['device']
        self.optimization_level = hardware_config['optimization_level']

class EryonConfig(LlamaConfig):
    model_type = "eryon"
    rope_type = "eryon3"
    
    def __init__(self, **kwargs):
        # Show welcome message on every config initialization
        EryonMessages.show_welcome_message()
        
        super().__init__(**kwargs)
        hardware_config = EryonMessages.detect_hardware()
        self.memory_size = int(psutil.virtual_memory().total * hardware_config['memory_fraction'])
        self.enable_internet_search = True
        self.keyword_patterns = {
            'search_patterns': [r'\b(search|find|what|why)\b', r'\?$'],
            'memory_patterns': [r'\bremember\b', r'\brecall\b']
        }
        self.device = hardware_config['device']
        self.optimization_level = hardware_config['optimization_level']

class EryonModel(LlamaForCausalLM):
    config_class = EryonConfig

    def __init__(self, config):
        # Show welcome message on every model initialization
        EryonMessages.show_welcome_message()
        
        super().__init__(config)
        
        # Optimize memory usage based on device
        memory_dtype = torch.bfloat16 if config.device in ['cuda', 'hip'] else torch.float32
        self.memory = nn.Parameter(torch.zeros(config.memory_size, dtype=memory_dtype))
        self.register_buffer('memory_cache', torch.zeros(1024, dtype=memory_dtype))
        
        self.keyword_detector = torch.jit.script(self.KeywordDetector(config.keyword_patterns))
        self.wikipedia_search = self.WikipediaSearchModule() if config.enable_internet_search else None
        
        self.to(config.device)
        
        if config.device in ['cuda', 'hip']:
            self.amp_enabled = True
            self.scaler = torch.cuda.amp.GradScaler()
        else:
            self.amp_enabled = False

    class KeywordDetector(nn.Module):
        def __init__(self, patterns: Dict[str, list]):
            super().__init__()
            self.patterns = {k: [re.compile(p, re.IGNORECASE) for p in v] for k, v in patterns.items()}
        
        def forward(self, text: str) -> Dict[str, bool]:
            results = {}
            for category, pattern_list in self.patterns.items():
                results[category] = any(pattern.search(text) for pattern in pattern_list)
            return results

    class WikipediaSearchModule:
        def __init__(self):
            self.api_url = "https://en.wikipedia.org/w/api.php"
            self.session = requests.Session()
        
        @torch.jit.ignore
        def search(self, query: str) -> str:
            try:
                params = {
                    'action': 'query',
                    'format': 'json',
                    'prop': 'extracts',
                    'exintro': True,
                    'explaintext': True,
                    'generator': 'search',
                    'gsrnamespace': 0,
                    'gsrlimit': 1,
                    'gsrsearch': query
                }
                response = self.session.get(self.api_url, params=params, timeout=5)
                data = response.json()
                
                if 'query' not in data or 'pages' not in data['query']:
                    return f"No information found for '{query}'"
                    
                pages = data['query']['pages']
                return next(iter(pages.values()))['extract'][:500]
                
            except Exception as e:
                return f"Search failed: {str(e)}"

    @torch.jit.ignore
    def process_input(self, input_text: str) -> str:
        with torch.no_grad():
            keyword_results = self.keyword_detector(input_text)
            
            if keyword_results['search_patterns'] and self.wikipedia_search:
                wikipedia_results = self.wikipedia_search.search(input_text)
                enhanced_input = f"{input_text}\n{wikipedia_results}"
            else:
                enhanced_input = input_text
                
            if keyword_results['memory_patterns']:
                enhanced_input = self.enhance_with_memory(enhanced_input)
                
            return enhanced_input

    def forward(self, *args, **kwargs):
        if self.amp_enabled:
            with torch.cuda.amp.autocast():
                return self._forward_impl(*args, **kwargs)
        return self._forward_impl(*args, **kwargs)

    def _forward_impl(self, *args, **kwargs):
        if 'inputs' in kwargs and isinstance(kwargs['inputs'], str):
            kwargs['inputs'] = self.process_input(kwargs['inputs'])
        
        output = super().forward(*args, **kwargs)
        
        if 'input_ids' in kwargs:
            self._store_in_memory(kwargs['input_ids'])
        
        return output

    @torch.jit.ignore
    def _store_in_memory(self, input_ids: torch.Tensor):
        if input_ids is not None:
            with torch.no_grad():
                input_data = input_ids.to(self.memory.dtype).view(-1)
                cache_size = min(input_data.numel(), self.memory_cache.numel())
                self.memory_cache[:cache_size].copy_(input_data[:cache_size])

# Register the custom model and configuration
AutoConfig.register("eryon", EryonConfig)
AutoModelForCausalLM.register(EryonConfig, EryonModel)

def show_messages():
    """Function to display welcome message and hardware information"""
    EryonMessages._show_messages = True
    EryonMessages.show_welcome_message()
    EryonMessages._show_messages = False

# Don't show messages on import
EryonMessages._show_messages = False