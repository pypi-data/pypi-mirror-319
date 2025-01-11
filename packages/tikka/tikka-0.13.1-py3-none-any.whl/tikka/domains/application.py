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

import gettext
import logging
from pathlib import Path
from time import sleep
from typing import Any

from tikka.adapters.network.accounts import NetworkAccounts
from tikka.adapters.network.authorities import NetworkAuthorities
from tikka.adapters.network.currency import NetworkCurrency
from tikka.adapters.network.identities import NetworkIdentities
from tikka.adapters.network.nodes import NetworkNodes
from tikka.adapters.network.rpc.connection import RPCConnection
from tikka.adapters.network.smiths import NetworkSmiths
from tikka.adapters.network.technical_committee import NetworkTechnicalCommittee
from tikka.adapters.network.transfers import NetworkTransfers
from tikka.adapters.repository.accounts import Sqlite3AccountsRepository
from tikka.adapters.repository.authorities import Sqlite3AuthoritiesRepository
from tikka.adapters.repository.categories import Sqlite3CategoriesRepository
from tikka.adapters.repository.config import FileConfigRepository
from tikka.adapters.repository.currencies import FileCurrenciesRepository
from tikka.adapters.repository.currency import Sqlite3CurrencyRepository
from tikka.adapters.repository.file_wallets import V1FileWalletsRepository
from tikka.adapters.repository.identities import Sqlite3IdentitiesRepository
from tikka.adapters.repository.nodes import Sqlite3NodesRepository
from tikka.adapters.repository.passwords import Sqlite3PasswordsRepository
from tikka.adapters.repository.preferences import Sqlite3PreferencesRepository
from tikka.adapters.repository.smiths import Sqlite3SmithsRepository
from tikka.adapters.repository.sqlite3 import Sqlite3Client
from tikka.adapters.repository.tabs import Sqlite3TabRepository
from tikka.adapters.repository.wallets import Sqlite3WalletsRepository
from tikka.domains.accounts import Accounts
from tikka.domains.amounts import Amounts
from tikka.domains.authorities import Authorities
from tikka.domains.categories import Categories
from tikka.domains.config import Config
from tikka.domains.connections import Connections
from tikka.domains.currencies import Currencies
from tikka.domains.entities.constants import LOCALES_PATH
from tikka.domains.entities.events import CurrencyEvent
from tikka.domains.events import EventDispatcher
from tikka.domains.identities import Identities
from tikka.domains.nodes import Nodes
from tikka.domains.passwords import Passwords
from tikka.domains.preferences import Preferences
from tikka.domains.smiths import Smiths
from tikka.domains.technical_committee import TechnicalCommittee
from tikka.domains.transfers import Transfers
from tikka.domains.vaults import Vaults
from tikka.domains.wallets import Wallets
from tikka.interfaces.adapters.network.currency import NetworkCurrencyException


