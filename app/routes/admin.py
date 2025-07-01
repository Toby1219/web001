from flask import Blueprint, render_template, g, redirect, url_for, request, jsonify, session, flash
from ..model.forms import ChangePhoneAdmin
from ..model.models import UserAccount, UserAccSchema, Transactions, TransactionSchema, Admin
from ..utils.handlers import (query_db_only, filter_transactions, update_db_handler,
                              change_data_handler_admin, get_totalPending, upate_walletJson)
from datetime import datetime
from ..utils.extension import openJson
import json

admin_bp = Blueprint("admin", __name__)


# ROUTES             
@admin_bp.route("/admin-homepage")
def homepage_admin():
    if session.get('role') != 'admin':
        return redirect(url_for('auth.login'))
    admin = Admin.query.all()
    total_user, total_p_d, total_p_w = get_totalPending()
    return render_template("admin/admin.html", user=admin[0], total=[total_user, total_p_w, total_p_d]), 200

@admin_bp.route("/admin-users", methods=["GET", "POST"])
def admin_users():
    if session.get('role') != 'admin':
        return redirect(url_for('auth.login'))
    user = UserAccount.query.all()
    data = UserAccSchema(many=True).dump(user)

    return render_template("admin/users.html", data=data), 200

@admin_bp.route("/admin-transactions", methods=["GET", "POST"])
def admin_transac():
    if session.get('role') != 'admin':
        return redirect(url_for('auth.login'))

    total_user, total_p_d, total_p_w = get_totalPending()
    args = ["id", "username", "email", "walletType", "walletAddress", 
        "balance", "withdrawn", "active_deposits"]
    user = Admin.query.all()
    data = query_db_only(UserAccount, UserAccSchema, 'admin', onlys=args)
    transactions = []
    if request.method == "POST":
        date_from = request.form.get("from")
        date_to = request.form.get("to")
        status = request.form.get("status")
        ttype = request.form.get("ttype")

        transactions = filter_transactions(date_from, date_to, status, ttype)
    if request.method == "GET":
        p_transaction = Transactions.query.all()
        p_transactionSchema  = TransactionSchema(many=True).dump(p_transaction)
        result = [s for s in p_transactionSchema]
        sorted_results = sorted(result, key=lambda x: datetime.strptime(f"{x['date']} {x['time']}", "%Y-%m-%d %H:%M"), reverse=True)
        return render_template("admin/admin.html", user=user[0], data=data, transaction=sorted_results,  total=[total_user, total_p_w, total_p_d]), 200

    return render_template("admin/transh.html", user=user[0], data=data, transaction=transactions), 200

@admin_bp.route('/admin-setting', methods=['GET', 'POST'])
def setting_admin():
    if session.get('role') != 'admin':
        return redirect(url_for('auth.login'))
    data = Admin.query.all()
    phone_form = ChangePhoneAdmin()
    wallets = openJson()
    ref_com = json.loads(data[0].ref_gift)
    if request.method == "POST":
        email = phone_form.email.data
        bal = phone_form.balance.data
        phonew = phone_form.phonew.data
        phonet = phone_form.phonet.data
        user = Admin.query.filter_by(id=g.user.id).first()     
        msg = change_data_handler_admin(user, bal, email, phonew, phonet)
        flash(msg)
        return redirect(url_for('admin.setting_admin'))
    return render_template("admin/sett.html", data=data[0], wallets=wallets, refCom=ref_com, phone_form=phone_form), 200



@admin_bp.route('/pending')
def pending_admin():
    user = Admin.query.all()
    pending = request.args.get("p")
    total_user, total_p_d, total_p_w = get_totalPending()
    if pending == 'w':
        p_transaction = Transactions.query.all()
        p_transactionSchema  = TransactionSchema(many=True).dump(p_transaction)
        result = [s for s in p_transactionSchema if s['status'].lower() == 'pending' and s['transac_type'] == 'withdraw']
        sorted_results = sorted(result, key=lambda x: datetime.strptime(f"{x['date']} {x['time']}", "%Y-%m-%d %H:%M"), reverse=True)
        
        return render_template("admin/admin.html", user=user[0], transaction=sorted_results, total=[total_user, total_p_w, total_p_d]), 200
    if pending == 'd':    
        p_transaction = Transactions.query.all()
        p_transactionSchema  = TransactionSchema(many=True).dump(p_transaction)
        result = [s for s in p_transactionSchema if s['status'].lower() == 'pending' and s['transac_type'] == 'deposit']
        sorted_results = sorted(result, key=lambda x: datetime.strptime(f"{x['date']} {x['time']}", "%Y-%m-%d %H:%M"), reverse=True)
        return render_template("admin/admin.html", user=user[0], transaction=sorted_results, total=[total_user, total_p_w, total_p_d]), 200
    
    return render_template("admin/admin.html", user=user[0], total=[total_user, total_p_w, total_p_d]), 200

