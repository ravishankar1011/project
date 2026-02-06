from behave import *
import tests.api.distribute.app_helper as ah
from tests.util.common_util import check_status_distribute

use_step_matcher("re")


@Step("I reward gold worth ([^']*) SGD for user ([^']*)")
def reward_gold_for_user(context, amount, uid):
    request = context.request

    data = {
        "amount": amount,
        "reward_id": ah.get_uuid(),
        "user_reward_id": ah.get_uuid(),
        "reward_source": "Hugosave",
        "source_id": ah.get_uuid(),
    }

    response = request.hugosave_post_request(
        ah.reward_urls["gold"],
        data=data,
        headers=ah.get_user_header(context, uid),
    )
    assert check_status_distribute(response, "200")


@Step("I deposit ([^']*) SGD in HUGOSAVE account type ([^']*) for user ([^']*)")
def deposit_hugosave_account(context, amount, acc_type ,uid):
    request = context.request

    response = request.hugosave_put_request(
        path=ah.dev_urls["deposit_hugosave_account"],
        data={"account_type": acc_type, "amount": float(amount)},
        headers=ah.get_user_header(context, uid),
    )
    assert check_status_distribute(response, "200")

@Step("I get the unlocked rewards for user ([^']*)")
def get_user_rewards(context, uid):
    request = context.request

    response = request.hugosave_get_request(
        path = ah.reward_urls["unlocked"],
        headers=ah.get_user_header(context, uid),
    )
    assert check_status_distribute(response, "200")

    for reward in response["data"]["userRewards"]:
        if not (reward["rewardStage"] == "UNLOCKED"):
          assert False,"Reward not unlocked"

    context.data["users"][uid]["userRewards"] = response["data"]["userRewards"]

@Step("I claim the reward for user ([^']*)")
def claim_reward(context, uid):
    request = context.request
    reward_id = ah.get_reward_id(context,uid)

    response = request.hugosave_post_request(
        path = ah.reward_urls["claim"].replace("{user-reward-id}",reward_id),
        headers = ah.get_user_header(context, uid)
    )

    assert check_status_distribute(response, "200")
    context.data["users"][uid]["rewardValue"] = response["data"]["value"]
