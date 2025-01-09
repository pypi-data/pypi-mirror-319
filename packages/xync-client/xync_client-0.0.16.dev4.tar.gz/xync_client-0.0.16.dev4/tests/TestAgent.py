import logging

import pytest
from xync_schema.enums import ExStatus, ExAction
from xync_schema.models import Ex, TestEx

from xync_client.Abc.BaseTest import BaseTest
from xync_client.Abc.Agent import BaseAgentClient
from xync_client.Abc.Base import BaseClient, DictOfDicts, ListOfDicts
from xync_client.TgWallet.ex import ExClient


@pytest.mark.asyncio(loop_scope="session")
class TestAgent(BaseTest):
    @pytest.fixture(scope="class", autouse=True)
    async def clients(self) -> list[BaseClient]:
        exs = await Ex.filter(status__gt=ExStatus.plan).prefetch_related("agents__ex")
        clients: list[BaseAgentClient] = [[ag for ag in ex.agents if ag.auth].pop().client() for ex in exs]
        yield clients
        [await cl.close() for cl in clients]

    # 0
    async def test_get_orders(self, clients: list[BaseAgentClient]):
        for client in clients:
            get_orders: ListOfDicts = await client.get_orders()
            ok = self.is_list_of_dicts(get_orders, False)
            t, _ = await TestEx.update_or_create({"ok": ok}, ex_id=client.agent.ex_id, action=ExAction.get_orders)
            assert t.ok, "No get orders"
            logging.info(f"{client.agent.ex_id}:{ExAction.get_orders.name} - ok")

    # 1
    async def test_order_request(self, clients: list[BaseAgentClient]):
        for client in clients:
            await client.agent.fetch_related('ex', 'ex__agents')
            ex_client: ExClient = client.agent.ex.client()
            ads = await ex_client.ads('USDT', 'RUB', True)
            for ad in ads:
                order_request: dict | bool = await client.order_request(ad['id'], ad['orderAmountLimits']['min'])
                if order_request:
                    continue
            ok = isinstance(order_request, dict)
            t, _ = await TestEx.update_or_create({"ok": ok}, ex_id=client.agent.ex_id, action=ExAction.order_request)
            assert t.ok, "No get orders"
            logging.info(f"{client.agent.ex_id}:{ExAction.order_request.name} - ok")

    # 25
    async def test_my_fiats(self, clients: list[BaseAgentClient]):
        for client in clients:
            my_fiats: DictOfDicts = await client.my_fiats()
            ok = self.is_dict_of_dicts(my_fiats)
            t, _ = await TestEx.update_or_create({"ok": ok}, ex_id=client.agent.ex_id, action=ExAction.my_fiats)
            assert t.ok, "No my fiats"
            logging.info(f"{client.agent.ex_id}:{ExAction.my_fiats.name} - ok")
