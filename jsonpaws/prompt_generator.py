class PromptGenerator:
    """Generates prompts for GPT-4 based on the JSON schema, with modes for analysis and synthesis."""

    def __init__(self, mode='analysis'):
        """
        Initialize the PromptGenerator with a specific mode.
        
        Args:
            mode (str): Mode of prompt generation. Either 'analysis' or 'synthesis'.
        """
        if mode not in ['analysis', 'synthesis']:
            raise ValueError("Mode must be either 'analysis' or 'synthesis'")
        self.mode = mode

    def generate_prompt(self, field_name, field_info):
        """Generate a prompt based on the mode and field type."""
        field_type = field_info.get('type')
        enum_values = field_info.get('enum')

        if self.mode == 'synthesis':
            return self.generate_synthesis_prompt(field_name, field_info)

        # Analysis prompt generation
        if enum_values:
            choices = ', '.join(enum_values)
            return f"Choose one of the following for '{field_name}': {choices}."

        if field_type == "string":
            return f"Extract only the '{field_name}' as a string from the provided text."
        elif field_type == "number":
            return f"Extract only the numeric value for '{field_name}' from the provided text."
        elif field_type == "boolean":
            return f"Determine only if '{field_name}' is true or false from the provided text."
        elif field_type == "array":
            return f"Extract only the array of items for '{field_name}' from the provided text."
        elif field_type == "object":
            return f"Extract only the specified fields for '{field_name}' as an object from the provided text."
        
        return f"Extract only the value for '{field_name}' from the provided text."

    def generate_synthesis_prompt(self, field_name, field_info):
        """Generate a synthesis prompt for field generation."""
        field_type = field_info.get('type')
        enum_values = field_info.get('enum')

        if enum_values:
            choices = ', '.join(enum_values)
            return f"Generate a realistic value for '{field_name}' by choosing one of the following: {choices}."

        # Detailed instructions for different field types
        if field_type == "string":
            return f"Generate a realistic '{field_name}' as a string, such as a name or description."
        elif field_type == "number":
            min_value = field_info.get('minimum', 0)
            max_value = field_info.get('maximum', 120)  # Use appropriate range
            return f"Generate a realistic numeric value for '{field_name}', between {min_value} and {max_value}."
        elif field_type == "boolean":
            return f"Generate a realistic boolean value for '{field_name}', either true or false."
        elif field_type == "array":
            item_type = field_info.get('items', {}).get('type', 'string')
            return f"Generate an array of realistic '{item_type}' items for '{field_name}'."
        elif field_type == "object":
            return f"Generate realistic values for fields within the '{field_name}' object."
        
        return f"Generate a realistic value for '{field_name}'."
