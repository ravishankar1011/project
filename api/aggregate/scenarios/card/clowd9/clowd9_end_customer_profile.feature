Feature: Card Service End-Customer Profile test scenarios for provider Clowd9

  Background: Setup Customer Profile on Card Service and provider Clowd9
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

  Scenario Outline: Onboarding End-Customer Profile on Card Service and provider <provider_name> who is not onboarded on Banking Service
    Given I onboard End-Customer Profile <end_customer_profile_identifier> of Customer Profile CPID1 on fund provider CASH and on card service on provider <provider_name>

    Then I wait until max time to verify End-Customer Profile <end_customer_profile_identifier> onboard status on card service provider <provider_name> as <onboard_status>

    Examples:
      | end_customer_profile_identifier | provider_name | onboard_status  |
      | ECPID1                          | Clowd9        | ONBOARD_SUCCESS |




