# UpdateFulfillmentOrderRequest

The request body schema for the `updateFulfillmentOrder` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**marketplace_id** | **str** | The marketplace the fulfillment order is placed against. | [optional] 
**displayable_order_id** | **str** | A fulfillment order identifier that the seller creates. This value displays as the order identifier in recipient-facing materials such as the outbound shipment packing slip. The value of &#x60;DisplayableOrderId&#x60; should match the order identifier that the seller provides to the recipient. The seller can use the &#x60;SellerFulfillmentOrderId&#x60; for this value or they can specify an alternate value if they want the recipient to reference an alternate order identifier. | [optional] 
**displayable_order_date** | **datetime** | Date timestamp | [optional] 
**displayable_order_comment** | **str** | Order-specific text that appears in recipient-facing materials such as the outbound shipment packing slip. | [optional] 
**shipping_speed_category** | [**ShippingSpeedCategory**](ShippingSpeedCategory.md) |  | [optional] 
**destination_address** | [**Address**](Address.md) |  | [optional] 
**fulfillment_action** | [**FulfillmentAction**](FulfillmentAction.md) |  | [optional] 
**fulfillment_policy** | [**FulfillmentPolicy**](FulfillmentPolicy.md) |  | [optional] 
**ship_from_country_code** | **str** | The two-character country code for the country from which the fulfillment order ships. Must be in ISO 3166-1 alpha-2 format. | [optional] 
**notification_emails** | **List[str]** | A list of email addresses that the seller provides that are used by Amazon to send ship-complete notifications to recipients on behalf of the seller. | [optional] 
**feature_constraints** | [**List[FeatureSettings]**](FeatureSettings.md) | A list of features and their fulfillment policies to apply to the order. | [optional] 
**items** | [**List[UpdateFulfillmentOrderItem]**](UpdateFulfillmentOrderItem.md) | An array of fulfillment order item information for updating a fulfillment order. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentOutbound_2020_07_01.models.update_fulfillment_order_request import UpdateFulfillmentOrderRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateFulfillmentOrderRequest from a JSON string
update_fulfillment_order_request_instance = UpdateFulfillmentOrderRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateFulfillmentOrderRequest.to_json())

# convert the object into a dict
update_fulfillment_order_request_dict = update_fulfillment_order_request_instance.to_dict()
# create an instance of UpdateFulfillmentOrderRequest from a dict
update_fulfillment_order_request_from_dict = UpdateFulfillmentOrderRequest.from_dict(update_fulfillment_order_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


