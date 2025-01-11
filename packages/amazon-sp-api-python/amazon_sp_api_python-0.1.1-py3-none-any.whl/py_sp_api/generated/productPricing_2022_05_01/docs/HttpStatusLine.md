# HttpStatusLine

The HTTP status line associated with the response for an individual request within a batch. For more information, refer to [RFC 2616](https://www.w3.org/Protocols/rfc2616/rfc2616-sec6.html).

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status_code** | **int** | The HTTP response status code. | [optional] 
**reason_phrase** | **str** | The HTTP response reason phrase. | [optional] 

## Example

```python
from py_sp_api.generated.productPricing_2022_05_01.models.http_status_line import HttpStatusLine

# TODO update the JSON string below
json = "{}"
# create an instance of HttpStatusLine from a JSON string
http_status_line_instance = HttpStatusLine.from_json(json)
# print the JSON string representation of the object
print(HttpStatusLine.to_json())

# convert the object into a dict
http_status_line_dict = http_status_line_instance.to_dict()
# create an instance of HttpStatusLine from a dict
http_status_line_from_dict = HttpStatusLine.from_dict(http_status_line_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


