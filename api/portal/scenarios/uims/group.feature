Feature: Group

  Background:
    Given I logged in with credentials
      | username                     | password |
      | mrityunjay.kumar@hugohub.com | abcd     |

  Scenario: Create group and update their details
    When I create a role RID1 with following details
      | role_name | description |
      | it role   | it role     |

    Then I create a group GID1 with role RID1
      | group_name | description |
      | group name | group description |

    When I create a role RID2 with following details
      | role_name | description |
      | it role   | it role     |

    Then I update group_name, group_description of group GID1 and verified the updated details
      | group_name          | group_description |
      | updated group mame  | update group description |

    Then I update role as RID2 of group GID1 and verified the updated details
