import pytest


@pytest.mark.asyncio
async def test_add_new_user(rep_controller):
    if not await rep_controller.get_user(1):
        await rep_controller.add_new_user(1)

    assert await rep_controller.get_user(1)
