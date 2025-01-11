# GetPackingSlipResponse

Response payload with packing slip.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**PackingSlip**](PackingSlip.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentShippingV1.models.get_packing_slip_response import GetPackingSlipResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetPackingSlipResponse from a JSON string
get_packing_slip_response_instance = GetPackingSlipResponse.from_json(json)
# print the JSON string representation of the object
print(GetPackingSlipResponse.to_json())

# convert the object into a dict
get_packing_slip_response_dict = get_packing_slip_response_instance.to_dict()
# create an instance of GetPackingSlipResponse from a dict
get_packing_slip_response_from_dict = GetPackingSlipResponse.from_dict(get_packing_slip_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


