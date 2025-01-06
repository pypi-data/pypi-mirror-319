#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) TCL DIGITAL TECHNOLOGY (SHENZHEN) CO., LTD."
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@tcl.com"

from enum import Enum

# 中国区红外键码值
_KEY_CODES_CN = {
    "CAMERA": "",
    "POWER": "FE DF 4F 05 AB E1",
    "MUTE": "FE DF CF 0F 03 C3",
    ".": "",
    "0": "FE DF CF 00 F3 3C",
    "1": "FE DF CF 08 73 B4",
    "2": "FE DF CF 04 B3 78",
    "3": "FE DF CF 0C 33 F0",
    "4": "FE DF CF 02 D3 1E",
    "5": "FE DF CF 0A 53 96",
    "6": "FE DF CF 06 93 5A",
    "7": "FE DF CF 0E 13 D2",
    "8": "FE DF CF 01 E3 2D",
    "9": "FE DF CF 09 63 A5",
    "UP": "FE DF AF 09 65 C3",
    "DOWN": "FE DF AF 01 E5 4B",
    "LEFT": "FE DF AF 06 95 3C",
    "RIGHT": "FE DF AF 0E 15 B4",
    "OK": "FE DF FF 02 D0 2D",
    "HOME": "FE DF 0F 01 EF E1",
    "VOLUME+": "FE DF 4F 0F 0B 4B",
    "VOLUME-": "FE DF 4F 07 8B C3",
    "P+": "FE DF 4F 0B 4B 0F",
    "P-": "FE DF 4F 03 CB 87",
    "RED": "FE DF 0F 00 FF F0",
    "GREEN": "FE DF 7F 01 E8 96",
    "YELLOW": "FE DF 7F 02 D8 A5",
    "BLUE": "FE DF BF 01 E4 5A",
    "PICTURE": "",
    "EPG": "",
    "TV": "",
    "MEDIA": "",
    "SETTING": "FE DF 3F 0F 0C 3C",
    "FREEZE": "",
    "INFO": "",
    "CN-INFO": "",
    "SOURCE": "FE DF 5F 0C 3A 69",
    "NEXT": "",
    "PLAY": "FE DF 8F 0A 57 D2",
    "PAUSE": "FE DF 8F 09 67 E1",
    "FAST-BACK": "FE DF 8F 0B 47 C3",
    "FAST-FORWARD": "FE DF 8F 03 C7 4B",
    "STOP": "FE DF 8F 0F 07 87",
    "LIST": "FE DF 6F 08 79 1E",
    "OPTION": "FE DF 7F 03 C8 B4",
    "MENU": "FE DF 9F 0B 46 D2",
    "EXIT": "FE DF 0F 06 9F 96",
    "BACK": "FE DF 4F 0E 1B 5A",
    "LANGUAGE": "FE DF BF 0F 04 B4",
    "SUBTITLE": "FE DF 1F 00 FE E1",
    "TEXT": "FE DF 8F 07 87 0F",
    "ZOOM": "",
    "NETFLIX": "FE DF 7F 0F 08 78",
    "YOUTUBE": "",
    "AMAZON": "",
    "T": "",
    "HISTORY": "",
    "CINEMA": "",
    "F-BACK": "FE DF 4F 0E 1B 5A",
    "F-P-IN": "FE EF 35 A0 FC 03",
    "F-P-OUT": "FE DF 35 A0 FC 69",
    "F-P-EXIT": "",
    "F-PW-ENTER": "FE DF 79 65 A8 B4",
    "F-PW-EXIT": "FE DF 79 6D 28 3C",
    "F-OOB": "FE DF B9 68 74 A5",
    "F-AV1": "FE DF FE 17 80 69",
    "F-AV2": "FE DF FE 1B 40 A5",
    "F-VGA": "FE DF FE 11 E0 0F",
    "F-HDMI1": "FE DF FE 1E 10 F0",
    "F-HDMI2": "FE DF FE 16 90 78",
    "F-HDMI3": "FE DF FE 1A 50 B4",
    "F-HDMI4": "FE DF FE 12 D0 3C",
    "F-USB": "FE DF FE 1C 30 D2",
    "F-3D-ON": "FE DF 3E 18 7C 5A",
    "F-3D-OFF": "FE DF 3E 14 BC 96",
    "F-SOURCE": "FE DF 5F 0C 3A 69",
    "F-MIC-ON": "FE DF 7E 16 98 F0",
    "F-MIC-OFF": "FE DF 7E 1E 18 78",
    "F-WIFI": "FE DF 79 64 B8 A5",
    "F-MUTE-ON": "FE DF 7E 19 68 0F",
    "F-MUTE-OFF": "FE DF 7E 11 E8 87",
    "F-C-TEMP": "FE DF BE 1E 14 B4",
    "F-M1": "FE DF DE 11 E2 2D",
    "F-M2": "FE DF DE 1E 12 D2",
    "F-SN-ON": "FE DF 7E 15 A8 C3",
    "F-SN-OFF": "FE DF 7E 1D 28 4B",
    "F-L-SR-ON": "FE DF 7E 1B 48 2D",
    "F-L-SR-OFF": "FE DF 7E 13 C8 A5",
    "THREE-IN": "",
    "TCL-HOME": "FE DF EF 0F 01 E1",
    "LIGHT+": "FE DF 6F 06 99 F0",
    "LIGHT-": "FE DF 6F 0A 59 3C",
    "IMAGE-TYPE": "FE DF 6F 02 D9 B4",

    "AV1": "FE DF FE 17 80 69",
    "AV2": "FE DF FE 1B 40 A5",
    "VGA": "FE DF 9E 18 76 F0",
    "HDMI1": "FE DF FE 1E 10 F0",
    "HDMI2": "FE DF FE 16 90 78",
    "HDMI3": "FE DF FE 1A 50 B4",
    "HDMI4": "FE DF FE 12 D0 3C",
    "CMP1": "FE DF FE 15 A0 4B",
    "CMP2": "FE DF FE 19 60 87",

    "USB": "FE DF FE 1C 30 D2",
    "P": "FE DF 35 A0 FC 69",
    "PW": "FE DF 79 6D 28 3C",

    "WIFI": "FE DF 79 64 B8 A5",
    "MIC": "FE DF 7E 16 98 F0",
    "3D": "FE DF 3E 14 BC 96",
    "SN": "FE DF 7E 15 A8 C3",

    "D.TEST": "FE DF 79 6C 38 2D",
    "SIZE": "FE DF 75 A6 98 4B",
    "PATTLE": "FE DF 19 60 FE 87",
    "C.TEMP": "FE DF BE 1E 14 B4",

    "PAT": "FE DF 0F 00 FF F0",
    "M1": "FE DF DE 1E 12 D2",
    "M2": "FE DF DE 16 92 5A",
    "SET": "FE DF BF 01 E4 5A"
}

