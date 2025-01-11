# AllowanceDetails

Monetary and tax details of the allowance.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** | Type of the allowance applied. | 
**description** | **str** | Description of the allowance. | [optional] 
**allowance_amount** | [**Money**](Money.md) |  | 
**tax_details** | [**List[TaxDetails]**](TaxDetails.md) | Tax amount details applied on this allowance. | [optional] 

## Example

```python
from py_sp_api.generated.vendorInvoices.models.allowance_details import AllowanceDetails

# TODO update the JSON string below
json = "{}"
# create an instance of AllowanceDetails from a JSON string
allowance_details_instance = AllowanceDetails.from_json(json)
# print the JSON string representation of the object
print(AllowanceDetails.to_json())

# convert the object into a dict
allowance_details_dict = allowance_details_instance.to_dict()
# create an instance of AllowanceDetails from a dict
allowance_details_from_dict = AllowanceDetails.from_dict(allowance_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


