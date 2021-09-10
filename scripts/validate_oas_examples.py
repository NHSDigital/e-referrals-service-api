#!/usr/bin/env python3

from json import load
from openapi_core import create_spec
from openapi_core.validation.request.validators import RequestValidator
from openapi_core.validation.request.datatypes import OpenAPIRequest
from openapi_core.validation.response.validators import ResponseValidator
from openapi_core.validation.response.datatypes import OpenAPIResponse

"""
# Idea for implementation
import glob
requests_files = glob.glob("specification/components/examples/**/requests/*.json", recursive=True)
responses_files = glob.glob("specification/components/examples/**/responses/*.json", recursive=True)
...
useful_to have = [{"endpoint1":"endpoint1_url", "req_files":[...], "res_files":[{"rf_1":rf_1_status_code}, ...]},
                   {endpoint2},
                   ...]
...
full_url_pattern = base_url + endpoint
"""

# Build Specification object
spec_path = "build/e-referrals-service-api.json"

try:
    with open(spec_path, "r") as spec_file:
        spec_dict = load(spec_file)
except FileNotFoundError:
    msg = (
        "File or path does not exist. Consider executing "
        "'make publish' to resolve/expand the spec."
    )
    print(msg)
    raise

spec = create_spec(spec_dict)

# Build request validator
req_validator = RequestValidator(spec)

# Build Open-API request
example_req_path = (
    "specification/components/examples/createReferral/requests/MinimalRequest.json"
)
with open(example_req_path, "r") as example_file:
    example_req_dict = load(example_file)

# sandbox url; shouldn't matter for validation
base_url = spec_dict["servers"][0]["url"]

create_referral_endpoint = "/STU3/v1/ReferralRequest/$ers.createReferral"

oapi_req = OpenAPIRequest(
    full_url_pattern=base_url + create_referral_endpoint,
    method="post",
    body=example_req_dict,
    mimetype="application/fhir+json",
)

# Validate request body
"""
openapi-core 0.14.2 has currently no way to validate only the body
without using validator._validate_body()
In future releases this might move to a class RequestBodyValidator
as seen on https://bit.ly/38Wsu7M
I've set poetry to use only version 0.14.2
So when this happens we might consider updating this script
and we'll have to tell poetry to use the latest version.
"""
result = req_validator._validate_body(oapi_req)

# Raise errors if request invalid
try:
    result.raise_for_errors()
except Exception as e:
    print("Request not valid.")
    print(e)
else:
    print("Request is valid.")

# Build response validator
res_validator = ResponseValidator(spec)

# Load response data
example_res_path = (
    "specification/components/examples/createReferral/responses/ReferralRequest.json"
)
with open(example_res_path, "r") as example_file:
    example_res_dict = load(example_file)

# Build openAPI response
oapi_res = OpenAPIResponse(
    data=example_res_dict, status_code=201, mimetype="application/fhir+json",
)

# Validate response
"""
The equivalent of the comment on ._validate_body()
 applies to this method
"""
result = res_validator._validate_data(oapi_req, oapi_res)

# Raise errors if response invalid
try:
    result.raise_for_errors()
except Exception as e:
    print("Response not valid.")
    print(e)
else:
    print("Response is valid.")
