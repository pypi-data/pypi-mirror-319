"""
Moonstream CLI
"""

import argparse
import json
import logging
import os
import uuid
from posix import listdir
from typing import Any, Callable, Dict, List, Optional, Union

from moonstreamdb.db import SessionLocal
from sqlalchemy.orm import with_expression

from ..settings import (
    BUGOUT_BROOD_URL,
    BUGOUT_SPIRE_URL,
    MOONSTREAM_ADMIN_ACCESS_TOKEN,
    MOONSTREAM_APPLICATION_ID,
    MOONSTREAM_MOONWORM_TASKS_JOURNAL,
    MOONSTREAM_USAGE_REPORTS_JOURNAL_ID,
)
from ..web3_provider import yield_web3_provider
from . import moonworm_tasks, queries, subscription_types, subscriptions, usage
from .migrations import (
    add_selectors,
    checksum_address,
    generate_entity_subscriptions,
    update_dashboard_subscription_key,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MIGRATIONS_FOLDER = "./moonstreamapi/admin/migrations"


def uuid_type(value):
    try:
        return uuid.UUID(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"{value} is not a valid UUID.")


def parse_boolean_arg(raw_arg: Optional[str]) -> Optional[bool]:
    if raw_arg is None:
        return None

    raw_arg_lower = raw_arg.lower()
    if raw_arg_lower in ["t", "true", "1", "y", "yes"]:
        return True
    return False


def migration_run(step_map, command, step, step_order):
    if step is None:
        # run all steps

        if step_order is None:
            raise ValueError(
                f"step_order is required when running all steps for {command}"
            )

        if command == "downgrade":
            step_order = reversed(step_order)

        for step in step_order:
            logger.info(
                f"Starting step {step}: {step_map[command][step]['description']}"
            )
            migration_function = step_map[command][step]["action"]
            if callable(migration_function):
                migration_function()
    elif step in step_map[command]:
        logger.info(f"Starting step {step}: {step_map[command][step]['description']}")
        migration_function = step_map[command][step]["action"]
        if callable(migration_function):
            migration_function()
    else:
        logger.error(f"Step {step} not found in {command}")
        logger.info(f"Available steps: {step_map[command].keys()}")


def migrations_list(args: argparse.Namespace) -> None:
    migrations_overview = f"""

- id: 20211101
name: {checksum_address.__name__}
description: {checksum_address.__doc__}
    """
    logger.info(migrations_overview)

    entity_migration_overview = f"""
- id: 20230213
name: {generate_entity_subscriptions.__name__}
description: {generate_entity_subscriptions.__doc__}
steps:
    - step 1: generate_entity_subscriptions_from_brood_resources - Generate entity subscriptions from brood resources
    - step 2: update_dashboards_connection - Update dashboards connection
- id: 20230501
name: fix_duplicates_keys_in_entity_subscription
description: Fix entity duplicates keys for all subscriptions introduced in 20230213
- id: 20230904
name fill_missing_selectors_in_moonworm_tasks
description: Get all moonworm jobs from moonworm journal and add selector tag if it not represent
    """
    logger.info(entity_migration_overview)

    json_migrations_oreview = "Available migrations files."
    for file in os.listdir(MIGRATIONS_FOLDER):
        if file.endswith(".json"):
            with open(os.path.join(MIGRATIONS_FOLDER, file), "r") as migration_file:
                json_migrations_oreview += "\n\n"

                migration = json.load(migration_file)
                json_migrations_oreview = "\n".join(
                    (json_migrations_oreview, f"- id: {migration['id']}")
                )
                json_migrations_oreview = "\n".join(
                    (json_migrations_oreview, f"  file: {file}")
                )
                json_migrations_oreview = "\n".join(
                    (
                        json_migrations_oreview,
                        f"  description: {migration['description']}",
                    )
                )

    logger.info(json_migrations_oreview)


def migrations_run(args: argparse.Namespace) -> None:
    web3_session = yield_web3_provider()
    db_session = SessionLocal()
    try:
        if args.id == 20230904:
            step_order = [
                "fill_missing_selectors_in_moonworm_tasks",
                "deduplicate_moonworm_tasks",
            ]
            step_map: Dict[str, Dict[str, Any]] = {
                "upgrade": {
                    "fill_missing_selectors_in_moonworm_tasks": {
                        "action": add_selectors.fill_missing_selectors_in_moonworm_tasks,
                        "description": "Get all moonworm jobs from moonworm journal and add selector tag if it not represent",
                    },
                    "deduplicate_moonworm_tasks": {
                        "action": add_selectors.deduplicate_moonworm_task_by_selector,
                        "description": "Deduplicate moonworm tasks by selector",
                    },
                },
                "downgrade": {},
            }
            if args.command not in ["upgrade", "downgrade"]:
                logger.info("Wrong command. Please use upgrade or downgrade")
            step = args.step

            migration_run(step_map, args.command, step, step_order)

        if args.id == 20230501:
            # fix entity duplicates keys for all subscriptions introduced in 20230213

            step_order = ["fix_duplicates_keys_in_entity_subscription"]
            step_map: Dict[str, Dict[str, Any]] = {
                "upgrade": {
                    "fix_duplicates_keys_in_entity_subscription": {
                        "action": generate_entity_subscriptions.fix_duplicates_keys_in_entity_subscription,
                        "description": "Fix entity duplicates keys for all subscriptions introduced in 20230213",
                    },
                },
                "downgrade": {},
            }
            if args.command not in ["upgrade", "downgrade"]:
                logger.info("Wrong command. Please use upgrade or downgrade")
            step = args.step

            migration_run(step_map, args.command, step, step_order)

        if args.id == 20230213:
            step_order = [
                "generate_entity_subscriptions_from_brood_resources",
                "update_dashboards_connection",
            ]
            step_map = {
                "upgrade": {
                    "generate_entity_subscriptions_from_brood_resources": {
                        "action": generate_entity_subscriptions.generate_entity_subscriptions_from_brood_resources,
                        "description": "Generate entity subscriptions from brood resources",
                    },
                    "update_dashboards_connection": {
                        "action": generate_entity_subscriptions.update_dashboards_connection,
                        "description": "Update dashboards connection",
                    },
                },
                "downgrade": {
                    "generate_entity_subscriptions_from_brood_resources": {
                        "action": generate_entity_subscriptions.delete_generated_entity_subscriptions_from_brood_resources,
                        "description": "Delete generated entity subscriptions from brood resources",
                    },
                    "update_dashboards_connection": {
                        "action": generate_entity_subscriptions.restore_dashboard_state,
                        "description": "Restore dashboard state",
                    },
                },
            }
            if args.command not in ["upgrade", "downgrade"]:
                logger.info("Wrong command. Please use upgrade or downgrade")
            step = args.step

            migration_run(step_map, args.command, step, step_order)

        elif args.id == 20211101:
            logger.info("Starting update of subscriptions in Brood resource...")
            checksum_address.checksum_all_subscription_addresses(web3_session)
            logger.info("Starting update of ethereum_labels in database...")
            checksum_address.checksum_all_labels_addresses(db_session, web3_session)
        elif args.id == 20211202:
            update_dashboard_subscription_key.update_dashboard_resources_key()
        elif args.id == 20211108:
            drop_keys = []

            if args.file is not None:
                with open(args.file) as migration_json_file:
                    migration_json = json.load(migration_json_file)

                if (
                    "match" not in migration_json
                    or "update" not in migration_json[args.command]
                    or "description" not in migration_json
                ):
                    print(
                        'Migration file plan have incorrect format require specified {"match": {},"description": "","upgrade": { "update": {}, "drop_keys": [] }, "downgrade": { "update": {}, "drop_keys": [] }}'
                    )
                    return

                match = migration_json["match"]
                description = migration_json["description"]
                update = migration_json[args.command]["update"]
                file = args.file

                if "drop_keys" in migration_json[args.command]:
                    drop_keys = migration_json[args.command]["drop_keys"]

                subscriptions.migrate_subscriptions(
                    match=match,
                    descriptions=description,
                    update=update,
                    drop_keys=drop_keys,
                    file=file,
                )

            else:
                print("Specified ID or migration FILE is required.")
                return
    finally:
        db_session.close()


def moonworm_tasks_list_handler(args: argparse.Namespace) -> None:
    moonworm_tasks.get_list_of_addresses()


def moonworm_tasks_add_subscription_handler(args: argparse.Namespace) -> None:
    moonworm_tasks.add_subscription(args.id)


def generate_usage_handler(args: argparse.Namespace) -> None:
    usage_info = usage.collect_usage_information(
        month=args.month,
        user_id=args.user_id,
        contracts=args.contracts,
    )

    if MOONSTREAM_USAGE_REPORTS_JOURNAL_ID is not None:

        usage.push_report_to_bugout_journal(
            name=args.name,
            user_id=args.user_id,
            month=args.month,
            journal_id=MOONSTREAM_USAGE_REPORTS_JOURNAL_ID,
            report=usage_info,
            token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
        )

    if args.output is not None:
        # create path if not exists

        if not os.path.exists(os.path.dirname(args.output)):
            os.makedirs(os.path.dirname(args.output))

        with open(args.output, "w") as output_file:
            output_file.write(json.dumps(usage_info, indent=4))


def moonworm_tasks_v3_migrate(args: argparse.Namespace) -> None:
    """
    Read users subsriptions and rewrite them to v3 jobs table
    """
    ### Request user resources from brood

    moonworm_tasks.migrate_v3_tasks(
        user_id=args.user_id, customer_id=args.customer_id, blockchain=args.blockchain
    )


def create_v3_task_handler(args: argparse.Namespace) -> None:

    moonworm_tasks.create_v3_task(
        user_id=args.user_id,
        customer_id=args.customer_id,
        blockchain=args.blockchain,
        address=args.address,
        abi=json.loads(args.abi.read()),
    )


def delete_v3_task_handler(args: argparse.Namespace) -> None:

    tasks = moonworm_tasks.get_v3_tasks(
        user_id=args.user_id,
        customer_id=args.customer_id,
        blockchain=args.blockchain,
        address=args.address,
    )

    tasks_dict_output: Dict[str, int] = {}
    for task in tasks:
        if task.chain not in tasks_dict_output:
            tasks_dict_output[task.chain] = 0
        tasks_dict_output[task.chain] += 1
    
    print("Found:")
    for k, v in tasks_dict_output.items():
        print(f"- {k} - {v} tasks")

    response = input(f"Delete {len(tasks)} tasks? (yes/y): ").strip().lower()
    if response != "yes" and response != "y":
        logger.warning("Canceled")
        return

    moonworm_tasks.delete_v3_tasks(tasks=tasks)


def main() -> None:
    cli_description = f"""Moonstream Admin CLI

Please make sure that the following environment variables are set in your environment and exported to
subprocesses:
1. MOONSTREAM_APPLICATION_ID
2. MOONSTREAM_ADMIN_ACCESS_TOKEN

Current Moonstream application ID: {MOONSTREAM_APPLICATION_ID}

This CLI is configured to work with the following API URLs:
- Brood: {BUGOUT_BROOD_URL} (override by setting BUGOUT_BROOD_URL environment variable)
- Spire: {BUGOUT_SPIRE_URL} (override by setting BUGOUT_SPIRE_URL environment variable)
"""
    parser = argparse.ArgumentParser(
        description=cli_description,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.set_defaults(func=lambda _: parser.print_help())
    subcommands = parser.add_subparsers(description="Moonstream commands")

    parser_subscription_types = subcommands.add_parser(
        "subtypes", description="Manage Moonstream subscription types"
    )
    parser_subscription_types.set_defaults(
        func=lambda _: parser_subscription_types.print_help()
    )
    subcommands_subscription_types = parser_subscription_types.add_subparsers()

    parser_subscription_types_create = subcommands_subscription_types.add_parser(
        "create", description="Create subscription type"
    )
    parser_subscription_types_create.add_argument(
        "-i", "--id", required=True, type=str, help="ID for the subscription type"
    )
    parser_subscription_types_create.add_argument(
        "-n",
        "--name",
        required=True,
        type=str,
        help="Human-friendly name for the subscription type",
    )
    parser_subscription_types_create.add_argument(
        "-d",
        "--description",
        required=True,
        type=str,
        help="Detailed description of the subscription type",
    )
    parser_subscription_types_create.add_argument(
        "-c",
        "--choices",
        nargs="*",
        help="Available subscription options for from builder.",
        required=True,
    )
    parser_subscription_types_create.add_argument(
        "--icon",
        required=True,
        help="URL to the icon representing this subscription type",
    )
    parser_subscription_types_create.add_argument(
        "--stripe-product-id",
        required=False,
        default=None,
        type=str,
        help="Stripe product id",
    )
    parser_subscription_types_create.add_argument(
        "--stripe-price-id",
        required=False,
        default=None,
        type=str,
        help="Stripe price id",
    )
    parser_subscription_types_create.add_argument(
        "--active",
        action="store_true",
        help="Set this flag to mark the subscription as active",
    )
    parser_subscription_types_create.set_defaults(
        func=subscription_types.cli_create_subscription_type
    )

    parser_subscription_types_list = subcommands_subscription_types.add_parser(
        "list", description="List subscription types"
    )
    parser_subscription_types_list.add_argument(
        "--active",
        action="store_true",
        help="Set this flag to only list active subscription types",
    )
    parser_subscription_types_list.set_defaults(
        func=subscription_types.cli_list_subscription_types
    )

    parser_subscription_types_get = subcommands_subscription_types.add_parser(
        "get", description="Get a subscription type by its ID"
    )
    parser_subscription_types_get.add_argument(
        "-i",
        "--id",
        required=True,
        help="ID of the subscription type you would like information about",
    )
    parser_subscription_types_get.set_defaults(
        func=subscription_types.cli_get_subscription_type
    )

    parser_subscription_types_update = subcommands_subscription_types.add_parser(
        "update", description="Update subscription type"
    )
    parser_subscription_types_update.add_argument(
        "-i", "--id", required=True, type=str, help="ID for the subscription type"
    )
    parser_subscription_types_update.add_argument(
        "-n",
        "--name",
        required=False,
        default=None,
        type=str,
        help="Human-friendly name for the subscription type",
    )
    parser_subscription_types_update.add_argument(
        "-d",
        "--description",
        required=False,
        default=None,
        type=str,
        help="Detailed description of the subscription type",
    )
    parser_subscription_types_update.add_argument(
        "-c",
        "--choices",
        nargs="*",
        help="Available subscription options for form builder.",
        required=False,
    )
    parser_subscription_types_update.add_argument(
        "--icon",
        required=False,
        default=None,
        help="URL to the icon representing this subscription type",
    )
    parser_subscription_types_update.add_argument(
        "--stripe-product-id",
        required=False,
        default=None,
        type=str,
        help="Stripe product id",
    )
    parser_subscription_types_update.add_argument(
        "--stripe-price-id",
        required=False,
        default=None,
        type=str,
        help="Stripe price id",
    )
    parser_subscription_types_update.add_argument(
        "--active",
        required=False,
        type=parse_boolean_arg,
        default=None,
        help="Mark the subscription as active (True) or inactive (False).",
    )
    parser_subscription_types_update.set_defaults(
        func=subscription_types.cli_update_subscription_type
    )

    parser_subscription_types_delete = subcommands_subscription_types.add_parser(
        "delete", description="Delete a subscription type by its ID"
    )
    parser_subscription_types_delete.add_argument(
        "-i",
        "--id",
        required=True,
        help="ID of the subscription type you would like to delete.",
    )
    parser_subscription_types_delete.set_defaults(
        func=subscription_types.cli_delete_subscription_type
    )

    parser_subscription_types_canonicalize = subcommands_subscription_types.add_parser(
        "ensure-canonical",
        description="Ensure that the connected Brood API contains resources for each of the canonical subscription types",
    )
    parser_subscription_types_canonicalize.set_defaults(
        func=subscription_types.cli_ensure_canonical_subscription_types
    )

    parser_migrations = subcommands.add_parser(
        "migrations", description="Manage database, resource and etc migrations"
    )
    parser_migrations.set_defaults(func=lambda _: parser_migrations.print_help())
    subcommands_migrations = parser_migrations.add_subparsers(
        description="Migration commands"
    )
    parser_migrations_list = subcommands_migrations.add_parser(
        "list", description="List migrations"
    )
    parser_migrations_list.set_defaults(func=migrations_list)
    parser_migrations_run = subcommands_migrations.add_parser(
        "run", description="Run migration"
    )
    parser_migrations_run.add_argument(
        "-i", "--id", required=False, type=int, help="Provide migration ID"
    )
    parser_migrations_run.add_argument(
        "-f", "--file", required=False, type=str, help="path to file"
    )
    parser_migrations_run.add_argument(
        "-c",
        "--command",
        default="upgrade",
        choices=["upgrade", "downgrade"],
        type=str,
        help="Command for migration",
    )
    parser_migrations_run.add_argument(
        "-s",
        "--step",
        required=False,
        type=str,
        help="How many steps to run",
    )
    parser_migrations_run.set_defaults(func=migrations_run)

    parser_moonworm_tasks = subcommands.add_parser(
        "moonworm-tasks", description="Manage tasks for moonworm journal."
    )

    parser_moonworm_tasks.set_defaults(func=lambda _: parser_migrations.print_help())
    subcommands_moonworm_tasks = parser_moonworm_tasks.add_subparsers(
        description="Moonworm taks commands"
    )
    parser_moonworm_tasks_list = subcommands_moonworm_tasks.add_parser(
        "list", description="Return list of addresses in moonworm journal."
    )

    parser_moonworm_tasks_list.set_defaults(func=moonworm_tasks_list_handler)

    parser_moonworm_tasks_add = subcommands_moonworm_tasks.add_parser(
        "add_subscription", description="Manage tasks for moonworm journal."
    )

    parser_moonworm_tasks_add.add_argument(
        "-i",
        "--id",
        type=str,
        help="Id of subscription for add to moonworm tasks.",
    )

    parser_moonworm_tasks_add.set_defaults(func=moonworm_tasks_add_subscription_handler)

    parser_moonworm_tasks_migrate = subcommands_moonworm_tasks.add_parser(
        "migrate-v2-tasks",
        description="Migrate moonworm tasks to abi_jobs of moonstream index",
    )

    parser_moonworm_tasks_migrate.add_argument(
        "--user-id",
        required=True,
        type=uuid_type,
        help="user-id of which we want see subscription.",
    )

    parser_moonworm_tasks_migrate.add_argument(
        "--customer-id",
        required=True,
        type=uuid_type,
        help="customer-id of which we want see subscription.",
    )

    parser_moonworm_tasks_migrate.add_argument(
        "--blockchain",
        required=False,
        type=str,
        help="Blockchain of which we want see subscription.",
    )

    parser_moonworm_tasks_migrate.set_defaults(func=moonworm_tasks_v3_migrate)

    parser_moonworm_tasks_v3_create = subcommands_moonworm_tasks.add_parser(
        "create-v3-tasks",
        description="Create new v3 tasks",
    )

    parser_moonworm_tasks_v3_create.add_argument(
        "--user-id",
        required=True,
        type=uuid_type,
        help="user-id of which we want see subscription.",
    )

    parser_moonworm_tasks_v3_create.add_argument(
        "--customer-id",
        required=True,
        type=uuid_type,
        help="customer-id of which we want see subscription.",
    )

    parser_moonworm_tasks_v3_create.add_argument(
        "--blockchain",
        required=True,
        type=str,
        help="Blockchain of which we want see subscription.",
    )

    parser_moonworm_tasks_v3_create.add_argument(
        "--address",
        required=True,
        type=str,
        help="Address of which we want see subscription.",
    )

    parser_moonworm_tasks_v3_create.add_argument(
        "--abi",
        required=True,
        type=argparse.FileType("r"),
        help="ABI of which we want see subscription.",
    )

    parser_moonworm_tasks_v3_create.set_defaults(func=create_v3_task_handler)

    parser_moonworm_tasks_v3_delete = subcommands_moonworm_tasks.add_parser(
        "delete-v3-tasks",
        description="Delete v3 tasks",
    )

    parser_moonworm_tasks_v3_delete.add_argument(
        "--user-id",
        type=uuid_type,
        help="The user ID of which we wish to delete the task",
    )

    parser_moonworm_tasks_v3_delete.add_argument(
        "--customer-id",
        type=uuid_type,
        help="The customer ID of which we wish to delete the task",
    )

    parser_moonworm_tasks_v3_delete.add_argument(
        "--blockchain",
        type=str,
        help="Blockchain name",
    )

    parser_moonworm_tasks_v3_delete.add_argument(
        "--address",
        type=str,
        help="Contract address",
    )

    parser_moonworm_tasks_v3_delete.set_defaults(func=delete_v3_task_handler)

    queries_parser = subcommands.add_parser(
        "queries", description="Manage Moonstream queries"
    )
    queries_parser.set_defaults(func=lambda _: queries_parser.print_help())

    queries_subcommands = queries_parser.add_subparsers(description="Query commands")

    create_query_parser = queries_subcommands.add_parser(
        "create-template", description="Create query template"
    )

    create_query_parser.add_argument(
        "--query-file",
        required=True,
        type=argparse.FileType("r"),
        help="File containing the query to add",
    )
    create_query_parser.add_argument(
        "-n", "--name", required=True, help="Name for the new query"
    )
    create_query_parser.set_defaults(func=queries.create_query_template)

    usage_parser = subcommands.add_parser(
        "usage", description="Manage Moonstream usage"
    )

    usage_parser.set_defaults(func=lambda _: usage_parser.print_help())

    usage_subcommands = usage_parser.add_subparsers(description="Usage commands")

    generate_usage_parser = usage_subcommands.add_parser(
        "generate", description="Generate usage"
    )

    generate_usage_parser.add_argument(
        "--month",
        required=True,
        type=str,
        help="Month for which to generate usage in YYYY-MM format (e.g. 2021-10)",
    )

    generate_usage_parser.add_argument(
        "--user-id",
        required=False,
        type=str,
        help="User token for which to generate usage (not implemented yet - use user-token instead)",
    )

    generate_usage_parser.add_argument(
        "--name",
        type=str,
        help="Name of the user for which to generate usage",
        default="",
    )

    generate_usage_parser.add_argument(
        "--contracts",
        required=False,
        type=json.loads,
        help="Contracts for which to generate usage Json format( { 'blockchain': ['contract_address',...] })",
    )

    generate_usage_parser.add_argument(
        "--output",
        required=False,
        type=str,
        help="Output file for usage",
    )

    generate_usage_parser.set_defaults(func=generate_usage_handler)

    ### databases commands
    databases_parser = subcommands.add_parser(
        "databases", description="Manage Moonstream databases"
    )

    databases_parser.set_defaults(func=lambda _: databases_parser.print_help())

    databases_subcommands = databases_parser.add_subparsers(
        description="Database commands"
    )

    database_labels_migration_parser = databases_subcommands.add_parser(
        "v2-to-v3-labels-migration",
        description="Migrate labels in database",
    )

    database_labels_migration_parser.add_argument(
        "--user-id",
        type=uuid_type,
        help="User ID for which to migrate labels",
    )

    database_labels_migration_parser.add_argument(
        "--customer-id",
        type=uuid_type,
        help="Customer ID for which to migrate labels",
    )

    database_labels_migration_parser.add_argument(
        "--blockchain",
        type=str,
        help="Blockchain for which to migrate labels",
    )

    database_labels_migration_parser.set_defaults(
        func=lambda args: print("Not implemented yet")
    )

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
