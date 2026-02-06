Feature: Silver module
  Background:
    Given I signup using bypass number
      | Casual Name | Legal Name    | Email          | Passcode |
      | Tony        | Tony Ferguson | tt@12gmail.com | 111111   |
    When I wait for the premium upgrade to complete
    When I deposit amount using non prod options 500
    When I move to the silver dashboard from the homescreen

  Scenario: I buy silver with balance in the save account
    When I click on the buy button
    When I enter amount 50 and click on preview
    When I click on the buy button
    Then I validate successfully bought message on the screen

  Scenario: I buy silver in grams
    When I click on the buy button
    When I switch to grams and enter 10 grams
    When I click on the preview button
    When I click on the buy button
    Then I validate successfully bought message on the screen

  Scenario: I sell silver
    When I click on the buy button
    When I enter amount 50 and click on preview
    When I click on the buy button
    Then I validate successfully bought message on the screen
    When I click on the skip button
    When I click on the sell button
    When I enter amount 5 and click on preview
    When I click on the sell button

  Scenario: I sell silver in grams
    When I click on the buy button
    When I enter amount 50 and click on preview
    When I click on the buy button
    Then I validate successfully bought message on the screen
    When I click on the skip button
    When I click on the sell button
    When I switch to grams and enter 10 grams
    When I click on the preview button
    When I click on the sell button




