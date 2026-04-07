import pytest


@pytest.mark.asyncio
async def test_increase_rep(rep_controller):
    if not await rep_controller.get_user(1):
        await rep_controller.add_new_user(1)

    rep_old = (await rep_controller.get_user(1)).reputation
    await rep_controller.increase_rep(1)
    rep_new = (await rep_controller.get_user(1)).reputation

    assert rep_new > rep_old
