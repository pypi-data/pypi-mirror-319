# ShipmentDestination

The Amazon fulfillment center address and warehouse ID.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**address** | [**Address**](Address.md) |  | [optional] 
**destination_type** | **str** | The type of destination for this shipment. Possible values: &#x60;AMAZON_OPTIMIZED&#x60;, &#x60;AMAZON_WAREHOUSE&#x60;. | 
**warehouse_id** | **str** | The warehouse that the shipment should be sent to. Empty if the destination type is &#x60;AMAZON_OPTIMIZED&#x60;. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.shipment_destination import ShipmentDestination

# TODO update the JSON string below
json = "{}"
# create an instance of ShipmentDestination from a JSON string
shipment_destination_instance = ShipmentDestination.from_json(json)
# print the JSON string representation of the object
print(ShipmentDestination.to_json())

# convert the object into a dict
shipment_destination_dict = shipment_destination_instance.to_dict()
# create an instance of ShipmentDestination from a dict
shipment_destination_from_dict = ShipmentDestination.from_dict(shipment_destination_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


