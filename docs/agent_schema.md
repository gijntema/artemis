# Schema Docs

- [1. [Required] Property root > name](#name)
- [2. [Required] Property root > nb_agents](#nb_agents)
- [3. [Required] Property root > catchability_coefficient](#catchability_coefficient)
- [4. [Required] Property root > choice_method](#choice_method)
  - [4.1. [Required] Property root > choice_method > name](#choice_method_name)
  - [4.2. [Required] Property root > choice_method > explore_attributes](#choice_method_explore_attributes)
    - [4.2.1. [Required] Property root > choice_method > explore_attributes > explore_probability](#choice_method_explore_attributes_explore_probability)
  - [4.3. [Required] Property root > choice_method > heatmap_attributes](#choice_method_heatmap_attributes)
    - [4.3.1. [Required] Property root > choice_method > heatmap_attributes > init_nb_alternative_known](#choice_method_heatmap_attributes_init_nb_alternative_known)
- [5. [Required] Property root > sharing](#sharing)
  - [5.1. [Required] Property root > sharing > sharing](#sharing_sharing)
    - [5.1.1. [Required] Property root > sharing > sharing > name](#sharing_sharing_name)
    - [5.1.2. [Required] Property root > sharing > sharing > no_sharing_attributes](#sharing_sharing_no_sharing_attributes)
    - [5.1.3. [Required] Property root > sharing > sharing > random_sharing_attributes](#sharing_sharing_random_sharing_attributes)
    - [5.1.4. [Required] Property root > sharing > sharing > nb_options_shared](#sharing_sharing_nb_options_shared)
  - [5.2. [Required] Property root > sharing > receiver_choice](#sharing_receiver_choice)
    - [5.2.1. [Required] Property root > sharing > receiver_choice > nb_receivers](#sharing_receiver_choice_nb_receivers)
  - [5.3. [Required] Property root > sharing > receiving](#sharing_receiving)
    - [5.3.1. [Required] Property root > sharing > receiving > name](#sharing_receiving_name)

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

<details>
<summary><strong> <a name="name"></a>1. [Required] Property root > name</strong>  

</summary>
<blockquote>

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** name of agent group

</blockquote>
</details>

<details>
<summary><strong> <a name="nb_agents"></a>2. [Required] Property root > nb_agents</strong>  

</summary>
<blockquote>

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | Yes      |

**Description:** the number of ForagerAgents that forage in the model

</blockquote>
</details>

<details>
<summary><strong> <a name="catchability_coefficient"></a>3. [Required] Property root > catchability_coefficient</strong>  

</summary>
<blockquote>

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | Yes      |

**Description:** the fraction of the resource stock in a given choice option / DiscreteAlternative/ environment unit an agent receives if foraging there

</blockquote>
</details>

<details>
<summary><strong> <a name="choice_method"></a>4. [Required] Property root > choice_method</strong>  

</summary>
<blockquote>

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | Yes                                                                       |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

**Description:** settings for the way an agent chooses a choice option / DiscreteAlternative/ environment unit

<details>
<summary><strong> <a name="choice_method_name"></a>4.1. [Required] Property root > choice_method > name</strong>  

</summary>
<blockquote>

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** name of the method an agent employs to choose a choice option / DiscreteAlternative/ environment unit to forage in

</blockquote>
</details>

<details>
<summary><strong> <a name="choice_method_explore_attributes"></a>4.2. [Required] Property root > choice_method > explore_attributes</strong>  

</summary>
<blockquote>

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | Yes                                                                       |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

**Description:** settings if 'explore' is part of the method an agent employs to choose a choice option / DiscreteAlternative/ environment unit

<details>
<summary><strong> <a name="choice_method_explore_attributes_explore_probability"></a>4.2.1. [Required] Property root > choice_method > explore_attributes > explore_probability</strong>  

</summary>
<blockquote>

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | Yes      |

**Description:** the probability an agent uses picks a random choice option / DiscreteAlternative/ environment unit

</blockquote>
</details>

</blockquote>
</details>

<details>
<summary><strong> <a name="choice_method_heatmap_attributes"></a>4.3. [Required] Property root > choice_method > heatmap_attributes</strong>  

</summary>
<blockquote>

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | Yes                                                                       |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

**Description:** settings if 'heatmap' is part of the method an agent employs to choose a choice option / DiscreteAlternative/ environment unit

<details>
<summary><strong> <a name="choice_method_heatmap_attributes_init_nb_alternative_known"></a>4.3.1. [Required] Property root > choice_method > heatmap_attributes > init_nb_alternative_known</strong>  

</summary>
<blockquote>

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | Yes      |

**Description:** initial number of choice option / DiscreteAlternative/ environment unit an agent has information/memory on

</blockquote>
</details>

</blockquote>
</details>

</blockquote>
</details>

<details>
<summary><strong> <a name="sharing"></a>5. [Required] Property root > sharing</strong>  

</summary>
<blockquote>

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | Yes                                                                       |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

**Description:** settings for the way an agent shares and receives information on choice option / DiscreteAlternative/ environment units with/from other agents

<details>
<summary><strong> <a name="sharing_sharing"></a>5.1. [Required] Property root > sharing > sharing</strong>  

</summary>
<blockquote>

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | Yes                                                                       |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

**Description:** settings for what information an agent shares with on choice option / DiscreteAlternative/ environment units

<details>
<summary><strong> <a name="sharing_sharing_name"></a>5.1.1. [Required] Property root > sharing > sharing > name</strong>  

</summary>
<blockquote>

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** name of the method an agent employs to determine what information on choice option / DiscreteAlternative/ environment unit to share with other agents

</blockquote>
</details>

<details>
<summary><strong> <a name="sharing_sharing_no_sharing_attributes"></a>5.1.2. [Required] Property root > sharing > sharing > no_sharing_attributes</strong>  

</summary>
<blockquote>

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | Yes                                                                       |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

**Description:** placeholder for settings if 'no_sharing' is part of the method an agent employs to determine what information on choice option / DiscreteAlternative/ environment unit with other agents

</blockquote>
</details>

<details>
<summary><strong> <a name="sharing_sharing_random_sharing_attributes"></a>5.1.3. [Required] Property root > sharing > sharing > random_sharing_attributes</strong>  

</summary>
<blockquote>

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | Yes                                                                       |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

**Description:** placeholder for settings if 'random_sharing' is part of the method an agent employs to determine what information on choice option / DiscreteAlternative/ environment unit with other agents

</blockquote>
</details>

<details>
<summary><strong> <a name="sharing_sharing_nb_options_shared"></a>5.1.4. [Required] Property root > sharing > sharing > nb_options_shared</strong>  

</summary>
<blockquote>

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | Yes      |

**Description:** number of choice option / DiscreteAlternative/ environment unit an agent shares information on with other agents every time unit

</blockquote>
</details>

</blockquote>
</details>

<details>
<summary><strong> <a name="sharing_receiver_choice"></a>5.2. [Required] Property root > sharing > receiver_choice</strong>  

</summary>
<blockquote>

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | Yes                                                                       |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

**Description:** settings for with whom an agent shares information on choice option / DiscreteAlternative/ environment units

<details>
<summary><strong> <a name="sharing_receiver_choice_nb_receivers"></a>5.2.1. [Required] Property root > sharing > receiver_choice > nb_receivers</strong>  

</summary>
<blockquote>

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | Yes      |

**Description:** number of agents that an agent shares information with every unit of time

</blockquote>
</details>

</blockquote>
</details>

<details>
<summary><strong> <a name="sharing_receiving"></a>5.3. [Required] Property root > sharing > receiving</strong>  

</summary>
<blockquote>

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | Yes                                                                       |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

**Description:** settings for how an agent receives/accepts information from other agents on choice option / DiscreteAlternative/ environment units

<details>
<summary><strong> <a name="sharing_receiving_name"></a>5.3.1. [Required] Property root > sharing > receiving > name</strong>  

</summary>
<blockquote>

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** name of the method an agent employs to receive/accept information from other agents on choice option / DiscreteAlternative/ environment unit

</blockquote>
</details>

</blockquote>
</details>

</blockquote>
</details>

----------------------------------------------------------------------------------------------------------------------------
Generated using [json-schema-for-humans](https://github.com/coveooss/json-schema-for-humans) on 2023-02-20 at 15:27:18 +0100