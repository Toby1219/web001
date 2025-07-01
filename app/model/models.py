from ..utils.extension import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
import uuid
from ..config import Config
import json

class UserAccount(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=True, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    otp = db.Column(db.String(6))
    otp_expiry = db.Column(db.DateTime)
    is_verified = db.Column(db.Boolean, default=False)
    paswrd = db.Column(db.String(30), nullable=False)
    walletType = db.Column(db.String(200), nullable=False)
    walletAddress = db.Column(db.String(200), default="0")
    ref_count = db.Column(db.String(200), default="0")
    referral_code = db.Column(db.String(200), unique=True)
    ref_by = db.Column(db.String(200))
    earned = db.Column(db.String(200), default="0.00")
    balance = db.Column(db.String(200), default="0.00")
    withdrawn = db.Column(db.String(200), default="0.00")
    invested = db.Column(db.String(200), default="0.00")
    active_deposits = db.Column(db.String(200), default="0.00")
    time = db.Column(db.String(200), default=f"{str(datetime.now().time().strftime("%H:%M"))}")
    date = db.Column(db.String(200), default=f"{str(datetime.now().date())}")
    a_w_type = db.Column(db.String(200), nullable=False)
    a_w_address = db.Column(db.String(200), nullable=False)
    transactions = db.relationship('Transactions', backref='user_account', lazy=True)
    is_first_payment = db.Column(db.Boolean, default=True)
    is_first_deposit = db.Column(db.Boolean, default=True)
    ref_earings = db.Column(db.String(200), default='0.00')
    
    def genResetpasswrd(self):
        import random
        u = [str(x) for x in random.sample(range(1, 10), 6)]
        self.otp = "".join(u)
    
    def generate_referral_code(self):
        add_f = f"{str(datetime.now().hour-12)}{str(datetime.now().year)}"
        self.referral_code = f"tm{add_f}{uuid.uuid4().hex[:6]}"

    def set_password(self, password):
        self.paswrd = password
        self.password = generate_password_hash(password)
        return self.password
    
    def check_password(self, password):
        if not self.password:
            raise ValueError("NO password provided")
        return check_password_hash(self.password, password)

        
    def create_user(self):
        db.session.add(self)
        db.session.commit()

class Transactions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_account.id'), nullable=False, default=0)
    username  = db.Column(db.String(200), nullable=False)
    time = db.Column(db.String(200), default=f"{str(datetime.now().time().strftime("%H:%M"))}")
    date = db.Column(db.String(200), default=f"{str(datetime.now().date())}")
    wa =   db.Column(db.String(200), nullable=False, default='-')
    wt =  db.Column(db.String(200), nullable=False, default='-')
    ammount = db.Column(db.String(200), nullable=False, default='-')
    remark = db.Column(db.String(10000), nullable=False, default='-')
    plan = db.Column(db.String(200), nullable=False, default='-')
    plan_perc = db.Column(db.String(200), nullable=False, default='-') 
    plan_hours = db.Column(db.String(200), nullable=False, default='-') 
    to = db.Column(db.String(200), default="Trusted Minner")
    status = db.Column(db.String(200), default="Pending")
    transac_type = db.Column(db.String(200), nullable=False, default='-')
    time_counter = db.Column(db.String(200), default='-')
    
    
    
    def create_transaction(self):
        db.session.add(self)
        db.session.commit()

   
class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, default=Config.ADMIN_NAME)
    email = db.Column(db.String(100), unique=True, default="trusted.minner09@gmail.com")
    password = db.Column(db.String(100), default=generate_password_hash(Config.PASSKEY))
    w_A = db.Column(db.String(200), default=Config.WALLET_ADDRESS)
    W_T = db.Column(db.String(200), default=Config.WALLET_TYPE)
    balance = db.Column(db.String(200), default="0.00")
    declined_payment = db.Column(db.String(200))
    approve_payment = db.Column(db.String(200))
    web_users = db.Column(db.String(200))
    PhoneNumberWhatsapp = db.Column(db.String(100), default='+14252822088')
    PhoneNumberTelegram = db.Column(db.String(100), default='+13183109638')
    ref_gift = db.Column(db.String(500), default=json.dumps({'BEGINNERS Plan':2.5,'BEGINNERS PRO':5,'PROMO PLAN':7.5,'PROFESSIONAL PLAN':10,'EXPERT TRADE':15}))
    
    def check_password(self, password):
        if not self.password:
            raise ValueError("NO password provided")
        return check_password_hash(self.password, password)

    def update_allowed_fields(self, email=None, balance=None, whatsapp=None, telegram=None, wallet_address=None, wallet_type=None, refg=None):
        """Only allows updating limited fields."""
        if balance is not None:
            self.balance = balance
        if whatsapp is not None:
            self.PhoneNumberWhatsapp = whatsapp
        if telegram is not None:
            self.PhoneNumberTelegram = telegram
        if wallet_address is not None:
            self.w_A = wallet_address
        if wallet_type is not None:
            self.W_T = wallet_type
        if refg is not None:
            self.ref_gift = refg
        if email is not None:
            self.email = email
        db.session.commit()
        
    def create_admin(self):
        existing_admin = Admin.query.filter_by(username=Config.ADMIN_NAME).first()
        if existing_admin:
            return "Admin already exists"
            
        admin = Admin()
        db.session.add(admin)
        db.session.commit()
        return "Admin created"


# SECHEMAS   
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested

class TransactionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Transactions
        load_instance = True 
        
class UserAccSchema(SQLAlchemyAutoSchema):
    transactions = Nested(TransactionSchema, many=True) 
    class Meta:
        model = UserAccount
        load_instance = True 
