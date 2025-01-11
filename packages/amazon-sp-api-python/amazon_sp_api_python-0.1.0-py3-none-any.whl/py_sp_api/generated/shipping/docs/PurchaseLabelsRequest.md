# PurchaseLabelsRequest

The request schema for the purchaseLabels operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**rate_id** | **str** | An identifier for the rating. | 
**label_specification** | [**LabelSpecification**](LabelSpecification.md) |  | 

## Example

```python
from py_sp_api.generated.shipping.models.purchase_labels_request import PurchaseLabelsRequest

# TODO update the JSON string below
json = "{}"
# create an instance of PurchaseLabelsRequest from a JSON string
purchase_labels_request_instance = PurchaseLabelsRequest.from_json(json)
# print the JSON string representation of the object
print(PurchaseLabelsRequest.to_json())

# convert the object into a dict
purchase_labels_request_dict = purchase_labels_request_instance.to_dict()
# create an instance of PurchaseLabelsRequest from a dict
purchase_labels_request_from_dict = PurchaseLabelsRequest.from_dict(purchase_labels_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


