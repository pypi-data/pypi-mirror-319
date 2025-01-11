# SAFETReimbursementItem

An item from a SAFE-T claim reimbursement.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**item_charge_list** | [**List[ChargeComponent]**](ChargeComponent.md) | A list of charge information on the seller&#39;s account. | [optional] 
**product_description** | **str** | The description of the item as shown on the product detail page on the retail website. | [optional] 
**quantity** | **str** | The number of units of the item being reimbursed. | [optional] 

## Example

```python
from py_sp_api.generated.financesV0.models.safet_reimbursement_item import SAFETReimbursementItem

# TODO update the JSON string below
json = "{}"
# create an instance of SAFETReimbursementItem from a JSON string
safet_reimbursement_item_instance = SAFETReimbursementItem.from_json(json)
# print the JSON string representation of the object
print(SAFETReimbursementItem.to_json())

# convert the object into a dict
safet_reimbursement_item_dict = safet_reimbursement_item_instance.to_dict()
# create an instance of SAFETReimbursementItem from a dict
safet_reimbursement_item_from_dict = SAFETReimbursementItem.from_dict(safet_reimbursement_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