@admin_bp.route('/update', methods=['POST'])
def update_db():
    if session.get('role') != 'admin':
        return redirect(url_for('auth.login'))
    data = request.get_json()
    id_ = data['id']
    remark = data['r']
    tt = data['tt']
    amt = data['amt']
    action = data['ac']
    update_db_handler(action, id_, remark, tt, amt)
    return redirect(url_for('admin.pending_admin', p=f'{tt}'))

    
 
 
# ALL API CALLS   
@admin_bp.route('/get-wallet', methods=['POST'])
def get_wallet():
    data = request.get_json()
    walletsType = [k for k, v in data.items()]
    walletsAddress = [v for k, v in data.items()]
    upate_walletJson(walletsType, walletsAddress)
    return jsonify({}), 200

@admin_bp.route('/get-ref-com', methods=['POST'])
def get_ref_com():
    data = request.get_json()
    name = [k for k, v in data.items()]
    value = [v for k, v in data.items()]
    user = Admin.query.all()
    ref_com:dict = json.loads(user[0].ref_gift)
    for i, k in enumerate(list(ref_com.keys())):
        if k == name[i]:
            ref_com[k] = value[i]        
    ref_gifts = json.dumps(ref_com)
    user[0].update_allowed_fields(refg=ref_gifts)
    return jsonify({}), 200

@admin_bp.route('/get_user', methods=['GET'])
def get_user():
    user = UserAccount.query.all()
    data = UserAccSchema(many=True).dump(user)
    t = request.args.get('t')
    if t:
        transac = Transactions.query.filter_by(username=t).all()
        transac_data = TransactionSchema(many=True, only=['id', 'ammount', 'plan', 'status']).dump(transac)
        user = UserAccount.query.filter_by(username=t).all()
        data = UserAccSchema(many=True).dump(user)
        status_pending = [x for x in transac_data if x['status'] == 'Pending']
        dat = {
            'id': transac_data[-1]['id'] if transac_data else "0.00",
            'ammount': status_pending[-1]['ammount'] if status_pending else "0.00",
            'plan': status_pending[-1]['plan'] if status_pending else "-",
            'password': data[0]['paswrd'],
            'balance': data[0]['balance'],
            'invsted': data[0]['invested'],
            'earned': data[0]['earned'],
            'wt': data[0]['walletType'],
            'wa': data[0]['walletAddress'],
            'ref_earning': data[0]['ref_earings'],
            'total_transac' : len(transac) if transac else 0
        }
        return jsonify(dat), 200
    return jsonify({"message": "None"}), 200

@admin_bp.route('/udate_user', methods=['POST'])
def update_user():
    data = request.get_json()
    id_ = data['id']
    username = data['username']
    passwrd = data['passwrd']
    balance = data['balance']
    invested = data['invested']
    earned = data['earned']
    pending = data['pending']
    activeplan = data['activeplan']
    user = UserAccount.query.filter_by(username=username).first()
    tran_user = Transactions.query.get(id_)
    if user:
        if passwrd:
            user.set_password(passwrd)
        if balance:
            user.balance = "{:,.2f}".format(float(balance.replace(",", "")))
        if invested:
            user.invested = "{:,.2f}".format(float(invested.replace(",", "")))
        if earned:
            user.earned = "{:,.2f}".format(float(earned.replace(",", "")))
        if tran_user:
            if pending is not None:
                user.active_deposits = "{:,.2f}".format(float(pending.replace(",", "")))
                tran_user.ammount = "{:,.2f}".format(float(pending.replace(",", "")))
            if activeplan:
                tran_user.plan = activeplan
            tran_user.create_transaction()
        user.create_user()
        
    return jsonify({}), 200
           
           
@admin_bp.route('/UpdateRefBal', methods=['POST'])
def credit_referral():
    data = request.get_json()
    user1 = UserAccount.query.filter_by(username=data['name']).first()
    ad = Admin.query.get(1)
    plans = json.loads(ad.ref_gift)
    percent = [v for k, v in plans.items() if k.lower() == data['plan'].lower()]
    if user1:
        user2 = UserAccount.query.filter_by(referral_code=user1.ref_by).first()
        if user1.is_first_deposit and user2:
            user1.is_first_deposit = False
            user2.balance = "{:,.2f}".format(percent[0] / 100 * float(data['amt']) + float(user2.balance))
            user1.create_user()
            user2.create_user()
    return jsonify({}), 200

 
    
    