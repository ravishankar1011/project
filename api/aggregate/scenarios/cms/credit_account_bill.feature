Feature: CMS service's Credit Account Bill Generation scenarios

  Background: Set Customer Profile

    Given I register KMS Namespace for CMS and verify status code as 200

    Given I set and verify customer Cid1, customer profile CPid1 in the context

    Given I onboard HUGOHUB Customer Profile for CMS and verify onboard status as ONBOARD_SUCCESS

    Then I onboard Customer Profile Cid1 to CMS and verify onboard status as ONBOARD_SUCCESS

    Then I create below End-Customer-Profile
      | customer_identifier | customer_profile_identifier | end_customer_profile_identifier | first_name | last_name | region | email         | phone_number   |
      | Cid1                | CPid1                       | ECPid1                          | John       | Snow      | SG     | john@snow.com | +63 1234567890 |

    Then I verify End-Customer-Profile exist with values
      | customer_profile_identifier | end_customer_profile_identifier | first_name | last_name | email         | phone_number   | status |
      | CPid1                       | ECPid1                          | John       | Snow      | john@snow.com | +63 1234567890 | ACTIVE |

    Then I onboard End Customer Profile ECPid1 to CMS and verify onboard status as ONBOARD_SUCCESS and status code as 200

    Then I create following products and verify product status to be PRODUCT_DRAFT and status code is 200
      | product_id | product_name   | product_type   | description                               | product_class | profile_type | product_category | param_group              |
      | Pid1       | My Credit Card | CREDIT_ACCOUNT | Premium Credit Card for Premium Customers | STANDARD      | CUSTOMER     | GEN              | normal_case_params_group |

    Then I create the following transaction codes and verify status code is 200
      | transaction_code | iso_code | description            |
      | TXN1             | ISO1     | First transaction code |
      | TXN2             | ISO2     | Second one             |
      | TXN3             | ISO3     | Third transaction code |
      | TXN4             | ISO4     | Fourth one             |

    Then I create bucket config for product Pid1 and verify status code is 200
      | bucket_name               | bucket_code | txn_codes  | interest_type      | repayment_priority | limit_percentage | apr  |
      | Standard Interest Bucket  | STD_001     | TXN1, TXN2 | STANDARD_INTEREST  | 1                  | 50.0             | 12.0 |
      | Immediate Interest Bucket | IMD_002     | TXN3, TXN4 | IMMEDIATE_INTEREST | 2                  | 30.0             | 12.0 |

    Then I approve following products and verify product status to be PRODUCT_SUCCESS and status code is 200
      | product_id |
      | Pid1       |

  Scenario: Successful Bill generation

    Then I create below credit accounts and verify account status is ACCOUNT_CREATED and status code is 200
      | end_customer_profile_id | account_id | product_id | country | currency | approved_limit | status_code | interest_rate |
      | ECPid1                  | CAid1      | Pid1       | SGP     | SGD      | 10000          | 200         | 10            |

    Given I have mocked the following transactions for CAid1 in the current billing cycle and status code is 200
      | amount | txn_type | day | months_to_shift | month_direction | txn_code | txn_status          |
      | 100    | DEBIT    | 5   | 1               | PAST            | TXN3     | TRANSACTION_SETTLED |
      | 150    | DEBIT    | 10  | 1               | PAST            | TXN3     | TRANSACTION_SETTLED |

    Then I Wait some time to get the transactions updated

    When I generate the credit bill for account CAid1 and verify status code is 200
      | tad |
      | 1   |

  Scenario: Bill Generation Failed For Closed Credit Account

    Then I create below credit accounts and verify account status is ACCOUNT_CREATED and status code is 200
      | end_customer_profile_id | account_id | product_id | country | currency | approved_limit | interest_rate |
      | ECPid1                  | CAid1      | Pid1       | SGP     | SGD      | 10000          | 10            |

    Given I attempt to close the following credit accounts and verify status code is 200
      | account_id |
      | CAid1      |

    When I generate the credit bill for account CAid1 and verify status code is CMSM_9648

  Scenario: Bill Generation Failed for Unknow Credit Account

    When I generate the credit bill for account CAid2 and verify status code is CMSM_9641

  Scenario: Bill Generation Successful for no transactions being made in the current billing cycle

    Then I create below credit accounts and verify account status is ACCOUNT_CREATED and status code is 200
      | end_customer_profile_id | account_id | product_id | country | currency | approved_limit | interest_rate |
      | ECPid1                  | CAid1      | Pid1       | SGP     | SGD      | 10000          | 10            |

    When I generate the credit bill for account CAid1 and verify status code is 200
      | tad |
      | 0   |
