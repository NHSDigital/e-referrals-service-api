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
from requests.models import Request
from requests.models import Response
from urllib3.response import HTTPResponse

from io import BytesIO

from json import loads as json_loads
from json import load
from json import dumps as json_dumps

from openapi_core import Spec
from openapi_core.app import OpenAPI
from openapi_core.configurations import Config
from openapi_core.contrib.requests import RequestsOpenAPIRequest
from openapi_core.contrib.requests import RequestsOpenAPIResponse
from openapi_core.validation.request.validators import V30RequestBodyValidator
from openapi_core.validation.response.validators import V30ResponseDataValidator
from openapi_core.validation.schemas.exceptions import ValidateError

from yaml import safe_load

SCRIPT_LOCATION = os.path.join(os.path.dirname(os.path.abspath(__file__)))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_LOCATION, ".."))
spec_path_json = os.path.join(REPO_ROOT, "build/e-referrals-service-api.json")
spec_path_yaml = os.path.join(REPO_ROOT, "specification/e-referrals-service-api.yaml")
spec_path = os.path.join(REPO_ROOT, "specification/")
oas_spec_map = {}
response_spec_keys_examples = ["content", "application/fhir+json", "examples"]

# List containing http methods in OAS file
http_methods = ["post", "put", "patch", "get", "head", "delete"]

# List containing http success response codes
http_success_codes = ["200", "201"]

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

for endpoint in all_endpoints_url:
    all_http_methods = oas_spec_from_yaml["paths"][endpoint]
    for http_method in all_http_methods:
        endpoint_spec = oas_spec_from_yaml["paths"][endpoint][http_method]["$ref"]
        try:
            with open(os.path.join(spec_path, endpoint_spec), "r") as spec_yaml_file:
                oas_spec_map[endpoint_spec] = safe_load(spec_yaml_file)
        except FileNotFoundError:
            msg = "Make Publish fails: The endpoint OAS file is missing "
            print(msg, endpoint_spec)
            raise


# Create OpenAPICore Spec
spec = Spec.from_dict(oas_spec)

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
        "requestBody",
        "content",
        "application/fhir+json",
        "examples",
    ]


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
        oas_spec_map.get(oas_spec_from_yaml["paths"][endpoint][http_method]["$ref"])[
            "responses"
        ].keys()
    )
    filtered_code = filter(lambda x: x in http_success_codes, endpoint_return_codes)
    return list(filtered_code)[0]


def validate_request_examples():
    """
    Validates examples for requests
    """
    # Build request validator

    # Build data object with endpoints and examples
    endpoints_and_examples_request = build_request_validation_data()

    file_count = 0
    print("Validating request examples.")
    config = Config(
        server_base_url=None,
        request_validator_cls=V30RequestBodyValidator,
        extra_media_type_deserializers={"application/fhir+json": json_loads},
    )

    openApiSpec = OpenAPI(spec, config)

    # Validate request examples
    for endpoint in endpoints_and_examples_request:
        file_count += len(endpoints_and_examples_request[endpoint])
        for example_req_path in endpoints_and_examples_request[endpoint]:
            print(f"Validating: {example_req_path}")
            abspath_example = absolute_path(example_req_path, endpoint)

            with open(abspath_example, "r") as example_file:
                example_request = load(example_file)

            request = Request(
                get_http_method(endpoint),
                base_url + endpoint,
                headers={"content-type": "application/fhir+json"},
                json=example_request,
            )
            oapi_req = RequestsOpenAPIRequest(request)

            # Validate request body

            try:
                openApiSpec.validate_apicall_request(oapi_req)
            except ValidateError as exc:
                print("\nError: JSON data file with path " + abspath_example)
                print(
                    "used in request example for endpoint "
                    + endpoint
                    + " is not valid."
                )
                print("See 'ValidationError' field below:")
                print(exc.__context__)
                exit(1)

    if file_count == 0:
        print("no request files found to validate")
        exit(2)
    print(
        f"JSON request {file_count} examples are valid for {len(endpoints_and_examples_request)} endpoints"
    )


