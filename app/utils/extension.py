from flask import session
import re, random, json
import phonenumbers
from phonenumbers import NumberParseException
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()
login_manager = LoginManager()
has_earned = False

# ================= OTP Utilities =================
def generate_otp():
    return str(random.randint(100000, 999999))

   
wallet_patterns = {
    "Bitcoin": r"^(bc1|[13])[a-zA-HJ-NP-Z0-9]{25,39}$",
    "Ethereum": r"^0x[a-fA-F0-9]{40}$",
    "Tether USDT ERC20": r"^0x[a-fA-F0-9]{40}$",
    "Tether USDT TRC20": r"^T[a-zA-Z0-9]{33}$",
    "Binance Coin BNB - BEP2": r"^bnb1[0-9a-z]{38}$",
    "Binance Smart Chain": r"^0x[a-fA-F0-9]{40}$",
    "Litecoin": r"^[LM3][a-km-zA-HJ-NP-Z1-9]{26,33}$",
    "Ripple XRP": r"^r[0-9a-zA-Z]{24,34}$",
    "Dogecoin": r"^D{1}[5-9A-HJ-NP-U]{1}[1-9A-HJ-NP-Za-km-z]{32}$",
    "Cardano": r"^addr1[0-9a-zA-Z]{58}$",
    "Polkadot": r"^1[a-km-zA-HJ-NP-Z1-9]{47,48}$",
    "Solana": r"^[1-9A-HJ-NP-Za-km-z]{32,44}$",
    "Monero XMR": r"^4[0-9AB][1-9A-HJ-NP-Za-km-z]{93}$",
    "Tron": r"^T[a-zA-Z0-9]{33}$",
    "Zcash": r"^t1[0-9A-Za-z]{33}$",
    "Dash": r"^X[1-9A-HJ-NP-Za-km-z]{33}$",
    "Cosmos": r"^cosmos1[0-9a-z]{38}$",
    "Avalanche": r"^0x[a-fA-F0-9]{40}$",
    "VeChain": r"^0x[a-fA-F0-9]{40}$",
    "NEO": r"^A[0-9a-zA-Z]{33}$",
}

