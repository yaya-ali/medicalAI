import re


class DataFilter:
    def filter(self, fields: list[str], conditions: list[str], data: list):
        """
         Filter data based on field names and conditions using regex
         Args:
             field_names (list): List of field names to filter by
             conditions (list): List of regex conditions to filter by
             data (list): List of dictionaries to filter

        Note: use "." to access nested fields, e.g. "patient.name"
        """

        self.data = data
        result = []

        # If there's only one condition for multiple fields, replicate it
        if len(fields) == 1 and len(conditions) == 1:
            fields *= len(self.data)

        # Iterate through each item in the data
        for item in self.data:
            match = True

            # Check each field and condition pair
            for field_name, condition in zip(fields, conditions):
                value = self.get_nested_value(item, field_name)

                # Apply the regex condition to the field value
                if value is not None and condition is not None:
                    if not re.match(condition, str(value)):
                        match = False
                        break

            # If all conditions are met, add the item to the result
            if match:
                result.append(item)

        return result

    def get_nested_value(self, data: list | dict, field_name: str):
        # Retrieve nested values from the data based on the provided field name
        fields = field_name.split(".")
        value = data

        for field in fields:
            try:
                # Handle both dictionary and list types
                value = value[field] if isinstance(value, dict) else value[int(field)]
            except (KeyError, IndexError, ValueError, TypeError):
                return None

        return value
