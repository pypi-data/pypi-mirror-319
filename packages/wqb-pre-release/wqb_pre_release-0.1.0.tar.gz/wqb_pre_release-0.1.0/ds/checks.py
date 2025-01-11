from typing import Any


class Check:
    _name: str
    _result: str
    _others: dict[str, Any]


'''
"checks": [
    {
        "name": "LOW_SHARPE",
        "result": "PASS",
        "limit": 1.58,
        "value": 2.21
    },
    {
        "name": "LOW_FITNESS",
        "result": "PASS",
        "limit": 1,
        "value": 2.78
    },
    {
        "name": "LOW_TURNOVER",
        "result": "PASS",
        "limit": 0.01,
        "value": 0.0758
    },
    {
        "name": "HIGH_TURNOVER",
        "result": "PASS",
        "limit": 0.7,
        "value": 0.0758
    },
    {
        "name": "CONCENTRATED_WEIGHT",
        "result": "PASS"
    },
    {
        "name": "LOW_SUB_UNIVERSE_SHARPE",
        "result": "PASS",
        "limit": 1.31,
        "value": 1.91
    },
    {
        "name": "SELF_CORRELATION",
        "result": "PENDING"
    },
    {
        "name": "DATA_DIVERSITY",
        "result": "PENDING"
    },
    {
        "name": "PROD_CORRELATION",
        "result": "PENDING"
    },
    {
        "name": "REGULAR_SUBMISSION",
        "result": "PENDING"
    },
    {
        "name": "IS_LADDER_SHARPE",
        "result": "PASS",
        "year": 2,
        "startDate": "2022-07-15",
        "endDate": "2020-07-16",
        "limit": 2.02,
        "value": 2.17
    },
    {
        "result": "PASS",
        "name": "MATCHES_PYRAMID",
        "multiplier": 1.3,
        "pyramids": [
            {
                "name": "HKG/D1/Price Volume",
                "multiplier": 1.3
            },
            {
                "name": "HKG/D1/Model",
                "multiplier": 1.6
            }
        ]
    }
]
'''
