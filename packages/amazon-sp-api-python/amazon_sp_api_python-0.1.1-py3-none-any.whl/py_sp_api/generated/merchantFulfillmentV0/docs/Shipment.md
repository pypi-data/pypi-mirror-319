# Shipment

The details of a shipment. Includes the shipment status.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**shipment_id** | **str** | An Amazon-defined shipment identifier. | 
**amazon_order_id** | **str** | An Amazon-defined order identifier, in 3-7-7 format. | 
**seller_order_id** | **str** | A seller-defined order identifier. | [optional] 
**item_list** | [**List[Item]**](Item.md) | The list of items you want to include in a shipment. | 
**ship_from_address** | [**Address**](Address.md) |  | 
**ship_to_address** | [**Address**](Address.md) |  | 
**package_dimensions** | [**PackageDimensions**](PackageDimensions.md) |  | 
**weight** | [**Weight**](Weight.md) |  | 
**insurance** | [**CurrencyAmount**](CurrencyAmount.md) |  | 
**shipping_service** | [**ShippingService**](ShippingService.md) |  | 
**label** | [**Label**](Label.md) |  | 
**status** | [**ShipmentStatus**](ShipmentStatus.md) |  | 
**tracking_id** | **str** | The shipment tracking identifier provided by the carrier. | [optional] 
**created_date** | **datetime** | Date-time formatted timestamp. | 
**last_updated_date** | **datetime** | Date-time formatted timestamp. | [optional] 

## Example

```python
from py_sp_api.generated.merchantFulfillmentV0.models.shipment import Shipment

# TODO update the JSON string below
json = "{}"
# create an instance of Shipment from a JSON string
shipment_instance = Shipment.from_json(json)
# print the JSON string representation of the object
print(Shipment.to_json())

# convert the object into a dict
shipment_dict = shipment_instance.to_dict()
# create an instance of Shipment from a dict
shipment_from_dict = Shipment.from_dict(shipment_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


