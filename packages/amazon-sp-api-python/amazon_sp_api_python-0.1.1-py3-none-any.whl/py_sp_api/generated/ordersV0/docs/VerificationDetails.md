# VerificationDetails

Additional information related to the verification of a regulated order.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**prescription_detail** | [**PrescriptionDetail**](PrescriptionDetail.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.ordersV0.models.verification_details import VerificationDetails

# TODO update the JSON string below
json = "{}"
# create an instance of VerificationDetails from a JSON string
verification_details_instance = VerificationDetails.from_json(json)
# print the JSON string representation of the object
print(VerificationDetails.to_json())

# convert the object into a dict
verification_details_dict = verification_details_instance.to_dict()
# create an instance of VerificationDetails from a dict
verification_details_from_dict = VerificationDetails.from_dict(verification_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


