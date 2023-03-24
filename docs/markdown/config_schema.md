# ARTEMIS scenario configuration input documentation

- [1. [Required] Property ARTEMIS scenario configuration input documentation > scenario_id](#scenario_id)
- [2. [Required] Property ARTEMIS scenario configuration input documentation > model](#model)
  - [2.1. [Required] Property ARTEMIS scenario configuration input documentation > model > duration](#model_duration)
  - [2.2. [Required] Property ARTEMIS scenario configuration input documentation > model > nb_iterations](#model_nb_iterations)
  - [2.3. [Required] Property ARTEMIS scenario configuration input documentation > model > reporting](#model_reporting)
- [3. [Required] Property ARTEMIS scenario configuration input documentation > agents](#agents)
- [4. [Required] Property ARTEMIS scenario configuration input documentation > fleet](#fleet)
  - [4.1. [Required] Property ARTEMIS scenario configuration input documentation > fleet > agent_order](#fleet_agent_order)
  - [4.2. [Required] Property ARTEMIS scenario configuration input documentation > fleet > receiver_choice](#fleet_receiver_choice)
    - [4.2.1. [Required] Property ARTEMIS scenario configuration input documentation > fleet > receiver_choice > name](#fleet_receiver_choice_name)
    - [4.2.2. [Required] Property ARTEMIS scenario configuration input documentation > fleet > receiver_choice > group_attributes](#fleet_receiver_choice_group_attributes)
      - [4.2.2.1. [Required] Property ARTEMIS scenario configuration input documentation > fleet > receiver_choice > group_attributes > nb_groups](#fleet_receiver_choice_group_attributes_nb_groups)
      - [4.2.2.2. [Required] Property ARTEMIS scenario configuration input documentation > fleet > receiver_choice > group_attributes > group_formation](#fleet_receiver_choice_group_attributes_group_formation)
      - [4.2.2.3. [Required] Property ARTEMIS scenario configuration input documentation > fleet > receiver_choice > group_attributes > group_dynamics](#fleet_receiver_choice_group_attributes_group_dynamics)
    - [4.2.3. [Required] Property ARTEMIS scenario configuration input documentation > fleet > receiver_choice > random_choice_attributes](#fleet_receiver_choice_random_choice_attributes)
- [5. [Required] Property ARTEMIS scenario configuration input documentation > options](#options)
  - [5.1. [Required] Property ARTEMIS scenario configuration input documentation > options > nb_options](#options_nb_options)
  - [5.2. [Required] Property ARTEMIS scenario configuration input documentation > options > growth](#options_growth)
    - [5.2.1. [Required] Property ARTEMIS scenario configuration input documentation > options > growth > growth_type](#options_growth_growth_type)
    - [5.2.2. [Required] Property ARTEMIS scenario configuration input documentation > options > growth > growth_attributes](#options_growth_growth_attributes)
      - [5.2.2.1. [Required] Property ARTEMIS scenario configuration input documentation > options > growth > growth_attributes > growth_factor](#options_growth_growth_attributes_growth_factor)
  - [5.3. [Required] Property ARTEMIS scenario configuration input documentation > options > stock_reset](#options_stock_reset)
    - [5.3.1. [Required] Property ARTEMIS scenario configuration input documentation > options > stock_reset > name](#options_stock_reset_name)
    - [5.3.2. [Required] Property ARTEMIS scenario configuration input documentation > options > stock_reset > reset_probability](#options_stock_reset_reset_probability)
    - [5.3.3. [Required] Property ARTEMIS scenario configuration input documentation > options > stock_reset > uniform_attributes](#options_stock_reset_uniform_attributes)
      - [5.3.3.1. [Required] Property ARTEMIS scenario configuration input documentation > options > stock_reset > uniform_attributes > min_stock](#options_stock_reset_uniform_attributes_min_stock)
      - [5.3.3.2. [Required] Property ARTEMIS scenario configuration input documentation > options > stock_reset > uniform_attributes > max_stock](#options_stock_reset_uniform_attributes_max_stock)
    - [5.3.4. [Required] Property ARTEMIS scenario configuration input documentation > options > stock_reset > normal_attributes](#options_stock_reset_normal_attributes)
      - [5.3.4.1. [Required] Property ARTEMIS scenario configuration input documentation > options > stock_reset > normal_attributes > init_stock](#options_stock_reset_normal_attributes_init_stock)
      - [5.3.4.2. [Required] Property ARTEMIS scenario configuration input documentation > options > stock_reset > normal_attributes > sd_init_stock](#options_stock_reset_normal_attributes_sd_init_stock)
- [6. [Required] Property ARTEMIS scenario configuration input documentation > competition](#competition)
  - [6.1. [Required] Property ARTEMIS scenario configuration input documentation > competition > name](#competition_name)
  - [6.2. [Required] Property ARTEMIS scenario configuration input documentation > competition > interference_attributes](#competition_interference_attributes)
    - [6.2.1. [Required] Property ARTEMIS scenario configuration input documentation > competition > interference_attributes > interference_factor](#competition_interference_attributes_interference_factor)

**Title:** ARTEMIS scenario configuration input documentation

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

**Description:** This document will tell you what fields are required in the scenario configuration yml-file.

<details>
<summary><strong> <a name="scenario_id"></a>1. [Required] Property ARTEMIS scenario configuration input documentation > scenario_id</strong>  

</summary>
<blockquote>

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** scenario identifier

</blockquote>
</details>

<details>
<summary><strong> <a name="model"></a>2. [Required] Property ARTEMIS scenario configuration input documentation > model</strong>  

</summary>
<blockquote>

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | Yes                                                                       |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

**Description:** general settings for the model

<details>
<summary><strong> <a name="model_duration"></a>2.1. [Required] Property ARTEMIS scenario configuration input documentation > model > duration</strong>  

</summary>
<blockquote>

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | Yes      |

**Description:** time a simulation runs for

</blockquote>
</details>

<details>
<summary><strong> <a name="model_nb_iterations"></a>2.2. [Required] Property ARTEMIS scenario configuration input documentation > model > nb_iterations</strong>  

</summary>
<blockquote>

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | Yes      |

**Description:** number of iterations per simulation every scenario is tested for

</blockquote>
</details>

<details>
<summary><strong> <a name="model_reporting"></a>2.3. [Required] Property ARTEMIS scenario configuration input documentation > model > reporting</strong>  

</summary>
<blockquote>

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

**Description:** indicates if a scenario run reports using all print statements in the script (False --> only report what scenario the model starts running and the total runtime)

</blockquote>
</details>

</blockquote>
</details>

<details>
<summary><strong> <a name="agents"></a>3. [Required] Property ARTEMIS scenario configuration input documentation > agents</strong>  

</summary>
<blockquote>

|              |         |
| ------------ | ------- |
| **Type**     | `array` |
| **Required** | Yes     |

**Description:** settings for the agents in the model; see agent_schema.yml

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | N/A                |

</blockquote>
</details>

<details>
<summary><strong> <a name="fleet"></a>4. [Required] Property ARTEMIS scenario configuration input documentation > fleet</strong>  

</summary>
<blockquote>

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | Yes                                                                       |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

**Description:** fleet settings; these apply to all agents defined under 'agents'

<details>
<summary><strong> <a name="fleet_agent_order"></a>4.1. [Required] Property ARTEMIS scenario configuration input documentation > fleet > agent_order</strong>  

</summary>
<blockquote>

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** setting for ordering agent between each time step (for now 'constant' or 'shuffle')

</blockquote>
</details>

<details>
<summary><strong> <a name="fleet_receiver_choice"></a>4.2. [Required] Property ARTEMIS scenario configuration input documentation > fleet > receiver_choice</strong>  

</summary>
<blockquote>

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | Yes                                                                       |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

**Description:** settings for with whom an agent shares information on choice option / DiscreteAlternative/ environment units

<details>
<summary><strong> <a name="fleet_receiver_choice_name"></a>4.2.1. [Required] Property ARTEMIS scenario configuration input documentation > fleet > receiver_choice > name</strong>  

</summary>
<blockquote>

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** name of the method an agent employs to determine with whom to share information on choice option / DiscreteAlternative/ environment unit

</blockquote>
</details>

<details>
<summary><strong> <a name="fleet_receiver_choice_group_attributes"></a>4.2.2. [Required] Property ARTEMIS scenario configuration input documentation > fleet > receiver_choice > group_attributes</strong>  

</summary>
<blockquote>

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | Yes                                                                       |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

**Description:** settings if 'group' is part of the method to determine with whom to share information on choice option / DiscreteAlternative/ environment units

<details>
<summary><strong> <a name="fleet_receiver_choice_group_attributes_nb_groups"></a>4.2.2.1. [Required] Property ARTEMIS scenario configuration input documentation > fleet > receiver_choice > group_attributes > nb_groups</strong>  

</summary>
<blockquote>

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | Yes      |

**Description:** determine how many 'friend' groups of agents are in the model

</blockquote>
</details>

<details>
<summary><strong> <a name="fleet_receiver_choice_group_attributes_group_formation"></a>4.2.2.2. [Required] Property ARTEMIS scenario configuration input documentation > fleet > receiver_choice > group_attributes > group_formation</strong>  

</summary>
<blockquote>

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** determines the way 'friend' groups are formed at the start of a model run

</blockquote>
</details>

<details>
<summary><strong> <a name="fleet_receiver_choice_group_attributes_group_dynamics"></a>4.2.2.3. [Required] Property ARTEMIS scenario configuration input documentation > fleet > receiver_choice > group_attributes > group_dynamics</strong>  

</summary>
<blockquote>

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

**Description:** determines how 'friend' group might change over time (False is no change)

</blockquote>
</details>

</blockquote>
</details>

<details>
<summary><strong> <a name="fleet_receiver_choice_random_choice_attributes"></a>4.2.3. [Required] Property ARTEMIS scenario configuration input documentation > fleet > receiver_choice > random_choice_attributes</strong>  

</summary>
<blockquote>

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | Yes                                                                       |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

**Description:** settings if 'random_choice' is part of the method to determine with whom to share information on choice option / DiscreteAlternative/ enviroment units

</blockquote>
</details>

</blockquote>
</details>

</blockquote>
</details>

<details>
<summary><strong> <a name="options"></a>5. [Required] Property ARTEMIS scenario configuration input documentation > options</strong>  

</summary>
<blockquote>

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | Yes                                                                       |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

**Description:** settings for the choice option / DiscreteAlternative/ environment units in the model

<details>
<summary><strong> <a name="options_nb_options"></a>5.1. [Required] Property ARTEMIS scenario configuration input documentation > options > nb_options</strong>  

</summary>
<blockquote>

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | Yes      |

**Description:** number of subdivisions of the environment (choice option / DiscreteAlternative/ environment units) (e.g. Grid cells) in the model and therefore the number of choices an agent has

</blockquote>
</details>

<details>
<summary><strong> <a name="options_growth"></a>5.2. [Required] Property ARTEMIS scenario configuration input documentation > options > growth</strong>  

</summary>
<blockquote>

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | Yes                                                                       |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

**Description:** settings on the way stocks that can be foraged in different choice option / DiscreteAlternative/ environment units change over time

<details>
<summary><strong> <a name="options_growth_growth_type"></a>5.2.1. [Required] Property ARTEMIS scenario configuration input documentation > options > growth > growth_type</strong>  

</summary>
<blockquote>

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** the way stocks in choice option / DiscreteAlternative/ environment units change over time

</blockquote>
</details>

<details>
<summary><strong> <a name="options_growth_growth_attributes"></a>5.2.2. [Required] Property ARTEMIS scenario configuration input documentation > options > growth > growth_attributes</strong>  

</summary>
<blockquote>

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | Yes                                                                       |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

**Description:** additional settings on the way stocks in choice option / DiscreteAlternative/ environment units change over time

<details>
<summary><strong> <a name="options_growth_growth_attributes_growth_factor"></a>5.2.2.1. [Required] Property ARTEMIS scenario configuration input documentation > options > growth > growth_attributes > growth_factor</strong>  

</summary>
<blockquote>

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | Yes      |

**Description:** speed of growth of stocks (per time unit) --> Stock(t+1) = Stock(t, growth_factor)

</blockquote>
</details>

</blockquote>
</details>

</blockquote>
</details>

<details>
<summary><strong> <a name="options_stock_reset"></a>5.3. [Required] Property ARTEMIS scenario configuration input documentation > options > stock_reset</strong>  

</summary>
<blockquote>

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | Yes                                                                       |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

**Description:** settings for the way a stock in a choice option / DiscreteAlternative/ environment units resets (if it resets) at the end of a time unit t

<details>
<summary><strong> <a name="options_stock_reset_name"></a>5.3.1. [Required] Property ARTEMIS scenario configuration input documentation > options > stock_reset > name</strong>  

</summary>
<blockquote>

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** the way a stock in a choice option / DiscreteAlternative/ environment units resets at the end of a time unit

</blockquote>
</details>

<details>
<summary><strong> <a name="options_stock_reset_reset_probability"></a>5.3.2. [Required] Property ARTEMIS scenario configuration input documentation > options > stock_reset > reset_probability</strong>  

</summary>
<blockquote>

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | Yes      |

**Description:** the probability a stock in a choice option / DiscreteAlternative/ environment units resets at the end of a time unit

</blockquote>
</details>

<details>
<summary><strong> <a name="options_stock_reset_uniform_attributes"></a>5.3.3. [Required] Property ARTEMIS scenario configuration input documentation > options > stock_reset > uniform_attributes</strong>  

</summary>
<blockquote>

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | Yes                                                                       |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

**Description:** settings if 'uniform' is in the way a stock in a choice option / DiscreteAlternative/ environment units is reset at the end of a time unit

<details>
<summary><strong> <a name="options_stock_reset_uniform_attributes_min_stock"></a>5.3.3.1. [Required] Property ARTEMIS scenario configuration input documentation > options > stock_reset > uniform_attributes > min_stock</strong>  

</summary>
<blockquote>

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | Yes      |

**Description:** the minimum value a stock in a choice option / DiscreteAlternative/ environment units can get after a reset

</blockquote>
</details>

<details>
<summary><strong> <a name="options_stock_reset_uniform_attributes_max_stock"></a>5.3.3.2. [Required] Property ARTEMIS scenario configuration input documentation > options > stock_reset > uniform_attributes > max_stock</strong>  

</summary>
<blockquote>

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | Yes      |

**Description:** the maximum value a stock in a choice option / DiscreteAlternative/ environment units can get after a reset

</blockquote>
</details>

</blockquote>
</details>

<details>
<summary><strong> <a name="options_stock_reset_normal_attributes"></a>5.3.4. [Required] Property ARTEMIS scenario configuration input documentation > options > stock_reset > normal_attributes</strong>  

</summary>
<blockquote>

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | Yes                                                                       |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

**Description:** settings if 'normal' is in the way a stock in a choice option / DiscreteAlternative/ environment units is reset at the end of a time unit

<details>
<summary><strong> <a name="options_stock_reset_normal_attributes_init_stock"></a>5.3.4.1. [Required] Property ARTEMIS scenario configuration input documentation > options > stock_reset > normal_attributes > init_stock</strong>  

</summary>
<blockquote>

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | Yes      |

**Description:** the mean value a stock in a stock in a choice option / DiscreteAlternative/ environment units can get after a reset

</blockquote>
</details>

<details>
<summary><strong> <a name="options_stock_reset_normal_attributes_sd_init_stock"></a>5.3.4.2. [Required] Property ARTEMIS scenario configuration input documentation > options > stock_reset > normal_attributes > sd_init_stock</strong>  

</summary>
<blockquote>

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | Yes      |

**Description:** the standard deviation of a value a stock in a choice option / DiscreteAlternative/ environment units can get after a reset

</blockquote>
</details>

</blockquote>
</details>

</blockquote>
</details>

</blockquote>
</details>

<details>
<summary><strong> <a name="competition"></a>6. [Required] Property ARTEMIS scenario configuration input documentation > competition</strong>  

</summary>
<blockquote>

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | Yes                                                                       |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

**Description:** settings for the way agents are hindered in foraging by other agents in the model

<details>
<summary><strong> <a name="competition_name"></a>6.1. [Required] Property ARTEMIS scenario configuration input documentation > competition > name</strong>  

</summary>
<blockquote>

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** the way agents are hindered in foraging by other agents in the model

</blockquote>
</details>

<details>
<summary><strong> <a name="competition_interference_attributes"></a>6.2. [Required] Property ARTEMIS scenario configuration input documentation > competition > interference_attributes</strong>  

</summary>
<blockquote>

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | Yes                                                                       |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

**Description:** settings if 'interference' is in the way agents are hindered in foraging by other agents in the model

<details>
<summary><strong> <a name="competition_interference_attributes_interference_factor"></a>6.2.1. [Required] Property ARTEMIS scenario configuration input documentation > competition > interference_attributes > interference_factor</strong>  

</summary>
<blockquote>

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | Yes      |

**Description:** the fraction foraging success is corrected for, for every other agent, if other agents choose the same choice option / DiscreteAlternative/ environment units to forage in in the same time unit

</blockquote>
</details>

</blockquote>
</details>

</blockquote>
</details>

----------------------------------------------------------------------------------------------------------------------------
Generated using [json-schema-for-humans](https://github.com/coveooss/json-schema-for-humans) on 2023-03-24 at 17:49:34 +0100