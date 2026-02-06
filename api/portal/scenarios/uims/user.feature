Feature: User

  Background:
    Given I logged in with credentials
      | username                     | password |
      | mrityunjay.kumar@hugohub.com | abcd     |

  Scenario: Successfully create an operator and update user info
    When I create a role RID1 with following details
      | role_name | description |
      | it role   | it role     |
    When I create a group GID1 with role none
      | group_name           | description |
      | it create user group | group       |
    When I create an operator UID1 with role RID1 and group GID1
       | first_name | last_name | email   | phone_number |
       | John       | Doe       | random  | +92123456789 |

    Then I fetch user UID1 and verified the details

    When I create a group GID2 with role none
      | group_name  | description |
      | new group   | group       |

    Then I update group of user UID1 to GID2

    When I create a role RID2 with following details
      | role_name        | description    |
      | update it role   | update it role |

    Then I update role of user UID1 to RID2

    Then I fetch user UID1 and verified GID2 and RID2 is present or not
