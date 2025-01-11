# ConfirmShipmentRequest

The request schema for an shipment confirmation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**package_detail** | [**PackageDetail**](PackageDetail.md) |  | 
**cod_collection_method** | **str** | The COD collection method (only supported in the JP marketplace). | [optional] 
**marketplace_id** | **str** | The unobfuscated marketplace identifier. | 

## Example

```python
from py_sp_api.generated.ordersV0.models.confirm_shipment_request import ConfirmShipmentRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ConfirmShipmentRequest from a JSON string
confirm_shipment_request_instance = ConfirmShipmentRequest.from_json(json)
# print the JSON string representation of the object
print(ConfirmShipmentRequest.to_json())

# convert the object into a dict
confirm_shipment_request_dict = confirm_shipment_request_instance.to_dict()
# create an instance of ConfirmShipmentRequest from a dict
confirm_shipment_request_from_dict = ConfirmShipmentRequest.from_dict(confirm_shipment_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


