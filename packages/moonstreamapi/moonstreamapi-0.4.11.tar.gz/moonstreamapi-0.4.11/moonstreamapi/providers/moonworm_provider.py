import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple, cast

from bugout.app import Bugout
from bugout.data import BugoutResource
from moonstreamdb.blockchain import AvailableBlockchainType, get_label_model
from sqlalchemy import and_, or_, text
from sqlalchemy.orm import Query, Session, query_expression
from sqlalchemy.sql.expression import label

from .. import data
from ..stream_boundaries import validate_stream_boundary
from ..stream_queries import StreamQuery

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARN)


ethereum_event_type = "ethereum_blockchain"
polygon_event_type = "polygon_blockchain"
proofofplay_apex_event_type = "proofofplay_apex_blockchain"
mumbai_event_type = "mumbai_blockchain"
amoy_event_type = "amoy_blockchain"
xdai_event_type = "xdai_blockchain"
zksync_era_testnet_event_type = "zksync_era_testnet_blockchain"
zksync_era_event_type = "zksync_era_blockchain"
zksync_era_sepolia_event_type = "zksync_era_sepolia_blockchain"
arbitrum_one_event_type = "arbitrum_one_blockchain"
arbitrum_nova_event_type = "arbitrum_nova_blockchain"
arbitrum_sepolia_event_type = "arbitrum_sepolia_blockchain"
xai_event_type = "xai_blockchain"
xai_sepolia_event_type = "xai_sepolia_blockchain"
avalanche_event_type = "avalanche_blockchain"
avalanche_fuji_sepolia_event_type = "avalanche_fuji_sepolia_blockchain"
blast_event_type = "blast_blockchain"
blast_sepolia_event_type = "blast_sepolia_blockchain"
mantle_event_type = "mantle_blockchain"
mantle_sepolia_event_type = "mantle_sepolia_blockchain"

allowed_tags = ["tag:erc721"]

description = f"""Event provider for transactions from the Ethereum blockchain.

To restrict your queries to this provider, add a filter of \"type:{ethereum_event_type}\{polygon_event_type}\" to your query (query parameter: \"q\") on the /streams endpoint."""

default_time_interval_seconds: int = 5 * 60

# 200 transactions per block, 4 blocks per minute.
estimated_events_per_time_interval: float = 5 * 800


@dataclass
class ArgsFilters:
    name: str
    value: Any
    type: str


@dataclass
class LabelsFilters:
    name: str
    type: str
    args: List[ArgsFilters] = field(default_factory=list)


@dataclass
class AddressFilters:
    address: str
    label_filters: List[LabelsFilters] = field(default_factory=list)


@dataclass
class Filters:
    addresses: List[AddressFilters] = field(default_factory=list)


