# TaxCollection

Information about withheld taxes.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**model** | **str** | The tax collection model applied to the item. | [optional] 
**responsible_party** | **str** | The party responsible for withholding the taxes and remitting them to the taxing authority. | [optional] 

## Example

```python
from py_sp_api.generated.ordersV0.models.tax_collection import TaxCollection

# TODO update the JSON string below
json = "{}"
# create an instance of TaxCollection from a JSON string
tax_collection_instance = TaxCollection.from_json(json)
# print the JSON string representation of the object
print(TaxCollection.to_json())

# convert the object into a dict
tax_collection_dict = tax_collection_instance.to_dict()
# create an instance of TaxCollection from a dict
tax_collection_from_dict = TaxCollection.from_dict(tax_collection_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


