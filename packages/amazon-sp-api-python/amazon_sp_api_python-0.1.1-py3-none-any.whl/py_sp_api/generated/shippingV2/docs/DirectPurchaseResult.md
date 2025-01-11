# DirectPurchaseResult

The payload for the directPurchaseShipment operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**shipment_id** | **str** | The unique shipment identifier provided by a shipping service. | 
**package_document_detail_list** | [**List[PackageDocumentDetail]**](PackageDocumentDetail.md) | A list of post-purchase details about a package that will be shipped using a shipping service. | [optional] 

## Example

```python
from py_sp_api.generated.shippingV2.models.direct_purchase_result import DirectPurchaseResult

# TODO update the JSON string below
json = "{}"
# create an instance of DirectPurchaseResult from a JSON string
direct_purchase_result_instance = DirectPurchaseResult.from_json(json)
# print the JSON string representation of the object
print(DirectPurchaseResult.to_json())

# convert the object into a dict
direct_purchase_result_dict = direct_purchase_result_instance.to_dict()
# create an instance of DirectPurchaseResult from a dict
direct_purchase_result_from_dict = DirectPurchaseResult.from_dict(direct_purchase_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


