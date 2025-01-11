# SubmitInvoicesRequest

The request schema for the submitInvoices operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**invoices** | [**List[Invoice]**](Invoice.md) | An array of Invoice objects representing the invoices or credit notes to be submitted. | [optional] 

## Example

```python
from py_sp_api.generated.vendorInvoices.models.submit_invoices_request import SubmitInvoicesRequest

# TODO update the JSON string below
json = "{}"
# create an instance of SubmitInvoicesRequest from a JSON string
submit_invoices_request_instance = SubmitInvoicesRequest.from_json(json)
# print the JSON string representation of the object
print(SubmitInvoicesRequest.to_json())

# convert the object into a dict
submit_invoices_request_dict = submit_invoices_request_instance.to_dict()
# create an instance of SubmitInvoicesRequest from a dict
submit_invoices_request_from_dict = SubmitInvoicesRequest.from_dict(submit_invoices_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


