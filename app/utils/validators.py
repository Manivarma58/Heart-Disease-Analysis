def valid_email(value):
    return "@" in value and "." in value.rsplit("@", 1)[-1]


def in_allowed(value, allowed):
    return value in allowed
