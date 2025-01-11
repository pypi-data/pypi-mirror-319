# CreateAmazonMotorsResponse

The response schema for the createAmazonMotors operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.messaging.models.create_amazon_motors_response import CreateAmazonMotorsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CreateAmazonMotorsResponse from a JSON string
create_amazon_motors_response_instance = CreateAmazonMotorsResponse.from_json(json)
# print the JSON string representation of the object
print(CreateAmazonMotorsResponse.to_json())

# convert the object into a dict
create_amazon_motors_response_dict = create_amazon_motors_response_instance.to_dict()
# create an instance of CreateAmazonMotorsResponse from a dict
create_amazon_motors_response_from_dict = CreateAmazonMotorsResponse.from_dict(create_amazon_motors_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


