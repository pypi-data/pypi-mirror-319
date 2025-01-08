from enum import Enum
from dataclasses import dataclass
from typing import Any, Optional


class Constants:
    networks = ["local", "finney", "test", "archive", "rao", "dev"]
    finney_entrypoint = "wss://entrypoint-finney.opentensor.ai:443"
    finney_test_entrypoint = "wss://test.finney.opentensor.ai:443"
    archive_entrypoint = "wss://archive.chain.opentensor.ai:443"
    rao_entrypoint = "wss://rao.chain.opentensor.ai:443/"
    dev_entrypoint = "wss://dev.chain.opentensor.ai:443 "
    local_entrypoint = "ws://127.0.0.1:9944"
    network_map = {
        "finney": finney_entrypoint,
        "test": finney_test_entrypoint,
        "archive": archive_entrypoint,
        "local": local_entrypoint,
        "dev": dev_entrypoint,
        "rao": rao_entrypoint,
    }
    delegates_detail_url = "https://raw.githubusercontent.com/opentensor/bittensor-delegates/main/public/delegates.json"


@dataclass
class DelegatesDetails:
    display: str
    additional: list[tuple[str, str]]
    web: str
    legal: Optional[str] = None
    riot: Optional[str] = None
    email: Optional[str] = None
    pgp_fingerprint: Optional[str] = None
    image: Optional[str] = None
    twitter: Optional[str] = None

    @classmethod
    def from_chain_data(cls, data: dict[str, Any]) -> "DelegatesDetails":
        def decode(key: str, default=""):
            try:
                if isinstance(data.get(key), dict):
                    value = next(data.get(key).values())
                    return bytes(value[0]).decode("utf-8")
                elif isinstance(data.get(key), int):
                    return data.get(key)
                elif isinstance(data.get(key), tuple):
                    return bytes(data.get(key)[0]).decode("utf-8")
                else:
                    return default
            except (UnicodeDecodeError, TypeError):
                return default

        return cls(
            display=decode("display"),
            additional=decode("additional", []),
            web=decode("web"),
            legal=decode("legal"),
            riot=decode("riot"),
            email=decode("email"),
            pgp_fingerprint=decode("pgp_fingerprint", None),
            image=decode("image"),
            twitter=decode("twitter"),
        )


class Defaults:
    netuid = 1

    class config:
        base_path = "~/.bittensor"
        path = "~/.bittensor/config.yml"
        dictionary = {
            "network": None,
            "wallet_path": None,
            "wallet_name": None,
            "wallet_hotkey": None,
            "use_cache": True,
            "metagraph_cols": {
                "UID": True,
                "GLOBAL_STAKE": True,
                "LOCAL_STAKE": True,
                "STAKE_WEIGHT": True,
                "RANK": True,
                "TRUST": True,
                "CONSENSUS": True,
                "INCENTIVE": True,
                "DIVIDENDS": True,
                "EMISSION": True,
                "VTRUST": True,
                "VAL": True,
                "UPDATED": True,
                "ACTIVE": True,
                "AXON": True,
                "HOTKEY": True,
                "COLDKEY": True,
            },
        }

    class subtensor:
        network = "rao"
        chain_endpoint = None
        _mock = False

    class pow_register:
        num_processes = None
        update_interval = 50_000
        output_in_place = True
        verbose = False

        class cuda:
            dev_id = 0
            use_cuda = False
            tpb = 256

    class wallet:
        name = "default"
        hotkey = "default"
        path = "~/.bittensor/wallets/"

    class logging:
        debug = False
        trace = False
        record_log = False
        logging_dir = "~/.bittensor/miners"


defaults = Defaults


class WalletOptions(Enum):
    PATH: str = "path"
    NAME: str = "name"
    HOTKEY: str = "hotkey"


class WalletValidationTypes(Enum):
    NONE = None
    WALLET = "wallet"
    WALLET_AND_HOTKEY = "wallet_and_hotkey"


