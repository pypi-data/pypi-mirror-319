# PrimeDetails

Amazon Prime details.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**eligibility** | **str** | Indicates whether the offer is an Amazon Prime offer. | 

## Example

```python
from py_sp_api.generated.productPricing_2022_05_01.models.prime_details import PrimeDetails

# TODO update the JSON string below
json = "{}"
# create an instance of PrimeDetails from a JSON string
prime_details_instance = PrimeDetails.from_json(json)
# print the JSON string representation of the object
print(PrimeDetails.to_json())

# convert the object into a dict
prime_details_dict = prime_details_instance.to_dict()
# create an instance of PrimeDetails from a dict
prime_details_from_dict = PrimeDetails.from_dict(prime_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


