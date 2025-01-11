# OrderAcknowledgement

Represents an acknowledgement for an order, including the purchase order number, selling party details, acknowledgement date, and a list of acknowledged items.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**purchase_order_number** | **str** | The purchase order number. Formatting Notes: 8-character alpha-numeric code. | 
**selling_party** | [**PartyIdentification**](PartyIdentification.md) |  | 
**acknowledgement_date** | **datetime** | The date and time when the purchase order is acknowledged, in ISO-8601 date/time format. | 
**items** | [**List[OrderAcknowledgementItem]**](OrderAcknowledgementItem.md) | A list of the items being acknowledged with associated details. | 

## Example

```python
from py_sp_api.generated.vendorOrders.models.order_acknowledgement import OrderAcknowledgement

# TODO update the JSON string below
json = "{}"
# create an instance of OrderAcknowledgement from a JSON string
order_acknowledgement_instance = OrderAcknowledgement.from_json(json)
# print the JSON string representation of the object
print(OrderAcknowledgement.to_json())

# convert the object into a dict
order_acknowledgement_dict = order_acknowledgement_instance.to_dict()
# create an instance of OrderAcknowledgement from a dict
order_acknowledgement_from_dict = OrderAcknowledgement.from_dict(order_acknowledgement_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


