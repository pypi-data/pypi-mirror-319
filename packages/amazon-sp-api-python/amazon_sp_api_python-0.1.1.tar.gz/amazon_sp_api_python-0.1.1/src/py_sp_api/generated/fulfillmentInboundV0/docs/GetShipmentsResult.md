# GetShipmentsResult

Result for the get shipments operation

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**shipment_data** | [**List[InboundShipmentInfo]**](InboundShipmentInfo.md) | A list of inbound shipment information. | [optional] 
**next_token** | **str** | When present and not empty, pass this string token in the next request to return the next response page. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInboundV0.models.get_shipments_result import GetShipmentsResult

# TODO update the JSON string below
json = "{}"
# create an instance of GetShipmentsResult from a JSON string
get_shipments_result_instance = GetShipmentsResult.from_json(json)
# print the JSON string representation of the object
print(GetShipmentsResult.to_json())

# convert the object into a dict
get_shipments_result_dict = get_shipments_result_instance.to_dict()
# create an instance of GetShipmentsResult from a dict
get_shipments_result_from_dict = GetShipmentsResult.from_dict(get_shipments_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


