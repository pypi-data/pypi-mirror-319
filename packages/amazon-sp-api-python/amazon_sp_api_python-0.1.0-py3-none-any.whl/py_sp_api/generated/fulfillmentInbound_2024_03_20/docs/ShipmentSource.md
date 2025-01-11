# ShipmentSource

Specifies the 'ship from' address for the shipment.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**address** | [**Address**](Address.md) |  | [optional] 
**source_type** | **str** | The type of source for this shipment. Possible values: &#x60;SELLER_FACILITY&#x60;. | 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.shipment_source import ShipmentSource

# TODO update the JSON string below
json = "{}"
# create an instance of ShipmentSource from a JSON string
shipment_source_instance = ShipmentSource.from_json(json)
# print the JSON string representation of the object
print(ShipmentSource.to_json())

# convert the object into a dict
shipment_source_dict = shipment_source_instance.to_dict()
# create an instance of ShipmentSource from a dict
shipment_source_from_dict = ShipmentSource.from_dict(shipment_source_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


