# GetUnmanifestedShipmentsRequest

The request schema for the GetUnmanifestedShipmentsRequest operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**client_reference_details** | [**List[ClientReferenceDetail]**](ClientReferenceDetail.md) | Object to pass additional information about the MCI Integrator shipperType: List of ClientReferenceDetail | [optional] 

## Example

```python
from py_sp_api.generated.shippingV2.models.get_unmanifested_shipments_request import GetUnmanifestedShipmentsRequest

# TODO update the JSON string below
json = "{}"
# create an instance of GetUnmanifestedShipmentsRequest from a JSON string
get_unmanifested_shipments_request_instance = GetUnmanifestedShipmentsRequest.from_json(json)
# print the JSON string representation of the object
print(GetUnmanifestedShipmentsRequest.to_json())

# convert the object into a dict
get_unmanifested_shipments_request_dict = get_unmanifested_shipments_request_instance.to_dict()
# create an instance of GetUnmanifestedShipmentsRequest from a dict
get_unmanifested_shipments_request_from_dict = GetUnmanifestedShipmentsRequest.from_dict(get_unmanifested_shipments_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