class MoonwormProvider:
    def __init__(
        self,
        event_type: str,
        blockchain: AvailableBlockchainType,
        description: str,
        streamboaundary_range_limit: int,
    ):
        self.event_type = event_type
        self.blockchain = blockchain
        self.description = description
        self.valid_period_seconds = streamboaundary_range_limit

    def default_filters(self, subscriptions: List[BugoutResource]) -> Filters:
        """
        Default filter strings for the given list of subscriptions.
        """
        filters = Filters()
        for subscription in subscriptions:
            subscription_address = cast(
                Optional[str], subscription.resource_data.get("address")
            )
            if subscription_address is not None:
                # How apply labels?
                filters.addresses.append(
                    AddressFilters(address=subscription_address, label_filters=[])
                )
            else:
                logger.warn(
                    f"Could not find subscription address for subscription with resource id: {subscription.id}"
                )
        return filters

    def apply_query_filters(self, filters: Filters, query_filters: StreamQuery):
        """
        Required to implement filters wich depends on procider
        """
        pass

    def events(self, row: Tuple) -> data.Event:
        """
        Parses a result from the result set of a database query for Ethereum transactions with block timestamp
        into an Event object.
        """
        (
            block_number,
            address,
            transaction_hash,
            label_data,
            block_timestamp,
            log_index,
            created_at,
        ) = row
        return data.Event(
            event_type=self.event_type,
            event_timestamp=block_timestamp,
            event_data={
                "hash": transaction_hash,
                "block_number": block_number,
                "address": address,
                "label_data": label_data,
                "log_index": log_index,
                "created_at": created_at,
            },
        )

    def parse_filters(
        self,
        query: StreamQuery,
        user_subscriptions: Dict[str, List[BugoutResource]],
    ) -> Optional[Filters]:
        """
        Passes raw filter strings into a Filters object which is used to construct a database query
        for ethereum transactions.
        Right now support only addresses query.
        """
        if query.subscription_types and not any(
            subtype == self.event_type for subtype in query.subscription_types
        ):
            return None

        provider_subscriptions = user_subscriptions.get(self.event_type)

        # If the user has no subscriptions to this event type, we do not have to return any data!
        if not provider_subscriptions:
            return None
        parsed_filters = self.default_filters(provider_subscriptions)

        self.apply_query_filters(parsed_filters, query)

        if not (parsed_filters.addresses):
            return None

        return parsed_filters

    def stream_boundary_validator(
        self, stream_boundary: data.StreamBoundary
    ) -> data.StreamBoundary:
        """
        Stream boundary validator for the events provider.

        Checks that stream boundaries do not exceed periods of greater than 24 hours.

        Raises an error for invalid stream boundaries, else returns None.
        """
        valid_period_seconds = self.valid_period_seconds

        _, stream_boundary = validate_stream_boundary(
            stream_boundary, valid_period_seconds, raise_when_invalid=True
        )
        return stream_boundary

    def generate_events_query(
        self,
        db_session: Session,
        stream_boundary: data.StreamBoundary,
        parsed_filters: Filters,
    ) -> Query:
        """
        Builds a database query for Ethereum transactions that occurred within the window of time that
        the given stream_boundary represents and satisfying the constraints of parsed_filters.
        """

        Labels = get_label_model(self.blockchain)

        query = db_session.query(
            Labels.block_number,
            Labels.address,
            Labels.transaction_hash,
            Labels.label_data,
            Labels.block_timestamp,
            Labels.log_index,
            Labels.created_at,
        ).filter(Labels.label == "moonworm")

        if stream_boundary.include_start:
            query = query.filter(Labels.block_timestamp >= stream_boundary.start_time)
        else:
            query = query.filter(Labels.block_timestamp > stream_boundary.start_time)

        if stream_boundary.end_time is not None:
            if stream_boundary.include_end:
                query = query.filter(Labels.block_timestamp <= stream_boundary.end_time)
            else:
                query = query.filter(Labels.block_timestamp <= stream_boundary.end_time)

        addresses_filters = []

        for address_filter in parsed_filters.addresses:
            labels_filters = []
            for label_filter in address_filter.label_filters:
                labels_filters.append(
                    and_(
                        *(
                            Labels.label_data["type"] == label_filter.type,
                            Labels.label_data["name"] == label_filter.name,
                        )
                    )
                )
            addresses_filters.append(
                and_(
                    *(
                        Labels.address == address_filter.address,
                        or_(*labels_filters),
                    )
                )
            )

        query = query.filter(or_(*addresses_filters))

        return query

    def get_events(
        self,
        db_session: Session,
        bugout_client: Bugout,
        data_journal_id: str,
        data_access_token: str,
        stream_boundary: data.StreamBoundary,
        query: StreamQuery,
        user_subscriptions: Dict[str, List[BugoutResource]],
    ) -> Optional[Tuple[data.StreamBoundary, List[data.Event]]]:
        """
        Returns blockchain events for the given addresses in the time period represented
        by stream_boundary.

        If the query does not require any data from this provider, returns None.
        """
        stream_boundary = self.stream_boundary_validator(stream_boundary)

        parsed_filters = self.parse_filters(query, user_subscriptions)
        if parsed_filters is None:
            return None

        ethereum_transactions = self.generate_events_query(
            db_session, stream_boundary, parsed_filters
        )

        ethereum_transactions = ethereum_transactions.order_by(
            text("block_timestamp desc")
        )

        # TODO(zomglings): Catch the operational error denoting that the statement timed out here
        # and wrap it in an error that tells the API to return the appropriate 400 response. Currently,
        # when the statement times out, the API returns a 500 status code to the client, which doesn't
        # do anything to help them get data from teh backend.
        # The error message on the API side when the statement times out:
        # > sqlalchemy.exc.OperationalError: (psycopg2.errors.QueryCanceled) canceling statement due to statement timeout
        events: List[data.Event] = [self.events(row) for row in ethereum_transactions]

        if (stream_boundary.end_time is None) and events:
            stream_boundary.end_time = events[0].event_timestamp
            stream_boundary.include_end = True

        return stream_boundary, events

    def latest_events(
        self,
        db_session: Session,
        bugout_client: Bugout,
        data_journal_id: str,
        data_access_token: str,
        query: StreamQuery,
        num_events: int,
        user_subscriptions: Dict[str, List[BugoutResource]],
    ) -> Optional[List[data.Event]]:
        """
        Returns the num_events latest events from the current provider, subject to the constraints imposed
        by the given filters.

        If the query does not require any data from this provider, returns None.
        """
        assert num_events > 0, f"num_events ({num_events}) should be positive."

        stream_boundary = data.StreamBoundary(
            start_time=0, include_start=True, end_time=None, include_end=False
        )
        parsed_filters = self.parse_filters(query, user_subscriptions)
        if parsed_filters is None:
            return None
        ethereum_transactions = (
            self.generate_events_query(db_session, stream_boundary, parsed_filters)
            .order_by(text("block_timestamp desc"))
            .limit(num_events)
        )

        return [self.events(row) for row in ethereum_transactions]

    def next_event(
        self,
        db_session: Session,
        bugout_client: Bugout,
        data_journal_id: str,
        data_access_token: str,
        stream_boundary: data.StreamBoundary,
        query: StreamQuery,
        user_subscriptions: Dict[str, List[BugoutResource]],
    ) -> Optional[data.Event]:
        """
        Returns the earliest event occuring after the given stream boundary corresponding to the given
        query from this provider.

        If the query does not require any data from this provider, returns None.
        """
        assert (
            stream_boundary.end_time is not None
        ), "Cannot return next event for up-to-date stream boundary"
        next_stream_boundary = data.StreamBoundary(
            start_time=stream_boundary.end_time,
            include_start=(not stream_boundary.include_end),
            end_time=None,
            include_end=False,
        )
        parsed_filters = self.parse_filters(query, user_subscriptions)
        if parsed_filters is None:
            return None

        maybe_ethereum_transaction = (
            self.generate_events_query(db_session, next_stream_boundary, parsed_filters)
            .order_by(text("block_timestamp asc"))
            .limit(1)
        ).one_or_none()

        if maybe_ethereum_transaction is None:
            return None
        return self.events(maybe_ethereum_transaction)

    def previous_event(
        self,
        db_session: Session,
        bugout_client: Bugout,
        data_journal_id: str,
        data_access_token: str,
        stream_boundary: data.StreamBoundary,
        query: StreamQuery,
        user_subscriptions: Dict[str, List[BugoutResource]],
    ) -> Optional[data.Event]:
        """
        Returns the latest event occuring before the given stream boundary corresponding to the given
        query from this provider.

        If the query does not require any data from this provider, returns None.
        """
        assert (
            stream_boundary.start_time != 0
        ), "Cannot return previous event for stream starting at time 0"
        previous_stream_boundary = data.StreamBoundary(
            start_time=0,
            include_start=True,
            end_time=stream_boundary.start_time,
            include_end=(not stream_boundary.include_start),
        )
        parsed_filters = self.parse_filters(query, user_subscriptions)
        if parsed_filters is None:
            return None

        maybe_ethereum_transaction = (
            self.generate_events_query(
                db_session, previous_stream_boundary, parsed_filters
            )
            .order_by(text("block_timestamp desc"))
            .limit(1)
        ).one_or_none()
        if maybe_ethereum_transaction is None:
            return None
        return self.events(maybe_ethereum_transaction)


