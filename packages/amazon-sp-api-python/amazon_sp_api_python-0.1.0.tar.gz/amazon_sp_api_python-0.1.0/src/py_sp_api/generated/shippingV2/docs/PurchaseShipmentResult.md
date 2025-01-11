# PurchaseShipmentResult

The payload for the purchaseShipment operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**shipment_id** | **str** | The unique shipment identifier provided by a shipping service. | 
**package_document_details** | [**List[PackageDocumentDetail]**](PackageDocumentDetail.md) | A list of post-purchase details about a package that will be shipped using a shipping service. | 
**promise** | [**Promise**](Promise.md) |  | 

## Example

```python
from py_sp_api.generated.shippingV2.models.purchase_shipment_result import PurchaseShipmentResult

# TODO update the JSON string below
json = "{}"
# create an instance of PurchaseShipmentResult from a JSON string
purchase_shipment_result_instance = PurchaseShipmentResult.from_json(json)
# print the JSON string representation of the object
print(PurchaseShipmentResult.to_json())

# convert the object into a dict
purchase_shipment_result_dict = purchase_shipment_result_instance.to_dict()
# create an instance of PurchaseShipmentResult from a dict
purchase_shipment_result_from_dict = PurchaseShipmentResult.from_dict(purchase_shipment_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


