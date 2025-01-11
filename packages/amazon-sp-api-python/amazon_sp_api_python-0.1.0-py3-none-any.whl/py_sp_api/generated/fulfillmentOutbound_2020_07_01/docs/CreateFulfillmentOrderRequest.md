# CreateFulfillmentOrderRequest

The request body schema for the `createFulfillmentOrder` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**marketplace_id** | **str** | The marketplace the fulfillment order is placed against. | [optional] 
**seller_fulfillment_order_id** | **str** | A fulfillment order identifier that the seller creates to track their fulfillment order. The &#x60;SellerFulfillmentOrderId&#x60; must be unique for each fulfillment order that a seller creates. If the seller&#39;s system already creates unique order identifiers, then these might be good values for them to use. | 
**displayable_order_id** | **str** | A fulfillment order identifier that the seller creates. This value displays as the order identifier in recipient-facing materials such as the outbound shipment packing slip. The value of &#x60;DisplayableOrderId&#x60; should match the order identifier that the seller provides to the recipient. The seller can use the &#x60;SellerFulfillmentOrderId&#x60; for this value or they can specify an alternate value if they want the recipient to reference an alternate order identifier.  The value must be an alpha-numeric or ISO 8859-1 compliant string from one to 40 characters in length. Cannot contain two spaces in a row. Leading and trailing white space is removed. | 
**displayable_order_date** | **datetime** | Date timestamp | 
**displayable_order_comment** | **str** | Order-specific text that appears in recipient-facing materials such as the outbound shipment packing slip. | 
**shipping_speed_category** | [**ShippingSpeedCategory**](ShippingSpeedCategory.md) |  | 
**delivery_window** | [**DeliveryWindow**](DeliveryWindow.md) |  | [optional] 
**destination_address** | [**Address**](Address.md) |  | 
**delivery_preferences** | [**DeliveryPreferences**](DeliveryPreferences.md) |  | [optional] 
**fulfillment_action** | [**FulfillmentAction**](FulfillmentAction.md) |  | [optional] 
**fulfillment_policy** | [**FulfillmentPolicy**](FulfillmentPolicy.md) |  | [optional] 
**cod_settings** | [**CODSettings**](CODSettings.md) |  | [optional] 
**ship_from_country_code** | **str** | The two-character country code for the country from which the fulfillment order ships. Must be in ISO 3166-1 alpha-2 format. | [optional] 
**notification_emails** | **List[str]** | A list of email addresses that the seller provides that are used by Amazon to send ship-complete notifications to recipients on behalf of the seller. | [optional] 
**feature_constraints** | [**List[FeatureSettings]**](FeatureSettings.md) | A list of features and their fulfillment policies to apply to the order. | [optional] 
**items** | [**List[CreateFulfillmentOrderItem]**](CreateFulfillmentOrderItem.md) | An array of item information for creating a fulfillment order. | 
**payment_information** | [**List[PaymentInformation]**](PaymentInformation.md) | An array of various payment attributes related to this fulfillment order. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentOutbound_2020_07_01.models.create_fulfillment_order_request import CreateFulfillmentOrderRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateFulfillmentOrderRequest from a JSON string
create_fulfillment_order_request_instance = CreateFulfillmentOrderRequest.from_json(json)
# print the JSON string representation of the object
print(CreateFulfillmentOrderRequest.to_json())

# convert the object into a dict
create_fulfillment_order_request_dict = create_fulfillment_order_request_instance.to_dict()
# create an instance of CreateFulfillmentOrderRequest from a dict
create_fulfillment_order_request_from_dict = CreateFulfillmentOrderRequest.from_dict(create_fulfillment_order_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


