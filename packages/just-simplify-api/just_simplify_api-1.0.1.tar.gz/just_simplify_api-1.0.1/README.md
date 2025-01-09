# Just Simplify API
Clean up your API function of tedious response and verification code. Make it easier to see what your API is doing and ensure consistency with all your responses!

## Verrify incomming body values
Verifying every value that comes with the request can be tedious and take up a lot of space in your code. Now you can verify all your incomming values with a single function! Heres how:
<br>
1. Create a bluprint of what kind of values your looking for. Here is an example of what that might look like:
  ```
  BODY_BLUEPRINT = {
    "email":    {"required":True, "type":"email"},
    "password": {"required":True, "type":"hash"},
    "address":  [{
        "required": True,
        "street1":  {"required":True,  "type":"string", "min_len":5,  "max_len":100},
        "street2":  {"required":False, "type":"string", "min_len":5,  "max_len":20},
        "city":     {"required":True,  "type":"string", "min_len":5,  "max_len":20},
        "state":    {"required":True,  "type":"selection", "options":["co", "id", "ut"]},
        "zip":      {"required":True,  "type":"zip code"}
    }],
    "details":  {"required":False, "type":"dictionary"}
  }
  ```
  <b>email</b>, <b>password</b>, and <b>details</b> are all examples of arguments with a single value. <b>address</b> is an example of an argument that can contain a list of values (`[{address1 details}, {address2 details}, etc...]`).
  <br>
  All listed items in the blueprint must contain the following keys:
  * <b>required: Boolean</b>
  Says if the that particular argument is required or optional.
  * <b>type: str</b>
  Specifies what type of value you are expecting the argument to be. Here is a list of types you can specify:
    * "email"
    * "hash"
    * "zip code"
    * "string" (optional "min_len" and "max_len" parameters can be added to limit the length of the string)
    * "number"
    * "list"
    * "dictionary"
    * "selection" (required "options" parameter to provide all the posiblities the value can be)
2. Run the verification process with `validator(args= request.json, scheme= BODY_BLUEPRINT)`. If the validation passes, nothing is returned. If it fails, a 400 failed response dictionary will be generated for you with helpfull details.
## Generate response
Its important to know the codes for specific return messages and to maintain a consistant return body so end users know what to look for each time. Here are the functions to do this for you:
* 200 Response (Success)
  * `success_200_response(code: int, result: dict) -> dict` both code and result are optional. <b>code</b> is if you want to overwrite the default 200, and <b>result</b> is a dictionary containing any information you want to provide the end user.
* 500 Response (Server Error)
  * `error_500_internal_server(exception: str) -> dict` Not only generates a server error, but prints/logs any internal notes that would be helpfull for understanding what happened. This message would be the <b>exeption</b> parameter.
* 400 Response (Bad Request)
  * `error_400_bad_request(err_type: str, **kwargs) -> dict` By default, this will generate a genaric "Bad Request" response. If an error type is provided, it will generate a response tied to that error. Here is a list of err_types you can give:
    * "Missing Parameters"
    * "Missing Headers"
    * "Invalid Values"
    * "Invalid Headers"
    * "Syntax Error"
    * "Missing Credentials"
    * "Invalid Credentials"
    * "Payment Required"
    * "Forbidden"
    * "Not Found"
    * "Method Not Allowed"
    * "Request Timeout"
    * "Unsupported Media Type"
  * <b>**kwargs</b> are any additional details you would like to provide the end user.
  
  
