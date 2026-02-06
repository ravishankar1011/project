Feature: CMS service's Product scenarios

  Background: Set Up Customer Profile

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

  Scenario: Successfully Approve a Product

    Then I create bucket config for product Pid1 and verify status code is 200
      | bucket_name              | bucket_code | txn_codes  | interest_type     | repayment_priority | limit_percentage | apr  |
      | Standard Interest Bucket | STD_001     | TXN1, TXN2 | STANDARD_INTEREST | 1                  | 50.0             | 10.5 |

    Then I approve following products and verify product status to be PRODUCT_SUCCESS and status code is 200
      | product_id |
      | Pid1       |

  Scenario Outline:Attempt to Create Products with Invalid Inputs

    Then I create following products and verify product status to be PRODUCT_DRAFT and status code is <status_code>
      | product_id | product_name   | product_type   | description                               | product_class | profile_type | product_category | param_group   |
      | Pid2       | My Credit Card | CREDIT_ACCOUNT | Premium Credit Card for Premium Customers | STANDARD      | CUSTOMER     | GEN              | <param_group> |

    Examples:
      | param_group                                 | status_code |
      | invalid_billing_date                        | E9400       |
      | invalid_annual_percentage_rate_range        | E9400       |
      | invalid_billing_frequency                   | E9400       |
      | missing_min_or_max_value_for_range_integers | E9400       |
      | empty_string_list                           | E9400       |


  Scenario: Invalid Product Approval Attempt with Insufficient Details

    Then I create following products and verify product status to be PRODUCT_DRAFT and status code is 200
      | product_id | product_name   | product_type   | description                               | product_class | profile_type | product_category | param_group         |
      | Pid1       | My Credit Card | CREDIT_ACCOUNT | Premium Credit Card for Premium Customers | STANDARD      | CUSTOMER     | GEN              | insufficient_detail |

    Then I create bucket config for product Pid1 and verify status code is 200
      | bucket_name              | bucket_code | txn_codes  | interest_type     | repayment_priority | limit_percentage | apr  |
      | Standard Interest Bucket | STD_001     | TXN1, TXN2 | STANDARD_INTEREST | 1                  | 50.0             | 10.5 |

    Then I approve following products and verify product status to be PRODUCT_SUCCESS and status code is CMSM_9695
      | product_id |
      | Pid1       |

  Scenario Outline: Update Product Details and Verify Changes

    Then I update the following products and verify the response status is <status_code>
      | product_id   | product_name   | product_description   | param_group   |
      | <product_id> | <product_name> | <product_description> | <param_group> |

    Then I fetch and verify the updated products given the status code is <status_code>
      | product_id   | product_name   | description           | param_group   |
      | <product_id> | <product_name> | <product_description> | <param_group> |

    Examples:
      | product_id | product_description             | product_name       | param_group         | status_code |
      | Pid1       | Updated description for product | My New Credit Card | update_params_group | 200         |
