# CreateReportResult


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**report_id** | **str** | The identifier for the report. This identifier is unique only in combination with a seller ID. | 

## Example

```python
from py_sp_api.generated.reports_2020_09_04.models.create_report_result import CreateReportResult

# TODO update the JSON string below
json = "{}"
# create an instance of CreateReportResult from a JSON string
create_report_result_instance = CreateReportResult.from_json(json)
# print the JSON string representation of the object
print(CreateReportResult.to_json())

# convert the object into a dict
create_report_result_dict = create_report_result_instance.to_dict()
# create an instance of CreateReportResult from a dict
create_report_result_from_dict = CreateReportResult.from_dict(create_report_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


