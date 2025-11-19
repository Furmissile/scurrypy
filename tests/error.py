from scurrypy.core.error import DiscordError

e = DiscordError(400, {
  "code": 50035,
  "errors": {
    "activities": {
      "0": {
        "platform": {
          "_errors": [
            {
              "code": "BASE_TYPE_CHOICES",
              "message": "Value must be one of ('desktop', 'android', 'ios')."
            }
          ]
        },
        "type": {
          "_errors": [
            {
              "code": "BASE_TYPE_CHOICES",
              "message": "Value must be one of (0, 1, 2, 3, 4, 5)."
            }
          ]
        }
      }
    }
  },
  "message": "Invalid Form Body"
})

platform_error = e.error_data['activities']['0']['platform']['_errors'][0]
assert platform_error['code'] is not None
assert platform_error['message'] is not None

type_error = e.error_data['activities']['0']['type']['_errors'][0]
assert type_error['code'] is not None
assert type_error['message'] is not None

print(e)
