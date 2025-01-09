"""
This is a library that contains usefull functions to send API messages
and do some basic validation.

Using this library will help maintain consistent response formatting and
simplified coding for your API function.
"""

### LINTER DISABLES ### (Avoid Using This)
# pylint: disable=line-too-long

### LIBRARIES ###
import re #Allows for matching values to patterns.

class Response:
    """
    This class contains methouds that help maintain consistent
    responses.
    """
    @classmethod
    def error_400_bad_request(cls, err_type: str = None, **kwargs) -> dict:
        """
        Returns a 400 error with the proper details

        PARAMETERS:
            err_type = identification of the type of 400 error.
            **kwargs = additional information on the error.
        """
        # List all the possible 400 bad_request responses.
        err_details = {
            "Bad Request"           : [400, "The server cannot process the request due to client error"], # default message

            "Missing Parameters"    : [400, "There are required parameters missing in the request body"],
            "Missing Headers"       : [400, "One or more of the request headers are missing"],
            "Invalid Values"        : [400, "There are parameters in the request body that contain invalid values"],
            "Invalid Headers"       : [400, "One or more of the request headers are invalid"],
            "Syntax Error"          : [400, "The JSON or XML is improperly formatted"],
            "Missing Credentials"   : [401, "The request lacks required authentication credentials"],
            "Invalid Credentials"   : [401, "The credentials procided are invalid"],
            "Payment Required"      : [402, "Payment must be made for the request to go through"],
            "Forbidden"             : [403, "You do not have the proper permissions to access this resource"],
            "Not Found"             : [404, "The requested source can not be found"],
            "Method Not Allowed"    : [405, "The request method is not supported by the target source"],
            "Request timeout"       : [408, "The request took to long to process"], 
            "Unsupported Media type": [415, "The Content-Type header specifies an unsupported media type"]
        }

        # If 'err_type' is not a valid 400 response error, set it to default response.
        if err_type is None or err_type not in err_details:
            err_type = "Bad Request"

        # Generate the error response based on the 'err_type'
        error = {
            "statusCode": err_details[err_type][0],
            "body": {
                "status": err_type,
                "message": err_details[err_type][1],
                "details": {}
            }
        }

        # Add any other provided details to the error response.
        for key, value in kwargs.items():
            error["details"][key] = value

        # Log the event
        print(f"{err_details[err_type][0]}: {err_type} = {err_details[err_type][1]}")

        return error

    @classmethod
    def error_500_internal_server(cls, exception: str) -> dict:
        """
        Returns a 400 error with the proper details

        PARAMETERS:
            exception = details on what broke in the server.
        """

        # Generate the error response based on the 'err_type'
        error = {
            "statusCode": 500,
            "body": {
                "status": "Internal Server Error",
                "details": ("An unexpected error occurred while processing the request.",
                            " If this error persists, please contact support.")
            }
        }

        # Log the event
        print(f"500 Internal Server Error: {exception}")

        return error

    @classmethod
    def success_200_response(cls, code = 200, result = {}) -> dict:
        """
        Returns a 200 success message with the required details.

        PARAMETERS:
            result = any information the API is expected to provide.
        """

        # Generate the success response
        response = {
            "statusCode": code,
            "body": {
                "status": "success",
                "details": result
            }
        }

        # Log the event
        print(f"{code}: Success")

        return response