def build_request_validation_data():
    """
    Builds dictionary with endpoints and requestBody examples' file paths
    """
    endpoints_request_examples = {}
    for endpoint in all_endpoints_url:
        http_method = get_http_method(endpoint)
        data = oas_spec_map.get(
            oas_spec_from_yaml["paths"][endpoint][http_method]["$ref"]
        )
        example_keys = request_example_keys(endpoint, http_method)
        path_examples = get_path_examples(example_keys, data)
        endpoints_request_examples[endpoint] = path_examples
    return endpoints_request_examples


def create_response(data, status_code=200, content_type="application/fhir+json"):
    bt = bytes(json_dumps(data), "utf-8")
    fp = BytesIO(bt)
    raw = HTTPResponse(fp, preload_content=False)
    resp = Response()
    resp.headers = {"Content-Type": content_type}
    resp.status_code = status_code
    resp.raw = raw
    return resp


def absolute_path(request_path, endpoint_path):
    args = list(filter(lambda x: x != "..", request_path.split("/")))

    path = (
        "specification/components/r4"
        if endpoint_path.startswith("/R4/")
        else "specification/components/stu3"
    )
    return os.path.join(REPO_ROOT, path, *args)


def validate_response_examples():
    """
    Validates examples for responses
    """

    # Build data object with endpoint info and examples
    endpoints_and_examples_response = build_response_validation_data()

    file_count = 0

    print("Validating example responses.")
    config = Config(
        server_base_url=None,
        response_validator_cls=V30ResponseDataValidator,
        extra_media_type_deserializers={"application/fhir+json": json_loads},
    )

    openApiSpec = OpenAPI(spec, config)

    # Validate response for each endpoint
    for endpoint_dict in endpoints_and_examples_response:
        file_count += len(endpoint_dict)
        for example_res_path in endpoint_dict["examples"]:
            print(f"Validating: {example_res_path}")
            # Process response example file path
            abspath_example = absolute_path(example_res_path, endpoint_dict["path"])

            with open(abspath_example, "r") as example_file:
                example_response = load(example_file)

            # Build open aip response
            response = create_response(
                example_response, status_code=endpoint_dict["code"]
            )
            oapi_res = RequestsOpenAPIResponse(response)

            # Dummy request
            request = Request(
                endpoint_dict["method"],
                base_url + endpoint_dict["path"],
                headers={"content-type": "application/fhir+json"},
            )
            oapi_req = RequestsOpenAPIRequest(request)
            try:
                openApiSpec.validate_apicall_response(oapi_req, oapi_res)
            except ValidateError as exc:
                print("\nError: JSON data file with path " + abspath_example)
                print(
                    "used in response example for endpoint "
                    + endpoint_dict["path"]
                    + " is not valid."
                )
                print("See 'ValidationError' field below:")
                print(exc.__context__)
                exit(1)

    if file_count == 0:
        print("no response files found to validate")
        exit(2)
    print(
        f"JSON response {file_count} examples are valid for {len(endpoints_and_examples_response)} endpoints"
    )


def get_response_path(endpoint, http_method, success_code):
    """
    Retrieve the response json file URL
    """
    data = oas_spec_map.get(oas_spec_from_yaml["paths"][endpoint][http_method]["$ref"])
    response_spec_path = data["responses"][success_code]["$ref"]
    if not response_spec_path:
        print(
            "Error: Could not get oas specification for "
            + endpoint
            + " success response file"
            + response_spec_path
        )
        exit(1)

    example_path = (
        "components/r4/schemas/"
        if endpoint.startswith("/R4/")
        else "components/stu3/schemas/"
    )

    return os.path.join(spec_path, response_spec_path.replace("../", example_path))


def build_response_validation_data():
    """
    Builds list of dictionaries with info and response examples from relevant endpoints
    """
    endpoints_response_examples = []
    for endpoint in all_endpoints_url:
        http_method = get_http_method(endpoint)
        success_code = get_success_code(endpoint, http_method)
        response_spec_path = get_response_path(endpoint, http_method, success_code)

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
