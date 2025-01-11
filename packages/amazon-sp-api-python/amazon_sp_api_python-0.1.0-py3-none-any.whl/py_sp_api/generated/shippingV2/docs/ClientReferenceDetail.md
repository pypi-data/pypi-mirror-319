# ClientReferenceDetail

Client Reference Details

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**client_reference_type** | **str** | Client Reference type. | 
**client_reference_id** | **str** | The Client Reference Id. | 

## Example

```python
from py_sp_api.generated.shippingV2.models.client_reference_detail import ClientReferenceDetail

# TODO update the JSON string below
json = "{}"
# create an instance of ClientReferenceDetail from a JSON string
client_reference_detail_instance = ClientReferenceDetail.from_json(json)
# print the JSON string representation of the object
print(ClientReferenceDetail.to_json())

# convert the object into a dict
client_reference_detail_dict = client_reference_detail_instance.to_dict()
# create an instance of ClientReferenceDetail from a dict
client_reference_detail_from_dict = ClientReferenceDetail.from_dict(client_reference_detail_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