class Validate:
    """
    This class contains methouds to perform a varioty of validations on
    parameters. There are also methouds for authentication.
    """

    @classmethod
    def validator(cls, args: dict, scheme: dict) -> dict:
        """
        Makes sure all the required parameters are accounted for and that
        each parameter contains a valid value.

        PARAMETERS:
            args   = json body parameters
            scheme = the blueprint of how the body should be
        """
        # Set up variables to hold parameters in error.
        missing_parameters = []
        invalid_parameters = []

        # Go through each parameter in the scheme and start comparing the recieved json
        #   body (args) to check if it meets the criteria.
        for parameter, details in scheme.items():

            # The current parameter contains a list of more parameters - key: [{key1:"", key2:"", etc...}]
            if isinstance(details, list):

                # If required is not found, default it to False
                if "required" not in details[0].keys():
                    details[0]["required"] = False

                # If the current parameter is not found and is required, add it to missing_parameters.
                if parameter not in args.keys() and details[0]["required"]:
                    missing_parameters.append(parameter)
                    continue

                # If the current parameter is not found but is not required, move on to the next parameter.
                elif parameter not in args.keys() and not details[0]["required"]:
                    continue

                # The current parameter is found. Validate its contents.
                else:
                    details[0].pop("required") #remove the "required" key.

                    # Go through each dictionary item the current parameter contains.
                    for item in args[parameter]:

                        # Start a new instance of validate_parameters() with contents of the current parameter.
                        errors = cls.validator(item, details[0])

                        # If errors were found, save them to the proper variable.
                        if errors and errors["error"] == "Missing Parameters":
                            missing_parameters.extend(errors["details"]["missingParameters"])

                        elif errors and errors["error"] == "Invalid values":
                            invalid_parameters.extend(errors["details"]["invalidValues"])

                # Everything for this parameter is compleated.
                # Move on to the next parameter in the scheme.
                continue

            # If required is not found, default it to False.
            if "required" not in details.keys():
                details["required"] = False

            # The Parameter is normal key:value pair
            # If the current parameter is not found and is required, add it to missing_parameters.
            if parameter not in args.keys() and details["required"]:
                missing_parameters.append(parameter)
                continue

            # If the current parameter is not found but is not required, move on to the next parameter.
            elif parameter not in args.keys() and not details["required"]:
                continue

            # The current parameter is found. Validate its contents.
            value = args[parameter]
            if (
                   (details['type'] == "email"      and not cls.is_email(value))
                or (details['type'] == "hash"       and not cls.is_hash(value))
                or (details['type'] == "zip code"   and not cls.is_zip_code(value))
                or (details['type'] == "string"     and not cls.is_string(value, details=details))
                or (details['type'] == "number"     and not cls.is_number(value))
                or (details['type'] == "list"       and not cls.is_list(value))
                or (details['type'] == "dictionary" and not cls.is_dict(value))
                or (details['type'] == "selection"  and not cls.is_selection(value, details["options"]))
                ):

                # The contents are invalid. Add it to invalid_parameters.
                invalid_parameters.append(parameter)

        # If there are any missing parameters, return this error first.
        if missing_parameters:
            return Response.error_400_bad_request("Missing Parameters", missingParameters=missing_parameters)

        # If there are no missing parameters but some contain invalid values, return this error.
        elif invalid_parameters:
            return Response.error_400_bad_request("Invalid Values", invalidValues=invalid_parameters)

        # All the required parameters are accounted for and valid.
        else:
            return None

    @classmethod
    def missing_parameters(cls, args, required_args: list) -> list:
        """
        Checks to see if the json body contains all the required
        parameters. Returns a list containing any parameters that
        are missing.

        Parameters:
            args            - the json body
            required_args (list) - a list containing all the required parameters
        """
        missing_parameters = []

        for key in args.keys():
            if key not in required_args:
                missing_parameters.append(key)

        return missing_parameters

    @classmethod
    def is_email(cls, value) -> bool:
        """
        Checks to see if the value matches an email structure.
        """
        if re.match(r"[^@]+@[^@]+\.[^@]+", value):
            return True
        else:
            return False

    @classmethod
    def is_hash(cls, value) -> bool:
        """
        Checks to see if the value is a valid hash
        """
        if re.match(r"^[a-f0-9]{32}$", value):
            return True
        else:
            return False

    @classmethod
    def is_zip_code(cls, value) -> bool:
        """
        Checks to se if the value is a valid zip code.
        ##### or #####-####
        """
        if re.match(r"^\d{5}(-\d{4})?$", value):
            return True
        else:
            return False

    @classmethod
    def is_string(cls, value, min_len: int = 0, max_len:int = 250, details:dict = None) -> bool:
        """
        Checks to see if the value is a string and fits a certian
        length

        Parameters:
            value (any)    - the value to validate
            min_len (int)  - the minimum length of the value
            max_len (int)  - the maximum length of the value
            details (dict) - used for cls.scheme_validator()
        """

        # If details were provided, check for custom lengths.
        if details:
            keys = details.keys()

            if "min_len" in keys:
                min_len = details["min_len"]

            if "max_len" in keys:
                max_len = details["max_len"]

        # Validate the value
        if isinstance(value, str) and min_len <= len(value) <= max_len:
            return True
        else:
            return False

    @classmethod
    def is_number(cls, value) -> bool:
        """
        Checks to see if the value is a number type
        """
        return isinstance(value, (int, float))

    @classmethod
    def is_list(cls, value) -> bool:
        """
        Checks to see if the value is a number type
        """
        return isinstance(value, list)

    @classmethod
    def is_dict(cls, value) -> bool:
        """
        Checks to see if the value is a number type
        """
        return isinstance(value, dict)

    @classmethod
    def is_selection(cls, value, options:list) -> bool:
        """
        Checks to see if the value equals one of the provided options.
        """
        return value in options