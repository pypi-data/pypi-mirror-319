# GetFulfillmentOrderResult

The request for the getFulfillmentOrder operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**fulfillment_order** | [**FulfillmentOrder**](FulfillmentOrder.md) |  | 
**fulfillment_order_items** | [**List[FulfillmentOrderItem]**](FulfillmentOrderItem.md) | An array of fulfillment order item information. | 
**fulfillment_shipments** | [**List[FulfillmentShipment]**](FulfillmentShipment.md) | An array of fulfillment shipment information. | [optional] 
**return_items** | [**List[ReturnItem]**](ReturnItem.md) | An array of items that Amazon accepted for return. Returns empty if no items were accepted for return. | 
**return_authorizations** | [**List[ReturnAuthorization]**](ReturnAuthorization.md) | An array of return authorization information. | 
**payment_information** | [**List[PaymentInformation]**](PaymentInformation.md) | An array of various payment attributes related to this fulfillment order. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentOutbound_2020_07_01.models.get_fulfillment_order_result import GetFulfillmentOrderResult

# TODO update the JSON string below
json = "{}"
# create an instance of GetFulfillmentOrderResult from a JSON string
get_fulfillment_order_result_instance = GetFulfillmentOrderResult.from_json(json)
# print the JSON string representation of the object
print(GetFulfillmentOrderResult.to_json())

# convert the object into a dict
get_fulfillment_order_result_dict = get_fulfillment_order_result_instance.to_dict()
# create an instance of GetFulfillmentOrderResult from a dict
get_fulfillment_order_result_from_dict = GetFulfillmentOrderResult.from_dict(get_fulfillment_order_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