EthereumMoonwormProvider = MoonwormProvider(
    event_type="ethereum_smartcontract",
    blockchain=AvailableBlockchainType("ethereum"),
    description="Provider for reviving transactions from Ethereum tables.",
    streamboaundary_range_limit=2 * 60 * 60,
)

PolygonMoonwormProvider = MoonwormProvider(
    event_type="polygon_smartcontract",
    blockchain=AvailableBlockchainType("polygon"),
    description="Provider for reviving transactions from Polygon tables.",
    streamboaundary_range_limit=2 * 60 * 60,
)

MumbaiMoonwormProvider = MoonwormProvider(
    event_type="mumbai_smartcontract",
    blockchain=AvailableBlockchainType("mumbai"),
    description="Provider for reviving transactions from Mumbai tables.",
    streamboaundary_range_limit=2 * 60 * 60,
)

AmoyMoonwormProvider = MoonwormProvider(
    event_type="amoy_smartcontract",
    blockchain=AvailableBlockchainType("amoy"),
    description="Provider for reviving transactions from Amoy tables.",
    streamboaundary_range_limit=2 * 60 * 60,
)

XDaiMoonwormProvider = MoonwormProvider(
    event_type="xdai_smartcontract",
    blockchain=AvailableBlockchainType("xdai"),
    description="Provider for reviving transactions from XDai tables.",
    streamboaundary_range_limit=2 * 60 * 60,
)

