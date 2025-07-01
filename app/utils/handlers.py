from flask import url_for, g, redirect
from..model.models import UserAccount, UserAccSchema, Transactions, TransactionSchema, Admin
from ..utils.extension import validate_wallet, assign_userWallet, openJson, writeJson
from datetime import datetime
from ..model.models import Transactions
import json
from itertools import zip_longest
from ..config import Config


def query_db_only(obj, obj_schema, cu, onlys=[], excludes=[]):
    user = obj.query.filter_by(username=cu).first()
    if excludes:
        schema = obj_schema(only=[a for a in onlys], exclude=[e for e in excludes]).dump(user)
        return schema
    schema = obj_schema(only=[a for a in onlys]).dump(user)
    return schema

def query_db_many(obj, obj_schema, cu, excludes=[]):
    user = obj.query.filter_by(username=cu)
    if excludes:
        schema = obj_schema(many=True, excludes=[e for e in excludes]).dump(user)
        return schema  
    schema = obj_schema(many=True).dump(user)
    return schema

def gen_referral_link(data):
    ref_by = UserAccount.query.filter_by(referral_code=data['ref_by']).first()
    ref_n = ''
    if ref_by:
        ref_n = ref_by.username
    referral_link = url_for('auth.register', ref=data['referral_code'], _external=True)
    return referral_link, ref_n


    """
    THis Handles both removal and adding of data into db
    """
def update_balance():
    args = ["id", 'balance', 'earned', 'invested', 'active_deposits']
    data, user = query_db_only(UserAccount, UserAccSchema, g.user.username, onlys=args)
    transaction_data, _ = query_db_many(Transactions, TransactionSchema, g.user.username)
    for tx in transaction_data:
        if tx['status'].lower() == 'success':
            user.balance = "{:,.2f}".format(float(tx['ammount'].replace(",", "")) + float(data['balance'].replace(",", "")))
            user.create_user()

def deposit_handler(*args):
    user = UserAccount.query.filter_by(id=g.user.id).first()
    deposit = Transactions(user_id=g.user.id, username=user.username, wa=args[0], 
                        wt=args[1], ammount="{:,.2f}".format(float(args[2])), plan=args[3], 
                        transac_type=args[4], remark=f"Payment for {args[3]} is under review", 
                        to=f"{user.a_w_type} => {user.a_w_address}", plan_perc=args[5], plan_hours=args[6])
    user.active_deposits = "{:,.2f}".format(float(user.active_deposits.replace(",", "")) + float(deposit.ammount.replace(",", "")))
    user.time_counter = "-"
    user.create_user()
    deposit.create_transaction()
    return 'views.account_page'

def withdraw_handler(*args):
    user = UserAccount.query.filter_by(id=g.user.id).first()
    deposit = Transactions(user_id=g.user.id, username=user.username, wa=args[0], 
                    wt=args[1], ammount="{:,.2f}".format(float(args[2])), transac_type=args[3])
    if args[4] == "f":
        deposit.status = 'Failed'
        deposit.remark = "Insufficient funds or an error occurred."
        deposit.create_transaction()
        return "views.withdraw_page"
    deposit.remark = f"withdrawal of usd {args[2]} is under review"
    user.balance = "{:,.2f}".format(float(user.balance.replace(",", "")) - float(args[2]))
    user.create_user()
    deposit.create_transaction()
    return 'views.account_page'
         
         
def filter_transactions(date_from=None, date_to=None, status=None, ttype=None):
    from datetime import datetime

    start_date = datetime.strptime(date_from, "%Y-%m-%d") if date_from else None
    end_date = datetime.strptime(date_to, "%Y-%m-%d") if date_to else None

    result = []
    t_schema = query_db_many(Transactions, TransactionSchema, g.user.username)

    for tx in t_schema:
        tx_date = datetime.strptime(tx['date'], "%Y-%m-%d")

        if start_date and tx_date < start_date:
            continue
        if end_date and tx_date > end_date:
            continue

        if status and status.lower() != "all":
            if tx.get("status", "").lower() != status.lower():
                continue

        if ttype and ttype.lower() != "all":
            if tx.get("transac_type", "").lower() != ttype.lower():
                continue

        result.append(tx)

    sorted_result = sorted(result, key=lambda x: datetime.strptime(f"{x['date']} {x['time']}", "%Y-%m-%d %H:%M"), reverse=True)
    return sorted_result

def change_data_handler(user, email=None, phone=None, pay_method=None, wallet_a=None, cur_passw=None, new_passw=None, co_new_passw=None):
        msg = ""
        if email:
            user.email = email
            msg = "Email changed successfully"
        if phone:
            user.phone = phone
            msg = "Phone number change successfully"
        
              
        if cur_passw and new_passw and co_new_passw:            
            if not user.check_password(cur_passw):
                msg =  "Wrong current Password"
            if not new_passw == co_new_passw:
                msg =  "New password does not match"
            
            user.set_password(new_passw)
  
            msg = "Password change successfully" 
        if pay_method and wallet_a:
            user = UserAccount.query.get(g.user.id)
            if validate_wallet(pay_method, wallet_a):
                user.walletType = pay_method
                user.walletAddress = wallet_a
                user.a_w_type, user.a_w_address = assign_userWallet(user.walletType)
        
                msg = "change wallet sucesfull"
            else:
                msg = "Wrong wallet information"
        user.create_user()
        return msg

    
# Intrest calculator

def fmtTime(date:str, time:str):
    d = [int(x) for x in date.split("-")]
    t = [int(x) for x in time.split(":")]
    result = [*d, *t]
    return result

