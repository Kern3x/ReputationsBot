import pytest


@pytest.mark.integration
@pytest.mark.asyncio
async def test_reputation_flow_postgres(pg_rep_controller):
    await pg_rep_controller.ensure_user(100)
    await pg_rep_controller.ensure_user(200)

    initial_target_rep = await pg_rep_controller.get_rep(200)

    await pg_rep_controller.increase_rep(200)
    raised_target_rep = await pg_rep_controller.get_rep(200)

    await pg_rep_controller.reduce_rep(200, "spam")
    reduced_target_rep = await pg_rep_controller.get_rep(200)
    history = await pg_rep_controller.get_reduce_rep_history(200)

    assert raised_target_rep > initial_target_rep
    assert reduced_target_rep < raised_target_rep
    assert history
    assert history[0].reason == "spam"
