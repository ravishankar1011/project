Feature: CMS Fee and Tax Scenarios

  Background: Set Up Customer Profile and Product

    Given I set and verify customer Cid1, customer profile CPid1 in the context

    Given I onboard HUGOHUB Customer Profile for CMS and verify onboard status as ONBOARD_SUCCESS

    Then I onboard Customer Profile Cid1 to CMS and verify onboard status as ONBOARD_SUCCESS

    Then I create following products and verify product status to be PRODUCT_DRAFT and status code is 200
      | product_id | product_name   | product_type   | description                               | product_class | profile_type | product_category | param_group              |
      | Pid1       | My Credit Card | CREDIT_ACCOUNT | Premium Credit Card for Premium Customers | STANDARD      | CUSTOMER     | GEN              | normal_case_params_group |

    Then I create the following transaction codes and verify status code is 200
      | transaction_code | iso_code | description            |
      | TXN1             | ISO1     | First transaction code |
      | TXN2             | ISO2     | Second one             |
      | TXN3             | ISO3     | Third transaction code |
      | TXN4             | ISO4     | Fourth one             |
      | FEE              | ISO5     | Fifth transaction code |
      | TAX              | ISO6     | Sixth Transaction Code |

    Then I create bucket config for product Pid1 and verify status code is 200
      | bucket_name               | bucket_code | txn_codes       | interest_type      | repayment_priority | limit_percentage | apr  |
      | Standard Interest Bucket  | STD_001     | TXN1, TXN2, FEE | STANDARD_INTEREST  | 1                  | 50.0             | 10.5 |
      | Immediate Interest Bucket | IMD_002     | TXN3, TXN4, TAX | IMMEDIATE_INTEREST | 2                  | 30.0             | 12.0 |

    Then I approve following products and verify product status to be PRODUCT_SUCCESS and status code is 200
      | product_id |
      | Pid1       |

  Scenario: Successful Fee Creation

    Then I create fee for the Product and verify status code as 200
      | product_id | fee_code | txn_code | fee_type   | push_overdraft | rule_group     | fee_details |
      | Pid1       | TEST_FEE | FEE      | ACTION_FEE | true           | fee_rule_group | ACTION      |

  Scenario: Fee Details Not Present -> Fee Creation Failed

    Then I create fee for the Product and verify status code as E9400
      | product_id | fee_code | txn_code | fee_type   | push_overdraft | rule_group     | fee_details |
      | Pid1       | TEST_FEE | FEE      | ACTION_FEE | true           | fee_rule_group | EMPTY       |

  Scenario: Invalid Fee Type -> Fee Creation Failed

    Then I create fee for the Product and verify status code as E9400
      | product_id | fee_code | txn_code | fee_type    | push_overdraft | rule_group     | fee_details |
      | Pid1       | TEST_FEE | FEE      | UNKNOWN_FEE | true           | fee_rule_group | EMPTY       |

  Scenario: Successful Tax Creation

    Then I create tax for the Product and verify status code as 200
      | tax_id | product_id |  | tax_code | txn_code | push_overdraft | rule_group |
      | TX1    | Pid1       |  | TEST_TAX | TAX      | true           | rule_group |

  Scenario: Create Tax (Success) -> Update Tax (Success)

    Then I create tax for the Product and verify status code as 200
      | tax_id | product_id | tax_code | txn_code | push_overdraft | rule_group |
      | TX1    | Pid1       | TEST_TAX | TAX      | true           | rule_group |

    Then I update tax for the Product and verify status code as 200 and verify the updated details
      | tax_id | tax_code | txn_code | push_overdraft | rule_group        |
      | TX1    | UPD_TAX  | TAX2     | false          | update_rule_group |
