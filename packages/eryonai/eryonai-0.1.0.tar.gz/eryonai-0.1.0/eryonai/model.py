# eryonai/model.py
import requests
import torch
import torch.nn as nn
from transformers import LlamaConfig, LlamaForCausalLM, AutoConfig, AutoModelForCausalLM
import re

# ASCII art to print on installation
ascii_art = """
@@@@@@@@@@@@@@@@@=     
+@@@@@@@@@@@@                                                                    @@@@@@@       @@@@@     :@@@@@@@@@@@@@@@@@@@@@+   
+@@@@@@@@@@@@                                                                   .@@@@@@@-      @@@@@     +@@@@@@@@@@@@@@@@@@@@@@   
+@@@@+          -@@@: -@@@@@@@@%     =@@@@     %@@@@@-      #@@@  +@@@@%        @@@@@@@@@      @@@@@     +@@@@@@@@@@@@@@@@@@@@@@   
+@@@@+          *@@@@@@@@@*:@@@@+    @@@@+  *@@@@@@@@@@@    @@@@@@@@@@@@@.     =@@@@ @@@@#     @@@@@     +@@@@@@@@@@@@@@@@@@@@@@   
+@@@@@@@@@@@    *@@@@@@=:-  +@@@@   @@@@@  #@@@@@  =@@@@@   @@@@@@-.*@@@@@     @@@@- =@@@@     @@@@@     +@@@@@@@@@@@@@@@@@@@@@@   
+@@@@@@@@@@@    *@@@@#       @@@@@  @@@@   @@@@@    +@@@@#  @@@@@    @@@@@    #@@@@   @@@@@    @@@@@     +@@@@@@@@@@@@@@@@@@@@@@   
+@@@@+          *@@@@-        @@@@-@@@@+   @@@@@    -@@@@@  @@@@@    @@@@@   :@@@@@@@@@@@@@-   @@@@@     +@@@@@@@@@@@@@@@@@@@@@@   
+@@@@+          *@@@@-        :@@@@@@@@    @@@@@.   @@@@@=  @@@@@    @@@@@   @@@@@@@@@@@@@@@   @@@@@     +@@@@@@@@@@@@@@@@@@@@@@   
+@@@@@@@@@@@@=  *@@@@-         #@@@@@@:    :@@@@@@@@@@@@@   @@@@@    @@@@@  -@@@@=     #@@@@-  @@@@@     +@@@@@@@@@@@@@@@@@@@@@@   
+@@@@@@@@@@@@+  *@@@@-          @@@@@#       @@@@@@@@@@.    @@@@@    @@@@@  @@@@@       @@@@@  @@@@@      @@@@@@@@@@@@@@@@@@@@@.   
                                   @@@@@           =**+.                                                      -@@@@@@@@@@@@@@@@@:     
                               .@@@@@@@                                                                                               
                               %@@@@@%                                                                                                
"""

# Print ASCII art on module import
print(ascii_art)

# Custom configuration class to define model parameters
class EryonConfig(LlamaConfig):
    model_type = "eryon"
    rope_type = "eryon3"
    memory_size = 1024 * 1024 * 100  # 100 MB for custom external memory
    enable_internet_search = True
    keyword_patterns = {
        'search_patterns': [r'\b(search|find|what|why)\b', r'\?$'],
        'memory_patterns': [r'\bremember\b', r'\brecall\b']
    }

# Eryon model class that extends LlamaForCausalLM
class EryonModel(LlamaForCausalLM):
    config_class = EryonConfig

    def __init__(self, config):
        super().__init__(config)
        self.memory = nn.Parameter(torch.zeros(config.memory_size, dtype=torch.bfloat16))
        self.memory_ptr = 0
        self.keyword_detector = self.KeywordDetector(config.keyword_patterns)
        self.wikipedia_search = self.WikipediaSearchModule() if config.enable_internet_search else None
        
    class KeywordDetector:
        def __init__(self, patterns):
            self.patterns = {k: [re.compile(p, re.IGNORECASE) for p in v] for k, v in patterns.items()}
        
        def detect_keywords(self, text):
            results = {}
            for category, pattern_list in self.patterns.items():
                results[category] = any(pattern.search(text) for pattern in pattern_list)
            return results
    
    class WikipediaSearchModule:
        def __init__(self):
            self.api_url = "https://en.wikipedia.org/w/api.php"
        
        def search(self, query):
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
                response = requests.get(self.api_url, params=params)
                data = response.json()
                if 'query' not in data or 'pages' not in data['query']:
                    return f"No information found for '{query}'. Try rephrasing your query."
                pages = data['query']['pages']
                extracted_data = []
                for page_id in pages:
                    page = pages[page_id]
                    if 'extract' in page:
                        extract = page['extract']
                        words = extract.split()[:50]
                        excerpt = " ".join(words)
                        extracted_data.append(f"Title: {page['title']}\nExtract: {excerpt}")
                    else:
                        extracted_data.append(f"Title: {page['title']}\nExtract: No extract available.")
                return "\n\n".join(extracted_data)
            except Exception as e:
                return f"Search failed: {str(e)}"

    def process_input(self, input_text):
        keyword_results = self.keyword_detector.detect_keywords(input_text)
        if keyword_results['search_patterns'] and self.wikipedia_search:
            wikipedia_results = self.wikipedia_search.search(input_text)
            enhanced_input = f"{input_text}\n{wikipedia_results}"
        else:
            enhanced_input = input_text
        if keyword_results['memory_patterns'] and self.memory is not None:
            enhanced_input = self.enhance_with_memory(enhanced_input)
        return enhanced_input
        
    def enhance_with_memory(self, input_text):
        if self.memory_ptr > 0:
            memory_content = self.memory[:self.memory_ptr].view(-1).tolist()
            return f"{input_text}\nFrom memory: {str(memory_content)}"
        return input_text

    def forward(self, *args, **kwargs):
        if 'inputs' in kwargs and isinstance(kwargs['inputs'], str):
            kwargs['inputs'] = self.process_input(kwargs['inputs'])
        output = super().forward(*args, **kwargs)
        if self.memory is not None and 'input_ids' in kwargs:
            self.store_in_memory(kwargs['input_ids'])
        return output

    def store_in_memory(self, input_ids):
        if input_ids is not None and self.memory_ptr + input_ids.numel() < self.config.memory_size:
            input_data = input_ids.float().view(-1)
            self.memory.data[self.memory_ptr:self.memory_ptr + input_data.numel()] = input_data.to(torch.bfloat16)  
            self.memory_ptr += input_data.numel()

# Register the custom model and configuration
AutoConfig.register("eryon", EryonConfig)
AutoModelForCausalLM.register(EryonConfig, EryonModel)
