# ChannelDetails

Shipment source channel related information.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**channel_type** | [**ChannelType**](ChannelType.md) |  | 
**amazon_order_details** | [**AmazonOrderDetails**](AmazonOrderDetails.md) |  | [optional] 
**amazon_shipment_details** | [**AmazonShipmentDetails**](AmazonShipmentDetails.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.shippingV2.models.channel_details import ChannelDetails

# TODO update the JSON string below
json = "{}"
# create an instance of ChannelDetails from a JSON string
channel_details_instance = ChannelDetails.from_json(json)
# print the JSON string representation of the object
print(ChannelDetails.to_json())

# convert the object into a dict
channel_details_dict = channel_details_instance.to_dict()
# create an instance of ChannelDetails from a dict
channel_details_from_dict = ChannelDetails.from_dict(channel_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


