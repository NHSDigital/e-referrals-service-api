provider "apigee" {
  org          = var.apigee_organization
  access_token = var.apigee_token
}

terraform {
  backend "azurerm" {}

  required_providers {
    apigee = "~> 0.0"
    archive = "~> 1.3"
  }
}


module "e-referrals-service-api" {
  source                   = "github.com/NHSDigital/api-platform-service-module"
  name                     = "e-referrals-service-api"
  path                     = "referrals"
  apigee_environment       = var.apigee_environment
  proxy_type               = (var.force_sandbox || length(regexall("sandbox", var.apigee_environment)) > 0) ? "sandbox" : "live"
  namespace                = var.namespace
  make_api_product         = !(length(regexall("sandbox", var.apigee_environment)) > 0)
  api_product_display_name = length(var.namespace) > 0 ? "e-referrals-service-api${var.namespace}" : "e-Referrals-Service"
  api_product_description  = "The NHS e-RS vision is to enable local innovation and adoption of paperless referrals. To support this vision NHS Digital have created a set of APIs which provide a well-defined, simple to use data interface to the NHS e-Referral Service (e-RS). See https://developer.nhs.uk/apis/e-Referrals/index.html"
}
