# OrderItemStatusAcknowledgementStatus

Acknowledgement status information.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**confirmation_status** | **str** | Confirmation status of line item. | [optional] 
**accepted_quantity** | [**ItemQuantity**](ItemQuantity.md) |  | [optional] 
**rejected_quantity** | [**ItemQuantity**](ItemQuantity.md) |  | [optional] 
**acknowledgement_status_details** | [**List[AcknowledgementStatusDetails]**](AcknowledgementStatusDetails.md) | Details of item quantity confirmed. | [optional] 

## Example

```python
from py_sp_api.generated.vendorOrders.models.order_item_status_acknowledgement_status import OrderItemStatusAcknowledgementStatus

# TODO update the JSON string below
json = "{}"
# create an instance of OrderItemStatusAcknowledgementStatus from a JSON string
order_item_status_acknowledgement_status_instance = OrderItemStatusAcknowledgementStatus.from_json(json)
# print the JSON string representation of the object
print(OrderItemStatusAcknowledgementStatus.to_json())

# convert the object into a dict
order_item_status_acknowledgement_status_dict = order_item_status_acknowledgement_status_instance.to_dict()
# create an instance of OrderItemStatusAcknowledgementStatus from a dict
order_item_status_acknowledgement_status_from_dict = OrderItemStatusAcknowledgementStatus.from_dict(order_item_status_acknowledgement_status_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


