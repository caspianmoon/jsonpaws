import json
from jsonpaws import JSONSchemaParser, PromptGenerator, ContentGenerator, JSONProcessor

# Set your OpenAI API key here
api_key = "OPENAI-API-KEY"

# Define the simple JSON schema
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
                    "name": {"type": "string"},
                    "age": {"type": "number", "minimum": 0, "maximum": 120},
                    "gender": {"type": "string", "enum": ["male", "female", "other"]},
                    "diagnosis": {"type": "string"},
                    "notes": {"type": "string"}
                }
            }
        }
    }
}

# Initialize the schema parser
schema_parser = JSONSchemaParser(json_schema)

# Instructions for synthesis mode
instructions = """
Generate a JSON with a report date and a list of patients, where each patient has fields like id, name, age, gender, diagnosis, and notes.
"""

# For synthesis mode
prompt_generator_synthesis = PromptGenerator(mode='synthesis')
content_generator_synthesis = ContentGenerator(api_key=api_key, model='gpt-4o-mini', mode='synthesis')
synthesis_processor = JSONProcessor(schema_parser, prompt_generator_synthesis, content_generator_synthesis, mode='synthesis')

# Generate the synthetic JSON data
generated_json = synthesis_processor.process(data={}, schema=json_schema)
print("Generated JSON (Synthesis):", json.dumps(generated_json, indent=4))

# For analysis mode
prompt_generator_analysis = PromptGenerator(mode='analysis')
content_generator_analysis = ContentGenerator(api_key=api_key, model='gpt-4o-mini', mode='analysis')
analysis_processor = JSONProcessor(schema_parser, prompt_generator_analysis, content_generator_analysis, mode='analysis')

# Example unstructured data
unstructured_data = """
Patient Report: John Doe is a 45-year-old male diagnosed with hypertension. The notes mention that he needs a follow-up in 3 months.
"""

generated_json_analysis = analysis_processor.process(unstructured_data, schema=json_schema)
print("Generated JSON (Analysis):", json.dumps(generated_json_analysis, indent=4))
