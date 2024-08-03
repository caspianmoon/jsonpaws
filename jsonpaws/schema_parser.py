class JSONSchemaParser:
    """Parses the JSON schema to extract structure and types."""

    def __init__(self, schema):
        self.schema = schema

    def parse(self):
        """Parses the schema into a structured format for generation."""
        return self.schema.get('properties', {})
