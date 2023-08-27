from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


async def validation_exception_handler(request, exc):
    """
    Handle request validation errors by converting into a user-friendly error message.

    Note: without this, the returned error message is:
        [{'loc': ['query', 'weather'],
        'msg': "value is not a valid enumeration member;
        permitted: 'sun', 'rain', 'snow', 'cloudy', 'fog', 'drizzle'",
        'type': 'type_error.enum',
        'ctx': {'enum_values': ['sun', 'rain', 'snow', 'cloudy', 'fog', 'drizzle']}}]

    """
    details = exc.errors()
    user_friendly_errors = []
    for detail in details:
        msg = detail.get("msg")
        loc = " -> ".join(detail.get("loc"))
        if detail.get("type") == "type_error.enum":
            msg = f"Invalid value for {loc}. Allowed values are: {[v.value for v in detail['ctx']['enum_values']]}"
        user_friendly_errors.append(msg)
    return JSONResponse(content={"detail": user_friendly_errors}, status_code=400)
