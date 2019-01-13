#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès



NODES_MAX = 15
DEFAULT_TEAM = 'cewe@eweg'

SCORE = [
    {'Process': {'Limits - CMRC': 10,
                 'Limits - Metiers': 5,
                 'Limits - Others': 1,
                 'Daily Fair Value Reserve': 1,
                 'EOM Fair Value Reserve': 10,
                 'EOM Prudent Valuation': 1,
                 'Daily MAP Calculation': 1,
                 'EOM MAP Calculation': 10,
                 'CMRC Stress Testing': 5,
                 'Regulatory Stress Testing': 5,
                 'VAR sign-off': 1,
                 'Trade Approval': 1,
                 'Risk Monitoring': 1,
                 'IRC/CRM Monitoring': 1,
                 'System Access/Technical Issues': 1,
                 'Regulatory Reporting': 1,
                 'Weekly Reporting': 1
                }},

    {'Perimeter': {"EQD": 1,
                   "Commodity": 1,
                   "FXLM": 1,
                   "G10 Rates": 1,
                   "Credit": 1,
                   "PS&F": 1,
                   "GLCM": 5,
                   "OPERA": 1,
                   "XVA": 1,
                   "GLOBAL": 10,
                   "BP2S": 1}},

    {'Financial Impact': {
        "High": 10,
        "Medium": 5,
        "Low": 1,
        "None": 0}},
    {'Reputational Impact': {
        "Regulator": 10,
        "Top Management": 8,
        "Management": 6,
        "FO": 4,
        "Risk": 2,
        "None": 0},
     },

    {"Urgency": {
        "ASAP": 10,
        "In 1 day": 9,
        "In 2 to 5 days": 8,
        "By the end of the week": 5,
        "By the end of the month": 5,
        "Other longer term deadline": 1
    }}
]

DSC = {
    'eng': '''
:dsc:
# Incident Scoring and Diagnosis

This project

## What is this project for ?

## Who are we ?

'''
}