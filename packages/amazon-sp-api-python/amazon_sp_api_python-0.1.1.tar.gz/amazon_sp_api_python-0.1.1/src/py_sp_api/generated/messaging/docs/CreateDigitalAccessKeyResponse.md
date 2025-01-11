# CreateDigitalAccessKeyResponse

The response schema for the `createDigitalAccessKey` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.messaging.models.create_digital_access_key_response import CreateDigitalAccessKeyResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CreateDigitalAccessKeyResponse from a JSON string
create_digital_access_key_response_instance = CreateDigitalAccessKeyResponse.from_json(json)
# print the JSON string representation of the object
print(CreateDigitalAccessKeyResponse.to_json())

# convert the object into a dict
create_digital_access_key_response_dict = create_digital_access_key_response_instance.to_dict()
# create an instance of CreateDigitalAccessKeyResponse from a dict
create_digital_access_key_response_from_dict = CreateDigitalAccessKeyResponse.from_dict(create_digital_access_key_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


