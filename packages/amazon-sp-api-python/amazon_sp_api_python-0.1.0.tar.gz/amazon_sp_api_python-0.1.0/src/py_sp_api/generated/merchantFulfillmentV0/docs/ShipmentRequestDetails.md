# ShipmentRequestDetails

Shipment information required for requesting shipping service offers or for creating a shipment.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**amazon_order_id** | **str** | An Amazon-defined order identifier, in 3-7-7 format. | 
**seller_order_id** | **str** | A seller-defined order identifier. | [optional] 
**item_list** | [**List[Item]**](Item.md) | The list of items you want to include in a shipment. | 
**ship_from_address** | [**Address**](Address.md) |  | 
**package_dimensions** | [**PackageDimensions**](PackageDimensions.md) |  | 
**weight** | [**Weight**](Weight.md) |  | 
**must_arrive_by_date** | **datetime** | Date-time formatted timestamp. | [optional] 
**ship_date** | **datetime** | Date-time formatted timestamp. | [optional] 
**shipping_service_options** | [**ShippingServiceOptions**](ShippingServiceOptions.md) |  | 
**label_customization** | [**LabelCustomization**](LabelCustomization.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.merchantFulfillmentV0.models.shipment_request_details import ShipmentRequestDetails

# TODO update the JSON string below
json = "{}"
# create an instance of ShipmentRequestDetails from a JSON string
shipment_request_details_instance = ShipmentRequestDetails.from_json(json)
# print the JSON string representation of the object
print(ShipmentRequestDetails.to_json())

# convert the object into a dict
shipment_request_details_dict = shipment_request_details_instance.to_dict()
# create an instance of ShipmentRequestDetails from a dict
shipment_request_details_from_dict = ShipmentRequestDetails.from_dict(shipment_request_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


