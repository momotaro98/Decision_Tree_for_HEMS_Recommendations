# Decision_Tree_for_HEMS_Recommendations

This is repo for momotaro98's master degree research.

## Usage

```
pip install decision_tree_for_hems_recommendations
```


### Preparing

`start_train_dt`
`end_train_dt`
**`ac_logs_list`**
`target_season`
`target_hour`

#### `ac_logs_list`
`ac_logs_list`


### Getting IsDeliverContent Flag

```
from decision_tree_for_hems_recommendations import (
	SettingTempDT,
	TotalUsageDT,
	ChangeUsageDT,
)


settemp_DT = SettingTempDT(
	start_train_dt=start_train_dt,
	end_train_dt=end_train_dt,
	ac_logs_list=ac_logs_list,
	target_season=target_season,
	target_hour=target_hour,
)
# get Future is_flag
is_deliver_settemp_content_future = settemp_DT.ret_predicted_Y_int()
# get Past is_flag
target_date = datetime(2015, 12, 24).date()
is_deliver_settemp_content_past = settemp_DT.ret_predicted_Y_int(target_date)

totalusage_DT = TotalUsageDT(
	start_train_dt=start_train_dt,
	end_train_dt=end_train_dt,
	ac_logs_list=ac_logs_list,
	target_season=target_season,
	target_hour=target_hour,
)
# get Future is_flag
is_deliver_settemp_content_future = totalusage_DT.ret_predicted_Y_int()
# get Past is_flag
target_date = datetime(2015, 12, 24).date()
is_deliver_settemp_content_past = totalusage_DT.ret_predicted_Y_int(target_date)


changeusage_DT = ChangeUsageDT(
	start_train_dt=start_train_dt,
	end_train_dt=end_train_dt,
	ac_logs_list=ac_logs_list,
	target_season=target_season,
	target_hour=target_hour,
)
# get Future is_flag
is_deliver_settemp_content_future = changeusage_DT.ret_predicted_Y_int()
# get Past is_flag
target_date = datetime(2015, 12, 24).date()
is_deliver_settemp_content_past = changeusage_DT.ret_predicted_Y_int(target_date)
```