TYPE_REGISTRY = {
    "types": {
        "Balance": "u64",  # Need to override default u128
    },
    "runtime_api": {
        "DelegateInfoRuntimeApi": {
            "methods": {
                "get_delegated": {
                    "params": [
                        {
                            "name": "coldkey",
                            "type": "Vec<u8>",
                        },
                    ],
                    "type": "Vec<u8>",
                },
                "get_delegates": {
                    "params": [],
                    "type": "Vec<u8>",
                },
            }
        },
        "NeuronInfoRuntimeApi": {
            "methods": {
                "get_neuron_lite": {
                    "params": [
                        {
                            "name": "netuid",
                            "type": "u16",
                        },
                        {
                            "name": "uid",
                            "type": "u16",
                        },
                    ],
                    "type": "Vec<u8>",
                },
                "get_neurons_lite": {
                    "params": [
                        {
                            "name": "netuid",
                            "type": "u16",
                        },
                    ],
                    "type": "Vec<u8>",
                },
                "get_neuron": {
                    "params": [
                        {
                            "name": "netuid",
                            "type": "u16",
                        },
                        {
                            "name": "uid",
                            "type": "u16",
                        },
                    ],
                    "type": "Vec<u8>",
                },
                "get_neurons": {
                    "params": [
                        {
                            "name": "netuid",
                            "type": "u16",
                        },
                    ],
                    "type": "Vec<u8>",
                },
            }
        },
        "StakeInfoRuntimeApi": {
            "methods": {
                "get_stake_info_for_coldkey": {
                    "params": [{"name": "coldkey_account_vec", "type": "Vec<u8>"}],
                    "type": "Vec<u8>",
                },
                "get_stake_info_for_coldkeys": {
                    "params": [
                        {"name": "coldkey_account_vecs", "type": "Vec<Vec<u8>>"}
                    ],
                    "type": "Vec<u8>",
                },
                "get_subnet_stake_info_for_coldkeys": {
                    "params": [
                        {"name": "coldkey_account_vecs", "type": "Vec<Vec<u8>>"},
                        {"name": "netuid", "type": "u16"},
                    ],
                    "type": "Vec<u8>",
                },
                "get_subnet_stake_info_for_coldkey": {
                    "params": [
                        {"name": "coldkey_account_vec", "type": "Vec<u8>"},
                        {"name": "netuid", "type": "u16"},
                    ],
                    "type": "Vec<u8>",
                },
                "get_total_subnet_stake": {
                    "params": [{"name": "netuid", "type": "u16"}],
                    "type": "Vec<u8>",
                },
            }
        },
        "ValidatorIPRuntimeApi": {
            "methods": {
                "get_associated_validator_ip_info_for_subnet": {
                    "params": [
                        {
                            "name": "netuid",
                            "type": "u16",
                        },
                    ],
                    "type": "Vec<u8>",
                },
            },
        },
        "SubnetInfoRuntimeApi": {
            "methods": {
                "get_subnet_hyperparams": {
                    "params": [
                        {
                            "name": "netuid",
                            "type": "u16",
                        },
                    ],
                    "type": "Vec<u8>",
                },
                "get_subnet_info": {
                    "params": [
                        {
                            "name": "netuid",
                            "type": "u16",
                        },
                    ],
                    "type": "Vec<u8>",
                },
                "get_subnets_info": {
                    "params": [],
                    "type": "Vec<u8>",
                },
                "get_subnet_info_v2": {
                    "params": [
                        {
                            "name": "netuid",
                            "type": "u16",
                        },
                    ],
                    "type": "Vec<u8>",
                },
                "get_subnets_info_v2": {
                    "params": [],
                    "type": "Vec<u8>",
                },
                "get_all_dynamic_info": {
                    "params": [],
                    "type": "Vec<u8>",
                },
                "get_dynamic_info": {
                    "params": [{"name": "netuid", "type": "u16"}],
                    "type": "Vec<u8>",
                },
                "get_subnet_state": {
                    "params": [{"name": "netuid", "type": "u16"}],
                    "type": "Vec<u8>",
                },
            }
        },
        "SubnetRegistrationRuntimeApi": {
            "methods": {"get_network_registration_cost": {"params": [], "type": "u64"}}
        },
        "ColdkeySwapRuntimeApi": {
            "methods": {
                "get_scheduled_coldkey_swap": {
                    "params": [
                        {
                            "name": "coldkey_account_vec",
                            "type": "Vec<u8>",
                        },
                    ],
                    "type": "Vec<u8>",
                },
                "get_remaining_arbitration_period": {
                    "params": [
                        {
                            "name": "coldkey_account_vec",
                            "type": "Vec<u8>",
                        },
                    ],
                    "type": "Vec<u8>",
                },
                "get_coldkey_swap_destinations": {
                    "params": [
                        {
                            "name": "coldkey_account_vec",
                            "type": "Vec<u8>",
                        },
                    ],
                    "type": "Vec<u8>",
                },
            }
        },
    },
}

