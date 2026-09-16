# Changelog
## 15/09/2026
* A015 (Retrieve Appointment Slots): documented support for `SERVICE_PROVIDER_CLINICIAN` and `SERVICE_PROVIDER_CLINICIAN_ADMIN` roles.
* A015 - Enhanced ErrorOutcome.yaml with comprehensive error code documentation for retrieveAppointmentSlots
  - Documented error conditions for referral state validation (NOT_BOOKED, TRIAGE service checks)
  - Added response headers: X-Correlation-ID, X-Request-ID, Content-Type
  - Configured FHIR JSON error response schema with STU3-OperationOutcome reference
