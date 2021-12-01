# Helper
Helper functions for machine learning models

* timer
    * Timer
    ```python
    from helper.timer import Timer

    timer = Timer()
    with timer.start():
        # run your code
        pass

    print(f"Elapse: {timer.diff}s")
    timer.reset()

    for i in range(5):
        with timer.start():
            # run your code
            pass
    print(f"Second per call: {timer.spc}s/iter")
    print(f"Call per second: {timer.cps}iter/s")
    ```
* loggers
    * get_global_logger
    ```python
    from helper.loggers import get_global_logger

    logger = get_global_logger(name="ExpName")
    logger.info("Results: 0.5")

    # Outputs
    # 2021-12-01 17:02:22 I Results: 0.5
    ```
* metrics
    * Accumulator
    ```python
    from helper.metrics import Accumulator

    accu = Accumulator(loss1=0., loss2=0.)
    accu.update(loss1=0.1, loss2=0.3)
    accu.update(loss1=0.1, loss2=0.1)
    print(accu.mean(["loss1", "loss2"]))
    print(accu.mean(["loss1", "loss2"], dic=True))

    # Output
    # [0.1, 0.2]
    # {'loss1': 0.1, 'loss2': 0.2}
    accu.reset()
    ```
* sacred_tools
    * MapConfig
    * recover_backup_names
    ```python
    from sacred import Experiment
    from helper.sacred_tools import MapConfig

    ex = Experiment("ExpName")

    @ex.automain
    def main(_config):
        opt = MapConfig(_config)
        print(opt.seed)
    ```