UNITS = [
    "\u03c4",  # τ (tau, 0)
    "\u03b1",  # α (alpha, 1)
    "\u03b2",  # β (beta, 2)
    "\u03b3",  # γ (gamma, 3)
    "\u03b4",  # δ (delta, 4)
    "\u03b5",  # ε (epsilon, 5)
    "\u03b6",  # ζ (zeta, 6)
    "\u03b7",  # η (eta, 7)
    "\u03b8",  # θ (theta, 8)
    "\u03b9",  # ι (iota, 9)
    "\u03ba",  # κ (kappa, 10)
    "\u03bb",  # λ (lambda, 11)
    "\u03bc",  # μ (mu, 12)
    "\u03bd",  # ν (nu, 13)
    "\u03be",  # ξ (xi, 14)
    "\u03bf",  # ο (omicron, 15)
    "\u03c0",  # π (pi, 16)
    "\u03c1",  # ρ (rho, 17)
    "\u03c3",  # σ (sigma, 18)
    "t",  # t (tau, 19)
    "\u03c5",  # υ (upsilon, 20)
    "\u03c6",  # φ (phi, 21)
    "\u03c7",  # χ (chi, 22)
    "\u03c8",  # ψ (psi, 23)
    "\u03c9",  # ω (omega, 24)
    # Hebrew letters
    "\u05d0",  # א (aleph, 25)
    "\u05d1",  # ב (bet, 26)
    "\u05d2",  # ג (gimel, 27)
    "\u05d3",  # ד (dalet, 28)
    "\u05d4",  # ה (he, 29)
    "\u05d5",  # ו (vav, 30)
    "\u05d6",  # ז (zayin, 31)
    "\u05d7",  # ח (het, 32)
    "\u05d8",  # ט (tet, 33)
    "\u05d9",  # י (yod, 34)
    "\u05da",  # ך (final kaf, 35)
    "\u05db",  # כ (kaf, 36)
    "\u05dc",  # ל (lamed, 37)
    "\u05dd",  # ם (final mem, 38)
    "\u05de",  # מ (mem, 39)
    "\u05df",  # ן (final nun, 40)
    "\u05e0",  # נ (nun, 41)
    "\u05e1",  # ס (samekh, 42)
    "\u05e2",  # ע (ayin, 43)
    "\u05e3",  # ף (final pe, 44)
    "\u05e4",  # פ (pe, 45)
    "\u05e5",  # ץ (final tsadi, 46)
    "\u05e6",  # צ (tsadi, 47)
    "\u05e7",  # ק (qof, 48)
    "\u05e8",  # ר (resh, 49)
    "\u05e9",  # ש (shin, 50)
    "\u05ea",  # ת (tav, 51)
    # Georgian Alphabet (Mkhedruli)
    "\u10d0",  # ა (Ani, 97)
    "\u10d1",  # ბ (Bani, 98)
    "\u10d2",  # გ (Gani, 99)
    "\u10d3",  # დ (Doni, 100)
    "\u10d4",  # ე (Eni, 101)
    "\u10d5",  # ვ (Vini, 102)
    # Armenian Alphabet
    "\u0531",  # Ա (Ayp, 103)
    "\u0532",  # Բ (Ben, 104)
    "\u0533",  # Գ (Gim, 105)
    "\u0534",  # Դ (Da, 106)
    "\u0535",  # Ե (Ech, 107)
    "\u0536",  # Զ (Za, 108)
    # "\u055e",  # ՞ (Question mark, 109)
    # Runic Alphabet
    "\u16a0",  # ᚠ (Fehu, wealth, 81)
    "\u16a2",  # ᚢ (Uruz, strength, 82)
    "\u16a6",  # ᚦ (Thurisaz, giant, 83)
    "\u16a8",  # ᚨ (Ansuz, god, 84)
    "\u16b1",  # ᚱ (Raidho, ride, 85)
    "\u16b3",  # ᚲ (Kaunan, ulcer, 86)
    "\u16c7",  # ᛇ (Eihwaz, yew, 87)
    "\u16c9",  # ᛉ (Algiz, protection, 88)
    "\u16d2",  # ᛒ (Berkanan, birch, 89)
    # Cyrillic Alphabet
    "\u0400",  # Ѐ (Ie with grave, 110)
    "\u0401",  # Ё (Io, 111)
    "\u0402",  # Ђ (Dje, 112)
    "\u0403",  # Ѓ (Gje, 113)
    "\u0404",  # Є (Ukrainian Ie, 114)
    "\u0405",  # Ѕ (Dze, 115)
    # Coptic Alphabet
    "\u2c80",  # Ⲁ (Alfa, 116)
    "\u2c81",  # ⲁ (Small Alfa, 117)
    "\u2c82",  # Ⲃ (Vida, 118)
    "\u2c83",  # ⲃ (Small Vida, 119)
    "\u2c84",  # Ⲅ (Gamma, 120)
    "\u2c85",  # ⲅ (Small Gamma, 121)
    # Arabic letters
    "\u0627",  # ا (alef, 52)
    "\u0628",  # ب (ba, 53)
    "\u062a",  # ت (ta, 54)
    "\u062b",  # ث (tha, 55)
    "\u062c",  # ج (jeem, 56)
    "\u062d",  # ح (ha, 57)
    "\u062e",  # خ (kha, 58)
    "\u062f",  # د (dal, 59)
    "\u0630",  # ذ (dhal, 60)
    "\u0631",  # ر (ra, 61)
    "\u0632",  # ز (zay, 62)
    "\u0633",  # س (seen, 63)
    "\u0634",  # ش (sheen, 64)
    "\u0635",  # ص (sad, 65)
    "\u0636",  # ض (dad, 66)
    "\u0637",  # ط (ta, 67)
    "\u0638",  # ظ (dha, 68)
    "\u0639",  # ع (ain, 69)
    "\u063a",  # غ (ghain, 70)
    "\u0641",  # ف (fa, 71)
    "\u0642",  # ق (qaf, 72)
    "\u0643",  # ك (kaf, 73)
    "\u0644",  # ل (lam, 74)
    "\u0645",  # م (meem, 75)
    "\u0646",  # ن (noon, 76)
    "\u0647",  # ه (ha, 77)
    "\u0648",  # و (waw, 78)
    "\u0649",  # ى (alef maksura, 79)
    "\u064a",  # ي (ya, 80)
    # Ogham Alphabet
    "\u1680",  #   (Space, 90)
    "\u1681",  # ᚁ (Beith, birch, 91)
    "\u1682",  # ᚂ (Luis, rowan, 92)
    "\u1683",  # ᚃ (Fearn, alder, 93)
    "\u1684",  # ᚄ (Sail, willow, 94)
    "\u1685",  # ᚅ (Nion, ash, 95)
    "\u169b",  # ᚛ (Forfeda, 96)
    # Tifinagh Alphabet
    "\u2d30",  # ⴰ (Ya, 127)
    "\u2d31",  # ⴱ (Yab, 128)
]

