"""
crate_anon/nlp_manager/tests/cloud_request_process_tests.py

===============================================================================

    Copyright (C) 2015, University of Cambridge, Department of Psychiatry.
    Created by Rudolf Cardinal (rnc1001@cam.ac.uk).

    This file is part of CRATE.

    CRATE is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    CRATE is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with CRATE. If not, see <https://www.gnu.org/licenses/>.

===============================================================================

Unit tests.

"""

import logging
import sys
from unittest import mock, TestCase

from cardinal_pythonlib.httpconst import HttpStatus
from sqlalchemy.exc import OperationalError

from crate_anon.nlprp.constants import (
    NlprpKeys as NKeys,
)
from crate_anon.nlp_manager.cloud_request import CloudRequestProcess


class CloudRequestProcessTests(TestCase):
    def setUp(self) -> None:
        self.mock_execute_method = mock.Mock()
        self.mock_session = mock.Mock(execute=self.mock_execute_method)
        self.mock_db = mock.Mock(session=self.mock_session)

        # can't set name attribute in constructor here as it has special
        # meaning
        mock_column = mock.Mock()
        mock_column.name = "fruit"  # so set it here

        self.mock_values_method = mock.Mock()
        mock_insert_object = mock.Mock(values=self.mock_values_method)
        mock_insert_method = mock.Mock(return_value=mock_insert_object)
        mock_sqla_table = mock.Mock(
            columns=[mock_column], insert=mock_insert_method
        )
        mock_get_table_method = mock.Mock(return_value=mock_sqla_table)
        self.mock_processor = mock.Mock(
            get_table=mock_get_table_method, dest_session=self.mock_session
        )

        self.mock_notify_transaction_method = mock.Mock()
        self.mock_nlpdef = mock.Mock(
            notify_transaction=self.mock_notify_transaction_method
        )
        self.mock_nlpdef.name = "fruitdef"
        self.process = CloudRequestProcess(nlpdef=self.mock_nlpdef)

    def test_process_all_inserts_values(self) -> None:
        nlp_values = [
            ("output", {"fruit": "apple"}, self.mock_processor),
            ("output", {"fruit": "banana"}, self.mock_processor),
            ("output", {"fruit": "fig"}, self.mock_processor),
        ]

        mock_get_nlp_values_method = mock.Mock(return_value=iter(nlp_values))

        with mock.patch.multiple(
            self.process, get_nlp_values=mock_get_nlp_values_method
        ):
            self.process.process_all()

        self.mock_values_method.assert_any_call({"fruit": "apple"})
        self.mock_values_method.assert_any_call({"fruit": "banana"})
        self.mock_values_method.assert_any_call({"fruit": "fig"})
        self.assertEqual(self.mock_values_method.call_count, 3)
        self.assertEqual(self.mock_execute_method.call_count, 3)

        self.mock_notify_transaction_method.assert_any_call(
            self.mock_session,
            n_rows=1,
            n_bytes=sys.getsizeof({"fruit": "apple"}),
            force_commit=mock.ANY,
        )
        self.mock_notify_transaction_method.assert_any_call(
            self.mock_session,
            n_rows=1,
            n_bytes=sys.getsizeof({"fruit": "banana"}),
            force_commit=mock.ANY,
        )
        self.mock_notify_transaction_method.assert_any_call(
            self.mock_session,
            n_rows=1,
            n_bytes=sys.getsizeof({"fruit": "fig"}),
            force_commit=mock.ANY,
        )
        self.assertEqual(self.mock_notify_transaction_method.call_count, 3)

    def test_process_all_handles_failed_insert(self) -> None:
        nlp_values = [
            ("output", {"fruit": "apple"}, self.mock_processor),
        ]

        self.mock_execute_method.side_effect = OperationalError(
            "Insert failed", None, None, None
        )

        mock_get_nlp_values_method = mock.Mock(return_value=iter(nlp_values))
        with self.assertLogs(level=logging.ERROR) as logging_cm:
            with mock.patch.multiple(
                self.process, get_nlp_values=mock_get_nlp_values_method
            ):
                self.process.process_all()

        self.mock_notify_transaction_method.assert_any_call(
            self.mock_session,
            n_rows=1,
            n_bytes=sys.getsizeof({"fruit": "apple"}),
            force_commit=mock.ANY,
        )
        logger_name = "crate_anon.nlp_manager.cloud_request"

        self.assertIn(f"ERROR:{logger_name}", logging_cm.output[0])
        self.assertIn("Insert failed", logging_cm.output[0])

    def test_not_ready_if_queue_id_is_none(self) -> None:
        self.process.queue_id = None
        with self.assertLogs(level=logging.WARNING) as logging_cm:
            ready = self.process.check_if_ready()
        self.assertFalse(ready)
        self.assertIn(
            "Tried to fetch from queue before sending request.",
            logging_cm.output[0],
        )

    def test_not_ready_if_fetched(self) -> None:
        self.process.queue_id = "queue_0001"
        self.process._fetched = True

        ready = self.process.check_if_ready()
        self.assertFalse(ready)

    def test_not_ready_if_no_response(self) -> None:
        self.process.queue_id = "queue_0001"
        with mock.patch.object(self.process, "_try_fetch", return_value=None):
            ready = self.process.check_if_ready()
        self.assertFalse(ready)

    def test_ready_for_status_ok(self) -> None:
        self.process.queue_id = "queue_0001"

        response = {
            NKeys.STATUS: HttpStatus.OK,
            NKeys.VERSION: "0.3.0",
        }

        with mock.patch.object(
            self.process, "_try_fetch", return_value=response
        ):
            ready = self.process.check_if_ready()
        self.assertTrue(ready)

    def test_not_ready_when_old_server_status_processing(self) -> None:
        self.process.queue_id = "queue_0001"

        response = {
            NKeys.STATUS: HttpStatus.PROCESSING,
            NKeys.VERSION: "0.2.0",
        }

        with mock.patch.object(
            self.process, "_try_fetch", return_value=response
        ):
            ready = self.process.check_if_ready()
        self.assertFalse(ready)

    def test_not_ready_when_new_server_status_accepted(self) -> None:
        self.process.queue_id = "queue_0001"

        response = {
            NKeys.STATUS: HttpStatus.ACCEPTED,
            NKeys.VERSION: "0.3.0",
        }

        with mock.patch.object(
            self.process, "_try_fetch", return_value=response
        ):
            ready = self.process.check_if_ready()
        self.assertFalse(ready)

    def test_not_ready_when_server_status_not_found(self) -> None:
        self.process.queue_id = "queue_0001"

        response = {
            NKeys.STATUS: HttpStatus.NOT_FOUND,
            NKeys.VERSION: "0.3.0",
        }

        with mock.patch.object(
            self.process, "_try_fetch", return_value=response
        ):
            with self.assertLogs(level=logging.WARNING) as logging_cm:
                ready = self.process.check_if_ready()
        self.assertFalse(ready)
        self.assertIn("Got HTTP status code 404", logging_cm.output[0])

    def test_not_ready_when_server_status_anything_else(self) -> None:
        self.process.queue_id = "queue_0001"

        response = {
            NKeys.STATUS: HttpStatus.FORBIDDEN,
            NKeys.VERSION: "0.3.0",
        }

        with mock.patch.object(
            self.process, "_try_fetch", return_value=response
        ):
            with self.assertLogs(level=logging.WARNING) as logging_cm:
                ready = self.process.check_if_ready()
        self.assertFalse(ready)
        self.assertIn("Got HTTP status code 403", logging_cm.output[0])
