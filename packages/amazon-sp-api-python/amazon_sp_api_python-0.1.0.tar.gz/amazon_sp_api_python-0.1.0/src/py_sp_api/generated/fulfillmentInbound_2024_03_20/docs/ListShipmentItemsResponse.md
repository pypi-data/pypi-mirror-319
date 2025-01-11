# ListShipmentItemsResponse

The `listShipmentItems` response.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**items** | [**List[Item]**](Item.md) | The items in a shipment. | 
**pagination** | [**Pagination**](Pagination.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.list_shipment_items_response import ListShipmentItemsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ListShipmentItemsResponse from a JSON string
list_shipment_items_response_instance = ListShipmentItemsResponse.from_json(json)
# print the JSON string representation of the object
print(ListShipmentItemsResponse.to_json())

# convert the object into a dict
list_shipment_items_response_dict = list_shipment_items_response_instance.to_dict()
# create an instance of ListShipmentItemsResponse from a dict
list_shipment_items_response_from_dict = ListShipmentItemsResponse.from_dict(list_shipment_items_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


