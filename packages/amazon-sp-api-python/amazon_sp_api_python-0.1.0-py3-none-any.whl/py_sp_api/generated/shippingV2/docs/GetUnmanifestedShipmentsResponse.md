# GetUnmanifestedShipmentsResponse

The Response  for the GetUnmanifestedShipmentsResponse operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**unmanifested_carrier_information_list** | [**List[UnmanifestedCarrierInformation]**](UnmanifestedCarrierInformation.md) | A list of UnmanifestedCarrierInformation | [optional] 

## Example

```python
from py_sp_api.generated.shippingV2.models.get_unmanifested_shipments_response import GetUnmanifestedShipmentsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetUnmanifestedShipmentsResponse from a JSON string
get_unmanifested_shipments_response_instance = GetUnmanifestedShipmentsResponse.from_json(json)
# print the JSON string representation of the object
print(GetUnmanifestedShipmentsResponse.to_json())

# convert the object into a dict
get_unmanifested_shipments_response_dict = get_unmanifested_shipments_response_instance.to_dict()
# create an instance of GetUnmanifestedShipmentsResponse from a dict
get_unmanifested_shipments_response_from_dict = GetUnmanifestedShipmentsResponse.from_dict(get_unmanifested_shipments_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