NETWORK_EXPLORER_MAP = {
    "opentensor": {
        "local": "https://polkadot.js.org/apps/?rpc=wss%3A%2F%2Fentrypoint-finney.opentensor.ai%3A443#/explorer",
        "endpoint": "https://polkadot.js.org/apps/?rpc=wss%3A%2F%2Fentrypoint-finney.opentensor.ai%3A443#/explorer",
        "finney": "https://polkadot.js.org/apps/?rpc=wss%3A%2F%2Fentrypoint-finney.opentensor.ai%3A443#/explorer",
    },
    "taostats": {
        "local": "https://x.taostats.io",
        "endpoint": "https://x.taostats.io",
        "finney": "https://x.taostats.io",
    },
}


HYPERPARAMS = {
    "serving_rate_limit": "sudo_set_serving_rate_limit",
    "min_difficulty": "sudo_set_min_difficulty",
    "max_difficulty": "sudo_set_max_difficulty",
    "weights_version": "sudo_set_weights_version_key",
    "weights_rate_limit": "sudo_set_weights_set_rate_limit",
    "max_weight_limit": "sudo_set_max_weight_limit",
    "immunity_period": "sudo_set_immunity_period",
    "min_allowed_weights": "sudo_set_min_allowed_weights",
    "activity_cutoff": "sudo_set_activity_cutoff",
    "network_registration_allowed": "sudo_set_network_registration_allowed",
    "network_pow_registration_allowed": "sudo_set_network_pow_registration_allowed",
    "min_burn": "sudo_set_min_burn",
    "max_burn": "sudo_set_max_burn",
    "adjustment_alpha": "sudo_set_adjustment_alpha",
    "rho": "sudo_set_rho",
    "kappa": "sudo_set_kappa",
    "difficulty": "sudo_set_difficulty",
    "bonds_moving_avg": "sudo_set_bonds_moving_average",
    "commit_reveal_weights_interval": "sudo_set_commit_reveal_weights_interval",
    "commit_reveal_weights_enabled": "sudo_set_commit_reveal_weights_enabled",
    "alpha_values": "sudo_set_alpha_values",
    "liquid_alpha_enabled": "sudo_set_liquid_alpha_enabled",
}

