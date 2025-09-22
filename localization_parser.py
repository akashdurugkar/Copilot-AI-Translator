"""
Localization Parser Module
Handles parsing of Microsoft Copilot Studio localization files and extracts context information.
"""

import json
import re
from typing import Dict, List, Tuple, Optional
from pathlib import Path

class LocalizationParser:
    """Parser for Copilot Studio localization files."""
    
    def __init__(self):
        self.topic_patterns = [
            r"topic\.([^'\.]+)",  # Extract topic name
            r"dialog\([^.]*\.topic\.([^'\.]+)\)",  # Alternative topic pattern
            r"globalVariable\([^.]*\.component\.([^)]+)\)",  # Global variable pattern
        ]
        
        self.context_patterns = {
            'action_type': r"action\(([^)]+)\)",
            'trigger': r"trigger\(([^)]+)\)",
            'component': r"\.(Card|Activity|Prompt|Entity)\.",
            'ui_element': r"\.(text|title|DisplayName)",
            'intent': r"Intent\.(DisplayName|TriggerQueries)"
        }
        
    def load_file(self, file_path: str) -> Dict[str, Dict]:
        """Load and parse a localization file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
            
        parsed_data = {}
        for key, value in raw_data.items():
            parsed_entry = self.parse_entry(key, value)
            parsed_data[key] = parsed_entry
            
        return parsed_data
        
    def parse_entry(self, key: str, value: str) -> Dict:
        """Parse a single localization entry."""
        return {
            'text': value,
            'topic': self.extract_topic(key),
            'context': self.extract_context(key),
            'ui_component': self.extract_ui_component(key),
            'element_type': self.extract_element_type(key),
            'description': self.generate_description(key)
        }
        
    def extract_topic(self, key: str) -> str:
        """Extract topic name from the key."""
        for pattern in self.topic_patterns:
            match = re.search(pattern, key)
            if match:
                topic = match.group(1)
                # Clean up topic name
                topic = topic.replace('_', ' ').replace('-', ' ')
                return self.format_topic_name(topic)
        
        # Handle global variables specifically
        if "'globalVariable(" in key:
            return "Global Variables"
                
        return "Unknown Topic"
        
    def extract_context(self, key: str) -> Dict[str, str]:
        """Extract context information from the key."""
        context = {}
        
        for context_type, pattern in self.context_patterns.items():
            match = re.search(pattern, key)
            if match:
                context[context_type] = match.group(1)
                
        return context
        
    def extract_ui_component(self, key: str) -> str:
        """Extract the UI component type."""
        components = ['Card', 'Activity', 'Prompt', 'Entity', 'Intent', 'Dialog']

        for component in components:
            if f'.{component}.' in key:
                return component

        # Handle global variables
        if "'globalVariable(" in key:
            return "GlobalVariable"

        # Knowledge source heuristics
        # Look for patterns like knowledgeSourceComponent(...) or knowledgeBase / knowledgeSource
        lowered = key.lower()
        if 'knowledgesourcecomponent' in lowered or 'knowledge_source_component' in lowered:
            return 'KnowledgeSourceComponent'
        if '.knowledgebase.' in lowered or 'knowledgebase(' in lowered or '.knowledgesource.' in lowered:
            return 'KnowledgeSource'

        # Root-level DisplayName for dialog itself (e.g., ...'dialog(x).DisplayName")
        # If key ends with ".DisplayName" and has "'dialog(" earlier without another component marker
        if key.endswith(".DisplayName") and "'dialog(" in key and '.Entity.' not in key and '.Card.' not in key and '.Activity.' not in key and '.Prompt.' not in key:
            return 'DialogDisplayName'

        return "Unknown"
        
    def extract_element_type(self, key: str) -> str:
        """Extract the specific element type (text, title, etc.)."""
        elements = ['text', 'title', 'DisplayName', 'TriggerQueries', 'Description']
        
        for element in elements:
            if key.endswith(f'.{element}') or f'.{element}[' in key:
                return element
                
        return "text"
        
    def format_topic_name(self, topic: str) -> str:
        """Format topic name for better readability."""
        # Handle camelCase
        topic = re.sub(r'([a-z])([A-Z])', r'\1 \2', topic)
        
        # Capitalize words
        words = topic.split()
        formatted_words = []
        
        for word in words:
            if word.lower() in ['copilot', 'ai', 'ui', 'api']:
                formatted_words.append(word.upper())
            elif len(word) > 1:
                formatted_words.append(word.capitalize())
            else:
                formatted_words.append(word.upper())
                
        return ' '.join(formatted_words)
        
    def generate_description(self, key: str) -> str:
        """Generate a human-readable description of what this entry represents."""
        parts = []
        
        # Topic
        topic = self.extract_topic(key)
        if topic != "Unknown Topic":
            parts.append(f"Topic: {topic}")
            
        # UI Component
        component = self.extract_ui_component(key)
        if component != "Unknown":
            parts.append(f"Component: {component}")
            
        # Element type
        element = self.extract_element_type(key)
        if element != "text":
            parts.append(f"Element: {element}")
            
        # Action context
        context = self.extract_context(key)
        if 'action_type' in context:
            action = context['action_type']
            if action.startswith('question_'):
                parts.append("Type: Question")
            elif action.startswith('sendActivity_'):
                parts.append("Type: Response")
            elif action.startswith('sendMessage_'):
                parts.append("Type: Message")
            else:
                parts.append(f"Type: {action}")
                
        if not parts:
            parts.append("General localization entry")
            
        return " | ".join(parts)
        
    def get_topic_summary(self, parsed_data: Dict[str, Dict]) -> Dict[str, int]:
        """Get a summary of topics and their entry counts."""
        topic_counts = {}
        
        for entry in parsed_data.values():
            topic = entry['topic']
            topic_counts[topic] = topic_counts.get(topic, 0) + 1
            
        return dict(sorted(topic_counts.items()))
        
    def get_component_summary(self, parsed_data: Dict[str, Dict]) -> Dict[str, int]:
        """Get a summary of UI components and their entry counts."""
        component_counts = {}
        
        for entry in parsed_data.values():
            component = entry['ui_component']
            component_counts[component] = component_counts.get(component, 0) + 1
            
        return dict(sorted(component_counts.items()))
        
    def filter_by_topic(self, parsed_data: Dict[str, Dict], topic: str) -> Dict[str, Dict]:
        """Filter entries by topic."""
        return {
            key: entry for key, entry in parsed_data.items() 
            if entry['topic'] == topic
        }
        
    def filter_by_component(self, parsed_data: Dict[str, Dict], component: str) -> Dict[str, Dict]:
        """Filter entries by UI component."""
        return {
            key: entry for key, entry in parsed_data.items() 
            if entry['ui_component'] == component
        }
        
    def search_entries(self, parsed_data: Dict[str, Dict], search_term: str) -> Dict[str, Dict]:
        """Search entries by text content or description."""
        search_term = search_term.lower()
        results = {}
        
        for key, entry in parsed_data.items():
            if (search_term in entry['text'].lower() or 
                search_term in entry['description'].lower() or
                search_term in entry['topic'].lower()):
                results[key] = entry
                
        return results
        
    def validate_structure(self, file_path: str) -> Tuple[bool, List[str]]:
        """Validate the structure of a localization file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            errors = []
            
            # Check if it's a dictionary
            if not isinstance(data, dict):
                errors.append("File must contain a JSON object")
                return False, errors
                
            # Check entries
            for key, value in data.items():
                if not isinstance(key, str):
                    errors.append(f"Key must be string: {key}")
                    
                if not isinstance(value, str):
                    errors.append(f"Value must be string for key: {key}")
                    
                # Check key format (basic validation)
                if not ("'dialog(" in key or "'topic(" in key or "'globalVariable(" in key):
                    errors.append(f"Key doesn't match expected format: {key}")
                    
            if len(errors) > 10:
                errors = errors[:10]
                errors.append("... (showing first 10 errors)")
                
            return len(errors) == 0, errors
            
        except json.JSONDecodeError as e:
            return False, [f"Invalid JSON format: {str(e)}"]
        except Exception as e:
            return False, [f"Error reading file: {str(e)}"]
            
    def export_analysis(self, parsed_data: Dict[str, Dict], output_path: str):
        """Export analysis of the localization data."""
        analysis = {
            'total_entries': len(parsed_data),
            'topics': self.get_topic_summary(parsed_data),
            'components': self.get_component_summary(parsed_data),
            'entries': []
        }
        
        for key, entry in list(parsed_data.items())[:100]:  # Limit to first 100 for readability
            analysis['entries'].append({
                'key': key,
                'text': entry['text'][:100] + "..." if len(entry['text']) > 100 else entry['text'],
                'topic': entry['topic'],
                'component': entry['ui_component'],
                'description': entry['description']
            })
            
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, ensure_ascii=False, indent=2)

