# GetShipmentItemsResult

Result for the get shipment items operation

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**item_data** | [**List[InboundShipmentItem]**](InboundShipmentItem.md) | A list of inbound shipment item information. | [optional] 
**next_token** | **str** | When present and not empty, pass this string token in the next request to return the next response page. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInboundV0.models.get_shipment_items_result import GetShipmentItemsResult

# TODO update the JSON string below
json = "{}"
# create an instance of GetShipmentItemsResult from a JSON string
get_shipment_items_result_instance = GetShipmentItemsResult.from_json(json)
# print the JSON string representation of the object
print(GetShipmentItemsResult.to_json())

# convert the object into a dict
get_shipment_items_result_dict = get_shipment_items_result_instance.to_dict()
# create an instance of GetShipmentItemsResult from a dict
get_shipment_items_result_from_dict = GetShipmentItemsResult.from_dict(get_shipment_items_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