class Application:
    """
    Application class
    """

    def __init__(self, data_path: Path):
        """
        Init application

        :param data_path: Path instance of application data folder
        """

        # data
        self.data_path = data_path
        # dependency injection
        # init event dispatcher
        self.event_dispatcher = EventDispatcher()
        # init network connection to node
        self.connections = Connections(RPCConnection(), self.event_dispatcher)
        self.validator_node_connections = Connections(
            RPCConnection(), self.event_dispatcher
        )

        # init currencies support list
        currencies_repository = FileCurrenciesRepository()

        # init config domain
        config_repository = FileConfigRepository(self.data_path)
        self.config = Config(config_repository)

        # if supported currencies has changed and config use an unknown currency...
        if (
            self.config.get(Config.CURRENCY_KEY)
            not in currencies_repository.code_names()
        ):
            # set current currency to first currency by default
            self.config.set(Config.CURRENCY_KEY, currencies_repository.code_names()[0])

        # init wallets adapter
        self.file_wallets_repository = V1FileWalletsRepository()
        # database adapter
        self.sqlite3_client = Sqlite3Client(
            self.config.get(Config.CURRENCY_KEY), self.data_path
        )
        # init SQL repositories
        accounts_repository = Sqlite3AccountsRepository(self.sqlite3_client)
        wallets_repository = Sqlite3WalletsRepository(self.sqlite3_client)
        identities_repository = Sqlite3IdentitiesRepository(self.sqlite3_client)
        smiths_repository = Sqlite3SmithsRepository(self.sqlite3_client)
        authorities_repository = Sqlite3AuthoritiesRepository(self.sqlite3_client)
        nodes_repository = Sqlite3NodesRepository(self.sqlite3_client)
        currency_repository = Sqlite3CurrencyRepository(self.sqlite3_client)
        categories_repository = Sqlite3CategoriesRepository(self.sqlite3_client)
        passwords_repository = Sqlite3PasswordsRepository(self.sqlite3_client)
        self.tab_repository = Sqlite3TabRepository(self.sqlite3_client)
        self.preferences_repository = Sqlite3PreferencesRepository(self.sqlite3_client)

        # init translation
        self.translator = self.init_i18n()

        # init domains
        self.preferences = Preferences(self.preferences_repository)
        self.currencies = Currencies(
            currencies_repository,
            currency_repository,
            NetworkCurrency(self.connections),
            self.config.get(Config.CURRENCY_KEY),
        )
        self.passwords = Passwords(passwords_repository)
        self.wallets = Wallets(wallets_repository, self.currencies)
        self.identities = Identities(
            identities_repository, NetworkIdentities(self.connections)
        )
        self.accounts = Accounts(
            accounts_repository,
            NetworkAccounts(self.connections),
            self.passwords,
            self.wallets,
            self.file_wallets_repository,
            self.currencies,
            self.event_dispatcher,
        )
        self.amounts = Amounts(self.currencies, self.translator)
        self.transfers = Transfers(
            self.wallets, NetworkTransfers(self.connections), self.event_dispatcher
        )
        self.nodes = Nodes(
            nodes_repository,
            self.preferences,
            self.connections,
            NetworkNodes(self.connections),
            self.config,
            self.currencies,
            self.event_dispatcher,
        )
        self.smiths = Smiths(smiths_repository, NetworkSmiths(self.connections))
        self.authorities = Authorities(
            authorities_repository,
            NetworkAuthorities(self.connections),
            self.nodes,
            self.smiths,
        )
        self.categories = Categories(
            categories_repository, self.accounts, self.event_dispatcher
        )
        self.technical_committee = TechnicalCommittee(
            NetworkTechnicalCommittee(self.connections), self.event_dispatcher
        )
        self.vaults = Vaults(
            NetworkAccounts(self.connections),
            self.accounts,
            self.currencies,
        )

        # init network connections
        if self.config.get(Config.RANDOM_CONNECTION_AT_START_KEY) is True:
            self.nodes.set_current_url_randomly()
        else:
            current_node = self.nodes.get(self.nodes.get_current_url())
            if current_node is not None:
                # connect to RPC API via websocket
                self.connections.connect(current_node)

        # if currency properties required for amount display not populated...
        if self.currencies.get_current().members_count is None:
            try:
                # fetch currency properties from network
                self.currencies.network_get_properties()
            except NetworkCurrencyException:
                self.currencies.get_current().members_count = 1

    def init_i18n(self) -> Any:
        """
        Init translator from configured language

        :return:
        """
        # define translator for configurated language
        translator = gettext.translation(
            "application",
            str(LOCALES_PATH),
            languages=[self.config.get(Config.LANGUAGE_KEY)],
        )
        # init translator
        translator.install()

        return translator

    def select_currency(self, code_name: str):
        """
        Change currency

        :return:
        """
        if self.config is None:
            raise NoConfigError

        # dispatch event EVENT_TYPE_CHANGED
        event = CurrencyEvent(CurrencyEvent.EVENT_TYPE_PRE_CHANGE, code_name)
        self.event_dispatcher.dispatch_event(event)

        self.config.set(Config.CURRENCY_KEY, code_name)

        if self.sqlite3_client is not None:
            self.sqlite3_client.close()

        while self.sqlite3_client.is_alive():
            sleep(1)
            logging.debug("wait sqlite3 thread to end...")

        # init database connection
        self.sqlite3_client = Sqlite3Client(code_name, self.data_path)

        while not self.sqlite3_client.is_alive():
            sleep(1)
            logging.debug("wait sqlite3 thread to start...")

        # create new repository adapters on the new database
        self.accounts.repository.set_client(self.sqlite3_client)  # type: ignore
        self.passwords.repository.set_client(self.sqlite3_client)  # type: ignore
        self.wallets.repository.set_client(self.sqlite3_client)  # type: ignore
        self.identities.repository.set_client(self.sqlite3_client)  # type: ignore
        self.smiths.repository.set_client(self.sqlite3_client)  # type: ignore
        self.authorities.repository.set_client(self.sqlite3_client)  # type: ignore
        self.tab_repository.set_client(self.sqlite3_client)
        self.preferences_repository.set_client(self.sqlite3_client)
        self.nodes.repository.set_client(self.sqlite3_client)  # type: ignore
        self.currencies.currency_repository.set_client(self.sqlite3_client)  # type: ignore
        self.categories.repository.set_client(self.sqlite3_client)  # type: ignore
        # fixme: domains should only access others domains, not repositories of other domains
        #        we should create a preferences domain (and tabs domain too)

        self.currencies.set_current(code_name)

        # init domains with new repository adapter
        self.nodes.init_repository()

        # get current entry point for new network connection
        current_node = self.nodes.get(self.nodes.get_current_url())
        if current_node is not None:
            # disconnect previous currency connection
            self.connections.disconnect()
            # connect to RPC API via websocket
            self.connections.connect(current_node)

        self.currencies.network_get_properties()

        # dispatch event EVENT_TYPE_CHANGED
        event = CurrencyEvent(
            CurrencyEvent.EVENT_TYPE_CHANGED, self.currencies.get_current().code_name
        )
        self.event_dispatcher.dispatch_event(event)

    def select_language(self, language: str):
        """
        Select GUI language

        :param language: Code of language (ex: "en_US", "fr_FR")
        :return:
        """
        if self.config is None:
            raise NoConfigError

        self.config.set(Config.LANGUAGE_KEY, language)
        self.translator = self.init_i18n()

    def close(self):
        """
        Quit application and close what needs to be closed

        :return:
        """
        # disconnect all connections
        self.connections.disconnect()
        # close Sqlite3 client thread
        self.sqlite3_client.close()


class NoDatabaseError(Exception):
    pass


class NoConfigError(Exception):
    pass
