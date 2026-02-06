Feature: Card Service Card test scenarios for provider Clowd9

  Background: Setup Customer Profile and End-Customer Profile on Card Service and on provider Clowd9
#    Given I create Customer, Customer Profile, Onboard to account,banking,card

    Given I set and verify customer CID1, customer profile CPID1 of SG region in the context

    Then I set the card design config id and card product ids
      | customer_profile_identifier | card_design_config_code | card_account_product_code | card_product_code |
      | CPID1                       | GREEN_C9                | C9_DEB_CA                 | C9_DEBIT          |

    Then I create below End-Customer-Profile
      | customer_profile_identifier | end_customer_profile_identifier | first_name | last_name | region | email         | phone_number   | address                                                                                                                                                                                                                             |
      | CPID1                       | ECPID1                          | John       | Snow      | SG     | john@snow.com | +63 1234567890 | {"address_line_1":"123 Main Street", "address_line_2":"Apt 48", "address_line_3":"Defence Colony", "address_line_4":"Paradise Island", "city":"Paradito", "state":"", "country": "", "country_code": "SGP", "local_code": "800003"} |

    Then I verify End-Customer-Profile exist with values
      | customer_profile_identifier | end_customer_profile_identifier | first_name | last_name | email         | phone_number   | status | address                                                                                                                                                                                                                             |
      | CPID1                       | ECPID1                          | John       | Snow      | john@snow.com | +63 1234567890 | ACTIVE | {"address_line_1":"123 Main Street", "address_line_2":"Apt 48", "address_line_3":"Defence Colony", "address_line_4":"Paradise Island", "city":"Paradito", "state":"", "country": "", "country_code": "SGP", "local_code": "800003"} |

    Given I onboard CustomerProfile CPID1 with customerId CID1 on cash service on below providers and expect status 200
      | provider_name |
      | DBS Bank Ltd  |

    Then I wait until max time to verify CustomerProfile CPID1 onboard status as ONBOARD_SUCCESS

    When I onboard EndCustomerProfile ECPID1 of CustomerProfile CPID1 on cash service on below providers and expect status 200
      | provider_name |
      | DBS Bank Ltd  |

    Then I wait until max time to verify EndCustomerProfile ECPID1 of CustomerProfile CPID1 onboard status as ONBOARD_SUCCESS

    Given I onboard End-Customer Profile ECPID1 of Customer Profile CPID1 on fund provider CASH and on card service on provider Clowd9

    Then I wait until max time to verify End-Customer Profile ECPID1 onboard status on card service provider Clowd9 as ONBOARD_SUCCESS

    Given I create a product with customer profile CPID1 provider as DBS Bank Ltd and expect product_status PRODUCT_DRAFT
      | identifier | product_type | profile_type | product_class | currency | country | account_type | minimum_balance_policy | minimum_balance_limit |
      | ProductID1 | WALLET       | END_CUSTOMER | SHARIAH       | SGD      | SGP     | SAVINGS      | LENIENT                | 0                     |

    Then I approve the product ProductID1 and verify status as PRODUCT_SUCCESS with provider DBS Bank Ltd for customerProfileId CPID1

    Given I create account for EndCustomerProfile with id ECPID1 for CustomerProfile CPID1 with product id ProductID1 with bank account type as e-money with provider DBS Bank Ltd and expect the header status 200
      | identifier | currency | country | in_trust | is_overdraft_allowed | on_behalf_of | metadata                    |
      | BankAccId  | SGD      | SGP     | false    | true                 | CUSTOMER     | {"key": "IntegrationTest1"} |

    Then I wait until max time to verify the bank account BankAccId status as CASH_WALLET_CREATED with provider DBS Bank Ltd for customerProfileId CPID1

    Given I create below Card Account
      | card_account_identifier | end_customer_profile_identifier | provider_name | fund_provider | bank_account_identifier | customer_address                                                                                                                                                                                                                                      |
      | CardAccId1              | ECPID1                          | Clowd9        | CASH          | BankAccId               | {"address_line_1":"Atlas Consolidated Labs", "address_line_2":"Mukunda Towers", "address_line_3":"Indian Airlines Colony", "address_line_4":"Begumpet", "city":"Hyderabad", "state":"", "country": "", "country_code": "SGP", "local_code": "800003"} |

    Then I wait until max time to verify Card Account CardAccId1 onboard status on card service provider Clowd9 as CARD_ACCOUNT_CREATED

  Scenario Outline: Issuing Card for the Card Account on provider Clowd9
    Given I issue Card for Card Account on provider Clowd9
      | card_identifier   | card_account_identifier | card_type   | emboss_name   | validity_in_months | three_d_secure_config                                                  | delivery_address                                                                                                                                                                                                                                      |
      | <card_identifier> | CardAccId1              | <card_type> | <emboss_name> | 60                 | {"security_question": "What is your name?", "security_answer": "John"} | {"address_line_1":"Atlas Consolidated Labs", "address_line_2":"Mukunda Towers", "address_line_3":"Indian Airlines Colony", "address_line_4":"Begumpet", "city":"Hyderabad", "state":"", "country": "", "country_code": "SGP", "local_code": "800003"} |

    Then I wait until max time to verify Card <card_identifier> status on card service provider Clowd9 as INACTIVE

    Examples:
      | card_identifier | card_type | emboss_name |
      | CardId1         | PHYSICAL  | Sasuke      |

  Scenario Outline: Activating Card on provider Clowd9
    Given I issue Card for Card Account on provider Clowd9
      | card_identifier   | card_account_identifier | card_type   | emboss_name   | validity_in_months | three_d_secure_config                                                  | delivery_address                                                                                                                                                                                                                                      |
      | <card_identifier> | CardAccId1              | <card_type> | <emboss_name> | 60                 | {"security_question": "What is your name?", "security_answer": "John"} | {"address_line_1":"Atlas Consolidated Labs", "address_line_2":"Mukunda Towers", "address_line_3":"Indian Airlines Colony", "address_line_4":"Begumpet", "city":"Hyderabad", "state":"", "country": "", "country_code": "SGP", "local_code": "800003"} |

    Then I wait until max time to verify Card <card_identifier> status on card service provider Clowd9 as INACTIVE

    Then I activate the Card
      | card_identifier   |
      | <card_identifier> |

    Then I validate card status by fetching card with id <card_identifier> and checking card status as ACTIVE

    Examples:
      | card_identifier | card_type | emboss_name |
      | CardId1         | PHYSICAL  | Sasuke      |

