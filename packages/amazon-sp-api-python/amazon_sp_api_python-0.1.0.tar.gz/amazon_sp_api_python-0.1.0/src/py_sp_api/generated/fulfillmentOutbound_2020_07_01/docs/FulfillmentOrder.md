# FulfillmentOrder

General information about a fulfillment order, including its status.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**seller_fulfillment_order_id** | **str** | The fulfillment order identifier submitted with the &#x60;createFulfillmentOrder&#x60; operation. | 
**marketplace_id** | **str** | The identifier for the marketplace the fulfillment order is placed against. | 
**displayable_order_id** | **str** | A fulfillment order identifier submitted with the &#x60;createFulfillmentOrder&#x60; operation. Displays as the order identifier in recipient-facing materials such as the packing slip. | 
**displayable_order_date** | **datetime** | Date timestamp | 
**displayable_order_comment** | **str** | A text block submitted with the &#x60;createFulfillmentOrder&#x60; operation. Displays in recipient-facing materials such as the packing slip. | 
**shipping_speed_category** | [**ShippingSpeedCategory**](ShippingSpeedCategory.md) |  | 
**delivery_window** | [**DeliveryWindow**](DeliveryWindow.md) |  | [optional] 
**destination_address** | [**Address**](Address.md) |  | 
**fulfillment_action** | [**FulfillmentAction**](FulfillmentAction.md) |  | [optional] 
**fulfillment_policy** | [**FulfillmentPolicy**](FulfillmentPolicy.md) |  | [optional] 
**cod_settings** | [**CODSettings**](CODSettings.md) |  | [optional] 
**received_date** | **datetime** | Date timestamp | 
**fulfillment_order_status** | [**FulfillmentOrderStatus**](FulfillmentOrderStatus.md) |  | 
**status_updated_date** | **datetime** | Date timestamp | 
**notification_emails** | **List[str]** | A list of email addresses that the seller provides that are used by Amazon to send ship-complete notifications to recipients on behalf of the seller. | [optional] 
**feature_constraints** | [**List[FeatureSettings]**](FeatureSettings.md) | A list of features and their fulfillment policies to apply to the order. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentOutbound_2020_07_01.models.fulfillment_order import FulfillmentOrder

# TODO update the JSON string below
json = "{}"
# create an instance of FulfillmentOrder from a JSON string
fulfillment_order_instance = FulfillmentOrder.from_json(json)
# print the JSON string representation of the object
print(FulfillmentOrder.to_json())

# convert the object into a dict
fulfillment_order_dict = fulfillment_order_instance.to_dict()
# create an instance of FulfillmentOrder from a dict
fulfillment_order_from_dict = FulfillmentOrder.from_dict(fulfillment_order_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


