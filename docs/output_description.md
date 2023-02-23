# Output data description to interpret the (raw) results of ARTEMIS

In this file the different outputs files are described and a legend is given for each column in the output
As of the version of 15 February 2022, running  `ARTEMIS.py` creates two raw data outputs:

- flat_time_x_environment_results<*scenario_name*>.csv
- flat_time_x_agent_results<*scenario_name*>.csv

By running `derive_statistics.py`, additional measures calculated from the raw data ARTEMIS generates, are calculated and combined with the raw data into:

- flat_time_x_environment_results_with_statistics_<*scenario_name*>.csv
- flat_time_x_agent_results_with_statistics_<*scenario_name*>.csv

alternatively by running `graphmaker.py` several graphs will be made: 

**WILL BE ADDED IN THE FUTURE:** GRAPHMAKER IS HIGHLY TAILORED AND NOT FLEXIBLE YET

Each of the above mentioned outputs is described in detail in the sections below.

## Raw Data (Direct outputs of running the model)
### flat_time_x_environment_results

| Column / Data Series Name | Description of Data |
| ----------- | ----------- |
|iteration_id|indicates what iteration of a scenario the data refers to |
|time_id|indicates with for what time step in the model the data is generated|
|alternative_id|indicates what alternative (e.g. Grid Cell) in the model the data is for|
|agents_visited|all agents (separated using vertical line) that visited a given alternative,for a given time and iteration|
|real_stock|resource stock present in a given alternative,for a given time and iteration|
|nb_agents_visited|number of agents that have visited a given alternative,for a given time and iteration|
|occurred_competition_correction|catch correction als a result of competition, caused by the amount of competitors each visiting agent has encountered (nb_agents_visited - 1), that is applied to any catch gained from a given alternative, for a given time and iteration|
|hypothetical_competition_correction|catch correction als a result of competition caused by the amount of competitors each visiting agent would've encountered, if a single extra competitor would have been present (nb_agents_visited - 1 + 1), that would have been applied to any catch gained from a given alternative, for a given time and iteration|
|<*agent_id*>_catch_expectation_heatmap|catch <*agent_id*> expected to gain according to their heatmap from a given alternative, for a given time and iteration|
|<*agent_id*>_catch_potential|catch <*agent_id*> would have achieved if it would have foraged, in the absence of competition, in a given alternative, for a given time and iteration|


### flat_time_x_agents_results

| Column / Data Series Name | Description of Data |
| ----------- | ----------- |
|iteration_id|indicates what iteration of a scenario the data refers to |
|time_id|indicates with for what time step in the model the data is generated|
|agent_id|indicates what agent in the model the data is for|
|group_allegiance|indicates, if agents only share information in groups, to what group the agent with agent_id belongs for a given agent, time and iteration|
|forage_visit|what alternative (e.g. Grid Cell) the agent has foraged in for a given agent, time and iteration|
|average_expected_competitors|theoretical measure that determines the average amount of competitors expected to encounter (based on the information comtained in all agens' heatmaps on average over all grid cells for a given agent, time and iteration|
|realised_competition|competition encountered in the alternative indicated in forage_visit for a given agent, time and iteration|
|knowledge_in_heatmap|number of entries in the heatmap that an agent has some catch expectation for, for a given agent, time and iteration|
|heatmap_expected_catch|catch that an agent was expecting to gain in the alternative indicated in forage_visit, according to its heatmap for a given agent, time and iteration|
|uncorrected_catch|catch that an agent would have gotten from the alternative indicated in forage_visit, if no competitors would have been present for a given agent, time and iteration|
|realised_catch|actual catch gained by foraging in the alternative indicated in forage_visit|

## Derived Data (outputs generated by running the tool derive_statistics.py)
### flat_time_x_environment_results_with_statistics

This dataset contains all data series from raw data, but adds some derived measures. For the data series also present in the raw data, see under 'Raw data' :arrow_right: flat_time_x_environment_results

| Column / Data Series Name | Description of Data |
| ----------- | ----------- |
|<*agent_id*>_heatmap_error|difference between what an agent would have caught and what he was expecting to catch, if foraging in a a given alternative, for a given time and iteration|


### flat_time_x_agent_result_with_statistics

This dataset contains all data series from raw data, but adds some derived measures. For the data series also present in the raw data, see under 'Raw data' :arrow_right: flat_time_x_agents_results

| Column / Data Series Name | Description of Data |
| ----------- | ----------- |
|mean_absolute_errors|the mean (over all alternatives) of the absolute difference between what an agent expects to catch (according to heatmap) and what an agent would have really caught if he foraged for a given agent, time and iteration|
|mean_negative_errors|the mean (over all alternatives) of the negative differences (overestimations) between what an agent expects to catch (according to heatmap) and what an agent would have really caught if he foraged for a given agent, time and iteration|
|mean_positive_errors|the mean (over all alternatives) of the negative differences (underestimations) between what an agent expects to catch (according to heatmap) and what an agent would have really caught if he foraged for a given agent, time and iteration|
|sd_absolute_errors|the standard deviation (over all alternatives) of the absolute difference between what an agent expects to catch (according to heatmap) and what an agent would have really caught if he foraged for a given agent, time and iteration|

## Graph outputs (by running the tool graphmaker.py)

Highly tailored tool to specific scenarios, not described here yet due to inflexibility of the tool