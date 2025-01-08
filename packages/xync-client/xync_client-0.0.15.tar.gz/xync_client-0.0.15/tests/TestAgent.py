import logging

import pytest
from xync_schema.enums import ExStatus, ExAction
from xync_schema.models import Ex, TestEx

from xync_client.Abc.BaseTest import BaseTest
from xync_client.Abc.Agent import BaseAgentClient
from xync_client.Abc.Base import BaseClient, MapOfIdsList


@pytest.mark.asyncio(loop_scope="session")
class TestAgent(BaseTest):
    @pytest.fixture(scope="class", autouse=True)
    async def clients(self) -> list[BaseClient]:
        exs = await Ex.filter(status__gt=ExStatus.plan).prefetch_related("agents__ex")
        clients: list[BaseAgentClient] = [[ag for ag in ex.agents if ag.auth].pop().client() for ex in exs]
        yield clients
        [await cl.close() for cl in clients]

    # 0
    async def test_my_fiats(self, clients: list[BaseAgentClient]):
        for client in clients:
            my_fiats: MapOfIdsList = await client.my_fiats()
            ok = self.is_map_of_ids(my_fiats)
            t, _ = await TestEx.update_or_create({"ok": ok}, ex_id=client.agent.ex_id, action=ExAction.my_fiats)
            assert t.ok, "No my fiats"
            logging.info(f"{client.agent.ex_id}:{ExAction.my_fiats.name} - ok")
