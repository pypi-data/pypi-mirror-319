# GetCollectionFormResponse

The Response  for the GetCollectionFormResponse operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**collections_form_document** | [**CollectionsFormDocument**](CollectionsFormDocument.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.shippingV2.models.get_collection_form_response import GetCollectionFormResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetCollectionFormResponse from a JSON string
get_collection_form_response_instance = GetCollectionFormResponse.from_json(json)
# print the JSON string representation of the object
print(GetCollectionFormResponse.to_json())

# convert the object into a dict
get_collection_form_response_dict = get_collection_form_response_instance.to_dict()
# create an instance of GetCollectionFormResponse from a dict
get_collection_form_response_from_dict = GetCollectionFormResponse.from_dict(get_collection_form_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


