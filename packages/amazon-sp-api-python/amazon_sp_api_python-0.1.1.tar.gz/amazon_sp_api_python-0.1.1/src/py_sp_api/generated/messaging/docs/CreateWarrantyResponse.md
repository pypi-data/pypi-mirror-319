# CreateWarrantyResponse

The response schema for the createWarranty operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.messaging.models.create_warranty_response import CreateWarrantyResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CreateWarrantyResponse from a JSON string
create_warranty_response_instance = CreateWarrantyResponse.from_json(json)
# print the JSON string representation of the object
print(CreateWarrantyResponse.to_json())

# convert the object into a dict
create_warranty_response_dict = create_warranty_response_instance.to_dict()
# create an instance of CreateWarrantyResponse from a dict
create_warranty_response_from_dict = CreateWarrantyResponse.from_dict(create_warranty_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


