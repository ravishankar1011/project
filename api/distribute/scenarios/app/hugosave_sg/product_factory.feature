Feature: Product Factory Card

  Scenario Outline: Card - Create, Activate, Create transaction codes

    When I initiate the card creation from <yaml_file_name>
    Then I check the product status for <product_code>
    When I request for the activation of the product <product_code>
    And I create transaction codes for the product <product_code> from <yaml_file_name>

    Examples:
      | product_code               | yaml_file_name            |
      | CARD_PRODUCT_CARD_ACCOUNT  | card_account_product.yaml |
      | CARD_PRODUCT_PHYSICAL_CARD | card_product.yaml         |
