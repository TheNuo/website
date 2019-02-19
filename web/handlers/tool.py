# 工具版块: 各种自制工具
# auther:KRzhao

import os
from flask import Blueprint, render_template, flash, send_from_directory
from ..forms import MergeForm, ReceivableForm
from analysis import finance

tool = Blueprint('tool', __name__, url_prefix='/tool')


@tool.route('/merge', methods=['GET', 'POST'])
def merge():
    form = MergeForm()
    if form.validate_on_submit():
        directory = os.path.join(os.getcwd(), 'web', 'static', 'tool')
        left_file_name = 'merge_left_file' + '.' + form.left_file.data.filename.split('.')[-1]
        form.left_file.data.save(os.path.join(directory, left_file_name))
        right_file_name = 'merge_right_file' + '.' + form.right_file.data.filename.split('.')[-1]
        form.right_file.data.save(os.path.join(directory, right_file_name))
        data = finance.merge(
            left_file=os.path.join(directory, left_file_name),
            right_file=os.path.join(directory, right_file_name),
            left_on=form.left_on.data,
            right_on=form.right_on.data,
            way=form.way.data
        )
        data.to_excel(os.path.join(directory, 'merge_excel_by_KRzhao.xlsx'))
        return send_from_directory(directory, 'merge_excel_by_KRzhao.xlsx', as_attachment=True)
    return render_template('tool/merge.html', form=form)


@tool.route('/receivable', methods=['GET', 'POST'])
def receivable():
    form = ReceivableForm()
    if form.validate_on_submit():
        directory = os.path.join(os.getcwd(), 'web', 'static', 'tool')
        bnys_file_name = 'bnys_file' + '.' + form.bnys_file.data.filename.split('.')[-1]
        form.bnys_file.data.save(os.path.join(directory, bnys_file_name))
        bnyye_file_name = 'bnyye_file' + '.' + form.bnyye_file.data.filename.split('.')[-1]
        form.bnyye_file.data.save(os.path.join(directory, bnyye_file_name))
        snyye_file_name = 'snyye_file' + '.' + form.snyye_file.data.filename.split('.')[-1]
        form.snyye_file.data.save(os.path.join(directory, snyye_file_name))
        khzl_file_name = 'khzl_file' + '.' + form.khzl_file.data.filename.split('.')[-1]
        form.khzl_file.data.save(os.path.join(directory, khzl_file_name))
        sybb_file_name = 'sybb_file' + '.' + form.sybb_file.data.filename.split('.')[-1]
        form.sybb_file.data.save(os.path.join(directory, sybb_file_name))
        data = finance.receivable(
            bnys_file=os.path.join(directory, bnys_file_name),
            bnyye_file=os.path.join(directory, bnyye_file_name),
            snyye_file=os.path.join(directory, snyye_file_name),
            khzl_file=os.path.join(directory, khzl_file_name),
            sybb_file=os.path.join(directory, sybb_file_name)
        )
        data.to_excel(os.path.join(directory, 'receivable_by_KRzhao.xlsx'))
        return send_from_directory(directory, 'receivable_by_KRzhao.xlsx', as_attachment=True)
    return render_template('tool/receivable.html', form=form)
