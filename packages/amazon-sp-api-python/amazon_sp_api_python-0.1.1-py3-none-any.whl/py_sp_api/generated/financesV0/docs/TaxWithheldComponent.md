# TaxWithheldComponent

Information about the taxes withheld.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**tax_collection_model** | **str** | The tax collection model applied to the item.  Possible values:  * MarketplaceFacilitator - Tax is withheld and remitted to the taxing authority by Amazon on behalf of the seller.  * Standard - Tax is paid to the seller and not remitted to the taxing authority by Amazon. | [optional] 
**taxes_withheld** | [**List[ChargeComponent]**](ChargeComponent.md) | A list of charge information on the seller&#39;s account. | [optional] 

## Example

```python
from py_sp_api.generated.financesV0.models.tax_withheld_component import TaxWithheldComponent

# TODO update the JSON string below
json = "{}"
# create an instance of TaxWithheldComponent from a JSON string
tax_withheld_component_instance = TaxWithheldComponent.from_json(json)
# print the JSON string representation of the object
print(TaxWithheldComponent.to_json())

# convert the object into a dict
tax_withheld_component_dict = tax_withheld_component_instance.to_dict()
# create an instance of TaxWithheldComponent from a dict
tax_withheld_component_from_dict = TaxWithheldComponent.from_dict(tax_withheld_component_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


