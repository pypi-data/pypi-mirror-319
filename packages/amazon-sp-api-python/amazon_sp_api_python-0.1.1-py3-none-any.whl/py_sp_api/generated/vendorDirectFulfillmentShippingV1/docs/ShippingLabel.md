# ShippingLabel

Shipping label information for an order, including the purchase order number, selling party, ship from party, label format, and package details.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**purchase_order_number** | **str** | This field will contain the Purchase Order Number for this order. | 
**selling_party** | [**PartyIdentification**](PartyIdentification.md) |  | 
**ship_from_party** | [**PartyIdentification**](PartyIdentification.md) |  | 
**label_format** | **str** | Format of the label. | 
**label_data** | [**List[LabelData]**](LabelData.md) | Provides the details of the packages in this shipment. | 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentShippingV1.models.shipping_label import ShippingLabel

# TODO update the JSON string below
json = "{}"
# create an instance of ShippingLabel from a JSON string
shipping_label_instance = ShippingLabel.from_json(json)
# print the JSON string representation of the object
print(ShippingLabel.to_json())

# convert the object into a dict
shipping_label_dict = shipping_label_instance.to_dict()
# create an instance of ShippingLabel from a dict
shipping_label_from_dict = ShippingLabel.from_dict(shipping_label_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


