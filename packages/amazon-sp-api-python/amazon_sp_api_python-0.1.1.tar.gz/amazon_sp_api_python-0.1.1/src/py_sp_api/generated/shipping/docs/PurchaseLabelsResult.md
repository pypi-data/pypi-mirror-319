# PurchaseLabelsResult

The payload schema for the purchaseLabels operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**shipment_id** | **str** | The unique shipment identifier. | 
**client_reference_id** | **str** | Client reference id. | [optional] 
**accepted_rate** | [**AcceptedRate**](AcceptedRate.md) |  | 
**label_results** | [**List[LabelResult]**](LabelResult.md) | A list of label results | 

## Example

```python
from py_sp_api.generated.shipping.models.purchase_labels_result import PurchaseLabelsResult

# TODO update the JSON string below
json = "{}"
# create an instance of PurchaseLabelsResult from a JSON string
purchase_labels_result_instance = PurchaseLabelsResult.from_json(json)
# print the JSON string representation of the object
print(PurchaseLabelsResult.to_json())

# convert the object into a dict
purchase_labels_result_dict = purchase_labels_result_instance.to_dict()
# create an instance of PurchaseLabelsResult from a dict
purchase_labels_result_from_dict = PurchaseLabelsResult.from_dict(purchase_labels_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


