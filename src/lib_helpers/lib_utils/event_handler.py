from jsonschema import validate

class EventHandler:
    """
    Class used to validate events according to a pre-defined JSON schema.

    Attributes:
        None

    Methods:
        handle_event(self, event: dict, schema: dict) -> dict:
            Validates the given event against the desired schema.

        Parameters:
            event : dict
                The event to be validated, a dictionary.
            
            schema : dict
                The schema against which the event will be validated, a dictionary defining the structure,
                types, and conditions that the event must adhere to.

        Returns:
            dict
                Returns the original event if successfully validated against the schema.

        Raises:
            ValidationError
                If the event does not conform to the expected schema, a ValidationError details the problem.

        Example:
            >>> event_handler = EventHandler()
            >>> event = {"name": "NewEvent", "timestamp": 1609459200}
            >>> schema = {
                            "type" : "object",
                            "properties" : {
                                "name" : {"type" : "string"},
                                "timestamp" : {"type" : "integer"}
                            },
                        }
            >>> event_handler.handle_event(event, schema)
            {'name': 'NewEvent', 'timestamp': 1609459200}
    """

    def handle_event(self, event, schema) -> dict:
        # Validate the event dictionary directly against the schema
        validate(instance=event, schema=schema)

        return event
