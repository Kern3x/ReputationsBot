import pytest


@pytest.mark.asyncio
async def test_reduce_rep(rep_controller):
    if not await rep_controller.get_user(1):
        await rep_controller.add_new_user(1)

    rep_old = (await rep_controller.get_user(1)).reputation
    await rep_controller.reduce_rep(1, "some reason")
    rep_new = (await rep_controller.get_user(1)).reputation

    assert rep_new < rep_old
    assert await rep_controller.get_reduce_rep_history(1)
