# OrderAcknowledgementItem

Details of an individual order being acknowledged.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**purchase_order_number** | **str** | The purchase order number for this order. Formatting Notes: alpha-numeric code. | 
**vendor_order_number** | **str** | The vendor&#39;s order number for this order. | 
**acknowledgement_date** | **datetime** | The date and time when the order is acknowledged, in ISO-8601 date/time format. For example: 2018-07-16T23:00:00Z / 2018-07-16T23:00:00-05:00 / 2018-07-16T23:00:00-08:00. | 
**acknowledgement_status** | [**AcknowledgementStatus**](AcknowledgementStatus.md) |  | 
**selling_party** | [**PartyIdentification**](PartyIdentification.md) |  | 
**ship_from_party** | [**PartyIdentification**](PartyIdentification.md) |  | 
**item_acknowledgements** | [**List[OrderItemAcknowledgement]**](OrderItemAcknowledgement.md) | Item details including acknowledged quantity. | 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentOrdersV1.models.order_acknowledgement_item import OrderAcknowledgementItem

# TODO update the JSON string below
json = "{}"
# create an instance of OrderAcknowledgementItem from a JSON string
order_acknowledgement_item_instance = OrderAcknowledgementItem.from_json(json)
# print the JSON string representation of the object
print(OrderAcknowledgementItem.to_json())

# convert the object into a dict
order_acknowledgement_item_dict = order_acknowledgement_item_instance.to_dict()
# create an instance of OrderAcknowledgementItem from a dict
order_acknowledgement_item_from_dict = OrderAcknowledgementItem.from_dict(order_acknowledgement_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


