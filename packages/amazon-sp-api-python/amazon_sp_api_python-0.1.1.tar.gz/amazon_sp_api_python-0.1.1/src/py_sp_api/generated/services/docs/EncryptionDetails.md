# EncryptionDetails

Encryption details for required client-side encryption and decryption of document contents.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**standard** | **str** | The encryption standard required to encrypt or decrypt the document contents. | 
**initialization_vector** | **str** | The vector to encrypt or decrypt the document contents using Cipher Block Chaining (CBC). | 
**key** | **str** | The encryption key used to encrypt or decrypt the document contents. | 

## Example

```python
from py_sp_api.generated.services.models.encryption_details import EncryptionDetails

# TODO update the JSON string below
json = "{}"
# create an instance of EncryptionDetails from a JSON string
encryption_details_instance = EncryptionDetails.from_json(json)
# print the JSON string representation of the object
print(EncryptionDetails.to_json())

# convert the object into a dict
encryption_details_dict = encryption_details_instance.to_dict()
# create an instance of EncryptionDetails from a dict
encryption_details_from_dict = EncryptionDetails.from_dict(encryption_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


