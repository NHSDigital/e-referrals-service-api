const proxy_path = context.getVariable('proxy.pathsuffix');
const regex_fhir_r4 = /.*\/FHIR\/R4\/.*/;
const regex_fhir_r4_v1 = /.*\/R4\/v1\/.*/;
const found_fhir_r4 = proxy_path.match(regex_fhir_r4);
const found_fhir_r4_v1 = proxy_path.match(regex_fhir_r4_v1);
const is_fhir_r4_path = (found_fhir_r4 || found_fhir_r4_v1) ? true : false;

context.setVariable("isFhirR4Path", is_fhir_r4_path);
