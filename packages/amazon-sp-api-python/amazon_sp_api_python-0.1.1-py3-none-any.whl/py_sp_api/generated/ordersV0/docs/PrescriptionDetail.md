# PrescriptionDetail

Information about the prescription that is used to verify a regulated product. This must be provided once per order and reflect the seller’s own records. Only approved orders can have prescriptions.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**prescription_id** | **str** | The identifier for the prescription used to verify the regulated product. | 
**expiration_date** | **datetime** | The expiration date of the prescription used to verify the regulated product, in [ISO 8601](https://developer-docs.amazon.com/sp-api/docs/iso-8601) date time format. | 
**written_quantity** | **int** | The number of units in each fill as provided in the prescription. | 
**total_refills_authorized** | **int** | The total number of refills written in the original prescription used to verify the regulated product. If a prescription originally had no refills, this value must be 0. | 
**refills_remaining** | **int** | The number of refills remaining for the prescription used to verify the regulated product. If a prescription originally had 10 total refills, this value must be &#x60;10&#x60; for the first order, &#x60;9&#x60; for the second order, and &#x60;0&#x60; for the eleventh order. If a prescription originally had no refills, this value must be 0. | 
**clinic_id** | **str** | The identifier for the clinic which provided the prescription used to verify the regulated product. | 
**usage_instructions** | **str** | The instructions for the prescription as provided by the approver of the regulated product. | 

## Example

```python
from py_sp_api.generated.ordersV0.models.prescription_detail import PrescriptionDetail

# TODO update the JSON string below
json = "{}"
# create an instance of PrescriptionDetail from a JSON string
prescription_detail_instance = PrescriptionDetail.from_json(json)
# print the JSON string representation of the object
print(PrescriptionDetail.to_json())

# convert the object into a dict
prescription_detail_dict = prescription_detail_instance.to_dict()
# create an instance of PrescriptionDetail from a dict
prescription_detail_from_dict = PrescriptionDetail.from_dict(prescription_detail_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


