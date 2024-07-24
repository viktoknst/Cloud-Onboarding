This document describes the requirements the product should cover - functional and technical, with levels of need (MUST - the product is not considered functional if these are not met, SHOULD - the product can function without these requirements, NICE-TO - possible future editions)
## Functional requirements
MUST - The ability to CRUD user profiles via HTTP.

MUST - The ability to CRUD and execute projects...
NICE-TO - ...in different languages (provided by the service instance), with said projects being owned by different users.
MUST - At least one language should be supported
MUST - The ability to get results from specific execution instances.

## Technical requirements
MUST - Be responsive. Requests shouldn't hang.

SHOULD - Minimize system resource usage via timeouts/code validation.

SHOULD - Authenticate users and deny un-authorized access to resources.

NICE-TO - Use HTTP hooks on completion.

NICE-TO - Return metadata, have useful/consistent msg responces.
