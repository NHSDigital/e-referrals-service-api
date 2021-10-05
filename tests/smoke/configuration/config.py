from .environment import ENV

# API Details
ENVIRONMENT = ENV["environment"]
BASE_URL = f"https://{ENVIRONMENT}.api.service.nhs.uk"
STATUS_ENDPOINT_API_KEY = ENV["status_endpoint_api_key"]

# e-RS
ERS_BASE_PATH = ENV["ers_base_path"]
