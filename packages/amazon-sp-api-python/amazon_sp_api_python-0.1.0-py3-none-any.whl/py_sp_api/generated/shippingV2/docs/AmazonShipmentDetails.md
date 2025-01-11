# AmazonShipmentDetails

Amazon shipment information.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**shipment_id** | **str** | This attribute is required only for a Direct Fulfillment shipment. This is the encrypted shipment ID. | 

## Example

```python
from py_sp_api.generated.shippingV2.models.amazon_shipment_details import AmazonShipmentDetails

# TODO update the JSON string below
json = "{}"
# create an instance of AmazonShipmentDetails from a JSON string
amazon_shipment_details_instance = AmazonShipmentDetails.from_json(json)
# print the JSON string representation of the object
print(AmazonShipmentDetails.to_json())

# convert the object into a dict
amazon_shipment_details_dict = amazon_shipment_details_instance.to_dict()
# create an instance of AmazonShipmentDetails from a dict
amazon_shipment_details_from_dict = AmazonShipmentDetails.from_dict(amazon_shipment_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


