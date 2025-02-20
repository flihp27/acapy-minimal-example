"""Minimal reproducible example script.

This script is for you to use to reproduce a bug or demonstrate a feature.
"""

import asyncio
from os import getenv

from controller import Controller
from controller.logging import logging_to_stdout
from controller.protocols import (
    connection,
    didexchange,
    indy_anoncred_credential_artifacts,
    indy_anoncred_onboard,
    indy_issue_credential_v1,
    indy_issue_credential_v2,
    indy_present_proof_v1,
    indy_present_proof_v2,
)

ALICE = getenv("ALICE", "http://alice:3001")
BOB = getenv("BOB", "http://bob:3001")


async def main():
    """Test Controller protocols."""
    async with Controller(base_url=ALICE) as alice, Controller(base_url=BOB) as bob:
        await connection(alice, bob)
        alice_conn, bob_conn = await didexchange(alice, bob)
        await indy_anoncred_onboard(alice)
        schema, cred_def = await indy_anoncred_credential_artifacts(
            alice, ["firstname", "lastname"]
        )

        alice_cred_ex, bob_cred_ex = await indy_issue_credential_v1(
            alice,
            bob,
            alice_conn.connection_id,
            bob_conn.connection_id,
            cred_def.credential_definition_id,
            {"firstname": "Bob", "lastname": "Builder"},
        )
        print(alice_cred_ex.json(by_alias=True, indent=2))
        alice_cred_ex, bob_cred_ex = await indy_issue_credential_v2(
            alice,
            bob,
            alice_conn.connection_id,
            bob_conn.connection_id,
            cred_def.credential_definition_id,
            {"firstname": "Bob", "lastname": "Builder"},
        )
        print(alice_cred_ex.json(by_alias=True, indent=2))

        bob_pres_ex, alice_pres_ex = await indy_present_proof_v1(
            bob,
            alice,
            bob_conn.connection_id,
            alice_conn.connection_id,
            requested_attributes=[{"name": "firstname"}],
        )
        print(alice_pres_ex.json(by_alias=True, indent=2))
        bob_pres_ex, alice_pres_ex = await indy_present_proof_v2(
            bob,
            alice,
            bob_conn.connection_id,
            alice_conn.connection_id,
            requested_attributes=[{"name": "firstname"}],
        )
        print(alice_pres_ex.json(by_alias=True, indent=2))


if __name__ == "__main__":
    logging_to_stdout()
    asyncio.run(main())
