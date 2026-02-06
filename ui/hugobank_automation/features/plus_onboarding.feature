Feature: Plus onboarding

  Scenario: Validate Upload document screen by selecting I earn as sources of funds
    Given I sign up with bypass number
        | mobile_prefix |  name  | place_of_birth | maiden_name |
        | +9247         | Ishaa  | Sector 17B     | Fernandez   |
    Then I navigate to source of incoming funds screen
    When I select I earn
    And I select Income options
    Then I click Continue
    Then I give details
        | name |  line1    | Line2       | city     | postal code|
        | John | street 5  | Apartment 4B| sydney   | 12345      |
    And I click continue to upload documents
    Then I should navigate to upload document screen
    Then I click back button
    Then I click back button
    And I select Income options
    When I select source of incoming funds freelance
    And I click Continue
    Then I choose Airline
    Then I click Continue
    And I click continue to upload documents
    Then I should navigate to upload document screen
    Then I click back button
    Then I click back button
    When I select source of incoming funds freelance
    When I select source of incoming funds inheritance
    And I click Continue
    And I click continue to upload documents
    Then I should navigate to upload document screen

  Scenario: Validate Upload document screen by selecting funded by sponsor as sources of funds
    Given I sign up with bypass number
        | mobile_prefix |  name  | place_of_birth | maiden_name |
        | +9247         | Ishaa  | Sector 17B     | Fernandez   |
    Then I navigate to source of incoming funds screen
    When I select Iam funded by sponsor
    And I select student
    And I click Continue
    Then I should navigate to upload document screen
    Then I click back button
    When I select unemployed
    And I click Continue
    Then I enter sponsor name Jin
    Then I select relationship with sponsor
    And I select Income options
    When I click Continue
    When I give details
        | name |  line1    | Line2       | city     | postal code|
        | John | street 5  | Apartment 4B| sydney   | 12345      |
    And I click continue to upload documents
    Then I should navigate to upload document screen

  Scenario: When range not selected and all required sponsor's details are not provided after selecting unemployed
    Given I sign up with bypass number
        | mobile_prefix |  name  | place_of_birth | maiden_name |
        | +9247         | Ishaa  | Sector 17B     | Fernandez   |
     When I click on unlock more
     And I click upgrade to plus button
     Then The continue button is disabled
     Then I click back button
     And I click upgrade to plus button
     When I check dual declaration checkbox
     Then The continue button is disabled
     Then I click back button
     And I click upgrade to plus button
     When I select Incoming PKR
     And I select outgoing PKR
     Then The continue button is disabled
     When I check dual declaration checkbox
     Then I click Continue
     Then The continue button is disabled in source of funds screen
     When I select Iam funded by sponsor
     When I select unemployed
     Then I click Continue
     When I enter sponsor name Jin
     Then The continue button is disabled
     Then I clear sponsor name input
     When I select source of income
     Then The continue button is disabled
     When I enter sponsor name Jin
     Then The continue button is disabled
     Then I clear sponsor name input
     When I select source of income
     When I choose relationship with sponsor
     Then The continue button is disabled
     When I enter sponsor name Jin
     Then The continue button is disabled
     Then I clear sponsor name input
     When I select source of income
     Then The continue button is disabled

  Scenario: when all required sponsor's details are not provided after selecting I earn
    Given I sign up with bypass number
       | mobile_prefix |  name  | place_of_birth | maiden_name |
       | +9247         | Ishaa  | Sector 17B     | Fernandez   |
     Then I navigate to source of incoming funds screen
     When I select I earn
     And I select Income options
     Then I click Continue
     When I choose Airline
     When I enter sponsor name Jin123
     Then Error text should appear
     And I give sponsor details then continue button should disable
        | name |  line1    | Line2       | city     | postal code|
        | John | street 5  | Apartment 4B| sydney   |   12345    |
