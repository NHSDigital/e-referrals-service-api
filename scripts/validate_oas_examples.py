#!/usr/bin/env python3

"""
The OAS file will contain JSON examples for
- Requests
    Endpoints that have a request body with content application/fhir+json
- Responses
    Endpoints that return content application/fhir+json

This script looks to validate these examples.

At the moment it is not validating example responses for failure scenarios.

Usage:
Running 'make publish' will execute this script
"""

import os.path
from json import load
from openapi_core import create_spec
from openapi_core.validation.request.validators import RequestValidator
from openapi_core.validation.request.datatypes import OpenAPIRequest
from openapi_core.validation.response.validators import ResponseValidator
from openapi_core.validation.response.datatypes import OpenAPIResponse
from yaml import safe_load

SCRIPT_LOCATION = os.path.join(os.path.dirname(os.path.abspath(__file__)))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_LOCATION, ".."))
spec_path_json = os.path.join(REPO_ROOT, "build/e-referrals-service-api.json")
spec_path_yaml = os.path.join(REPO_ROOT, "specification/e-referrals-service-api.yaml")

# List containing http methods in OAS file
http_methods = ["post", "put", "patch", "get"]

# List containing http success response codes
http_success_codes = ["200", "201", "307"]

# Open OAS JSON file
try:
    with open(spec_path_json, "r") as spec_file:
        oas_spec = load(spec_file)
except FileNotFoundError:
    msg = "File or path does not exist. Consider executing " "'make publish'."
    print(msg)
    raise

# Open OAS YAML file
with open(spec_path_yaml) as yaml_file:
    oas_spec_from_yaml = safe_load(yaml_file)

# List all endpoints
all_endpoints_url = oas_spec_from_yaml["paths"].keys()

# Create OpenAPICore Spec
spec = create_spec(oas_spec)

# Fetch base URL (will not matter for validation)
base_url = oas_spec["servers"][0]["url"]


def deep_get(d, keys, default=None):
    """
    Supports traversing nested dictionaries and searching for keys.
    Returns None if keys don't exist.
    Example:
        d = {'meta': {'status': 'OK', 'status_code': 200}}
        deep_get(d, ['meta', 'status_code'])          # => 200
        deep_get(d, ['garbage', 'status_code'])       # => None
        deep_get(d, ['meta', 'garbage'], default='-') # => '-'
    """
    assert type(keys) is list
    if d is None:
        return default
    if not keys:
        return d
    return deep_get(d.get(keys[0]), keys[1:], default)


def request_example_keys(endpoint, method):
    """
    Returns list with keys for accessing request examples in oas dictionary
    """
    return [
        "paths",
        endpoint,
        method,
        "requestBody",
        "content",
        "application/fhir+json",
        "examples",
    ]


def response_example_keys(endpoint, method, success_code):
    """
    Returns tuple of lists with keys for accessing response examples in oas dictionary
    """
    return (
        ["paths", endpoint, method, "responses", success_code, "$ref"],
        ["content", "application/fhir+json", "examples"],
    )


def get_path_examples(keys_lst, spec=oas_spec_from_yaml):
    """
    Returns a list with the paths for the corresponding endpoint's examples
    """
    path_examples = []
    examples = deep_get(spec, keys_lst)
    if examples is not None:
        for example in examples:
            path = deep_get(examples, [example, "value", "$ref"])
            if not path:
                print(
                    "Error: Could not get path for "
                    + keys_lst[1]
                    + " example "
                    + example
                )
                exit(1)
            path_examples.append(path)
    return path_examples


def get_http_method(endpoint):
    """
    Returns http method used by the endpoint
    """
    return list(
        filter(
            lambda x: x in http_methods, oas_spec_from_yaml["paths"][endpoint].keys()
        )
    )[0]


def get_success_code(endpoint, http_method):
    """
    Returns HTTP success response code
    """
    endpoint_return_codes = list(
        oas_spec_from_yaml["paths"][endpoint][http_method]["responses"].keys()
    )
    filtered_code = filter(lambda x: x in http_success_codes, endpoint_return_codes)

    return list(filtered_code)[0]


