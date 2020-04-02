
def validate_response(response, acceptable_codes=None):
    if acceptable_codes is None:
        acceptable_codes = [200]
    if response.status_code not in acceptable_codes:
        raise Exception("HTTP Request failure. URL: [%s] Code: [%d]" % (response.url, response.status_code))
    return response
