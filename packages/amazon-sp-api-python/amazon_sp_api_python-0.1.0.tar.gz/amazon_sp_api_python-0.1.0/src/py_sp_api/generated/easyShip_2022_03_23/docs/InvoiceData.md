# InvoiceData

Invoice number and date.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**invoice_number** | **str** | A string of up to 255 characters. | 
**invoice_date** | **datetime** | A datetime value in ISO 8601 format. | [optional] 

## Example

```python
from py_sp_api.generated.easyShip_2022_03_23.models.invoice_data import InvoiceData

# TODO update the JSON string below
json = "{}"
# create an instance of InvoiceData from a JSON string
invoice_data_instance = InvoiceData.from_json(json)
# print the JSON string representation of the object
print(InvoiceData.to_json())

# convert the object into a dict
invoice_data_dict = invoice_data_instance.to_dict()
# create an instance of InvoiceData from a dict
invoice_data_from_dict = InvoiceData.from_dict(invoice_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


