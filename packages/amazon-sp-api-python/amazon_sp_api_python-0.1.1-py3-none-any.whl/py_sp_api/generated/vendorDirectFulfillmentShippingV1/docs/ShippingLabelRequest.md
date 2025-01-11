# ShippingLabelRequest

Represents the request payload for creating a shipping label, containing the purchase order number, selling party, ship from party, and a list of containers or packages in the shipment.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**purchase_order_number** | **str** | Purchase order number of the order for which to create a shipping label. | 
**selling_party** | [**PartyIdentification**](PartyIdentification.md) |  | 
**ship_from_party** | [**PartyIdentification**](PartyIdentification.md) |  | 
**containers** | [**List[Container]**](Container.md) | A list of the packages in this shipment. | [optional] 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentShippingV1.models.shipping_label_request import ShippingLabelRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ShippingLabelRequest from a JSON string
shipping_label_request_instance = ShippingLabelRequest.from_json(json)
# print the JSON string representation of the object
print(ShippingLabelRequest.to_json())

# convert the object into a dict
shipping_label_request_dict = shipping_label_request_instance.to_dict()
# create an instance of ShippingLabelRequest from a dict
shipping_label_request_from_dict = ShippingLabelRequest.from_dict(shipping_label_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


