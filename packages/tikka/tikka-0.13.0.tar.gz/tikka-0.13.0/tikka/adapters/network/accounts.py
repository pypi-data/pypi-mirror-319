# Copyright 2021 Vincent Texier <vit@free.fr>
#
# This software is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import logging
from typing import Dict, List, Optional

from tikka.interfaces.adapters.network.accounts import (
    NetworkAccountsException,
    NetworkAccountsInterface,
)
from tikka.interfaces.adapters.network.connection import NetworkConnectionError


class NetworkAccounts(NetworkAccountsInterface):
    """
    NetworkAccounts class
    """

    def get_balance(self, address: str) -> Optional[int]:
        __doc__ = (  # pylint: disable=redefined-builtin, unused-variable
            NetworkAccountsInterface.get_balance.__doc__
        )
        if not self.connections.is_connected() or self.connections.rpc.client is None:
            raise NetworkAccountsException(NetworkConnectionError())

        # system.account: FrameSystemAccountInfo
        # {
        #   nonce: 1
        #   consumers: 0
        #   providers: 1
        #   sufficients: 0
        #   data: {
        #     randomId: 0x18a4d...
        #     free: 9,799
        #     reserved: 0
        #     feeFrozen: 0
        #   }
        # }
        try:
            result = self.connections.rpc.client.query("System", "Account", [address])
        except Exception as exception:
            logging.exception(exception)
            raise NetworkAccountsException(exception)

        if result.meta_info["result_found"] is False:
            balance = None
        else:
            balance = result.value["data"]["free"] + result.value["data"]["reserved"]

        return balance

    def get_balances(self, addresses: List[str]) -> Dict[str, Optional[int]]:
        __doc__ = (  # pylint: disable=redefined-builtin, unused-variable
            NetworkAccountsInterface.get_balances.__doc__
        )
        if not self.connections.is_connected() or self.connections.rpc.client is None:
            raise NetworkAccountsException(NetworkConnectionError())

        storage_keys = []
        for address in addresses:
            storage_keys.append(
                self.connections.rpc.client.create_storage_key(
                    "System", "Account", [address]
                )
            )

        try:
            multi_result = self.connections.rpc.client.query_multi(storage_keys)
        except Exception as exception:
            logging.exception(exception)
            raise NetworkAccountsException(exception)

        balances: Dict[str, Optional[int]] = {}
        for storage_key, value_obj in multi_result:
            if value_obj.meta_info["result_found"] is False:
                balances[storage_key.params[0]] = None
            else:
                balances[storage_key.params[0]] = (
                    value_obj.value["data"]["free"]
                    + value_obj.value["data"]["reserved"]
                )

        return balances

    def get_unclaimed_ud_balance(self, first_eligible_ud: int) -> int:
        __doc__ = (  # pylint: disable=redefined-builtin, unused-variable
            NetworkAccountsInterface.get_unclaimed_ud_balance.__doc__
        )
        if not self.connections.is_connected() or self.connections.rpc.client is None:
            raise NetworkAccountsException(NetworkConnectionError())

        if first_eligible_ud == 0:
            return 0

        try:
            result = self.connections.rpc.client.query(
                "UniversalDividend", "CurrentUdIndex"
            )
        except Exception as exception:
            logging.exception(exception)
            raise NetworkAccountsException(exception)

        current_index = result.value

        try:
            result = self.connections.rpc.client.query(
                "UniversalDividend", "PastReevals"
            )
        except Exception as exception:
            logging.exception(exception)
            raise NetworkAccountsException(exception)

        if result.meta_info["result_found"] is False:
            return 0

        balance = 0
        index = current_index
        for reeval_index, reeval_value in reversed(result.value):
            if reeval_index <= first_eligible_ud:
                count = index - first_eligible_ud
                balance += count * reeval_value
                break
            else:
                count = index - reeval_index
                balance += count * reeval_value
                index = reeval_index

        return balance
