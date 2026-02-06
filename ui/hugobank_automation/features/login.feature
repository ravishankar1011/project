Feature: Login of existing user

  Scenario: Login of existing user
    Given I sign up with bypass number
      | mobile_prefix |  name  | place_of_birth | maiden_name |
      | +9247         | Ishaa  | Sector 17B     | Fernandez   |
    When I click on profile icon
    And I click on logout
    When I enter mobile number
    When I click on the continue button
    When I enter the OTP
    And I enter passcode 123456
    When I click Allow notifications button
    Then I should be navigated to Home page
    When App gets opened
    And I authenticate with passcode 123456
    Then I should be navigated to Home page

  Scenario: Reset Passcode while Login
    Given I sign up with bypass number
      | mobile_prefix |  name  | place_of_birth | maiden_name |
      | +9247         | Ishaa  | Sector 17B     | Fernandez   |
    When I click on profile icon
    And I click on logout
    When I enter mobile number
    When I click on the continue button
    When I enter the OTP
    And I enter passcode 111111
    Then Incorrect passcode error text should appear
    When I click on Forgot Passcode
    Then I click Continue
    When I provide the reset-passcode OTP
    And I enter passcodes in both fields
      | passcode1   | passcode2 |
      | 111111      | 111111    |
    Then I click Continue
    When I enter mobile number
    When I click on the continue button
    When I enter the OTP
    And I enter passcode 111111
    When I click Allow notifications button
    Then I should be navigated to Home page
