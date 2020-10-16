import asyncio

from yapapi.log import enable_default_logger, log_summary, log_event_repr # noqa
from yapapi.runner import Engine, Task, vm
from yapapi.runner.ctx import WorkContext
from datetime import timedelta


async def main(subnet_tag='testnet'):
    package = await vm.repo(
        image_hash='1349c4db6af235533c448ee09d993fad1fce4f5db2145acdd958ca23',
        min_mem_gib=0.5,
        min_storage_gib=2.0,
    )

    async def worker(ctx: WorkContext, tasks):
        async for task in tasks:
            ctx.send_file('make.sh', '/golem/work/make.sh')
            ctx.run('/bin/sh', '/golem/work/make.sh')
            output_file = 'vim'
            ctx.download_file('/golem/work/vim/src/vim', 'vim')
            ctx.download_file('/golem/work/out.txt', 'log')
            yield ctx.commit()
            task.accept_task(result=output_file)

        ctx.log(f'VIM compiled!')

    tasks: range = range(0, 1, 1)

    async with Engine(
        package=package,
        max_workers=1,
        budget=10.0,
        timeout=timedelta(minutes=10),
        subnet_tag=subnet_tag,
        event_emitter=log_summary(log_event_repr),
    ) as engine:

        async for task in engine.map(worker, [Task(data=task) for task in tasks]):
            print(f'\033[36;1mTask computed: {task}, result: {task.output}\033[0m')


enable_default_logger()
loop = asyncio.get_event_loop()
task = loop.create_task(main(subnet_tag='devnet-alpha.2'))
try:
    asyncio.get_event_loop().run_until_complete(task)
except (Exception, KeyboardInterrupt) as e:
    print(e)
    task.cancel()
    asyncio.get_event_loop().run_until_complete(task)
