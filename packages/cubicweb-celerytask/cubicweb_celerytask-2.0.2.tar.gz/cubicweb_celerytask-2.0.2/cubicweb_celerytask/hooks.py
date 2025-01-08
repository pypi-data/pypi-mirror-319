# copyright 2016-2024 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""cubicweb-celerytask specific hooks and operations"""

import errno
import os.path

from celery import current_app

from cubicweb import ConfigurationError
from cubicweb.predicates import is_instance
from cubicweb.server.hook import Hook, DataOperationMixIn, Operation

from cw_celerytask_helpers import fileutils

# CloudWatch and S3 dependencies are optional
try:
    from cw_celerytask_helpers import cloudwatchutils
except ImportError:
    cloudwatchutils = None
try:
    from cw_celerytask_helpers import s3utils
except ImportError:
    s3utils = None


class DeleteCeleryTaskOp(DataOperationMixIn, Operation):
    def postcommit_event(self):
        tasks = set(self.get_data())
        if tasks:
            current_app.control.revoke(list(tasks), terminate=True, signal="SIGKILL")
        for task_id in tasks:
            for utils in [fileutils, cloudwatchutils, s3utils]:
                if utils:
                    try:
                        utils.flush_task_logs(task_id)
                    except Exception:
                        pass


class CeleryTaskDeletedHook(Hook):
    """revoke task and flush task logs when a task is deleted"""

    __regid__ = "celerytask.celerytask_deleted"
    __select__ = Hook.__select__ & is_instance("CeleryTask")
    events = ("before_delete_entity",)

    def __call__(self):
        op = DeleteCeleryTaskOp.get_instance(self._cw)
        for task in self.entity.child_tasks():
            op.add_data(task.task_id)


class CeleryTaskStartupHook(Hook):
    """Initialize CUBICWEB_CELERYTASK_LOGDIR"""

    __regid__ = "celerytask.server-startup-hook"
    events = ("server_startup", "server_maintenance")

    def __call__(self):
        self.setup_celerytask_logdir(self.repo.vreg.config)

    @staticmethod
    def setup_celerytask_logdir(config):
        celery_logdir = current_app.conf.get("CUBICWEB_CELERYTASK_LOGDIR")
        logdir = config["celerytask-log-dir"]
        if celery_logdir and logdir and celery_logdir != logdir:
            raise ConfigurationError(
                (
                    "You misconfigured your application by setting two different "
                    "celerytask log directories: "
                    "{} in celeryconfig and {} in cubicweb all-in-one.conf"
                ).format(celery_logdir, logdir)
            )
        elif celery_logdir and not logdir:
            logdir = config["celerytask-log-dir"] = celery_logdir
        elif not celery_logdir:
            if not logdir:
                logdir = os.path.join(config.appdatahome, "logs")
            current_app.conf["CUBICWEB_CELERYTASK_LOGDIR"] = logdir
            config["celerytask-log-dir"] = logdir
        # ensure directory exist
        try:
            os.makedirs(logdir)
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
