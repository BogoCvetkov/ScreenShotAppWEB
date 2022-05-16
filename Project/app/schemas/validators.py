from marshmallow import ValidationError

countries = { 'ALL': True,'AF': True, 'AL': True, 'DZ': True, 'AS': True, 'AD': True, 'AO': True, 'AI': True, 'AQ': True,
              'AG': True, 'AR': True, 'AM': True, 'AW': True, 'AU': True, 'AT': True, 'AZ': True, 'BS': True,
              'BH': True, 'BD': True, 'BB': True, 'BY': True, 'BE': True, 'BZ': True, 'BJ': True, 'BM': True,
              'BT': True, 'BO': True, 'BQ': True, 'BA': True, 'BW': True, 'BV': True, 'BR': True, 'IO': True,
              'BN': True, 'BG': True, 'BF': True, 'BI': True, 'CV': True, 'KH': True, 'CM': True, 'CA': True,
              'KY': True, 'CF': True, 'TD': True, 'CL': True, 'CN': True, 'CX': True, 'CC': True, 'CO': True,
              'KM': True, 'CD': True, 'CG': True, 'CK': True, 'CR': True, 'HR': True, 'CU': True, 'CW': True,
              'CY': True, 'CZ': True, 'CI': True, 'DK': True, 'DJ': True, 'DM': True, 'DO': True, 'EC': True,
              'EG': True, 'SV': True, 'GQ': True, 'ER': True, 'EE': True, 'SZ': True, 'ET': True, 'FK': True,
              'FO': True, 'FJ': True, 'FI': True, 'FR': True, 'GF': True, 'PF': True, 'TF': True, 'GA': True,
              'GM': True, 'GE': True, 'DE': True, 'GH': True, 'GI': True, 'GR': True, 'GL': True, 'GD': True,
              'GP': True, 'GU': True, 'GT': True, 'GG': True, 'GN': True, 'GW': True, 'GY': True, 'HT': True,
              'HM': True, 'VA': True, 'HN': True, 'HK': True, 'HU': True, 'IS': True, 'IN': True, 'ID': True,
              'IR': True, 'IQ': True, 'IE': True, 'IM': True, 'IL': True, 'IT': True, 'JM': True, 'JP': True,
              'JE': True, 'JO': True, 'KZ': True, 'KE': True, 'KI': True, 'KP': True, 'KR': True, 'KW': True,
              'KG': True, 'LA': True, 'LV': True, 'LB': True, 'LS': True, 'LR': True, 'LY': True, 'LI': True,
              'LT': True, 'LU': True, 'MO': True, 'MG': True, 'MW': True, 'MY': True, 'MV': True, 'ML': True,
              'MT': True, 'MH': True, 'MQ': True, 'MR': True, 'MU': True, 'YT': True, 'MX': True, 'FM': True,
              'MD': True, 'MC': True, 'MN': True, 'ME': True, 'MS': True, 'MA': True, 'MZ': True, 'MM': True,
              'NA': True, 'NR': True, 'NP': True, 'NL': True, 'NC': True, 'NZ': True, 'NI': True, 'NE': True,
              'NG': True, 'NU': True, 'NF': True, 'MP': True, 'NO': True, 'OM': True, 'PK': True, 'PW': True,
              'PS': True, 'PA': True, 'PG': True, 'PY': True, 'PE': True, 'PH': True, 'PN': True, 'PL': True,
              'PT': True, 'PR': True, 'QA': True, 'MK': True, 'RO': True, 'RU': True, 'RW': True, 'RE': True,
              'BL': True, 'SH': True, 'KN': True, 'LC': True, 'MF': True, 'PM': True, 'VC': True, 'WS': True,
              'SM': True, 'ST': True, 'SA': True, 'SN': True, 'RS': True, 'SC': True, 'SL': True, 'SG': True,
              'SX': True, 'SK': True, 'SI': True, 'SB': True, 'SO': True, 'ZA': True, 'GS': True, 'SS': True,
              'ES': True, 'LK': True, 'SD': True, 'SR': True, 'SJ': True, 'SE': True, 'CH': True, 'SY': True,
              'TW': True, 'TJ': True, 'TZ': True, 'TH': True, 'TL': True, 'TG': True, 'TK': True, 'TO': True,
              'TT': True, 'TN': True, 'TR': True, 'TM': True, 'TC': True, 'TV': True, 'UG': True, 'UA': True,
              'AE': True, 'GB': True, 'UM': True, 'US': True, 'UY': True, 'UZ': True, 'VU': True, 'VE': True,
              'VN': True, 'VG': True, 'VI': True, 'WF': True, 'EH': True, 'YE': True, 'ZM': True, 'ZW': True,
              'AX': True }


def validate_country(n):
    if not countries.get(n, None):
        raise ValidationError("Country code is not valid. Note: Use 2-letter Capitalized codes only.")