## Input parameter description to interpret the parameters of the model that are adaptable

In this file the different inputs (parameters) that can be defined in any config .csv file. 
A legend is given for each column in the config template file, displaying what the input parameters entails
and, if known what the limits of the parameter are. If the parameter is limited to a fixed set of string values, 
these are discussed further below the main table. All functionality reported here are used in running  
`ARTEMIS.py` as it exists in the version of 15 February 2022.

### Main Table of parameters
| Column / input parameter Name | parameter format|Description of input parameter | known limits of parameter                                                                                                                                                                                                      |
| ----------- | ----------- | ----------- |--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|scenario_id|**string** |chosen name (string) or code for the scenario, any output of the runs of this scenario will have this name in output files| --                                                                                                                                                                                                                              |
|model >  duration|**integer** |duration the model runs in number of time steps (can be separate for different scenarios) | it is advised to choose a duration longer than 100 to allow the model to set                                                                                                                                                   |
|model > nb_iterations|**integer**| determines how many simulations a scenario is run for| --                                                                                                                                                                                                                              |
|model > reporting|**boolean**| value that determines is the model prints information in the console during the runs. If False, only the start of a scenario and runtime needed to execute all scenarios is printed.  | --                                                                                                                                                                                                                              |
|agents > nb_agents|**integer**|determines the number of foragers agents that will populate the model and attempt to forage every time step| no limits, but over or undercrowding the grid is not recommended                                                                                                                                                               |
|agents > catchability_coefficient|**float**|Determines how much (as fraction) of the stock present is gained if an agent forages somewhere| values outside of 0 and 1 are not realistic from a real world perspective (catching more than 100% of the stock or a negative catch                                                                                            |
|agents > choice_method > name|**string**|Determines how an agent chooses an alternative to forage in (e.g. in what Grid Cell)| in the Current Version supports the following values: <ul><li>random</li><li>full_heatmap</li><li>explore_heatmap</li><li>full_weighted_heatmap</li><li>explore_weighted_heatmap</li></ul>                                     |
|agents > choice_method > explore_attributes > explore_probability|**float**|if the choice_method includes 'explore' in the value, this value represents the chance an agent forages in a random alternative| values outside of 0 and 1 are not realistic from a real world perspective (more than 100% or less than 0% chance of picking a random alternative)                                                                              |
|agents > choice_method > heatmap_attributes > init_nb_alternative_known|**integer**|determines the initial fill of an agents' heatmap: how many options are known | a value from 0 to the number options in the model (impossible to know more than can be known from a real-world perspective)                                                                                                    |
|agents > sharing > sharing > name|**string**|Determines what (alternatives) an agent shares (e.g. information on what Grid Cells)| in the Current Version supports the following values: <ul><li>no_sharing</li><li>random_sharing</li><li>last_event_sharing</li></ul>                                                                                           |
|agents > sharing > sharing > nb_options_shared|**integer** or **float**|Determines information on how many cells is shared with other agents. Whole values are always shared, if the value has decimals the decimals represent the chance at sharing information on 1 additional alternative| value has to be in the range 0 and the total number of alternatives (options > nb_options)                                                                                                                                |
|agents > sharing > sharing > no_sharing_attributes|**-**|*Placeholder* : column added if future functionality requires more parameters to execute the 'no_sharing' style of sharing data in the model | *Placeholder* : Not Functional in this version of the model                                                                                                                                                                    |
|agents > sharing > sharing > random_sharing_attributes|**-**|*Placeholder* : column added if future functionality requires more parameters to execute the 'random_sharing' style of sharing data in the model | *Placeholder* : Not Functional in this version of the model                                                                                                                                                                    |
|agents > sharing > receiver_choice > nb_receivers|**integer**|determines with how many agents an agent will share data if sharing is on (if sharing > name is not 'no_sharing')| limits to integers <0 <ul><li>**TODO: check What happens if nb_receivers < nb_agents**</li></ul>                                                                                                                               |
|agents > sharing > receiving > name|**string**|determines what an agent does with information shared with him by other agents| in the Current Version supports the following values: <ul><li>no_receiver</li><li>willing_receiver</li><li>combine_receiver</li><li>stubborn_receiver</li></ul>                                                                |
|fleet > agent_order|**string**| determines how agents are ordered before interacting| the current Version supports the following values: <ul><li>shuffle</li><li>constant</li></ul>                                                                                   |
|fleet > receiver_choice > name|**string**| determines how an agent chooses with whom to share information (for instance with friends or within social groups)| in the Current Version supports the following values: <ul><li>random_choice</li><li>~~static_group_choice~~ (Needs to be repaired)</li></ul>                                                                                   |
|fleet > receiver_choice > group_attributes > nb_groups|**integer**|determines, if the agents form social groups, how many of these groups will be in the model| values need to be > 0, and  nb_agents / nb_groups should result in an integer                                                                                                                                                  |
|fleet > receiver_choice > group_attributes > group_formation|**string**|determines, if the agents form social groups, how these (initial) groups are formed| in the Current Version supports the following values: <ul><li>equal_mutually_exclusive_groups</li></ul>                                                                                                                        |
|fleet > receiver_choice > group_attributes > group_dynamics|**string** or **boolean**|*Placeholder* determines, if the agents form social groups, if these groups can change over time| *Placeholder* : Not Functional in this version of the model                                                                                                                                                                    |
|fleet > receiver_choice > random_choice_attributes|**-**|*Placeholder* : column added if future functionality requires more parameters to execute the 'random_choice' style of picking a receiver in the model | *Placeholder* : Not Functional in this version of the model                                                                                                                                                                    |
|options > nb_options|**integer**|determines how many alternatives/options an agent can choose to forage in (e.g. Grid Cells)| limits to an integer <0. Other considerations need to be a proper balance between the number of agents and number of options these agents can choose, to prevent over- or undercrowding                                        |
|options > growth > growth_type|**string**|*Placeholder* determines the shape of the growth curve for the stock present in each alternative/option| *Placeholder* Changes in value currently have no effect as the model automatically defaults to 'exponential' growth (development has not been focused on introducing stock growth See also next line for recommended settings) |
|options > growth > growth_attributes > growth_factor|**float**|determines the rate at which a stock grows in each alternative (e.g. in case of exponential growth Stock t+1 = stock t^growth_factor)| limits to values >0, recommended to keep value at 1.0 (Stock t+1 = stock t) as stock growth is not the focus of the current version of the model and the functionality has not been developed with stock growth in mind        |
|options > stock_reset > name|**string**|determines if and how a stock resets at the end of a time period| in the Current Version supports the following values: <ul><li>normal_random_repeat</li><li>uniform_random_repeat</li></ul>                                                                                                     |
|options > stock_reset > reset_probability|**float**|determines the probability a stock resets at the end of a time period, if stock reset is turned on (see one line above)| realistically speaking, this value should be within a range 0-1 as negative probabilities or probabilities larger than 100% are not possible in real world situations                                                          |
|options > stock_reset > uniform_attributes > min_stock|**integer** or **float**|determines the minimum possible stock if the stock is drawn from a uniform_distribution (if stock_reset_name contains 'uniform')| value < 0 as a negative stock is not realistic in real world situations and zero will cause model bugging                                                                                                                      |
|options > stock_reset > uniform_attributes > max_stock|**integer** or **float**|determines the maximum possible stock if the stock is drawn from a uniform_distribution (if stock_reset_name contains 'uniform')| value > min_stock as a maximum value lower than the minimum value is not possible                                                                                                                                              |
|options > stock_reset > normal_attributes > init_stock|**integer** or **float**|determines the mean of the normal distribution for stock, if the stock is drawn from a normal distribution (if stock_reset_name contains 'normal')| given that the model corrects the value below 0 to an infinite small number it is wise for functionality not to pick a number close to 0 (also in combination with a standard deviation -- one line below)                     |
|options > stock_reset > normal_attributes > sd_init_stock|**integer** or **float**|determines the standard deviation of the normal distribution for stock, if the stock is drawn from a normal distribution (if stock_reset_name contains 'normal')| given that the model corrects the value below 0 to an infinite small number it is wise for functionality not to pick a number that yields many draws at or below 0 (also in combination with a mean -- one line above)         |
|competition > name|**string**|determines how agents experience competition when choosing the same alternative/option at the same moment| in the Current Version supports the following values: <ul><li>absent</li><li>interference-simple</li><li>split-catch</li></ul>                                                                                                 |
|competition > interference_attributes > interference_factor|**float**|determines, if the competition > name contains interference, how strong the competition is (e.g. in interference-simple: competition correction of catch = interference_factor^(nb_agents making the same choice - 1)| interference factor is not limited in numbers, however values higher than 1 can result in the opposite of competition in some scenarios (e.g. interference-simple)                                                             |

### Further details on limited values represented by string names

#### Agents choosing in what alternative to forage (agents | choice_method | name)

|Parameter Value (Name)|Description of Value|Further Parameters Employed|
| ----------- | ----------- | ----------- |
|random|the agent picks a random alternative to forage in|-- |
|full_heatmap|the agent picks the alternative corresponding the highest value in the heatmap|-- |
|explore_heatmap|the agent picks the alternative corresponding the highest value in the heatmap, however the agent has a chance to pick a random alternative|the chance an agent chooses are random alternative is determined by the explore_probability parameter|
|full_weighted_heatmap|based on heatmap values, probability values are constructed that determine the chance each alternative is chosen by the agent |-- |
|explore_weighted_heatmap|based on heatmap values, probability values are constructed that determine the chance each alternative is chosen by the agent, however the agent has a chance to pick a random alternative|the chance an agent chooses are random alternative is determined by the explore_probability parameter |

#### Sharing information - what is shared (agents|sharing|sharing|name)
|Parameter Value (Name)|Description of Value|Further Parameters Employed|
| ----------- | ----------- | ----------- |
|no_sharing|agents share no data with others|-- |
|random_sharing| agents share information on a number of random alternatives|nb_options_shared determines information on how many cells is shared|
|no_sharing|agents share the data on the last alternative they foraged in|-- |

#### Sharing Information - with whom (agents|sharing|receiver_choice|name)
|Parameter Value (Name)|Description of Value|Further Parameters Employed|
| ----------- | ----------- | ----------- |
|random_choice|agents choose with whom to share information at random|-- |
|static_group_choice|agents choose information from a list with 'friends' (e.g. a social groups/communities)|Requires groups to be formed at initialisation of the model|


#### forming initial social groups (agents|sharing|receiver_choice|group_attributes|group_formation)
|Parameter Value (Name)|Description of Value|Further Parameters Employed|
| ----------- | ----------- | ----------- |
|equal_mutually_exclusive_groups|all initial social groups are of equal size and agents can (initially) not belong to multiple groups|groups are formed based on dividing the agents equally over a number of groups (agents > sharing > receiver_choice > group_attributes > nb_groups) |

#### Accepting shared information (agents|sharing|receiving|name)
|Parameter Value (Name)|Description of Value|Further Parameters Employed|
| ----------- | ----------- | ----------- |
|no_receiver|an agents rejects any information shared by other agents|-- |
|willing_receiver|an agent accepts all information from other agents completely, overwriting any information it already holds|-- |
|combine_receiver|an agent evaluates if the information given regards an alternative/option it already has information on and if so, takes the average of its current estimate and the information given. if it has no information yet, it will accept the information provided without question|-- |
|stubborn_receiver|an agent evaluates if the information given regards an alternative/option it already has information on and if so, rejects the information given. if it has no information yet, it will accept the information provided without question|-- |

#### Resource stocks grow (options|growth|growth_type) 
-- Values inflexible as it always default to 'exponential' in the current version of the model--

|Parameter Value (Name)|Description of Value|Further Parameters Employed|
| ----------- | ----------- | ----------- |
|exponential|growth of stocks in options occurs as Stock(t+1) = stock(t) * growth_factor|options > growth > growth_attributes > growth_factor is used to as part of the growth function|

#### Resource stocks reset (options|stock_reset|name)
|Parameter Value (Name)|Description of Value|Further Parameters Employed|
| ----------- | ----------- | ----------- |
|normal_random_repeat|every time step the stock has a chance to be redrawn from a normal distribution with a mean and standard deviation, draws of stock values <= 0 are always redrawn an extra time|<ul><li>options > stock_reset > reset_probability represent the chance the stock in an alternative/option is redrawn</li><li>options > stock_reset > normal_attributes > init_stock represents the mean of the normal distribution from which the stock will be redrawn</li><li>options > stock_reset > normal_attributes > sd_init_stock represents the standard deviation of the normal distribution from which the stock will be redrawn</li></ul>|
|uniform_random_repeat|every time step the stock has a chance to be redrawn from a uniform distribution with a minimum and maximum, draws of stock values <= 0 are always redrawn an extra time|<ul><li>options > stock_reset > reset_probability represent the chance the stock in an alternative/option is redrawn</li><li>options > stock_reset > uniform_attributes > max_stock represents the maximum value of the uniform distribution from which the stock will be redrawn</li><li>options > stock_reset > uniform_attributes  > min_stock represents the minimum value of the uniform distribution from which the stock will be redrawn</li></ul>|

#### Competition hindrance (competition|name)
|Parameter Value (Name)|Description of Value|Further Parameters Employed|
| ----------- | ----------- | ----------- |
|absent|agents experience no effects of competition if other agents choose the same alternative/option|-- |
|interference-simple|agents experience competition by a factor reduction in catch for every other agent that is present as Catch = Potential Catch * interference factor^(agents choosing the option-1)|competition > interference_attributes > interference_factor is used as interference factor in the equation described|
|split-catch|total catch is a fixed and equally divided over all agents that choose an alternative/option|-- |
