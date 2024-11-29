import logging
import sys
from gunicorn.arbiter import Arbiter
from uvicorn_worker import UvicornWorker
from simplerest.settings import LOGGING
from uvicorn.server import Server
import asyncio
from asyncio import current_task, all_tasks, as_completed, Task

class MyTask(Task):
    def __init__(self, coro, *, loop) -> None:
        print(f"task started {coro.__name__}")
        super().__init__(coro, loop=loop)
        #self.print_stack

    def __del__(self) -> None:
        print("task finished")
        return super().__del__()

class MyUvicornWorker(UvicornWorker):
    CONFIG_KWARGS = {
        "loop": "asyncio",  ## test uvloop performance
        "http": "auto",
        "lifespan": "off",
        "log_config": LOGGING,
        "limit_concurrency": 30, ## issues with limit_concurrency = 10 it's created 2 tasks for each connection _accept_connection2, run_asgi
        #"timeout_graceful_shutdown": 15,
        #"timeout_keep_alive": 15,
    }

    async def monitor(self, server) -> None:
        while True:
            await asyncio.sleep(0.1)
            #print(f"len = {len(server.server_state.connections)}")
            #print([ f"{conn.client if conn.client else ''}" for conn in server.server_state.connections])
            #print([ f"{task.get_name()}" for task in server.server_state.tasks])

            # server_state stores only open connections and running tasks

    def install_task_factory(self):
        loop = asyncio.get_running_loop()
        def factory(loop, coro, context=None):
            return MyTask(coro, loop=loop)
        loop.set_task_factory(factory)


    async def _serve(self) -> None:
        current_task().set_name("server")
        self.config.app = self.wsgi
        server = Server(config=self.config)
        self._install_sigquit_handler()
        self.install_task_factory()
        #asyncio.create_task(self.monitor(server), name="monitor")
        await server.serve(sockets=self.sockets)
        if not server.started:
            sys.exit(Arbiter.WORKER_BOOT_ERROR)

    def run(self) -> None:
        return asyncio.run(self._serve(), debug=True)