# Test the parser with the sample file
if __name__ == "__main__":
    parser = LocalizationParser()
    
    # Test with sample file if it exists
    sample_path = Path("Sample.json")
    if sample_path.exists():
        print("Testing parser with Sample.json...")
        
        # Validate structure
        is_valid, errors = parser.validate_structure(str(sample_path))
        if not is_valid:
            print("Validation errors:")
            for error in errors:
                print(f"  - {error}")
        else:
            print("File structure is valid!")
            
        # Parse the file
        try:
            data = parser.load_file(str(sample_path))
            print(f"\nParsed {len(data)} entries")
            
            # Show topic summary
            topics = parser.get_topic_summary(data)
            print(f"\nTopics found ({len(topics)}):")
            for topic, count in topics.items():
                print(f"  - {topic}: {count} entries")
                
            # Show component summary
            components = parser.get_component_summary(data)
            print(f"\nComponents found ({len(components)}):")
            for component, count in components.items():
                print(f"  - {component}: {count} entries")
                
            # Show first few entries
            print(f"\nFirst 3 entries:")
            for i, (key, entry) in enumerate(list(data.items())[:3]):
                print(f"\n{i+1}. {entry['description']}")
                print(f"   Text: {entry['text'][:100]}...")
                print(f"   Topic: {entry['topic']}")
                
        except Exception as e:
            print(f"Error parsing file: {e}")
    else:
        print("Sample.json not found in current directory")