# PurchaseLabelsResponse

The response schema for the purchaseLabels operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**PurchaseLabelsResult**](PurchaseLabelsResult.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.shipping.models.purchase_labels_response import PurchaseLabelsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of PurchaseLabelsResponse from a JSON string
purchase_labels_response_instance = PurchaseLabelsResponse.from_json(json)
# print the JSON string representation of the object
print(PurchaseLabelsResponse.to_json())

# convert the object into a dict
purchase_labels_response_dict = purchase_labels_response_instance.to_dict()
# create an instance of PurchaseLabelsResponse from a dict
purchase_labels_response_from_dict = PurchaseLabelsResponse.from_dict(purchase_labels_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


