"""
Translation Service Module
Handles AI-powered translations using OpenAI's API with context-aware prompts.
"""

import os
import json
from typing import Dict, List, Optional, Tuple
from openai import AzureOpenAI
from dotenv import load_dotenv
import time
import hashlib

# Load environment variables
load_dotenv()

class TranslationService:
    """AI-powered translation service for localization content."""
    
    def __init__(self):
        self.client = None
        self.api_key = os.getenv('AZURE_OPENAI_API_KEY')
        self.azure_endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
        self.api_version = os.getenv('AZURE_OPENAI_API_VERSION', '2024-02-15-preview')
        self.deployment_name = os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME', 'gpt-4')
        self.max_tokens = int(os.getenv('MAX_TOKENS', '2000'))
        self.temperature = float(os.getenv('TEMPERATURE', '0.3'))
        
        # Translation cache to avoid duplicate API calls
        self.translation_cache = {}
        self.cache_file = "translation_cache.json"
        self.load_cache()
        
        # Initialize Azure OpenAI client if credentials are available
        if (self.api_key and self.api_key != 'your_azure_openai_api_key_here' and
            self.azure_endpoint and self.azure_endpoint != 'your_azure_openai_endpoint_here'):
            try:
                self.client = AzureOpenAI(
                    api_key=self.api_key,
                    api_version=self.api_version,
                    azure_endpoint=self.azure_endpoint
                )
            except Exception as e:
                print(f"Warning: Failed to initialize Azure OpenAI client: {e}")
                
        # Style templates for different translation approaches
        self.style_templates = {
            'formal': {
                'description': 'Professional, formal tone suitable for business applications',
                'prompt_addition': 'Use formal, professional language appropriate for business software.'
            },
            'conversational': {
                'description': 'Natural, conversational tone for user interactions',
                'prompt_addition': 'Use natural, conversational language that feels friendly and approachable.'
            },
            'chatbot': {
                'description': 'Friendly, helpful tone optimized for chatbot interactions',
                'prompt_addition': 'Use friendly, helpful language optimized for chatbot conversations. Be concise and clear.'
            }
        }
        
    def load_cache(self):
        """Load translation cache from file."""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    self.translation_cache = json.load(f)
        except Exception as e:
            print(f"Warning: Failed to load translation cache: {e}")
            self.translation_cache = {}
            
    def save_cache(self):
        """Save translation cache to file."""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.translation_cache, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Warning: Failed to save translation cache: {e}")
            
    def get_cache_key(self, text: str, target_language: str, style: str, context: str) -> str:
        """Generate a cache key for the translation."""
        content = f"{text}|{target_language}|{style}|{context}"
        return hashlib.md5(content.encode('utf-8')).hexdigest()
        
    def translate(self, text: str, target_language: str, style: str = 'formal', 
                 context: str = '', max_retries: int = 3) -> str:
        """
        Translate text with context awareness.
        
        Args:
            text: The text to translate
            target_language: Target language for translation
            style: Translation style (formal, conversational, chatbot)
            context: Context information (topic, component type, etc.)
            max_retries: Maximum number of retry attempts
            
        Returns:
            Translated text
        """
        # Check cache first
        cache_key = self.get_cache_key(text, target_language, style, context)
        if cache_key in self.translation_cache:
            return self.translation_cache[cache_key]
            
        # If no Azure OpenAI client, return mock translation
        if not self.client:
            return self._mock_translate(text, target_language, style)
            
        # Prepare the translation prompt
        prompt = self._build_translation_prompt(text, target_language, style, context)
        
        # Attempt translation with retries
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.deployment_name,  # This is the deployment name in Azure
                    messages=[
                        {"role": "system", "content": "You are a professional translator specializing in software localization."},
                        {"role": "user", "content": prompt}
                    ],
                    max_completion_tokens=self.max_tokens,
                    temperature=1
                )
                
                translated_text = response.choices[0].message.content.strip()
                
                # Remove quotes if present
                if (translated_text.startswith('"') and translated_text.endswith('"')) or \
                   (translated_text.startswith("'") and translated_text.endswith("'")):
                    translated_text = translated_text[1:-1]
                    
                # Cache the result
                self.translation_cache[cache_key] = translated_text
                self.save_cache()
                
                return translated_text
                
            except Exception as e:
                if attempt == max_retries - 1:
                    # Final attempt failed, return error message
                    error_msg = f"Translation failed: {str(e)}"
                    print(error_msg)
                    return f"[ERROR: {error_msg}]"
                else:
                    # Wait before retry
                    time.sleep(2 ** attempt)
                    
        return "[ERROR: Translation failed after retries]"
        
    def _build_translation_prompt(self, text: str, target_language: str, 
                                style: str, context: str) -> str:
        """Build a context-aware translation prompt."""
        style_info = self.style_templates.get(style, self.style_templates['formal'])
        
        prompt = f"""Translate the following text to {target_language}.

Context: This text is from a Microsoft Copilot Studio chatbot interface.
"""
        
        if context:
            prompt += f"Specific context: {context}\n"
            
        prompt += f"""
Translation style: {style_info['description']}
{style_info['prompt_addition']}

Important guidelines:
1. Maintain the exact meaning and intent of the original text
2. Preserve any formatting, placeholders (like {{variables}}), or special characters
3. Keep emoji and Unicode characters as they are
4. Ensure the translation is culturally appropriate for the target language
5. For UI elements, use standard terminology for that language's software interfaces
6. For chatbot responses, maintain the conversational flow and tone

Text to translate:
"{text}"

Provide only the translated text without any explanations or additional content."""

        return prompt
        
    def _mock_translate(self, text: str, target_language: str, style: str) -> str:
        """
        Provide mock translations when OpenAI API is not available.
        This is useful for development and testing.
        """
        # Simple mock translation by adding a prefix
        style_prefix = {
            'formal': '[FORMAL]',
            'conversational': '[CONV]',
            'chatbot': '[BOT]'
        }.get(style, '[TRANS]')
        
        return f"{style_prefix} {text} [{target_language.upper()}]"
        
    def translate_batch(self, texts: List[str], target_language: str, 
                       style: str = 'formal', contexts: List[str] = None,
                       progress_callback=None) -> List[str]:
        """
        Translate multiple texts in batch.
        
        Args:
            texts: List of texts to translate
            target_language: Target language
            style: Translation style
            contexts: List of context strings (optional)
            progress_callback: Callback function for progress updates
            
        Returns:
            List of translated texts
        """
        if contexts is None:
            contexts = [''] * len(texts)
            
        results = []
        total = len(texts)
        
        for i, (text, context) in enumerate(zip(texts, contexts)):
            translated = self.translate(text, target_language, style, context)
            results.append(translated)
            
            if progress_callback:
                progress_callback(i + 1, total, text, translated)
                
        return results
        
    def validate_translation(self, original: str, translated: str, 
                           target_language: str) -> Dict[str, any]:
        """
        Validate a translation for quality and correctness.
        
        Args:
            original: Original text
            translated: Translated text
            target_language: Target language
            
        Returns:
            Dictionary with validation results
        """
        validation_result = {
            'is_valid': True,
            'warnings': [],
            'errors': [],
            'score': 1.0
        }
        
        # Check for empty translation
        if not translated or translated.strip() == '':
            validation_result['errors'].append("Translation is empty")
            validation_result['is_valid'] = False
            validation_result['score'] = 0.0
            return validation_result
            
        # Check for error messages
        if translated.startswith('[ERROR:'):
            validation_result['errors'].append("Translation contains error message")
            validation_result['is_valid'] = False
            validation_result['score'] = 0.0
            return validation_result
            
        # Check for preserved placeholders
        original_placeholders = self._extract_placeholders(original)
        translated_placeholders = self._extract_placeholders(translated)
        
        if original_placeholders != translated_placeholders:
            validation_result['warnings'].append(
                f"Placeholder mismatch: {original_placeholders} vs {translated_placeholders}"
            )
            validation_result['score'] -= 0.2
            
        # Check length ratio (translations shouldn't be extremely different in length)
        length_ratio = len(translated) / len(original) if len(original) > 0 else 1
        if length_ratio > 3 or length_ratio < 0.3:
            validation_result['warnings'].append(
                f"Unusual length ratio: {length_ratio:.2f}"
            )
            validation_result['score'] -= 0.1
            
        # Check for common issues
        if original.lower() == translated.lower():
            validation_result['warnings'].append("Translation appears unchanged")
            validation_result['score'] -= 0.3
            
        # Ensure score doesn't go below 0
        validation_result['score'] = max(0.0, validation_result['score'])
        
        return validation_result
        
    def _extract_placeholders(self, text: str) -> List[str]:
        """Extract placeholders like {variable} from text."""
        import re
        return re.findall(r'\{[^}]+\}', text)
        
    def get_supported_languages(self) -> List[str]:
        """Get list of supported languages."""
        return [
            "English", "Spanish", "French", "German", "Italian", "Portuguese",
            "Dutch", "Russian", "Chinese (Simplified)", "Chinese (Traditional)",
            "Japanese", "Korean", "Arabic", "Hindi", "Swedish", "Norwegian",
            "Danish", "Finnish", "Polish", "Czech", "Hungarian", "Romanian",
            "Bulgarian", "Croatian", "Serbian", "Slovak", "Slovenian",
            "Estonian", "Latvian", "Lithuanian", "Greek", "Turkish",
            "Hebrew", "Thai", "Vietnamese", "Indonesian", "Malay"
        ]
        
    def get_translation_styles(self) -> Dict[str, str]:
        """Get available translation styles with descriptions."""
        return {
            style: info['description'] 
            for style, info in self.style_templates.items()
        }
        
    def estimate_cost(self, text_count: int, avg_text_length: int) -> Dict[str, float]:
        """
        Estimate translation costs based on OpenAI pricing.
        
        Args:
            text_count: Number of texts to translate
            avg_text_length: Average length of texts
            
        Returns:
            Dictionary with cost estimates
        """
        # Rough token estimation (1 token ≈ 4 characters)
        input_tokens_per_text = (avg_text_length + 200) / 4  # +200 for prompt overhead
        output_tokens_per_text = avg_text_length / 4
        
        total_input_tokens = text_count * input_tokens_per_text
        total_output_tokens = text_count * output_tokens_per_text
        
        # GPT-4 pricing (as of 2024)
        input_cost_per_1k = 0.03  # $0.03 per 1K input tokens
        output_cost_per_1k = 0.06  # $0.06 per 1K output tokens
        
        input_cost = (total_input_tokens / 1000) * input_cost_per_1k
        output_cost = (total_output_tokens / 1000) * output_cost_per_1k
        total_cost = input_cost + output_cost
        
        return {
            'input_tokens': total_input_tokens,
            'output_tokens': total_output_tokens,
            'input_cost': input_cost,
            'output_cost': output_cost,
            'total_cost': total_cost,
            'cost_per_translation': total_cost / text_count if text_count > 0 else 0
        }
        
# Test the translation service
if __name__ == "__main__":
    service = TranslationService()
    
    # Test basic translation
    test_text = "Vänligen ge feedback på svaret:"
    print(f"Original: {test_text}")
    
    for style in ['formal', 'conversational', 'chatbot']:
        translated = service.translate(
            text=test_text,
            target_language="English",
            style=style,
            context="Chatbot feedback request"
        )
        print(f"{style.capitalize()}: {translated}")
        
    # Test validation
    validation = service.validate_translation(
        test_text, 
        "Please provide feedback on the answer:",
        "English"
    )
    print(f"\nValidation: {validation}")
    
    # Test cost estimation
    cost = service.estimate_cost(100, 50)
    print(f"\nCost estimate for 100 texts (avg 50 chars): ${cost['total_cost']:.4f}")