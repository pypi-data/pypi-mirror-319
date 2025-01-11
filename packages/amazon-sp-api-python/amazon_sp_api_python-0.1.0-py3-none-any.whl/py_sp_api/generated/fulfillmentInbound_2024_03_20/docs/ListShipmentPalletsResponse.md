# ListShipmentPalletsResponse

The `listShipmentPallets` response.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pagination** | [**Pagination**](Pagination.md) |  | [optional] 
**pallets** | [**List[Pallet]**](Pallet.md) | The pallets in a shipment. | 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.list_shipment_pallets_response import ListShipmentPalletsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ListShipmentPalletsResponse from a JSON string
list_shipment_pallets_response_instance = ListShipmentPalletsResponse.from_json(json)
# print the JSON string representation of the object
print(ListShipmentPalletsResponse.to_json())

# convert the object into a dict
list_shipment_pallets_response_dict = list_shipment_pallets_response_instance.to_dict()
# create an instance of ListShipmentPalletsResponse from a dict
list_shipment_pallets_response_from_dict = ListShipmentPalletsResponse.from_dict(list_shipment_pallets_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