# Help Panels for cli help
HELP_PANELS = {
    "WALLET": {
        "MANAGEMENT": "Wallet Management",
        "TRANSACTIONS": "Wallet Transactions",
        "IDENTITY": "Identity Management",
        "INFORMATION": "Wallet Information",
        "OPERATIONS": "Wallet Operations",
        "SECURITY": "Security & Recovery",
    },
    "ROOT": {
        "NETWORK": "Network Information",
        "WEIGHT_MGMT": "Weights Management",
        "GOVERNANCE": "Governance",
        "REGISTRATION": "Registration",
        "DELEGATION": "Delegation",
    },
    "STAKE": {
        "STAKE_MGMT": "Stake Management",
        "CHILD": "Child Hotkeys",
    },
    "SUDO": {
        "CONFIG": "Subnet Configuration",
        "GOVERNANCE": "Governance",
        "TAKE": "Delegate take configuration",
    },
    "SUBNETS": {
        "INFO": "Subnet Information",
        "CREATION": "Subnet Creation & Management",
        "REGISTER": "Neuron Registration",
    },
    "WEIGHTS": {"COMMIT_REVEAL": "Commit / Reveal"},
}

COLOR_PALETTE = {
    "GENERAL": {
        "HEADER": "#4196D6",           # Light Blue
        "LINKS": "#8CB9E9",           # Sky Blue
        "HINT": "#A2E5B8",            # Mint Green
        "COLDKEY": "#9EF5E4",         # Aqua
        "HOTKEY": "#ECC39D",          # Light Orange/Peach
        "SUBHEADING_MAIN": "#7ECFEC", # Light Cyan
        "SUBHEADING": "#AFEFFF",      # Pale Blue
        "SUBHEADING_EXTRA_1": "#96A3C5", # Grayish Blue
        "SUBHEADING_EXTRA_2": "#6D7BAF", # Slate Blue
        "CONFIRMATION_Y_N_Q": "#EE8DF8", # Light Purple/Pink
        "SYMBOL": "#E7CC51",          # Gold
        "BALANCE": "#4F91C6",         # Medium Blue
        "COST": "#53B5A0",           # Teal
        "SUCCESS": "#53B5A0",         # Teal
        "NETUID": "#CBA880",          # Tan
        "NETUID_EXTRA": "#DDD5A9",    # Light Khaki
        "TEMPO": "#67A3A5",           # Grayish Teal
    },
    "STAKE": {
        "STAKE_AMOUNT": "#53B5A0",    # Teal
        "STAKE_ALPHA": "#53B5A0",     # Teal
        "STAKE_SWAP": "#67A3A5",      # Grayish Teal
        "TAO": "#4F91C6",             # Medium Blue
        "SLIPPAGE_TEXT": "#C25E7C",   # Rose
        "SLIPPAGE_PERCENT": "#E7B195", # Light Coral
        "NOT_REGISTERED": "#EB6A6C",   # Salmon Red
        "EXTRA_1": "#D781BB",         # Pink
    },
    "POOLS": {
        "TAO": "#4F91C6",             # Medium Blue
        "ALPHA_IN": "#D09FE9",        # Light Purple
        "ALPHA_OUT": "#AB7CC8",       # Medium Purple
        "RATE": "#F8D384",            # Light Orange
        "TAO_EQUIV": "#8CB9E9",       # Sky Blue
        "EMISSION": "#F8D384",        # Light Orange
        "EXTRA_1": "#CAA8FB",         # Lavender
        "EXTRA_2": "#806DAF",         # Dark Purple
    },
    "GREY": {
        "GREY_100": "#F8F9FA",        # Almost White
        "GREY_200": "#F1F3F4",        # Very Light Grey
        "GREY_300": "#DBDDE1",        # Light Grey
        "GREY_400": "#BDC1C6",        # Medium Light Grey
        "GREY_500": "#5F6368",        # Medium Grey
        "GREY_600": "#2E3134",        # Medium Dark Grey
        "GREY_700": "#282A2D",        # Dark Grey
        "GREY_800": "#17181B",        # Very Dark Grey
        "GREY_900": "#0E1013",        # Almost Black
        "BLACK": "#000000",           # Pure Black
    },
    "SUDO": {
        "HYPERPARAMETER": "#4F91C6",  # Medium Blue
        "VALUE": "#D09FE9",           # Light Purple
        "NORMALIZED": "#AB7CC8",      # Medium Purple
    },
}


