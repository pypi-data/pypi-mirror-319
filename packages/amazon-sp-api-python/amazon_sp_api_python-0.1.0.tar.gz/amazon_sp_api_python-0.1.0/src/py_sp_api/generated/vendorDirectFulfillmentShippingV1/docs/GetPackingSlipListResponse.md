# GetPackingSlipListResponse

Response payload with the list of Packing Slips.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**PackingSlipList**](PackingSlipList.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentShippingV1.models.get_packing_slip_list_response import GetPackingSlipListResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetPackingSlipListResponse from a JSON string
get_packing_slip_list_response_instance = GetPackingSlipListResponse.from_json(json)
# print the JSON string representation of the object
print(GetPackingSlipListResponse.to_json())

# convert the object into a dict
get_packing_slip_list_response_dict = get_packing_slip_list_response_instance.to_dict()
# create an instance of GetPackingSlipListResponse from a dict
get_packing_slip_list_response_from_dict = GetPackingSlipListResponse.from_dict(get_packing_slip_list_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


