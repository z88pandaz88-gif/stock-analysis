import os

# 50 سهم للبداية (يمكن زيادتهم لاحقاً)
EGYPTIAN_STOCKS = [
    'COMI', 'HRHO', 'SWDY', 'ETEL', 'ISPH', 'ORWE', 'PHDC', 'SKPC',
    'AMOC', 'CIEB', 'EFIH', 'EGTS', 'HELI', 'ISMI', 'MNHD', 'MTOR',
    'PACH', 'PRCL', 'SPMD', 'SUGR', 'TMGH', 'EFIC', 'ABUK', 'EAST',
    'EGAL', 'ELKA', 'GDWA', 'IFAP', 'IRON', 'SAUD',
    # EGX70
    'ACAMD', 'ACGC', 'ADPC', 'AFDI', 'AFMC', 'AIFI', 'AMER', 'AMIA',
    'ANFI', 'ARAB', 'ASCM', 'ASPI', 'ATLC', 'BIOC', 'BTFH', 'CABI',
    'Cairo', 'CCAP', 'CEFM', 'CERA', 'CFIV', 'CICH', 'CIRA', 'CLHO',
    'CNTX', 'COMS', 'CPID', 'DAPH', 'DCCI', 'DELT', 'DOHA', 'DSCW',
    'EDBM', 'EDFM', 'EGAL', 'EGCH', 'EGHD', 'EGTS', 'EHDR', 'EICH',
    'EKHO', 'ELKA', 'EMFD', 'EMRI', 'ENGC', 'ENPI', 'EPAY', 'EPCO',
    'ESRS', 'ETRS', 'EXPA', 'FATA', 'FWRY', 'GDWA', 'GEMA', 'GENP',
    'GHNR', 'GILT', 'GIHD', 'GLAX', 'GOLD', 'HDBK', 'HELI', 'HFRI',
    'HISH', 'HKTM', 'HOTE', 'HRHO', 'IBNS', 'IDHC', 'IDRE', 'IFAP',
    'IMBD', 'INFI', 'ISAI', 'ISMA', 'ITFC', 'JIEH', 'JSOR', 'KABO',
    'KARO', 'KDEV', 'KRDI', 'KZPC', 'LCFI', 'MAAL', 'MASR', 'MCRO',
    'MCQE', 'MEDC', 'MEGA', 'MENA', 'MEPA', 'MFPC', 'MICH', 'MISR',
    'MOIL', 'MPRC', 'NAHO', 'NHPS', 'NICE', 'NIND', 'NIPH', 'NLSH',
    'NSGB', 'NTCC', 'OCDI', 'ODIN', 'OFH', 'OIH', 'OLFI', 'ORAS',
    'ORWE', 'OSUL', 'OTMT', 'PACH', 'PHAR', 'PHDC', 'PID', 'POUL',
    'PRDC', 'PRMH', 'PRCL', 'PRTM', 'QATA', 'RAKT', 'RAYA', 'RMDA',
    'SAUD', 'SCFM', 'SCTS', 'SEED', 'SFGH', 'SGC', 'SHJT', 'SIDI',
    'SIGC', 'SIPC', 'SKPC', 'SMFR', 'SMRT', 'SPAN', 'SPMD', 'SUGR',
    'SWDY', 'TAQA', 'TAWA', 'TCSE', 'TDFM', 'TMGH', 'TRTO', 'TSFE',
    'UBAS', 'UDCD', 'UEGC', 'UFM', 'UHEW', 'UNIP', 'UNIT', 'UPCM',
    'USC', 'VODA', 'WCDF', 'ZATR', 'ZMH', 'BUEI', 'CCAT', 'ECAP',
    'EFID', 'EGIC', 'EICM', 'GBCO', 'HDFH', 'ICMI', 'IDHC', 'MBSC',
    'MEPA', 'MICH', 'MILS', 'MISR', 'NSGB', 'OCDI', 'SALF', 'SAUD',
    'SCTS', 'SEED', 'SFGH', 'SGC', 'SIDI', 'SIGC', 'SMFR', 'SPAN',
    'SPMD', 'SUGR', 'TAQA', 'TAWA', 'TCSE', 'TDFM', 'TMGH', 'TRTO',
    'TSFE', 'UBAS', 'UDCD', 'UEGC', 'UFM', 'UHEW', 'UNIP', 'UNIT',
    'UPCM', 'USC', 'VODA', 'WCDF', 'ZATR', 'ZMH'
]

# API Keys من متغيرات البيئة
TWELVE_DATA_API_KEY = os.getenv('ef45fbafa1314d1f870467256cd7810a', '')
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///stock.db')