#    Valid Permutations
  Scenario Outline: Clowd9-Active -> Block -> Unblock -> Block -> Disable
    Given I issue Card for Card Account on provider Clowd9
      | card_identifier   | card_account_identifier | card_type   | emboss_name   | validity_in_months | three_d_secure_config                                                  | delivery_address                                                                                                                                                                                                                                      |
      | <card_identifier> | CardAccId1              | <card_type> | <emboss_name> | 60                 | {"security_question": "What is your name?", "security_answer": "John"} | {"address_line_1":"Atlas Consolidated Labs", "address_line_2":"Mukunda Towers", "address_line_3":"Indian Airlines Colony", "address_line_4":"Begumpet", "city":"Hyderabad", "state":"", "country": "", "country_code": "SGP", "local_code": "800003"} |

    Then I wait until max time to verify Card <card_identifier> status on card service provider Clowd9 as INACTIVE

    Then I activate the Card
      | card_identifier   |
      | <card_identifier> |

    Then I validate card status by fetching card with id <card_identifier> and checking card status as ACTIVE

    Then I update the status of Card with id <card_identifier>
      | card_status |
      | BLOCK       |
      | UNBLOCK     |
      | BLOCK       |
      | DISABLE     |

    Examples:
      | card_identifier | card_type | emboss_name |
      | CardId1         | PHYSICAL  | Sasuke      |

  Scenario Outline: Clowd9-Active -> Block -> Unblock -> Disable
    Given I issue Card for Card Account on provider Clowd9
      | card_identifier   | card_account_identifier | card_type   | emboss_name   | validity_in_months | three_d_secure_config                                                  | delivery_address                                                                                                                                                                                                                                      |
      | <card_identifier> | CardAccId1              | <card_type> | <emboss_name> | 60                 | {"security_question": "What is your name?", "security_answer": "John"} | {"address_line_1":"Atlas Consolidated Labs", "address_line_2":"Mukunda Towers", "address_line_3":"Indian Airlines Colony", "address_line_4":"Begumpet", "city":"Hyderabad", "state":"", "country": "", "country_code": "SGP", "local_code": "800003"} |

    Then I wait until max time to verify Card <card_identifier> status on card service provider Clowd9 as INACTIVE

    Then I activate the Card
      | card_identifier   |
      | <card_identifier> |

    Then I validate card status by fetching card with id <card_identifier> and checking card status as ACTIVE

    Then I update the status of Card with id <card_identifier>
      | card_status |
      | BLOCK       |
      | UNBLOCK     |
      | DISABLE     |

    Then I validate card status by fetching card with id <card_identifier> and checking card status as DISABLED

    Examples:
      | card_identifier | card_type | emboss_name |
      | CardId1         | PHYSICAL  | Sasuke      |

  Scenario Outline: Disabling inactive card on provider Clowd9
    Given I issue Card for Card Account on provider Clowd9
      | card_identifier   | card_account_identifier | card_type   | emboss_name   | validity_in_months | three_d_secure_config                                                  | delivery_address                                                                                                                                                                                                                                      |
      | <card_identifier> | CardAccId1              | <card_type> | <emboss_name> | 60                 | {"security_question": "What is your name?", "security_answer": "John"} | {"address_line_1":"Atlas Consolidated Labs", "address_line_2":"Mukunda Towers", "address_line_3":"Indian Airlines Colony", "address_line_4":"Begumpet", "city":"Hyderabad", "state":"", "country": "", "country_code": "SGP", "local_code": "800003"} |

    Then I wait until max time to verify Card <card_identifier> status on card service provider Clowd9 as INACTIVE

    Then I update the status of Card with id <card_identifier>
      | card_status |
      | DISABLE     |

    Then I validate card status by fetching card with id <card_identifier> and checking card status as DISABLED

    Examples:
      | card_identifier | card_type | emboss_name |
      | CardId1         | PHYSICAL  | Sasuke      |

