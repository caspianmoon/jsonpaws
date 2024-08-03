import json
import openai

class ContentGenerator:
    """Generates content for each field using GPT-4 with modes for analysis and synthesis."""

    def __init__(self, api_key, model='gpt-4', mode='analysis', max_attempts=3, temperature=None):
        """
        Initialize the ContentGenerator with a specific mode and other configurations.
        
        Args:
            api_key (str): OpenAI API key.
            model (str): The model name to be used for content generation.
            mode (str): Mode of content generation. Either 'analysis' or 'synthesis'.
            max_attempts (int): Number of attempts to generate content.
            temperature (float): Temperature setting for GPT-4's response diversity.
        """
        if mode not in ['analysis', 'synthesis']:
            raise ValueError("Mode must be either 'analysis' or 'synthesis'")
        
        self.api_key = api_key
        openai.api_key = self.api_key

        self.model = model
        self.mode = mode
        self.max_attempts = max_attempts
        
        # Set default temperatures for each mode if not explicitly provided
        self.temperature = temperature if temperature is not None else (0.5 if mode == 'analysis' else 0.7)

    def generate_content(self, prompt, json_schema, unstructured_data=None, expected_type=None, field_name=None, field_info=None):
        """
        Generate content using GPT-4 based on the selected mode.

        Args:
            prompt (str): Base prompt to be sent to GPT-4.
            json_schema (dict): The JSON schema being used for generation or analysis.
            unstructured_data (str): Additional text data for analysis mode.
            expected_type (str): Expected data type for the field (used in analysis).
            field_name (str): Name of the field (used in analysis).
            field_info (dict): Additional field information (used in analysis).

        Returns:
            object: Extracted or generated content based on the selected mode.
        """
        for attempt in range(self.max_attempts):
            try:
                if self.mode == 'analysis':
                    # Construct prompt for analysis
                    analysis_prompt = f"{prompt}\n\nSchema: {json.dumps(json_schema)}\n\nText: {unstructured_data}"

                    # Send prompt to GPT-4 for analysis
                    response = openai.chat.completions.create(
                        model=self.model,
                        response_format={ "type": "json_object" },
                        messages=[
                            {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
                            {"role": "user", "content": f"{analysis_prompt} Do not include anything beyond what is provided in the input. If any information is not included in the input, for example, the date of birth of someone, don't generate any value for that"}
                        ],
                        temperature=self.temperature
                    )

                    # Extract content
                    content = response.choices[0].message.content.strip()

                    # Parse JSON response and extract the value for the field
                    extracted_value = self.extract_json_value(content, field_name, expected_type, field_info)
                    if extracted_value is not None:
                        return extracted_value

                else:  # self.mode == 'synthesis'
                    synthesis_prompt = f"{prompt}\n\nSchema: {json.dumps(json_schema)}"

                    # Send prompt to GPT-4 for synthesis
                    response = openai.chat.completions.create(
                        model=self.model,
                        response_format={ "type": "json_object" },
                        messages=[
                            {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
                            {"role": "user", "content": synthesis_prompt}
                        ],
                        temperature=self.temperature
                    )

                    # Extract content
                    content = response.choices[0].message.content.strip()

                    # Ensure the content is formatted as JSON
                    parsed_json = json.loads(content)
                    return parsed_json  # If valid, return it

            except json.JSONDecodeError as e:
                print(f"Failed to parse JSON: {e}")
                print("Received content:", content)
            except Exception as e:
                print(f"Error during content generation: {e}")

        # Return a fallback if generation fails (Analysis) or None (Synthesis)
        return self.get_fallback(expected_type) if self.mode == 'analysis' else None

    def extract_json_value(self, content, field_name, expected_type, field_info):
        """
        Extract the desired value from the JSON content for analysis.

        Args:
            content (str): JSON content returned by GPT-4.
            field_name (str): Name of the field to extract.
            expected_type (str): Expected data type of the field.
            field_info (dict): Additional field information for extraction.

        Returns:
            object: Extracted value from the JSON content.
        """
        try:
            data = json.loads(content)
            # Implement specific extraction logic based on expected_type and field_info
            # Example extraction logic:
            if expected_type == 'string':
                return data.get(field_name, "")
            elif expected_type == 'number':
                return data.get(field_name, 0)
            elif expected_type == 'boolean':
                return data.get(field_name, False)
            elif expected_type == 'array':
                return data.get(field_name, [])
            elif expected_type == 'object':
                return data.get(field_name, {})
            return data.get(field_name)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON during extraction: {e}")
            return None

    def get_fallback(self, expected_type):
        """
        Provide a fallback value if content generation fails in analysis mode.

        Args:
            expected_type (str): Expected data type for the field.

        Returns:
            object: Fallback value for the given expected type.
        """
        # Implement fallback logic based on expected_type
        # Example fallback logic:
        if expected_type == 'string':
            return "N/A"
        elif expected_type == 'number':
            return 0
        elif expected_type == 'boolean':
            return False
        elif expected_type == 'array':
            return []
        elif expected_type == 'object':
            return {}
        return None
