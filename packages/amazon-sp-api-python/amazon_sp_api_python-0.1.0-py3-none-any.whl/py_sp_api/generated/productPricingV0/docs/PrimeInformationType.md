# PrimeInformationType

Amazon Prime information.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**is_prime** | **bool** | Indicates whether the offer is an Amazon Prime offer. | 
**is_national_prime** | **bool** | Indicates whether the offer is an Amazon Prime offer throughout the entire marketplace where it is listed. | 

## Example

```python
from py_sp_api.generated.productPricingV0.models.prime_information_type import PrimeInformationType

# TODO update the JSON string below
json = "{}"
# create an instance of PrimeInformationType from a JSON string
prime_information_type_instance = PrimeInformationType.from_json(json)
# print the JSON string representation of the object
print(PrimeInformationType.to_json())

# convert the object into a dict
prime_information_type_dict = prime_information_type_instance.to_dict()
# create an instance of PrimeInformationType from a dict
prime_information_type_from_dict = PrimeInformationType.from_dict(prime_information_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


