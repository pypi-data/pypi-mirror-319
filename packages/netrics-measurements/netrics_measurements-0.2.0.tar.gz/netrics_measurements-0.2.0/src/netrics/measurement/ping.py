"""Measure ping latency to configured hosts."""
import subprocess
from collections import defaultdict

from schema import Optional

from netrics import task
from netrics.util import procutils

from .common import default, output, require_lan


#
# ping exit codes
#
# if ping returns any code other than the below something is *very* wrong
#
# (the error code 2 is included -- unclear if ping *can* return anything higher than that.)
#
PING_CODES = {
    0,  # success
    1,  # no reply
    2,  # error (e.g. dns)
}


#
# params schema
#
# input -- a (deserialized) mapping -- is entirely optional.
#
# a dict, of the optional param keys, their defaults, and validations of
# their values, is given below, (extending the globally-supported input
# parameter schema given by `task.schema`).
#
PARAMS = task.schema.extend('ping_latency', {
    # destinations: (ping): list of hosts
    #                       OR mapping of hosts to their labels (for results)
    Optional('destinations',
             default=default.DESTINATIONS): task.schema.DestinationCollection(),

    # count: (ping): natural number
    Optional('count', default='10'): task.schema.NaturalStr('count'),

    # interval: (ping): int/decimal seconds no less than 2ms
    Optional('interval',
             default='0.25'): task.schema.BoundedRealStr(
                 lambda interval: interval >= 0.002,
                 'interval: seconds may be no less than 0.002 (2ms)'
    ),

    # deadline: (ping): positive integer seconds
    Optional('deadline', default='5'): task.schema.PositiveIntStr('deadline', 'seconds'),
})


@task.param.require(PARAMS)
@require_lan
def main(params):
    """Measure ping latency to configured hosts.

    The local network is queried first to ensure operation.
    (See: `require_lan`.)

    Ping queries are then executed, in parallel, to each configured host
    (`destinations`) according to configured ping command arguments:
    `count`, `interval` and `deadline`.

    Ping outputs are parsed into structured results and written out
    according to configuration (`result`).

    """
    # parallelize pings
    pool = [
        subprocess.Popen(
            (
                'ping',
                '-c', params.count,
                '-i', params.interval,
                '-w', params.deadline,
                destination,
            ),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        ) for destination in params.destinations
    ]

    # wait and map to completed processes
    processes = {
        destination: procutils.complete(process)
        for (destination, process) in zip(params.destinations, pool)
    }

    # check for exceptions
    failures = [(destination, process) for (destination, process) in processes.items()
                if process.returncode not in PING_CODES]

    if failures:
        fail_total = len(failures)

        # directly log first few failures
        some_failures = failures[:3]

        for (fail_count, (destination, process)) in enumerate(some_failures, 1):
            task.log.critical(
                dest=destination,
                status=f'Error ({process.returncode})',
                failure=f"({fail_count}/{fail_total})",
                args=process.args,
                stdout=process.stdout,
                stderr=process.stderr,
            )

        if fail_count < fail_total:
            task.log.critical(
                dest='...',
                status='Error (...)',
                failure=f"(.../{fail_total})",
                args='...',
                stdout='...',
                stderr='...',
            )

        return task.status.software_error

    # log summary/general results
    statuses = defaultdict(int)
    for process in processes.values():
        statuses[process.returncode] += 1

    task.log.info({'dest-status': statuses})

    # parse detailed results
    results = {
        destination: output.parse_ping(process.stdout)
        for (destination, process) in processes.items()
    }

    # label results
    if isinstance(params.destinations, dict):
        results = {
            params.destinations[destination]: result
            for (destination, result) in results.items()
        }

    # flatten results
    if params.result.flat:
        results = {f'{label}_{feature}': value
                   for (label, data) in results.items()
                   for (feature, value) in data.items()}

    # write results
    task.result.write(results,
                      label=params.result.label,
                      annotate=params.result.annotate)

    return task.status.success