# 国外红外键码值
_KEY_CODES_NA = {
    "CAMERA": "",
    "POWER": "FE DF 4F 05 AB E1",
    "MUTE": "FE DF CF 0F 03 C3",
    ".": "",
    "0": "FE DF CF 00 F3 3C",
    "1": "FE DF CF 08 73 B4",
    "2": "FE DF CF 04 B3 78",
    "3": "FE DF CF 0C 33 F0",
    "4": "FE DF CF 02 D3 1E",
    "5": "FE DF CF 0A 53 96",
    "6": "FE DF CF 06 93 5A",
    "7": "FE DF CF 0E 13 D2",
    "8": "FE DF CF 01 E3 2D",
    "9": "FE DF CF 09 63 A5",
    "UP": "FE DF AF 09 65 C3",
    "DOWN": "FE DF AF 01 E5 4B",
    "LEFT": "FE DF AF 06 95 3C",
    "RIGHT": "FE DF AF 0E 15 B4",
    "OK": "FE DF FF 02 D0 2D",
    "HOME": "FE DF 0F 01 EF E1",
    "VOLUME+": "FE DF 4F 0F 0B 4B",
    "VOLUME-": "FE DF 4F 07 8B C3",
    "P+": "FE DF 4F 0B 4B 0F",
    "P-": "FE DF 4F 03 CB 87",
    "RED": "FE DF 0F 00 FF F0",
    "GREEN": "FE DF 7F 01 E8 96",
    "YELLOW": "FE DF 7F 02 D8 A5",
    "BLUE": "FE DF BF 01 E4 5A",
    "PICTURE": "",
    "EPG": "",
    "TV": "",
    "MEDIA": "",
    "SETTING": "FE DF 3F 0F 0C 3C",
    "FREEZE": "",
    "INFO": "",
    "CN-INFO": "",
    "SOURCE": "FE DF 5F 0C 3A 69",
    "NEXT": "",
    "PLAY": "FE DF 8F 0A 57 D2",
    "PAUSE": "FE DF 8F 09 67 E1",
    "FAST-BACK": "FE DF 8F 0B 47 C3",
    "FAST-FORWARD": "FE DF 8F 03 C7 4B",
    "STOP": "FE DF 8F 0F 07 87",
    "LIST": "FE DF 6F 08 79 1E",
    "OPTION": "FE DF 7F 03 C8 B4",
    "MENU": "FE DF 7F 03 C8 B4",
    "EXIT": "FE DF 0F 06 9F 96",
    "BACK": "FE DF 4F 0E 1B 5A",
    "LANGUAGE": "FE DF BF 0F 04 B4",
    "SUBTITLE": "FE DF 1F 00 FE E1",
    "TEXT": "FE DF 8F 07 87 0F",
    "ZOOM": "",
    "NETFLIX": "FE DF 7F 0F 08 78",
    "YOUTUBE": "",
    "AMAZON": "",
    "T": "",
    "HISTORY": "",
    "CINEMA": "",
    "F-BACK": "FE DF 4F 0E 1B 5A",
    "F-P-IN": "FE EF 35 A0 FC 03",
    "F-P-OUT": "FE DF 35 A0 FC 69",
    "F-P-EXIT": "",
    "F-PW-ENTER": "FE DF 79 65 A8 B4",
    "F-PW-EXIT": "FE DF 79 6D 28 3C",
    "F-OOB": "FE DF B9 68 74 A5",
    "F-AV1": "FE DF FE 17 80 69",
    "F-AV2": "FE DF FE 1B 40 A5",
    "F-VGA": "FE DF FE 11 E0 0F",
    "F-HDMI1": "FE DF FE 1E 10 F0",
    "F-HDMI2": "FE DF FE 16 90 78",
    "F-HDMI3": "FE DF FE 1A 50 B4",
    "F-HDMI4": "FE DF FE 12 D0 3C",
    "F-USB": "FE DF FE 1C 30 D2",
    "F-3D-ON": "FE DF 3E 18 7C 5A",
    "F-3D-OFF": "FE DF 3E 14 BC 96",
    "F-SOURCE": "FE DF 5F 0C 3A 69",
    "F-MIC-ON": "FE DF 7E 16 98 F0",
    "F-MIC-OFF": "FE DF 7E 1E 18 78",
    "F-WIFI": "FE DF 79 64 B8 A5",
    "F-MUTE-ON": "FE DF 7E 19 68 0F",
    "F-MUTE-OFF": "FE DF 7E 11 E8 87",
    "F-C-TEMP": "FE DF BE 1E 14 B4",
    "F-M1": "FE DF DE 11 E2 2D",
    "F-M2": "FE DF DE 1E 12 D2",
    "F-SN-ON": "FE DF 7E 15 A8 C3",
    "F-SN-OFF": "FE DF 7E 1D 28 4B",
    "F-L-SR-ON": "FE DF 7E 1B 48 2D",
    "F-L-SR-OFF": "FE DF 7E 13 C8 A5",
    "THREE-IN": "",
    "TCL-HOME": "FE DF EF 0F 01 E1",

    "AV1": "FE DF FE 17 80 69",
    "AV2": "FE DF FE 1B 40 A5",
    "VGA": "FE DF 9E 18 76 F0",
    "HDMI1": "FE DF FE 1E 10 F0",
    "HDMI2": "FE DF FE 16 90 78",
    "HDMI3": "FE DF FE 1A 50 B4",
    "HDMI4": "FE DF FE 12 D0 3C",
    "CMP1": "FE DF FE 15 A0 4B",
    "CMP2": "FE DF FE 19 60 87",

    "USB": "FE DF FE 1C 30 D2",
    "P": "FE DF 35 A0 FC 69",
    "PW": "FE DF 79 65 A8 B4",
    "PW1": "FE DF 79 6D 28 3C",

    "WIFI": "FE DF 79 64 B8 A5",
    "MIC": "FE DF 7E 16 98 F0",
    "3D": "FE DF 3E 14 BC 96",
    "SN": "FE DF 7E 15 A8 C3",

    "D.TEST": "FE DF 79 6C 38 2D",
    "SIZE": "FE DF 75 A6 98 4B",
    "PATTLE": "FE DF 19 60 FE 87",
    "C.TEMP": "FE DF BE 1E 14 B4",

    "PAT": "FE DF 0F 00 FF F0",
    "M1": "FE DF DE 1E 12 D2",
    "M2": "FE DF DE 16 92 5A",
    "SET": "FE DF BF 01 E4 5A"
}

