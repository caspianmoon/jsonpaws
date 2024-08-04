# jsonpaws

**jsonpaws** is an open-source Python library for generating structured and consistent JSON outputs using GPT-4o. It provides modes for **analysis**, **synthesis**, and **image analysis** to extract and generate structured JSON data from unstructured text or based on a given schema.

## Features
* Analysis Mode: Extract structured information from unstructured text. Perfect for data extraction and transformation tasks.
* Synthesis Mode: Generate realistic structured JSON data from a specified schema, ideal for creating synthetic datasets for simulations or testing.
* Image Analysis Mode: Analyze images to extract structured data and generate JSON outputs, making it suitable for computer vision applications.
* Customizable: Allows users to configure the OpenAI model and temperature settings for tailored data generation.
* Easy Integration: Seamlessly integrates into existing Python projects with a straightforward API and minimal setup.

## Installation

Install jsonpaws using pip:
```
pip install json_paws
```

## Getting Started
### Setting the API Key

To use jsonpaws, you'll need an OpenAI API key. You can set it as an environment variable or pass it directly to the library.

**Environment Variable**
```
export OPENAI_API_KEY=your_api_key
```

**Directly in Your Code**

```
import openai

openai.api_key = "your_api_key"
```

### Importing jsonpaws
Begin by importing the necessary components from the library:

```
from jsonpaws import JSONSchemaParser, PromptGenerator, ContentGenerator, JSONProcessor
```

## Usage
### Analysis Mode
In **Analysis Mode**, jsonpaws extracts structured data from unstructured text using a predefined JSON schema.

**Example**
```
import json
from jsonpaws import JSONSchemaParser, PromptGenerator, ContentGenerator, JSONProcessor

# Set your OpenAI API key here
api_key = "OPENAI-API-KEY"

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
content_generator_analysis = ContentGenerator(api_key=api_key, model='gpt-4o', mode='analysis', instructions=instructions)
analysis_processor = JSONProcessor(schema_parser, prompt_generator_analysis, content_generator_analysis, mode='analysis')

# Process the data
generated_json_analysis = analysis_processor.process(instructions=instructions, schema=json_schema)

# Print the extracted structured JSON
print("Generated JSON (Analysis):", json.dumps(generated_json_analysis, indent=4))
```

**Output**
```
Generated JSON (Analysis): {
    "report_date": "August 4, 2024",
    "patients": [
        {
            "id": "1",
            "firstName": "John",
            "lastName": "Doe",
            "age": 45,
            "gender": "male",
            "diagnosis": "hypertension",
            "medications": [
                "lisinopril",
                "atorvastatin"
            ]
        },
        {
            "id": "2",
            "firstName": "Jane",
            "lastName": "Smith",
            "age": 30,
            "gender": "female",
            "diagnosis": "diabetes",
            "medications": [
                "metformin"
            ]
        },
        {
            "id": "3",
            "firstName": "Sam",
            "lastName": "Brown",
            "age": 60,
            "gender": "male",
            "diagnosis": "arthritis",
            "medications": [
                "ibuprofen",
                "methotrexate"
            ]
        }
    ]
}
```

### Synthesis Mode
In **Synthesis Mode**, jsonpaws generates realistic structured JSON data from a specified schema.

**Example**
```
import json
from jsonpaws import JSONSchemaParser, PromptGenerator, ContentGenerator, JSONProcessor

# Set your OpenAI API key here
api_key = "OPENAI-API-KEY"

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

```
**Output**

