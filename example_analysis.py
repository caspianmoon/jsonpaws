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

# For analysis mode
instructions = """
Extract patient information from the text and populate the JSON schema accordingly.
The report dated August 4, 2024, details the patient records for the day.
Among the patients, there is John Doe, a 45-year-old male diagnosed with hypertension, who is currently prescribed lisinopril and atorvastatin.
Another patient, Jane Smith, a 30-year-old female, has been diagnosed with diabetes and is on metformin.
The list also includes Sam Brown, a 60-year-old male suffering from arthritis, for which he is taking ibuprofen and methotrexate.
"""
prompt_generator_analysis = PromptGenerator(mode='analysis')
content_generator_analysis = ContentGenerator(api_key=api_key, model='gpt-4o-mini', mode='analysis', instructions=instructions)
analysis_processor = JSONProcessor(schema_parser, prompt_generator_analysis, content_generator_analysis, mode='analysis')

# Process the data
generated_json_analysis = analysis_processor.process(instructions=instructions, schema=json_schema)

# Print the extracted structured JSON
print("Generated JSON (Analysis):", json.dumps(generated_json_analysis, indent=4))