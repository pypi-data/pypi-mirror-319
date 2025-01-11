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
from tikka.adapters.network.rpc.connection import RPCConnection
from tikka.domains.entities.events import ConnectionsEvent
from tikka.domains.entities.node import Node
from tikka.domains.events import EventDispatcher
from tikka.interfaces.domains.connections import ConnectionsInterface


class Connections(ConnectionsInterface):
    """
    Connections class
    """

    def __init__(self, rpc: RPCConnection, event_dispatcher: EventDispatcher) -> None:
        __doc__ = (  # pylint: disable=redefined-builtin, unused-variable
            ConnectionsInterface.__init__.__doc__
        )
        super().__init__(rpc, event_dispatcher)

    def connect(self, node: Node):
        """
        Connect all connections

        :return:
        """
        self.rpc.connect(node)
        if self.rpc.is_connected():
            self.event_dispatcher.dispatch_event(
                ConnectionsEvent(ConnectionsEvent.EVENT_TYPE_CONNECTED)
            )
        else:
            self.event_dispatcher.dispatch_event(
                ConnectionsEvent(ConnectionsEvent.EVENT_TYPE_DISCONNECTED)
            )

    def disconnect(self):
        """
        Disconnect all connections

        :return:
        """
        if self.rpc.is_connected():
            self.rpc.disconnect()
        self.event_dispatcher.dispatch_event(
            ConnectionsEvent(ConnectionsEvent.EVENT_TYPE_DISCONNECTED)
        )

    def is_connected(self) -> bool:
        """
        Return True if connection is active, False otherwise

        :return:
        """
        return self.rpc.is_connected()