```
Generated JSON (Synthesis): {
    "report_date": {
        "report_date": "2023-10-18",
        "patients": [
            {
                "id": "P001",
                "firstName": "John",
                "lastName": "Doe",
                "age": 45,
                "gender": "male",
                "diagnosis": "Hypertension",
                "medications": [
                    "Lisinopril",
                    "Amlodipine"
                ]
            },
            {
                "id": "P002",
                "firstName": "Jane",
                "lastName": "Smith",
                "age": 30,
                "gender": "female",
                "diagnosis": "Diabetes Type 2",
                "medications": [
                    "Metformin",
                    "Glyburide"
                ]
            },
            {
                "id": "P003",
                "firstName": "Emily",
                "lastName": "Johnson",
                "age": 60,
                "gender": "female",
                "diagnosis": "Osteoarthritis",
                "medications": [
                    "Ibuprofen",
                    "Glucosamine"
                ]
            },
            {
                "id": "P004",
                "firstName": "Michael",
                "lastName": "Brown",
                "age": 72,
                "gender": "male",
                "diagnosis": "Congestive Heart Failure",
                "medications": [
                    "Furosemide",
                    "Digoxin"
                ]
            }
        ]
    },
    "patients": {
        "report_date": "2023-10-15",
        "patients": [
            {
                "id": "P001",
                "firstName": "John",
                "lastName": "Doe",
                "age": 45,
                "gender": "male",
                "diagnosis": "Hypertension",
                "medications": [
                    "Lisinopril",
                    "Amlodipine"
                ]
            },
            {
                "id": "P002",
                "firstName": "Jane",
                "lastName": "Smith",
                "age": 34,
                "gender": "female",
                "diagnosis": "Type 2 Diabetes",
                "medications": [
                    "Metformin",
                    "Glipizide"
                ]
            },
            {
                "id": "P003",
                "firstName": "Emily",
                "lastName": "Johnson",
                "age": 28,
                "gender": "female",
                "diagnosis": "Anxiety Disorder",
                "medications": [
                    "Sertraline"
                ]
            },
            {
                "id": "P004",
                "firstName": "Michael",
                "lastName": "Williams",
                "age": 62,
                "gender": "male",
                "diagnosis": "Chronic Obstructive Pulmonary Disease",
                "medications": [
                    "Tiotropium",
                    "Albuterol"
                ]
            },
            {
                "id": "P005",
                "firstName": "David",
                "lastName": "Brown",
                "age": 50,
                "gender": "male",
                "diagnosis": "Hyperlipidemia",
                "medications": [
                    "Atorvastatin"
                ]
            },
            {
                "id": "P006",
                "firstName": "Sophia",
                "lastName": "Davis",
                "age": 40,
                "gender": "female",
                "diagnosis": "Asthma",
                "medications": [
                    "Fluticasone",
                    "Salbutamol"
                ]
            },
            {
                "id": "P007",
                "firstName": "Daniel",
                "lastName": "Miller",
                "age": 75,
                "gender": "male",
                "diagnosis": "Heart Failure",
                "medications": [
                    "Furosemide",
                    "Carvedilol"
                ]
            },
            {
                "id": "P008",
                "firstName": "Olivia",
                "lastName": "Garcia",
                "age": 22,
                "gender": "female",
                "diagnosis": "Major Depressive Disorder",
                "medications": [
                    "Citalopram"
                ]
            },
            {
                "id": "P009",
                "firstName": "James",
                "lastName": "Martinez",
                "age": 30,
                "gender": "male",
                "diagnosis": "Bipolar Disorder",
                "medications": [
                    "Lithium",
                    "Lamotrigine"
                ]
            },
            {
                "id": "P010",
                "firstName": "Ava",
                "lastName": "Hernandez",
                "age": 55,
                "gender": "female",
                "diagnosis": "Osteoarthritis",
                "medications": [
                    "Ibuprofen",
                    "Glucosamine"
                ]
            }
        ]
    }
}          
```
### Image Analysis Mode

In **Image Analysis Mode**, jsonpaws analyzes images to extract structured JSON data.

**Example**
```
import json
from jsonpaws import JSONSchemaParser, PromptGenerator, ContentGenerator, JSONProcessor

# Set your OpenAI API key here
api_key = 'OPENAI_API_KEY'

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
image_url = "https://cdn.britannica.com/34/235834-050-C5843610/two-different-breeds-of-cats-side-by-side-outdoors-in-the-garden.jpg"

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

```

**Output**
```
Generated JSON (Image Analysis): {
    "animal": "cat"
}
```
### Customization
**jsonpaws** allows users to customize the OpenAI model and temperature settings:

* **Model**: Specify the model to use (e.g., gpt-4o, gpt-4o-mini).
* **Temperature**: Control the randomness of the output. A higher temperature results in more random output.
**Example**
```
# Customize the content generator
content_generator_custom = ContentGenerator(
    api_key=api_key,
    model='gpt-4o',
    mode='synthesis',
    temperature=0.8  # Higher temperature for more randomness
)

# Use the custom content generator in your processor
synthesis_processor_custom = JSONProcessor(schema_parser, prompt_generator_synthesis, content_generator_custom, mode='synthesis')

# Generate the synthetic JSON data
generated_json_custom = synthesis_processor_custom.process(data={}, schema=json_schema)
print("Generated JSON (Custom):", json.dumps(generated_json_custom, indent=4))
```

## Contributing
Contributions are welcome! Please submit a pull request or open an issue to discuss potential improvements or features.

## License
This project is licensed under the MIT License.