ZkSyncEraTestnetMoonwormProvider = MoonwormProvider(
    event_type="zksync_era_testnet_smartcontract",
    blockchain=AvailableBlockchainType("zksync_era_testnet"),
    description="Provider for reviving transactions from zkSync Era testnet tables.",
    streamboaundary_range_limit=2 * 60 * 60,
)

ZkSyncEraMoonwormProvider = MoonwormProvider(
    event_type="zksync_era_smartcontract",
    blockchain=AvailableBlockchainType("zksync_era"),
    description="Provider for reviving transactions from zkSync Era tables.",
    streamboaundary_range_limit=2 * 60 * 60,
)

ZkSyncEraSepoliaMoonwormProvider = MoonwormProvider(
    event_type="zksync_era_sepolia_smartcontract",
    blockchain=AvailableBlockchainType("zksync_era_sepolia"),
    description="Provider for reviving transactions from zkSync Era Sepolia tables.",
    streamboaundary_range_limit=2 * 60 * 60,
)

ArbitrumOneMoonwormProvider = MoonwormProvider(
    event_type="arbitrum_one_smartcontract",
    blockchain=AvailableBlockchainType("arbitrum_one"),
    description="Provider for reviving transactions from Arbitrum One tables.",
    streamboaundary_range_limit=2 * 60 * 60,
)

ArbitrumNovaMoonwormProvider = MoonwormProvider(
    event_type="arbitrum_nova_smartcontract",
    blockchain=AvailableBlockchainType("arbitrum_nova"),
    description="Provider for reviving transactions from Arbitrum Nova tables.",
    streamboaundary_range_limit=2 * 60 * 60,
)

ArbitrumSepoliaMoonwormProvider = MoonwormProvider(
    event_type="arbitrum_sepolia_smartcontract",
    blockchain=AvailableBlockchainType("arbitrum_sepolia"),
    description="Provider for reviving transactions from Arbitrum Sepolia tables.",
    streamboaundary_range_limit=2 * 60 * 60,
)

XaiMoonwormProvider = MoonwormProvider(
    event_type="xai_smartcontract",
    blockchain=AvailableBlockchainType("xai"),
    description="Provider for reviving transactions from Xai tables.",
    streamboaundary_range_limit=2 * 60 * 60,
)

XaiSepoliaMoonwormProvider = MoonwormProvider(
    event_type="xai_sepolia_smartcontract",
    blockchain=AvailableBlockchainType("xai_sepolia"),
    description="Provider for reviving transactions from Xai Sepolia tables.",
    streamboaundary_range_limit=2 * 60 * 60,
)

AvalancheMoonwormProvider = MoonwormProvider(
    event_type="avalanche_smartcontract",
    blockchain=AvailableBlockchainType("avalanche"),
    description="Provider for reviving transactions from Avalanche tables.",
    streamboaundary_range_limit=2 * 60 * 60,
)

AvalancheFujiMoonwormProvider = MoonwormProvider(
    event_type="avalanche_fuji_smartcontract",
    blockchain=AvailableBlockchainType("avalanche_fuji"),
    description="Provider for reviving transactions from Avalanche Fuji tables.",
    streamboaundary_range_limit=2 * 60 * 60,
)

BlastMoonwormProvider = MoonwormProvider(
    event_type="blast_smartcontract",
    blockchain=AvailableBlockchainType("blast"),
    description="Provider for reviving transactions from Blast tables.",
    streamboaundary_range_limit=2 * 60 * 60,
)

BlastSepoliaMoonwormProvider = MoonwormProvider(
    event_type="blast_sepolia_smartcontract",
    blockchain=AvailableBlockchainType("blast_sepolia"),
    description="Provider for reviving transactions from Blast Sepolia tables.",
    streamboaundary_range_limit=2 * 60 * 60,
)

ProofOfPlayApexMoonwormProvider = MoonwormProvider(
    event_type="proofofplay_apex_smartcontract",
    blockchain=AvailableBlockchainType("proofofplay_apex"),
    description="Provider for reviving transactions from Proof of Play Apex tables.",
    streamboaundary_range_limit=2 * 60 * 60,
)

MantleMoonwormProvider = MoonwormProvider(
    event_type="mantle_smartcontract",
    blockchain=AvailableBlockchainType("mantle"),
    description="Provider for reviving transactions from Mantle tables.",
    streamboaundary_range_limit=2 * 60 * 60,
)

MantleSepoliaMoonwormProvider = MoonwormProvider(
    event_type="mantle_sepolia_smartcontract",
    blockchain=AvailableBlockchainType("mantle_sepolia"),
    description="Provider for reviving transactions from Mantle Sepolia tables.",
    streamboaundary_range_limit=2 * 60 * 60,
)
