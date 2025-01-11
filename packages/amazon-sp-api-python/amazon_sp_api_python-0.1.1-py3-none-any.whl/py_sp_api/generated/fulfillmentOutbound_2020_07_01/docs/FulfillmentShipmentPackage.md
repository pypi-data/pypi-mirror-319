# FulfillmentShipmentPackage

Package information for a shipment in a fulfillment order.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**package_number** | **int** | Identifies a package in a shipment. | 
**carrier_code** | **str** | Identifies the carrier who will deliver the shipment to the recipient. | 
**tracking_number** | **str** | The tracking number, if provided, can be used to obtain tracking and delivery information. | [optional] 
**estimated_arrival_date** | **datetime** | Date timestamp | [optional] 
**locker_details** | [**LockerDetails**](LockerDetails.md) |  | [optional] 
**delivery_information** | [**DeliveryInformation**](DeliveryInformation.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentOutbound_2020_07_01.models.fulfillment_shipment_package import FulfillmentShipmentPackage

# TODO update the JSON string below
json = "{}"
# create an instance of FulfillmentShipmentPackage from a JSON string
fulfillment_shipment_package_instance = FulfillmentShipmentPackage.from_json(json)
# print the JSON string representation of the object
print(FulfillmentShipmentPackage.to_json())

# convert the object into a dict
fulfillment_shipment_package_dict = fulfillment_shipment_package_instance.to_dict()
# create an instance of FulfillmentShipmentPackage from a dict
fulfillment_shipment_package_from_dict = FulfillmentShipmentPackage.from_dict(fulfillment_shipment_package_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