#    Invalid permutations
  Scenario Outline: Updating Card Status from Disabled on provider Clowd9
    Given I issue Card for Card Account on provider Clowd9
      | card_identifier   | card_account_identifier | card_type   | emboss_name   | validity_in_months | three_d_secure_config                                                  | delivery_address                                                                                                                                                                                                                                      |
      | <card_identifier> | CardAccId1              | <card_type> | <emboss_name> | 60                 | {"security_question": "What is your name?", "security_answer": "John"} | {"address_line_1":"Atlas Consolidated Labs", "address_line_2":"Mukunda Towers", "address_line_3":"Indian Airlines Colony", "address_line_4":"Begumpet", "city":"Hyderabad", "state":"", "country": "", "country_code": "SGP", "local_code": "800003"} |

    Then I wait until max time to verify Card <card_identifier> status on card service provider Clowd9 as INACTIVE

    Then I activate the Card
      | card_identifier   |
      | <card_identifier> |

    Then I validate card status by fetching card with id <card_identifier> and checking card status as ACTIVE

    Then I update the status of Card with id <card_identifier>
      | card_status |
      | DISABLE     |

    Then I validate card status by fetching card with id <card_identifier> and checking card status as DISABLED

    Then To test the invalid scenario, I update the status of Card with id <card_identifier>
      | card_status |
      | BLOCK       |
      | UNBLOCK     |

    Then I validate card status by fetching card with id <card_identifier> and checking card status as DISABLED

    Examples:
      | card_identifier | card_type | emboss_name |
      | CardId1         | PHYSICAL  | Sasuke      |

  Scenario Outline: Activating the Blocked Card on provider Clowd9
    Given I issue Card for Card Account on provider Clowd9
      | card_identifier   | card_account_identifier | card_type   | emboss_name   | validity_in_months | three_d_secure_config                                                  | delivery_address                                                                                                                                                                                                                                      |
      | <card_identifier> | CardAccId1              | <card_type> | <emboss_name> | 60                 | {"security_question": "What is your name?", "security_answer": "John"} | {"address_line_1":"Atlas Consolidated Labs", "address_line_2":"Mukunda Towers", "address_line_3":"Indian Airlines Colony", "address_line_4":"Begumpet", "city":"Hyderabad", "state":"", "country": "", "country_code": "SGP", "local_code": "800003"} |

    Then I wait until max time to verify Card <card_identifier> status on card service provider Clowd9 as INACTIVE

    Then I activate the Card
      | card_identifier   |
      | <card_identifier> |

    Then I validate card status by fetching card with id <card_identifier> and checking card status as ACTIVE

    Then I update the status of Card with id <card_identifier>
      | card_status |
      | BLOCK       |

    Then I validate card status by fetching card with id <card_identifier> and checking card status as BLOCKED

    Then I activate the Card
      | card_identifier   |
      | <card_identifier> |

    Then I validate card status by fetching card with id <card_identifier> and checking card status as BLOCKED

    Examples:
      | card_identifier | card_type | emboss_name |
      | CardId1         | PHYSICAL  | Sasuke      |

  Scenario Outline: Activating the disabled Card on provider Clowd9
    Given I issue Card for Card Account on provider Clowd9
      | card_identifier   | card_account_identifier | card_type   | emboss_name   | validity_in_months | three_d_secure_config                                                  | delivery_address                                                                                                                                                                                                                                      |
      | <card_identifier> | CardAccId1              | <card_type> | <emboss_name> | 60                 | {"security_question": "What is your name?", "security_answer": "John"} | {"address_line_1":"Atlas Consolidated Labs", "address_line_2":"Mukunda Towers", "address_line_3":"Indian Airlines Colony", "address_line_4":"Begumpet", "city":"Hyderabad", "state":"", "country": "", "country_code": "SGP", "local_code": "800003"} |

    Then I wait until max time to verify Card <card_identifier> status on card service provider Clowd9 as INACTIVE

    Then I activate the Card
      | card_identifier   |
      | <card_identifier> |

    Then I validate card status by fetching card with id <card_identifier> and checking card status as ACTIVE

    Then I update the status of Card with id <card_identifier>
      | card_status |
      | DISABLE     |

    Then I validate card status by fetching card with id <card_identifier> and checking card status as DISABLED

    Then I activate the Card
      | card_identifier   |
      | <card_identifier> |

    Then I validate card status by fetching card with id <card_identifier> and checking card status as DISABLED

    Examples:
      | card_identifier | card_type | emboss_name |
      | CardId1         | PHYSICAL  | Sasuke      |

  Scenario Outline: Blocking an inactive card on provider Clowd9
    Given I issue Card for Card Account on provider Clowd9
      | card_identifier   | card_account_identifier | card_type   | emboss_name   | validity_in_months | three_d_secure_config                                                  | delivery_address                                                                                                                                                                                                                                      |
      | <card_identifier> | CardAccId1              | <card_type> | <emboss_name> | 60                 | {"security_question": "What is your name?", "security_answer": "John"} | {"address_line_1":"Atlas Consolidated Labs", "address_line_2":"Mukunda Towers", "address_line_3":"Indian Airlines Colony", "address_line_4":"Begumpet", "city":"Hyderabad", "state":"", "country": "", "country_code": "SGP", "local_code": "800003"} |

    Then I wait until max time to verify Card <card_identifier> status on card service provider Clowd9 as INACTIVE

    Then To test the invalid scenario, I update the status of Card with id <card_identifier>
      | card_status |
      | BLOCK       |

    Then I validate card status by fetching card with id <card_identifier> and checking card status as INACTIVE

    Examples:
      | card_identifier | card_type | emboss_name |
      | CardId1         | PHYSICAL  | Sasuke      |

  Scenario Outline: Attempting to activate card with invalid activation token on provider Clowd9
    Given I issue Card for Card Account on provider Clowd9
      | card_identifier   | card_account_identifier | card_type   | emboss_name   | validity_in_months | three_d_secure_config                                                  | delivery_address                                                                                                                                                                                                                                      |
      | <card_identifier> | CardAccId1              | <card_type> | <emboss_name> | 60                 | {"security_question": "What is your name?", "security_answer": "John"} | {"address_line_1":"Atlas Consolidated Labs", "address_line_2":"Mukunda Towers", "address_line_3":"Indian Airlines Colony", "address_line_4":"Begumpet", "city":"Hyderabad", "state":"", "country": "", "country_code": "SGP", "local_code": "800003"} |

    Then I wait until max time to verify Card <card_identifier> status on card service provider Clowd9 as INACTIVE

    Then I attempt to activate the card <card_identifier> with token 123456789 and verify activation failed with CDSM_9408

    Then I validate card status by fetching card with id <card_identifier> and checking card status as INACTIVE

    Examples:
      | card_identifier | card_type | emboss_name |
      | CardId1         | PHYSICAL  | Sasuke      |

  Scenario Outline: Get Secure Card Detail from provider Clowd9
    Given I issue Card for Card Account on provider Clowd9
      | card_identifier   | card_account_identifier | card_type   | emboss_name   | validity_in_months | three_d_secure_config                                                  | delivery_address                                                                                                                                                                                                                                      |
      | <card_identifier> | CardAccId1              | <card_type> | <emboss_name> | 60                 | {"security_question": "What is your name?", "security_answer": "John"} | {"address_line_1":"Atlas Consolidated Labs", "address_line_2":"Mukunda Towers", "address_line_3":"Indian Airlines Colony", "address_line_4":"Begumpet", "city":"Hyderabad", "state":"", "country": "", "country_code": "SGP", "local_code": "800003"} |

    Then I wait until max time to verify Card <card_identifier> status on card service provider Clowd9 as INACTIVE

    Given I get Secure Card Detail with id <card_identifier>

    Examples:
      | card_identifier | card_type | emboss_name |
      | CardId1         | PHYSICAL  | Sasuke      |