def validate_request_examples():
    """
    Validates examples for requests
    """
    # Build request validator
    req_validator = RequestValidator(spec)

    # Build data object with endpoints and examples
    endpoints_and_examples_request = build_request_validation_data()

    # Validate request examples
    for endpoint in endpoints_and_examples_request:
        for example_req_path in endpoints_and_examples_request[endpoint]:

            abs_path = os.path.join(REPO_ROOT, "specification", example_req_path)
            with open(abs_path, "r") as example_file:
                example_request = load(example_file)

            oapi_req = OpenAPIRequest(
                full_url_pattern=base_url + endpoint,
                method=get_http_method(endpoint),
                body=example_request,
                mimetype="application/fhir+json",
            )

            # Validate request body
            result = req_validator._validate_body(oapi_req)

            # Raise errors if request invalid
            try:
                result.raise_for_errors()
            except Exception as e:
                print("\nError: JSON data file with path " + abs_path)
                print(
                    "used in request example for endpoint "
                    + endpoint
                    + " is not valid."
                )
                print("See 'ValidationError' field below:")
                print(e)
                exit(1)

    print("JSON request examples are valid for each endpoint")


def build_request_validation_data():
    """
    Builds dictionary with endpoints and requestBody examples' file paths
    """
    endpoints_request_examples = {}
    for endpoint in all_endpoints_url:
        http_method = get_http_method(endpoint)
        example_keys = request_example_keys(endpoint, http_method)
        path_examples = get_path_examples(example_keys)
        endpoints_request_examples[endpoint] = path_examples
    return endpoints_request_examples


def validate_response_examples():
    """
    Validates examples for responses
    """

    # Build response validator
    res_validator = ResponseValidator(spec)

    # Build data object with endpoint info and examples
    endpoints_and_examples_response = build_response_validation_data()

    # Validate response for each endpoint
    for endpoint_dict in endpoints_and_examples_response:
        for example_res_path in endpoint_dict["examples"]:

            # Process response example file path
            args = list(filter(lambda x: x != "..", example_res_path.split("/")))
            abspath_example = os.path.join(REPO_ROOT, "specification/components", *args)

            with open(abspath_example, "r") as example_file:
                example_response = load(example_file)

            # Dummy request
            oapi_req = OpenAPIRequest(
                full_url_pattern=base_url + endpoint_dict["path"],
                method=endpoint_dict["method"],
                body={},
                mimetype="application/fhir+json",
            )

            # Build openAPI response
            oapi_res = OpenAPIResponse(
                data=example_response,
                status_code=endpoint_dict["code"],
                mimetype="application/fhir+json",
            )

            result = res_validator._validate_data(oapi_req, oapi_res)

            # Raise errors if request invalid
            try:
                result.raise_for_errors()
            except Exception as e:
                print("\nError: JSON data file with path " + abspath_example)
                print(
                    "used in response example for endpoint "
                    + endpoint_dict["path"]
                    + " is not valid."
                )
                print("See 'ValidationError' field below:")
                print(e)
                exit(1)

    print("JSON response examples are valid for each endpoint")


def build_response_validation_data():
    """
    Builds list of dictionaries with info and response examples from relevant endpoints
    """
    endpoints_response_examples = []
    for endpoint in all_endpoints_url:

        http_method = get_http_method(endpoint)
        success_code = get_success_code(endpoint, http_method)
        response_spec_keys, response_spec_keys_examples = response_example_keys(
            endpoint, http_method, success_code
        )
        response_spec_path = deep_get(oas_spec_from_yaml, response_spec_keys)
        if not response_spec_path:
            print(
                "Error: Could not get oas specification for "
                + endpoint
                + " success response"
            )
            exit(1)

        # Open response example file
        with open(
            os.path.join(REPO_ROOT, "specification", response_spec_path)
        ) as yaml_file:
            yaml_data = yaml_file.read()
            yaml_data = yaml_data.replace("`", "")
            response_spec = safe_load(yaml_data)

        response_path_examples = get_path_examples(
            response_spec_keys_examples, response_spec
        )

        endpoint_dict = {
            "code": success_code,
            "path": endpoint,
            "method": http_method,
            "examples": response_path_examples,
        }

        endpoints_response_examples.append(endpoint_dict)

    return endpoints_response_examples


if __name__ == "__main__":
    # Call validation methods
    validate_request_examples()
    validate_response_examples()