def create_transc(*args):
    t =  Transactions(user_id=g.user.id, username=g.user.username, status='Success',
                      ammount=args[0], plan=args[1], 
                        transac_type='Intrest', remark=args[2], 
                        to="_", plan_perc=args[3], plan_hours=args[4])
    t.create_transaction()
  
def calculateInterest(user, transaction):
    transactions = [t for t in transaction if t.status == 'Success' and t.transac_type == 'deposit']
    transc = None
    if transactions:
        transc = transactions[-1]
    if transc:
        timestap = json.loads(transc.time_counter)
        ammount = float(user.invested.replace(',', '').strip())
        dt = fmtTime(timestap['date'], timestap['time'])
        storedTime = datetime(dt[0], dt[1], dt[2], dt[3], dt[4])
        current_time = datetime.now()
        time_diff = current_time - storedTime
        hours_passed = time_diff.total_seconds() / 3600
        if ammount and hours_passed == float(transc.plan_hours) - 1:
            earned = ammount * float(transc.plan_perc) / 100 + float(user.earned)
            user.earned = earned
            create_transc("{:,.2f}".format(float(user.earned)), transc.plan, 
                          f"Intrest of {transc.plan_perc}% paid to earned account", transc.plan_perc, 
                          transc.plan_hours)
            user.earnedUpdate = True
            user.create_user()
            
        if ammount and hours_passed >= float(transc.plan_hours): 
            earned = ammount * float(transc.plan_perc) / 100 
            prevBal = float(user.balance.replace(',', '').strip())
            newBal = "{:,.2f}".format(earned + prevBal + float(user.invested.replace(',', '').strip()))
            user.balance = newBal
            user.invested = "0.00"
            user.earned = '0.00'
            create_transc(earned, transc.plan, 
                            f"Intrest of {transc.plan_perc}% paid to balance account", transc.plan_perc, 
                            transc.plan_hours)
            user.earnedUpdate = False
            user.create_user()



# Admin HANDLERS
def get_totalPending():
    user = UserAccount.query.all()
    data = UserAccSchema(many=True).dump(user)
    p_transaction = Transactions.query.all()
    p_transactionSchema  = TransactionSchema(many=True).dump(p_transaction)
    result1 = [s for s in p_transactionSchema if s['status'].lower() == 'pending' and s['transac_type'] == 'withdraw']
    result2 = [s for s in p_transactionSchema if s['status'].lower() == 'pending' and s['transac_type'] == 'deposit']
    total_user = len(data)
    total_p_w = len(result1)
    total_p_d = len(result2)
    return total_user, total_p_w, total_p_d

    
def update_db_handler(action, id_, remark, tt, amt):
    trans = Transactions.query.filter_by(id=id_).first()
    user = UserAccount.query.filter_by(username=trans.username).first()
    admin_ = Admin.query.filter_by(username=Config.ADMIN_NAME).first()
    balance = admin_.balance
    if action == 'success':
        trans.remark = remark
        if tt == "w":
            trans.status =  "Success"
            user.withdrawn = "{:,.2f}".format(float(user.withdrawn.replace(",", "")) + float(amt.replace("USD", '').replace(",", "").strip()))
            trans.ammount = amt
            balance = "{:,.2f}".format(float(admin_.balance.replace(",", "")) - float(amt.replace(",", "").replace("USD", "").strip()))
        else:  
            user.invested = "{:,.2f}".format(float(user.invested.replace(",", "")) + float(amt.replace("USD", '').replace(",", "").strip()))
            na = float(user.active_deposits.replace(",", "")) - float(amt.replace("USD", '').replace(",", "").strip())
            if na <= 0:
                user.active_deposits ="0.00"
            else:
                user.active_deposits = "{:,.2f}".format(na)
            trans.status =  "Success"
            trans.ammount =  "{:,.2f}".format(float(amt.replace(",", "").replace("USD", "").strip()))
            balance = "{:,.2f}".format(float(admin_.balance.replace(",", "")) + float(amt.replace(",", "").replace("USD", "").strip()))
            
            trans.time_counter = json.dumps({'time': f'{datetime.now().time().strftime('%H:%M')}', 'date': f'{datetime.now().date()}'})
            
        trans.create_transaction()
        user.create_user()
        admin_.update_allowed_fields(balance=balance)
    if action == 'failed':
        if tt =='w':
            user.balance = "{:,.2f}".format(float(user.balance.replace(",", "")) + float(amt.replace("USD", '').replace(",", "").strip()))
            trans.ammount = amt
        else:
            na = float(user.active_deposits.replace(",", "")) - float(amt.replace("USD", '').replace(",", "").strip())
            if na <= 0:
                user.active_deposits ="0.00"
            else:
                user.active_deposits = "{:,.2f}".format(na)
        trans.remark = remark
        trans.status =  "Failed"
        trans.ammount = amt
        trans.create_transaction()
        user.create_user()

def change_data_handler_admin(user, bal, email=None, phonew=None, phonet=None, pay_method=None, wallet_a=None):
        msg = ""
        if bal:
            user.update_allowed_fields(balance=bal)
        if email:
            user.update_allowed_fields(email=email)
        if phonew or phonet:
            user.update_allowed_fields(whatsapp=phonew)
            user.update_allowed_fields(telegram=phonet)
            msg = "Phone Number change successfully"
        if pay_method and wallet_a:
            user.update_allowed_fields(wallet_address=wallet_a, wallet_type=str(pay_method).capitalize())
            msg = "change wallet sucesfull"
        return msg

def upate_walletJson(name=[], address=[]):
    datas = openJson()
    for data in datas:
        for n, a, in zip_longest(name, address):
            if data['name'].lower() == n.lower():
                data['address'] = a
    writeJson("app/utils/wallets.json", datas)



