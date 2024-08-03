class JSONProcessor:
    """Processes JSON data for both analysis and synthesis based on the mode."""

    def __init__(self, schema_parser, prompt_generator, content_generator, mode='analysis'):
        """
        Initialize the JSONProcessor with specific mode and components.
        
        Args:
            schema_parser (object): An object for parsing the JSON schema.
            prompt_generator (object): An object for generating prompts.
            content_generator (object): An object for generating content.
            mode (str): Mode of operation. Either 'analysis' or 'synthesis'.
        """
        if mode not in ['analysis', 'synthesis']:
            raise ValueError("Mode must be either 'analysis' or 'synthesis'")
        
        self.schema_parser = schema_parser
        self.prompt_generator = prompt_generator
        self.content_generator = content_generator
        self.mode = mode

    def process(self, data, schema=None):
        """
        Process the data based on the mode.

        Args:
            data (str or dict): Unstructured data for analysis or JSON data for synthesis.
            schema (dict): JSON schema for synthesis mode.

        Returns:
            dict: Processed JSON data.
        """
        if self.mode == 'analysis':
            return self.assemble_json(data, schema)
        elif self.mode == 'synthesis':
            if schema is None:
                raise ValueError("Schema must be provided for synthesis mode")
            return self.generate_synthetic_json(schema)

    def assemble_json(self, unstructured_data, schema, properties=None):
        """
        Assemble the JSON output based on unstructured data and schema properties.

        Args:
            unstructured_data (str): The unstructured data to be processed.
            schema (dict): JSON schema for analyzing data.
            properties (dict): The properties from the JSON schema.

        Returns:
            dict: Generated JSON data.
        """
        if properties is None:
            properties = self.schema_parser.parse()

        generated_json = {}

        for field_name, field_info in properties.items():
            field_type = field_info.get('type')

            if field_type == 'object':
                # Recursively parse nested objects
                nested_properties = field_info.get('properties', {})
                nested_object = self.assemble_json(unstructured_data, schema, nested_properties)
                generated_json[field_name] = nested_object
            elif field_type == 'array':
                # Handle arrays by extracting each item
                prompt = self.prompt_generator.generate_prompt(field_name, field_info)
                content = self.content_generator.generate_content(prompt, schema, unstructured_data, field_type, field_name, field_info)
                
                # Process array items
                extracted_items = []
                if isinstance(content, list):
                    for item in content:
                        extracted_item = {}
                        for key, sub_field_info in field_info.get('items', {}).get('properties', {}).items():
                            # Use content mapping for schema keys
                            extracted_item[key] = item.get(key, self.content_generator.get_fallback(sub_field_info['type']))
                        extracted_items.append(extracted_item)
                    generated_json[field_name] = extracted_items
            else:
                prompt = self.prompt_generator.generate_prompt(field_name, field_info)
                content = self.content_generator.generate_content(prompt, schema, unstructured_data, field_type, field_name, field_info)
                generated_json[field_name] = content

        return generated_json

    def generate_synthetic_json(self, schema):
        """
        Generate synthetic JSON data based on the schema.

        Args:
            schema (dict): JSON schema for generating data.

        Returns:
            dict: Synthetic JSON data generated based on the schema.
        """
        properties = schema.get('properties', {})
        generated_json = {}

        for field_name, field_info in properties.items():
            prompt = self.prompt_generator.generate_prompt(field_name, field_info)
            content = self.content_generator.generate_content(prompt, schema)
            generated_json[field_name] = content

        return generated_json

    def validate_and_normalize_json(self, data, schema):
        """
        Validate and normalize JSON data according to the schema.

        Args:
            data (dict): The JSON data to be validated and normalized.
            schema (dict): The schema to use for validation and normalization.

        Returns:
            dict: The validated and normalized JSON data.
        """
        if isinstance(data, dict) and "properties" in schema:
            # Iterate through schema properties
            for key, prop_schema in schema["properties"].items():
                if key in data:
                    # Recursively apply defaults and remove unnecessary fields for objects
                    if prop_schema.get("type") == "object":
                        self.validate_and_normalize_json(data[key], prop_schema)
                    elif prop_schema.get("type") == "array":
                        if isinstance(data[key], list):
                            for item in data[key]:
                                self.validate_and_normalize_json(item, prop_schema["items"])
                        else:
                            data[key] = []
                else:
                    # Assign default values if the key is missing
                    if "default" in prop_schema:
                        data[key] = prop_schema["default"]
                    elif prop_schema.get("type") == "object":
                        data[key] = {}
                        self.validate_and_normalize_json(data[key], prop_schema)
                    elif prop_schema.get("type") == "array":
                        data[key] = []
                        if "items" in prop_schema:
                            default_item = {}
                            self.validate_and_normalize_json(default_item, prop_schema["items"])
                            data[key].append(default_item)

            # Remove fields not in the schema
            keys_to_remove = [key for key in data.keys() if key not in schema["properties"]]
            for key in keys_to_remove:
                del data[key]

        return data
