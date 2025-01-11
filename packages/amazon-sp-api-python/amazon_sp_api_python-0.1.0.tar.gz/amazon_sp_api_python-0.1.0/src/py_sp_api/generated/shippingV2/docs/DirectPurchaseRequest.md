# DirectPurchaseRequest

The request schema for the directPurchaseShipment operation. When the channel type is Amazon, the shipTo address is not required and will be ignored.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**ship_to** | [**Address**](Address.md) |  | [optional] 
**ship_from** | [**Address**](Address.md) |  | [optional] 
**return_to** | [**Address**](Address.md) |  | [optional] 
**packages** | [**List[Package]**](Package.md) | A list of packages to be shipped through a shipping service offering. | [optional] 
**channel_details** | [**ChannelDetails**](ChannelDetails.md) |  | 
**label_specifications** | [**RequestedDocumentSpecification**](RequestedDocumentSpecification.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.shippingV2.models.direct_purchase_request import DirectPurchaseRequest

# TODO update the JSON string below
json = "{}"
# create an instance of DirectPurchaseRequest from a JSON string
direct_purchase_request_instance = DirectPurchaseRequest.from_json(json)
# print the JSON string representation of the object
print(DirectPurchaseRequest.to_json())

# convert the object into a dict
direct_purchase_request_dict = direct_purchase_request_instance.to_dict()
# create an instance of DirectPurchaseRequest from a dict
direct_purchase_request_from_dict = DirectPurchaseRequest.from_dict(direct_purchase_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


