Feature: Role Management

  Background:
    Given I logged in with credentials
      | username                     | password  |
      | mrityunjay.kumar@hugohub.com | abcd      |

  Scenario: Create role and update role info
    When I create a role RID1 with following details
      | role_name | description |
      | it role   | it role     |

    When I update the role RID1 with the following details and verified updated details
      | role_name      | description |
      | update it role | updated role description |

  Scenario:  Create role with permission
    Given I fetch all the permissions the logged-in user has

    Given I create a group GID1 with role none
      | group_name       | description |
      | it checker group | it checker group |

    When I create a role RID1 with permission and checker_group as GID1

    Then I fetched the permission of RID1 and verified
