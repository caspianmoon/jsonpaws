def validate_and_normalize_json(data, schema):
    """Validate and normalize JSON data according to the schema."""
    if isinstance(data, dict) and "properties" in schema:
        # Iterate through schema properties
        for key, prop_schema in schema["properties"].items():
            if key in data:
                # Recursively apply defaults and remove unnecessary fields for objects
                if prop_schema.get("type") == "object":
                    validate_and_normalize_json(data[key], prop_schema)
                elif prop_schema.get("type") == "array":
                    if isinstance(data[key], list):
                        for item in data[key]:
                            validate_and_normalize_json(item, prop_schema["items"])
                    else:
                        data[key] = []
            else:
                # Assign default values if the key is missing
                if "default" in prop_schema:
                    data[key] = prop_schema["default"]
                elif prop_schema.get("type") == "object":
                    data[key] = {}
                    validate_and_normalize_json(data[key], prop_schema)
                elif prop_schema.get("type") == "array":
                    data[key] = []
                    if "items" in prop_schema:
                        default_item = {}
                        validate_and_normalize_json(default_item, prop_schema["items"])
                        data[key].append(default_item)

        # Remove fields not in the schema
        keys_to_remove = [key for key in data.keys() if key not in schema["properties"]]
        for key in keys_to_remove:
            del data[key]

    return data
