# FeatureSettings

`FeatureSettings` allows users to apply fulfillment features to an order. To block an order from being shipped using Amazon Logistics (AMZL) and an AMZL tracking number, use `featureName` as `BLOCK_AMZL` and `featureFulfillmentPolicy` as `Required`. Blocking AMZL will incur an additional fee surcharge on your MCF orders and increase the risk of some of your orders being unfulfilled or delivered late if there are no alternative carriers available. Using `BLOCK_AMZL` in an order request will take precedence over your Seller Central account setting. To ship in non-Amazon branded packaging (blank boxes), use featureName `BLANK_BOX`.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**feature_name** | **str** | The name of the feature. | [optional] 
**feature_fulfillment_policy** | **str** | Specifies the policy to use when fulfilling an order. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentOutbound_2020_07_01.models.feature_settings import FeatureSettings

# TODO update the JSON string below
json = "{}"
# create an instance of FeatureSettings from a JSON string
feature_settings_instance = FeatureSettings.from_json(json)
# print the JSON string representation of the object
print(FeatureSettings.to_json())

# convert the object into a dict
feature_settings_dict = feature_settings_instance.to_dict()
# create an instance of FeatureSettings from a dict
feature_settings_from_dict = FeatureSettings.from_dict(feature_settings_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