countries_data = [
    ("🇺🇸", "+1", "202-555-0143", "United States"),
    ("🇬🇧", "+44", "7400 123456", "United Kingdom"),
    ("🇳🇬", "+234", "802 123 4567", "Nigeria"),
    ("🇮🇳", "+91", "91234 56789", "India"),
    ("🇯🇵", "+81", "090-1234-5678", "Japan"),
    ("🇨🇦", "+1", "613-555-0134", "Canada"),
    ("🇦🇺", "+61", "412 345 678", "Australia"),
    ("🇩🇪", "+49", "1512 3456789", "Germany"),
    ("🇫🇷", "+33", "6 12 34 56 78", "France"),
    ("🇧🇷", "+55", "11 91234-5678", "Brazil"),
    ("🇷🇺", "+7", "912 345-67-89", "Russia"),
    ("🇨🇳", "+86", "138 0013 8000", "China"),
    ("🇿🇦", "+27", "82 123 4567", "South Africa"),
    ("🇰🇪", "+254", "712 345678", "Kenya"),
    ("🇪🇬", "+20", "100 123 4567", "Egypt"),
    ("🇲🇽", "+52", "55 1234 5678", "Mexico"),
    ("🇪🇸", "+34", "612 34 56 78", "Spain"),
    ("🇮🇹", "+39", "312 345 6789", "Italy"),
    ("🇸🇦", "+966", "50 123 4567", "Saudi Arabia"),
    ("🇹🇷", "+90", "531 234 5678", "Turkey"),
    ("🇦🇷", "+54", "9 11 2345-6789", "Argentina"),
    ("🇨🇴", "+57", "300 1234567", "Colombia"),
    ("🇵🇰", "+92", "300 1234567", "Pakistan"),
    ("🇧🇩", "+880", "1712-345678", "Bangladesh"),
    ("🇺🇦", "+380", "50 123 4567", "Ukraine"),
    ("🇵🇭", "+63", "912 345 6789", "Philippines"),
    ("🇮🇩", "+62", "812-3456-7890", "Indonesia"),
    ("🇲🇾", "+60", "12-345 6789", "Malaysia"),
    ("🇸🇬", "+65", "8123 4567", "Singapore"),
    ("🇳🇿", "+64", "21 123 4567", "New Zealand"),
    ("🇵🇱", "+48", "512 345 678", "Poland"),
    ("🇷🇴", "+40", "712 345 678", "Romania"),
    ("🇨🇭", "+41", "79 123 45 67", "Switzerland"),
    ("🇸🇪", "+46", "70 123 45 67", "Sweden"),
    ("🇳🇴", "+47", "412 34 567", "Norway"),
    ("🇩🇰", "+45", "20 12 34 56", "Denmark"),
    ("🇧🇪", "+32", "470 12 34 56", "Belgium"),
    ("🇦🇹", "+43", "660 1234567", "Austria"),
    ("🇨🇿", "+420", "601 123 456", "Czech Republic"),
    ("🇭🇺", "+36", "30 123 4567", "Hungary"),
    ("🇬🇷", "+30", "691 234 5678", "Greece"),
    ("🇮🇱", "+972", "50-123-4567", "Israel"),
    ("🇦🇪", "+971", "50 123 4567", "United Arab Emirates"),
    ("🇶🇦", "+974", "3312 3456", "Qatar"),
    ("🇰🇼", "+965", "5123 4567", "Kuwait"),
    ("🇧🇭", "+973", "3600 1234", "Bahrain"),
    ("🇴🇲", "+968", "9212 3456", "Oman"),
    ("🇻🇳", "+84", "91 234 56 78", "Vietnam"),
    ("🇹🇭", "+66", "91 234 5678", "Thailand"),
    ("🇰🇷", "+82", "10-1234-5678", "South Korea"),
    ("🇲🇲", "+95", "9 420 123456", "Myanmar"),
    ("🇳🇵", "+977", "9812345678", "Nepal"),
    ("🇱🇰", "+94", "712 345 678", "Sri Lanka"),
    ("🇿🇲", "+260", "955 123456", "Zambia"),
    ("🇬🇭", "+233", "24 123 4567", "Ghana"),
    ("🇨🇲", "+237", "6 71 23 45 67", "Cameroon"),
    ("🇹🇿", "+255", "712 345 678", "Tanzania"),
    ("🇿🇼", "+263", "71 234 5678", "Zimbabwe"),
    ("🇺🇬", "+256", "712 345678", "Uganda"),
    ("🇧🇯", "+229", "97 12 34 56", "Benin"),
    ("🇲🇱", "+223", "65 12 34 56", "Mali"),
    ("🇸🇳", "+221", "77 123 45 67", "Senegal"),
    ("🇩🇿", "+213", "661 23 45 67", "Algeria"),
    ("🇲🇦", "+212", "612-345678", "Morocco"),
    ("🇹🇳", "+216", "20 123 456", "Tunisia"),
    ("🇵🇪", "+51", "912 345 678", "Peru"),
    ("🇨🇱", "+56", "9 6123 4567", "Chile"),
    ("🇪🇨", "+593", "99 123 4567", "Ecuador"),
    ("🇧🇴", "+591", "71234567", "Bolivia"),
    ("🇺🇾", "+598", "94 123 456", "Uruguay"),
    ("🇻🇪", "+58", "412-1234567", "Venezuela"),
    ("🇰🇿", "+7", "701 123 4567", "Kazakhstan"),
    ("🇹🇲", "+993", "65 123456", "Turkmenistan"),
    ("🇦🇿", "+994", "50 123 45 67", "Azerbaijan"),
    ("🇬🇪", "+995", "555 12 34 56", "Georgia"),
    ("🇦🇲", "+374", "91 123456", "Armenia"),
    ("🇲🇳", "+976", "8812 3456", "Mongolia"),
    ("🇧🇳", "+673", "712 3456", "Brunei"),
]

#app\utils\wallets.json
def openJson(file="app/utils/wallets.json"):
    with open(file, 'r') as f:
        wallets = json.load(f)
    return wallets
        
def writeJson(file, data):
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)

def assign_userWallet(user):
    a = ''
    t = ''
    for dat in openJson():
        if user.lower() == dat['name'].lower():
            a = dat['address']
            t = dat['name']
    return a, t

def validate_wallet(coin:str, address):
    c = coin.capitalize()
    pattern = wallet_patterns.get(c)
    if pattern:
        return bool(re.match(pattern, address))
    return False

def is_valid_phone(phone, region=None):
    try:
        number = phonenumbers.parse(phone, region)
        return phonenumbers.is_valid_number(number)
    except NumberParseException:
        return False
    
def add_session(id_, role='user'):
    session['user_id'] = id_
    session['role'] = role
    session.permanent = True
    
def is_auth(role='user'):
    if session.get('role') != role:
        return False
    