SUBNETS = {
    0: "root",
    1: "apex",
    2: "omron",
    3: "templar",
    4: "targon",
    5: "kaito",
    6: "infinite",
    7: "subvortex",
    8: "ptn",
    9: "pretrain",
    10: "sturday",
    11: "dippy",
    12: "horde",
    13: "dataverse",
    14: "palaidn",
    15: "deval",
    16: "bitads",
    17: "3gen",
    18: "cortex",
    19: "inference",
    20: "bitagent",
    21: "any-any",
    22: "meta",
    23: "social",
    24: "omega",
    25: "protein",
    26: "alchemy",
    27: "compute",
    28: "oracle",
    29: "coldint",
    30: "bet",
    31: "naschain",
    32: "itsai",
    33: "ready",
    34: "mind",
    35: "logic",
    36: "automata",
    37: "tuning",
    38: "distributed",
    39: "edge",
    40: "chunk",
    41: "sportsensor",
    42: "masa",
    43: "graphite",
    44: "score",
    45: "gen42",
    46: "neural",
    47: "condense",
    48: "nextplace",
    49: "automl",
    50: "audio",
    51: "celium",
    52: "dojo",
    53: "frontier",
    54: "docs-insight",
    56: "gradients",
    57: "gaia",
    58: "dippy-speech",
    59: "agent-arena",
    61: "red-team",
}
