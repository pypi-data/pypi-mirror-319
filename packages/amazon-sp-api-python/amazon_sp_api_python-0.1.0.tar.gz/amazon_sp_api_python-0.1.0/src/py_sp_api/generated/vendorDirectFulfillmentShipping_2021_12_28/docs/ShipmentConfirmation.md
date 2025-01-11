# ShipmentConfirmation

Represents the confirmation details of a shipment, including the purchase order number and other shipment details.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**purchase_order_number** | **str** | Purchase order number corresponding to the shipment. | 
**shipment_details** | [**ShipmentDetails**](ShipmentDetails.md) |  | 
**selling_party** | [**PartyIdentification**](PartyIdentification.md) |  | 
**ship_from_party** | [**PartyIdentification**](PartyIdentification.md) |  | 
**items** | [**List[Item]**](Item.md) | Provide the details of the items in this shipment. If any of the item details field is common at a package or a pallet level, then provide them at the corresponding package. | 
**containers** | [**List[Container]**](Container.md) | Provide the details of the items in this shipment. If any of the item details field is common at a package or a pallet level, then provide them at the corresponding package. | [optional] 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentShipping_2021_12_28.models.shipment_confirmation import ShipmentConfirmation

# TODO update the JSON string below
json = "{}"
# create an instance of ShipmentConfirmation from a JSON string
shipment_confirmation_instance = ShipmentConfirmation.from_json(json)
# print the JSON string representation of the object
print(ShipmentConfirmation.to_json())

# convert the object into a dict
shipment_confirmation_dict = shipment_confirmation_instance.to_dict()
# create an instance of ShipmentConfirmation from a dict
shipment_confirmation_from_dict = ShipmentConfirmation.from_dict(shipment_confirmation_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


