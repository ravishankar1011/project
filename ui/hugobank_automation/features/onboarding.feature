 Feature: Sign up: Create a new Account

  Scenario: Full onboarding with valid details
    Given I sign up with bypass number
          | prefix    |  name  | place_of_birth | maiden_name |
          | +9247     | Ishaa  | Sector 17B     | Fernandez   |

  Scenario: Validate empty mobile input field
    When I clear mobile number input field
    Then An error text should appear

  Scenario: Input a mobile number containing more than 10 digits
    When I enter mobile number containing more than 10 digits with prefix +9247
    Then An error text should appear

  Scenario: Disable continue button for Invalid Mobile Number
    When I enter an invalid mobile number 123
    Then The continue button should be disabled

  Scenario: Enter an Invalid OTP After a Valid Mobile Number
    When I enter the valid mobile number with prefix +9247
    Then I click on the continue button
    Then I enter OTP 123453
    Then An error message Incorrect OTP should display

  Scenario: Validate error after four invalid OTP attempts
    When I enter the valid mobile number with prefix +9247
    Then I click on the continue button
    Then I enter Invalid OTP 111111 for four times
    Then maximum attempts reached text should appear

  Scenario: Validate OTP sent SMS message
      When I enter the valid mobile number with prefix +9247
      Then I click on the continue button
      Then After 20sec Resend OTP button should appear
      When I click on Resend OTP
      Then OTP sent SMS should appear

  Scenario: Casual Name field left blank and checkbox is not selected
      When I enter the valid mobile number with prefix +9247
      Then I click on the continue button
      Then I enter OTP 123456
      Then The continue button is disabled

  Scenario: Enter Invalid casual name and select the checkbox
    When I enter the valid mobile number with prefix +9247
    Then I click on the continue button
    Then I enter OTP 123456
    When I enter casual name Jin123
    And I tick the terms checkbox
    Then An error message should be displayed
    And The continue button is disabled

  Scenario: Enter valid casual name and leave checkbox unselected
    When I enter the valid mobile number with prefix +9247
    Then I click on the continue button
    Then I enter OTP 123456
    When I enter casual name Jin
    Then The continue button is disabled

  Scenario: Account usage options are not selected
    When I enter the valid mobile number with prefix +9247
    Then I click on the continue button
    Then I enter OTP 123456
    When I enter casual name Jin
    And I tick the terms checkbox
    When I click Continue
    Then The continue button is disabled in account usage options screen

  Scenario: Enter mismatched passcodes
    When I enter the valid mobile number with prefix +9247
    Then I click on the continue button
    Then I enter OTP 123456
    When I enter casual name Jin
    And I tick the terms checkbox
    When I click Continue
    When I select usage options
    When I click Continue
    When I enter passcodes in both fields
      | passcode1   | passcode2 |
      | 111111      | 123456   |
    Then Passcode error text should display

  Scenario: Validate error when both Place of Birth and Mother's Maiden Name fields are empty
    When I enter the valid mobile number with prefix +9247
    Then I click on the continue button
    Then I enter OTP 123456
    When I enter casual name Jin
    And I tick the terms checkbox
    When I click Continue
    When I select usage options
    When I click Continue
    When I enter passcodes in both fields
      | passcode1   | passcode2 |
      | 123456      | 123456    |
    When I click Continue
    Then The continue button is disabled in security questions screen

  Scenario: Validate with missing Mother's Maiden Name and valid Place of Birth
    When I enter the valid mobile number with prefix +9247
    Then I click on the continue button
    Then I enter OTP 123456
    When I enter casual name Jin
    And I tick the terms checkbox
    When I click Continue
    When I select usage options
    When I click Continue
    When I enter passcodes in both fields
      | passcode1   | passcode2 |
      | 123456      | 123456    |
    When I click Continue
    When I enter place of birth Sector 17B
    Then The continue button is disabled

  Scenario: Validate with missing Place of Birth and valid Mother's Maiden Name
    When I enter the valid mobile number with prefix +9247
    Then I click on the continue button
    Then I enter OTP 123456
    When I enter casual name Jin
    And I tick the terms checkbox
    When I click Continue
    When I select usage options
    When I click Continue
    When I enter passcodes in both fields
      | passcode1   | passcode2 |
      | 123456      | 123456    |
    When I click Continue
    When I enter Maiden name Fernandez
    Then The continue button is disabled

  Scenario: Enter invalid Mother's maiden name
    When I enter the valid mobile number with prefix +9247
    Then I click on the continue button
    Then I enter OTP 123456
    When I enter casual name Jin
    And I tick the terms checkbox
    When I click Continue
    When I select usage options
    When I click Continue
    When I enter passcodes in both fields
      | passcode1   | passcode2 |
      | 123456      | 123456    |
    When I click Continue
    When I enter the personal details
    | place_of_birth   | mother_maiden_name |
    | Sector 17B       | Fernandez12 |
    Then I validate that error message appear for invalid Mother's maiden name
    And The continue button is disabled
