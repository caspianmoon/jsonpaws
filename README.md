# jsonpaws

**jsonpaws** is a Python library designed to generate structured and consistent JSON outputs using GPT-4o. The library provides both **analysis** and **synthesis** modes to extract and generate structured JSON data from unstructured text or based on a given schema.

## Features

- **Analysis Mode**: Extracts structured information from unstructured data. Ideal for data extraction and transformation tasks.
- **Synthesis Mode**: Generates realistic structured JSON data based on a specified schema. Perfect for creating synthetic datasets for simulations or testing.
- **Customizable**: Allows users to customize the OpenAI model and temperature settings for tailored data generation.
- **Easy Integration**: Designed for seamless integration into existing Python projects, with a straightforward API and minimal setup.

## Installation

Install jsonpaws using pip:

```
pip install json_paws
```

## Usage

### Getting Started
To use jsonpaws, you'll need to have an OpenAI API key. You can set it as an environment variable or pass it directly to the library.

### Setting the API Key
You can set the API key as an environment variable:

```
export OPENAI_API_KEY=your_api_key
```

Or pass it directly in your code:

```
import openai

openai.api_key = "your_api_key"
```

### Importing jsonpaws

Start by importing the necessary components from the library:
```
from jsonpaws import JSONSchemaParser, PromptGenerator, ContentGenerator, JSONProcessor
```

### Analysis Mode
In **Analysis Mode**, jsonpaws extracts structured data from unstructured text using a predefined JSON schema. This is useful for data extraction and transformation tasks.

**Example**
```
import json
from jsonpaws import JSONSchemaParser, PromptGenerator, ContentGenerator, JSONProcessor

# Set your OpenAI API key here
api_key = "YOUR_OPENAI_API_KEY"

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
prompt_generator_analysis = PromptGenerator(mode='analysis')
content_generator_analysis = ContentGenerator(api_key=api_key, model='gpt-4', mode='analysis')
analysis_processor = JSONProcessor(schema_parser, prompt_generator_analysis, content_generator_analysis, mode='analysis')

# Example unstructured data
unstructured_data = """
Patient Report: John Doe is a 45-year-old male diagnosed with hypertension.
The notes mention that he needs a follow-up in 3 months.
"""

# Process the unstructured data
generated_json_analysis = analysis_processor.process(unstructured_data, schema=json_schema)

# Print the extracted structured JSON
print("Generated JSON (Analysis):", json.dumps(generated_json_analysis, indent=4))
```

**Output**

```
Generated JSON (Analysis): {
    "report_date": "",
    "patients": [
        {
            "id": "1",
            "name": "John Doe",
            "age": 45,
            "gender": "male",
            "diagnosis": "hypertension",
            "notes": "He needs a follow-up in 3 months."
        }
    ]
}
```

### Synthesis Mode
In **Synthesis Mode**, jsonpaws generates realistic structured JSON data based on a specified schema. This mode is great for creating synthetic datasets for testing and simulations.

**Example**

```
import json
from jsonpaws import JSONSchemaParser, PromptGenerator, ContentGenerator, JSONProcessor

# Set your OpenAI API key here
api_key = "YOUR_OPENAI_API_KEY"

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
content_generator_synthesis = ContentGenerator(api_key=api_key, model='gpt-4', mode='synthesis')
synthesis_processor = JSONProcessor(schema_parser, prompt_generator_synthesis, content_generator_synthesis, mode='synthesis')

# Generate the synthetic JSON data
generated_json_synthesis = synthesis_processor.process(data={}, schema=json_schema)

# Print the generated synthetic JSON
print("Generated JSON (Synthesis):", json.dumps(generated_json_synthesis, indent=4))
```
**Output**

```
Generated JSON (Synthesis): {
    "report_date": {
        "report_date": "2023-10-15",
        "patients": [
            {
                "id": "p001",
                "name": "John Doe",
                "age": 45,
                "gender": "male",
                "diagnosis": "Hypertension",
                "notes": "Patient advised to follow a low-sodium diet."
            },
            {
                "id": "p002",
                "name": "Jane Smith",
                "age": 34,
                "gender": "female",
                "diagnosis": "Type 2 Diabetes",
                "notes": "Monitor blood sugar levels regularly."
            },
            {
                "id": "p003",
                "name": "Alex Johnson",
                "age": 28,
                "gender": "other",
                "diagnosis": "Anxiety Disorder",
                "notes": "Recommended therapy sessions once a week."
            }
        ]
    },
    "patients": {
        "report_date": "2023-10-15",
        "patients": [
            {
                "id": "P001",
                "name": "John Doe",
                "age": 45,
                "gender": "male",
                "diagnosis": "Hypertension",
                "notes": "Patient advised to monitor blood pressure regularly."
            },
            {
                "id": "P002",
                "name": "Jane Smith",
                "age": 34,
                "gender": "female",
                "diagnosis": "Type 2 Diabetes",
                "notes": "Diet and exercise plan recommended."
            },
            {
                "id": "P003",
                "name": "Alex Johnson",
                "age": 28,
                "gender": "other",
                "diagnosis": "Anxiety Disorder",
                "notes": "Referred to a mental health specialist."
            },
            {
                "id": "P004",
                "name": "Emily Davis",
                "age": 60,
                "gender": "female",
                "diagnosis": "Osteoarthritis",
                "notes": "Physical therapy suggested."
            },
            {
                "id": "P005",
                "name": "Michael Brown",
                "age": 72,
                "gender": "male",
                "diagnosis": "Chronic Heart Failure",
                "notes": "Medication adjustments required."
            },
            {
                "id": "P006",
                "name": "Linda Wilson",
                "age": 51,
                "gender": "female",
                "diagnosis": "Hyperlipidemia",
                "notes": "Lifestyle changes discussed."
            },
            {
                "id": "P007",
                "name": "David Lee",
                "age": 39,
                "gender": "male",
                "diagnosis": "Asthma",
                "notes": "Inhaler usage reviewed."
            },
            {
                "id": "P008",
                "name": "Sophia Taylor",
                "age": 29,
                "gender": "female",
                "diagnosis": "Depression",
                "notes": "Follow-up in one month."
            },
            {
                "id": "P009",
                "name": "James Anderson",
                "age": 75,
                "gender": "male",
                "diagnosis": "Alzheimer's Disease",
                "notes": "Support for caregivers discussed."
            },
            {
                "id": "P010",
                "name": "Olivia Martinez",
                "age": 22,
                "gender": "female",
                "diagnosis": "Migraine",
                "notes": "Triggers identified and managed."
            }
        ]
    }
}
```

### Customization
**jsonpaws** allows users to customize the OpenAI model and temperature settings:

* **Model**: You can specify the model you want to use (e.g., gpt-4o, gpt-4o-mini).
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

## Configuration

Set your OpenAI API key as an environment variable:
```
export OPENAI_API_KEY=your_api_key
```

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss potential improvements or features.

## License
This project is licensed under the MIT License.