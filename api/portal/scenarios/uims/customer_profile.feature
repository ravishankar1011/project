Feature: Customer profile

  Background:
    Given I logged in with credentials
      | username                     | password |
      | mrityunjay.kumar@hugohub.com | abcd     |

  Scenario: Onboard a customer and update their details
    When I onboard a new customer CPID1 with the following details
      | name            | corporate_email   | phone_number  | theme  | logo_url             | admin_first_name  | admin_last_name   | admin_email | admin_phone_number  | regex     | length | require_special_characters | require_numbers | require_uppercase | allowed_special_characters | idle_time_threshold_in_minutes | max_failed_attempts | lock_time_duration  | allowed_domains              |
      | it customer     | random            | +911234567890 | dark   | http://logo.url/acme | it customer       | profile           | random      | +919876543210       | ^[a-z]+$  | 8      | true                       | true            | true              | !@#%&*                     | 15                             | 5                   | 2                   | hugohub.com, hugosave.com    |

    Then I update the following details of customer CPID1 and verified updated details
      | name         | corporate_email    | phone_number |  regex     | length | require_special_characters | require_numbers | require_uppercase | allowed_special_characters | idle_time_threshold_in_minutes | max_failed_attempts | lock_time_duration | allowed_domains   |
      | Acme Updated | updated@acme.com   | 9876543210   | ^[a-z]+$  | 10     | true                       | true            | true              | !@#$%^&*                   | 30                              | 3                  | 6                    | acme.com,acme.org |
