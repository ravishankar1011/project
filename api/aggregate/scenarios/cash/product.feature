Feature: Cash service CustomerProfile, EndCustomerProfile Products

  Background: Setup CustomerProfile and EndCustomerProfile profile onto cash

    #CustomerProfile verifying and Onboarding on to banking service on given providers
    Given I set and verify customer CId1, customer profile CPId1 on cash service on below providers and expect status 200 in the context
      | provider_name |
      | DBS Bank Ltd  |

    Then I wait until max time to verify CustomerProfile CPId1 onboard status as ONBOARD_SUCCESS

    Then I create below End-Customer-Profile
      | customer_identifier | customer_profile_identifier | end_customer_profile_identifier | first_name | last_name | region | email   | phone_number |
      | CId1                | CPId1                       | ECPId1                          | cash       | service   | SG     | x@y.com | 00000000     |

    Then I verify End-Customer-Profile exist with values
      | customer_profile_identifier | end_customer_profile_identifier | customer_profile_id   | first_name | last_name | email   | phone_number | status |
      | CPId1                       | ECPId1                          | <customer_profile_id> | cash       | service   | x@y.com | 00000000     | ACTIVE |

    # EndCustomerProfile Onboarding
    Given I onboard EndCustomerProfile ECPId1 of CustomerProfile CPId1 on cash service on below providers and expect status 200
      | provider_name |
      | DBS Bank Ltd  |

    Then I wait until max time to verify EndCustomerProfile ECPId1 of CustomerProfile CPId1 onboard status as ONBOARD_SUCCESS

  Scenario Outline: Create Cash Wallet and Cash Account Products
    Given I create a product with customer profile <customer_profile_identifier> provider as <provider> and expect product_status PRODUCT_DRAFT
      | identifier | product_type | profile_type | product_class | currency   | country   | account_type | minimum_balance_limit | minimum_balance_policy |
      | ProductID1 | CASH_WALLET  | CUSTOMER     | STANDARD      | <currency> | <country> | SAVINGS      | 0                     | STRICT                 |

    Then I approve the product ProductID1 and verify status as PRODUCT_SUCCESS with provider <provider> for customerProfileId <customer_profile_identifier>

    Given I create a cash account product with customer profile CPId1 provider as DBS Bank Ltd and expect product_status PRODUCT_DRAFT
      | identifier | product_type | profile_type | product_class | max_active_cash_wallets | primary_currency | supported_currencies |
      | ProductID2 | CASH_ACCOUNT | CUSTOMER     | STANDARD      | 1                       | SGD              | SGD                  |

    Then I approve the product ProductID2 and verify status as PRODUCT_SUCCESS with provider <provider> for customerProfileId <customer_profile_identifier>

    Examples:
      | customer_profile_identifier | provider     | currency | country |
      | CPId1                       | DBS Bank Ltd | SGD      | SGP     |
