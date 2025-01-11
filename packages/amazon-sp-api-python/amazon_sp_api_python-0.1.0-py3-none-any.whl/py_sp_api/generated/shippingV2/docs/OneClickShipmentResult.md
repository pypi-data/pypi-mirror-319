# OneClickShipmentResult

The payload for the OneClickShipment API.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**shipment_id** | **str** | The unique shipment identifier provided by a shipping service. | 
**package_document_details** | [**List[PackageDocumentDetail]**](PackageDocumentDetail.md) | A list of post-purchase details about a package that will be shipped using a shipping service. | 
**promise** | [**Promise**](Promise.md) |  | 
**carrier** | [**Carrier**](Carrier.md) |  | 
**service** | [**Service**](Service.md) |  | 
**total_charge** | [**Currency**](Currency.md) |  | 

## Example

```python
from py_sp_api.generated.shippingV2.models.one_click_shipment_result import OneClickShipmentResult

# TODO update the JSON string below
json = "{}"
# create an instance of OneClickShipmentResult from a JSON string
one_click_shipment_result_instance = OneClickShipmentResult.from_json(json)
# print the JSON string representation of the object
print(OneClickShipmentResult.to_json())

# convert the object into a dict
one_click_shipment_result_dict = one_click_shipment_result_instance.to_dict()
# create an instance of OneClickShipmentResult from a dict
one_click_shipment_result_from_dict = OneClickShipmentResult.from_dict(one_click_shipment_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