# 日本红外键码值
_KEY_CODES_JP = {
    "CAMERA": "0F0F",
    "POWER": "FE AF 2C 16 B9 D5 2A",
    "MUTE": "FEAF2C16B9C03F",
    "0": "FEAF2C16B950AF",
    "1": "FEAF2C16B9CE31",
    "2": "FEAF2C16B9CD32",
    "3": "FEAF2C16B9CC33",
    "4": "FEAF2C16B9CB34",
    "5": "FEAF2C16B9CA35",
    "6": "FEAF2C16B9C936",
    "7": "FEAF2C16B9C837",
    "8": "FEAF2C16B9C738",
    "9": "FEAF2C16B9C639",
    "UP": "FEAF2C16B9A659",
    "DOWN": "FE AF 2C 16 B9 A7 58",
    "LEFT": " FE AF 2C 16 B9 A9 56",
    "RIGHT": "FE AF 2C 16 B9 A8 57",
    "OK": "FE AF 2C 16 B9 0B F4",
    "HOME": "FEAF2C16B9F708",
    "VOLUME+": "FEAF2C16B9D02F",
    "VOLUME-": "FEAF2C16B9D12E",
    "P+": "FEAF2C16B9D22D",
    "P-": "FEAF2C16B9D32C",
    "RED": "FEAF2C16B9FF00",
    "GREEN": "FEAF2C16B917E8",
    "YELLOW": "FEAF2C16B91BE4",
    "BLUE": "FEAF2C16B927D8",
    "PICTURE": "ED",
    "EPG": "FEAF2C16B9E51A",
    "TV": "C5",
    "MEDIA": "FD",
    "SETTING": "FEAF2C16B930CF",
    "FREEZE": "F3",
    "INFO": "C3",
    "CN-INFO": "2E",
    "SOURCE": "FEAF2C16B95CA3",
    "NEXT": "FEAF2C16B9AC53",
    "PLAY": "FEAF2C16B9EA15",
    "PAUSE": "FEAF2C16B9E619",
    "FAST-BACK": "FEAF2C16B9E21D",
    "FAST-FORWARD": "FEAF2C16B9E31C",
    "STOP": "FEAF2C16B9E01F",
    "LIST": "9E",
    "OPTION": "13",
    "MENU": "FEAF2C16B913EC",
    "EXIT": "FEAF2C16B9D827",
    "BACK": "FEAF2C16B9D827",
    "LANGUAGE": "20",
    "SUBTITLE": "FEAF2C16B97F80",
    "TEXT": "E1",
    "ZOOM": "6F",
    "NETFLIX": "FEAF2C16B910EF",
    "YOUTUBE": "FEAF2C16B91DE2",
    "AMAZON": "16",
    "F-OOB": "FE DF B9 68 74 A5",
    "BS": "FEAF2C16B95FA0",
    "TR": "FE AF 2C 16 B9 55 AA",
    "THREE-IN": "FE AF 2C 16 B9 53 AC",
    "PVR-LIST": "FE AF 2C 16 B9 5D A2",
    "PVR": "FE AF 2C 16 B9 E8 17",
    "PVR-END": "FE AF 2C 16 B9 E0 1F",
    "AUDIOSWITCH": "FE AF 2C 16 B9 A5 5A"
}


class KEYCODES(Enum):
    KEY_CODE_CN = _KEY_CODES_CN
    KEY_CODE_NA = _KEY_CODES_NA
    KEY_CODE_JP = _KEY_CODES_JP
