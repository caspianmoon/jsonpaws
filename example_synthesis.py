import json
from jsonpaws import JSONSchemaParser, PromptGenerator, ContentGenerator, JSONProcessor

# Set your OpenAI API key here
api_key = 'OPENAI-API-KEY'

# Define the JSON schema
json_schema = {
    "type": "object",
    "properties": {
        "report_date": {"type": "string"},
        "patients": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "firstName": {"type": "string"},
                    "lastName": {"type": "string"},
                    "age": {"type": "number", "minimum": 0, "maximum": 120},
                    "gender": {"type": "string", "enum": ["male", "female"]},
                    "diagnosis": {"type": "string"},
                    "medications": {
                        "type": "array",
                        "items": {"type": "string"}
                    }
                }
            }
        }
    }
}

# Initialize the schema parser
schema_parser = JSONSchemaParser(json_schema)

# Instructions for synthesis mode
instructions = """
Generate a JSON with a report date and a list of patients, where each patient has fields like id, firstName, lastName, age, gender, diagnosis, and medications.
"""

# For synthesis mode
prompt_generator_synthesis = PromptGenerator(mode='synthesis')
content_generator_synthesis = ContentGenerator(api_key=api_key, model='gpt-4o', mode='synthesis', instructions=instructions)
synthesis_processor = JSONProcessor(schema_parser, prompt_generator_synthesis, content_generator_synthesis, mode='synthesis')

# Generate the synthetic JSON data
generated_json_synthesis = synthesis_processor.process(instructions=instructions, schema=json_schema)

# Print the generated synthetic JSON
print("Generated JSON (Synthesis):", json.dumps(generated_json_synthesis, indent=4))