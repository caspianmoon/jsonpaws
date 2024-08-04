import json
from jsonpaws import JSONSchemaParser, PromptGenerator, ContentGenerator, JSONProcessor


# Set your OpenAI API key here
api_key = 'OPENAI-API-KEY'

# Define the JSON schema
json_schema = {
    "type": "object",
    "properties": {
        "logos_in_image": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "scene": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "demographics": {
            "type": "object",
            "properties": {
                "age_group": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": [
                            "Under 5 years", "5 to 9 years", "10 to 14 years",
                            "15 to 19 years", "20 to 24 years", "25 to 29 years",
                            "30 to 34 years", "35 to 39 years", "40 to 44 years",
                            "45 to 49 years", "50 to 54 years", "55 to 59 years",
                            "60 to 64 years", "65 to 69 years", "70 to 74 years",
                            "75 to 79 years", "80 to 84 years", "85 years and over"
                        ]
                    }
                },
                "races": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": [
                            "White", "African American", "American Indian", "Asian", "Other"
                        ]
                    }
                },
                "gender": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": ["Male", "Female", "Non-binary", "Other"]
                    }
                }
            }
        },
        "objects": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "activity": {
            "type": "array",
            "items": {
                "type": "string"
            }
        }
    }
}


# Instructions for image analysis
instructions = '''
Analyze the following image and provide the results in JSON
'''
image_url = "https://cdn1.picuki.com/hosted-by-instagram/q/0exhNuNYnjBGZDHIdN5WmL9I2PwkAQ9OKftSQ7e71yJjMBhsLH6QvJA0mpCl6yRxIwVgFDeSYztj4oouUFlQAz17NEfWT7yKRTxV7q2RVean0Fph9JBikLc0LnIbZ3ap8MQvU2bABCxWFOkXULjh7uZDu7%7C%7CzNnZSyWaRMdsCmWYK4dv1CPol9YIosuzX2A3a5YcOLCkX+2UyMEgvsNzX5DwDWeKiYIMm66d5R%7C%7CkKiMQB5aHgnjH+LmMpRG1%7C%7CA23O6tqHoOAAuizgd2ge8VGoXo0fNk4G2WTsvDgntakgpIajOctq0Ppl4qLWFGQEDWpp9005xJG7liKaazL43hdQxjLXkOfmI6dgo5H9eNKtau24nAThT5D%7C%7CNf1PXnhSV7GDFVDUfaXmOOlgt61KCuhegEql+yeRQLnGxCxdIwNYuT+CIsNmcunN5vyiwiLcii+ChQs%7C%7CqP39dLYBngh%7C%7Cppyuz1Y9RnLFOttGP2mEgAl7EIY=.jpeg"

# Initialize components for image analysis
schema_parser = JSONSchemaParser(json_schema)
prompt_generator = PromptGenerator(mode='image')
content_generator = ContentGenerator(api_key=api_key, mode='image', instructions=instructions, temperature=0)

json_processor = JSONProcessor(
    schema_parser=schema_parser,
    prompt_generator=prompt_generator,
    content_generator=content_generator,
    mode='image'
)

result = json_processor.process(instructions=instructions, schema=json_schema, image_url=image_url)
print("Generated JSON (Image Analysis):", json.dumps(result, indent=4))