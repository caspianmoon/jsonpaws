import json
from jsonpaws import JSONSchemaParser, PromptGenerator, ContentGenerator, JSONProcessor

# Set your OpenAI API key here
api_key = 'OPENAI-API-KEY'

# Define the JSON schema
json_schema = {
    "properties": {
        "animal": {
            "type": "string",
            "enum": ["cat", "dog", "bird"]
        }
    }
}

# Initialize the schema parser
schema_parser = JSONSchemaParser(json_schema)

# Instructions for image analysis
instructions = '''
Analyze the image and identify the animal according to the given schema.
'''
# URL of the image to analyze
image_url = "image url here"

# Initialize components for image analysis
prompt_generator = PromptGenerator(mode='image')
content_generator = ContentGenerator(api_key=api_key, model='gpt-4o-mini', mode='image', instructions=instructions)
image_processor = JSONProcessor(
    schema_parser=schema_parser,
    prompt_generator=prompt_generator,
    content_generator=content_generator,
    mode='image'
)

# Perform image analysis and generate JSON
generated_json_image = image_processor.process(instructions=instructions, schema=json_schema, image_url=image_url)
print("Generated JSON (Image Analysis):", json.dumps(generated_json_image, indent=4))
