# -*- coding: utf-8 -*-
import pandas as pd


def merge(left_file, right_file, left_on, right_on, way):
    left_data = pd.read_excel(left_file)
    right_data = pd.read_excel(right_file)
    data = pd.merge(left_data, right_data, left_on=left_on, right_on=right_on, how=way)
    return data

def receivable(bnys_file, bnyye_file, snyye_file, khzl_file, sybb_file):
    # 读取数据
    bnys = pd.read_excel(bnys_file)
    bnyye = pd.read_excel(bnyye_file)
    snyye = pd.read_excel(snyye_file)
    khzl = pd.read_excel(khzl_file)
    sybb = pd.read_excel(sybb_file)
    # 拆分结账月, 区分年初数据和当期数据
    jzy = list({i for i in bnys['结账月']})
    ncys = bnys[bnys['结账月'] == jzy[0]]
    qcys = bnys[bnys['结账月'] == jzy[-1]]
    qcys.index = range(len(qcys))
    for i in ['1月余额', '2月余额', '3月余额', '4月余额', '5月余额', '6月余额', '7月余额', '8月余额', '9月余额', '10月余额', '11月余额', '12月余额']:
        bnyye[i] = bnyye[i].fillna(0)
        snyye[i] = snyye[i].fillna(0)
    # 创建新容器
    data = pd.DataFrame(None, index=range(len(qcys)))
    data['单位标识'] = qcys['客户ID']
    data['信用期'] = None
    data['公司名称'] = qcys['客户名称']
    data['客户代码'] = qcys['客户编码']
    data['客户类型'] = None
    data['关联关系'] = None
    for i in data.index.values:
        data.loc[i, '客户类型'] = khzl[khzl['单位标识'] == data.loc[i, '单位标识']]['企业性质'].iloc[0]
        if len(ncys[ncys['客户ID'] == data.loc[i, '单位标识']]) != 0:
            data.loc[i, '年初余额'] = ncys[ncys['客户ID'] == data.loc[i, '单位标识']]['期初金额'].iloc[0]
        else:
            data.loc[i, '年初余额'] = 0
        data.loc[i, '年度含税销售'] = bnys[bnys['客户ID'] == data.loc[i, '单位标识']]['借方金额'].sum()
        data.loc[i, '年度无税销售'] = None
        data.loc[i, '年度回笼'] = bnys[bnys['客户ID'] == data.loc[i, '单位标识']]['贷方金额'].sum()
        data.loc[i, '期初余额'] = qcys[qcys['客户ID'] == data.loc[i, '单位标识']]['期初金额'].iloc[0]
        data.loc[i, '当月含税销售'] = qcys[qcys['客户ID'] == data.loc[i, '单位标识']]['借方金额'].iloc[0]
        data.loc[i, '当月无税销售'] = None
        data.loc[i, '当月回笼'] = qcys[qcys['客户ID'] == data.loc[i, '单位标识']]['贷方金额'].iloc[0]
        data.loc[i, '期末余额'] = qcys[qcys['客户ID'] == data.loc[i, '单位标识']]['期末金额'].iloc[0]
        if len(bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]) != 0:
            if str(jzy[-1])[-2:] == '01':
                data.loc[i, '0-30天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['1月余额'].iloc[0]
                data.loc[i, '31-60天'] = snyye[snyye['单位标识'] == data.loc[i, '单位标识']]['12月余额'].iloc[0]
                data.loc[i, '61-90天'] = snyye[snyye['单位标识'] == data.loc[i, '单位标识']]['11月余额'].iloc[0]
                data.loc[i, '91-120天'] = snyye[snyye['单位标识'] == data.loc[i, '单位标识']]['10月余额'].iloc[0]
                data.loc[i, '121-150天'] = snyye[snyye['单位标识'] == data.loc[i, '单位标识']]['9月余额'].iloc[0]
                data.loc[i, '151-180天'] = snyye[snyye['单位标识'] == data.loc[i, '单位标识']]['8月余额'].iloc[0]
                data.loc[i, '181-210天'] = snyye[snyye['单位标识'] == data.loc[i, '单位标识']]['7月余额'].iloc[0]
                data.loc[i, '211-240天'] = snyye[snyye['单位标识'] == data.loc[i, '单位标识']]['6月余额'].iloc[0]
                data.loc[i, '241-270天'] = snyye[snyye['单位标识'] == data.loc[i, '单位标识']]['5月余额'].iloc[0]
                data.loc[i, '271-365天'] = snyye[snyye['单位标识'] == data.loc[i, '单位标识']]['4月余额'].iloc[0] + \
                                          snyye[snyye['单位标识'] == data.loc[i, '单位标识']]['3月余额'].iloc[0] + \
                                          snyye[snyye['单位标识'] == data.loc[i, '单位标识']]['2月余额'].iloc[0]
            if str(jzy[-1])[-2:] == '02':
                data.loc[i, '0-30天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['2月余额'].iloc[0]
                data.loc[i, '31-60天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['1月余额'].iloc[0]
                data.loc[i, '61-90天'] = snyye[snyye['单位标识'] == data.loc[i, '单位标识']]['12月余额'].iloc[0]
                data.loc[i, '91-120天'] = snyye[snyye['单位标识'] == data.loc[i, '单位标识']]['11月余额'].iloc[0]
                data.loc[i, '121-150天'] = snyye[snyye['单位标识'] == data.loc[i, '单位标识']]['10月余额'].iloc[0]
                data.loc[i, '151-180天'] = snyye[snyye['单位标识'] == data.loc[i, '单位标识']]['9月余额'].iloc[0]
                data.loc[i, '181-210天'] = snyye[snyye['单位标识'] == data.loc[i, '单位标识']]['8月余额'].iloc[0]
                data.loc[i, '211-240天'] = snyye[snyye['单位标识'] == data.loc[i, '单位标识']]['7月余额'].iloc[0]
                data.loc[i, '241-270天'] = snyye[snyye['单位标识'] == data.loc[i, '单位标识']]['6月余额'].iloc[0]
                data.loc[i, '271-365天'] = snyye[snyye['单位标识'] == data.loc[i, '单位标识']]['5月余额'].iloc[0] + \
                                          snyye[snyye['单位标识'] == data.loc[i, '单位标识']]['4月余额'].iloc[0] + \
                                          snyye[snyye['单位标识'] == data.loc[i, '单位标识']]['3月余额'].iloc[0]
            if str(jzy[-1])[-2:] == '03':
                data.loc[i, '0-30天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['3月余额'].iloc[0]
                data.loc[i, '31-60天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['2月余额'].iloc[0]
                data.loc[i, '61-90天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['1月余额'].iloc[0]
                data.loc[i, '91-120天'] = snyye[snyye['单位标识'] == data.loc[i, '单位标识']]['12月余额'].iloc[0]
                data.loc[i, '121-150天'] = snyye[snyye['单位标识'] == data.loc[i, '单位标识']]['11月余额'].iloc[0]
                data.loc[i, '151-180天'] = snyye[snyye['单位标识'] == data.loc[i, '单位标识']]['10月余额'].iloc[0]
                data.loc[i, '181-210天'] = snyye[snyye['单位标识'] == data.loc[i, '单位标识']]['9月余额'].iloc[0]
                data.loc[i, '211-240天'] = snyye[snyye['单位标识'] == data.loc[i, '单位标识']]['8月余额'].iloc[0]
                data.loc[i, '241-270天'] = snyye[snyye['单位标识'] == data.loc[i, '单位标识']]['7月余额'].iloc[0]
                data.loc[i, '271-365天'] = snyye[snyye['单位标识'] == data.loc[i, '单位标识']]['6月余额'].iloc[0] + \
                                          snyye[snyye['单位标识'] == data.loc[i, '单位标识']]['5月余额'].iloc[0] + \
                                          snyye[snyye['单位标识'] == data.loc[i, '单位标识']]['4月余额'].iloc[0]
            if str(jzy[-1])[-2:] == '04':
                data.loc[i, '0-30天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['4月余额'].iloc[0]
                data.loc[i, '31-60天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['3月余额'].iloc[0]
                data.loc[i, '61-90天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['2月余额'].iloc[0]
                data.loc[i, '91-120天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['1月余额'].iloc[0]
                data.loc[i, '121-150天'] = snyye[snyye['单位标识'] == data.loc[i, '单位标识']]['12月余额'].iloc[0]
                data.loc[i, '151-180天'] = snyye[snyye['单位标识'] == data.loc[i, '单位标识']]['11月余额'].iloc[0]
                data.loc[i, '181-210天'] = snyye[snyye['单位标识'] == data.loc[i, '单位标识']]['10月余额'].iloc[0]
                data.loc[i, '211-240天'] = snyye[snyye['单位标识'] == data.loc[i, '单位标识']]['9月余额'].iloc[0]
                data.loc[i, '241-270天'] = snyye[snyye['单位标识'] == data.loc[i, '单位标识']]['8月余额'].iloc[0]
                data.loc[i, '271-365天'] = snyye[snyye['单位标识'] == data.loc[i, '单位标识']]['7月余额'].iloc[0] + \
                                          snyye[snyye['单位标识'] == data.loc[i, '单位标识']]['6月余额'].iloc[0] + \
                                          snyye[snyye['单位标识'] == data.loc[i, '单位标识']]['5月余额'].iloc[0]
            if str(jzy[-1])[-2:] == '05':
                data.loc[i, '0-30天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['5月余额'].iloc[0]
                data.loc[i, '31-60天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['4月余额'].iloc[0]
                data.loc[i, '61-90天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['3月余额'].iloc[0]
                data.loc[i, '91-120天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['2月余额'].iloc[0]
                data.loc[i, '121-150天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['1月余额'].iloc[0]
                data.loc[i, '151-180天'] = snyye[snyye['单位标识'] == data.loc[i, '单位标识']]['12月余额'].iloc[0]
                data.loc[i, '181-210天'] = snyye[snyye['单位标识'] == data.loc[i, '单位标识']]['11月余额'].iloc[0]
                data.loc[i, '211-240天'] = snyye[snyye['单位标识'] == data.loc[i, '单位标识']]['10月余额'].iloc[0]
                data.loc[i, '241-270天'] = snyye[snyye['单位标识'] == data.loc[i, '单位标识']]['9月余额'].iloc[0]
                data.loc[i, '271-365天'] = snyye[snyye['单位标识'] == data.loc[i, '单位标识']]['8月余额'].iloc[0] + \
                                          snyye[snyye['单位标识'] == data.loc[i, '单位标识']]['7月余额'].iloc[0] + \
                                          snyye[snyye['单位标识'] == data.loc[i, '单位标识']]['6月余额'].iloc[0]
            if str(jzy[-1])[-2:] == '06':
                data.loc[i, '0-30天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['6月余额'].iloc[0]
                data.loc[i, '31-60天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['5月余额'].iloc[0]
                data.loc[i, '61-90天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['4月余额'].iloc[0]
                data.loc[i, '91-120天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['3月余额'].iloc[0]
                data.loc[i, '121-150天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['2月余额'].iloc[0]
                data.loc[i, '151-180天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['1月余额'].iloc[0]
                data.loc[i, '181-210天'] = snyye[snyye['单位标识'] == data.loc[i, '单位标识']]['12月余额'].iloc[0]
                data.loc[i, '211-240天'] = snyye[snyye['单位标识'] == data.loc[i, '单位标识']]['11月余额'].iloc[0]
                data.loc[i, '241-270天'] = snyye[snyye['单位标识'] == data.loc[i, '单位标识']]['10月余额'].iloc[0]
                data.loc[i, '271-365天'] = snyye[snyye['单位标识'] == data.loc[i, '单位标识']]['9月余额'].iloc[0] + \
                                          snyye[snyye['单位标识'] == data.loc[i, '单位标识']]['8月余额'].iloc[0] + \
                                          snyye[snyye['单位标识'] == data.loc[i, '单位标识']]['7月余额'].iloc[0]
            if str(jzy[-1])[-2:] == '07':
                data.loc[i, '0-30天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['7月余额'].iloc[0]
                data.loc[i, '31-60天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['6月余额'].iloc[0]
                data.loc[i, '61-90天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['5月余额'].iloc[0]
                data.loc[i, '91-120天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['4月余额'].iloc[0]
                data.loc[i, '121-150天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['3月余额'].iloc[0]
                data.loc[i, '151-180天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['2月余额'].iloc[0]
                data.loc[i, '181-210天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['1月余额'].iloc[0]
                data.loc[i, '211-240天'] = snyye[snyye['单位标识'] == data.loc[i, '单位标识']]['12月余额'].iloc[0]
                data.loc[i, '241-270天'] = snyye[snyye['单位标识'] == data.loc[i, '单位标识']]['11月余额'].iloc[0]
                data.loc[i, '271-365天'] = snyye[snyye['单位标识'] == data.loc[i, '单位标识']]['10月余额'].iloc[0] + \
                                          snyye[snyye['单位标识'] == data.loc[i, '单位标识']]['9月余额'].iloc[0] + \
                                          snyye[snyye['单位标识'] == data.loc[i, '单位标识']]['8月余额'].iloc[0]
            if str(jzy[-1])[-2:] == '08':
                data.loc[i, '0-30天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['8月余额'].iloc[0]
                data.loc[i, '31-60天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['7月余额'].iloc[0]
                data.loc[i, '61-90天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['6月余额'].iloc[0]
                data.loc[i, '91-120天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['5月余额'].iloc[0]
                data.loc[i, '121-150天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['4月余额'].iloc[0]
                data.loc[i, '151-180天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['3月余额'].iloc[0]
                data.loc[i, '181-210天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['2月余额'].iloc[0]
                data.loc[i, '211-240天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['1月余额'].iloc[0]
                data.loc[i, '241-270天'] = snyye[snyye['单位标识'] == data.loc[i, '单位标识']]['12月余额'].iloc[0]
                data.loc[i, '271-365天'] = snyye[snyye['单位标识'] == data.loc[i, '单位标识']]['11月余额'].iloc[0] + \
                                          snyye[snyye['单位标识'] == data.loc[i, '单位标识']]['10月余额'].iloc[0] + \
                                          snyye[snyye['单位标识'] == data.loc[i, '单位标识']]['9月余额'].iloc[0]
            if str(jzy[-1])[-2:] == '09':
                data.loc[i, '0-30天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['9月余额'].iloc[0]
                data.loc[i, '31-60天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['8月余额'].iloc[0]
                data.loc[i, '61-90天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['7月余额'].iloc[0]
                data.loc[i, '91-120天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['6月余额'].iloc[0]
                data.loc[i, '121-150天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['5月余额'].iloc[0]
                data.loc[i, '151-180天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['4月余额'].iloc[0]
                data.loc[i, '181-210天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['3月余额'].iloc[0]
                data.loc[i, '211-240天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['2月余额'].iloc[0]
                data.loc[i, '241-270天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['1月余额'].iloc[0]
                data.loc[i, '271-365天'] = snyye[snyye['单位标识'] == data.loc[i, '单位标识']]['12月余额'].iloc[0] + \
                                          snyye[snyye['单位标识'] == data.loc[i, '单位标识']]['11月余额'].iloc[0] + \
                                          snyye[snyye['单位标识'] == data.loc[i, '单位标识']]['10月余额'].iloc[0]
            if str(jzy[-1])[-2:] == '10':
                data.loc[i, '0-30天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['10月余额'].iloc[0]
                data.loc[i, '31-60天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['9月余额'].iloc[0]
                data.loc[i, '61-90天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['8月余额'].iloc[0]
                data.loc[i, '91-120天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['7月余额'].iloc[0]
                data.loc[i, '121-150天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['6月余额'].iloc[0]
                data.loc[i, '151-180天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['5月余额'].iloc[0]
                data.loc[i, '181-210天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['4月余额'].iloc[0]
                data.loc[i, '211-240天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['3月余额'].iloc[0]
                data.loc[i, '241-270天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['2月余额'].iloc[0]
                data.loc[i, '271-365天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['1月余额'].iloc[0] + \
                                          snyye[snyye['单位标识'] == data.loc[i, '单位标识']]['12月余额'].iloc[0] + \
                                          snyye[snyye['单位标识'] == data.loc[i, '单位标识']]['11月余额'].iloc[0]
            if str(jzy[-1])[-2:] == '11':
                data.loc[i, '0-30天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['11月余额'].iloc[0]
                data.loc[i, '31-60天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['10月余额'].iloc[0]
                data.loc[i, '61-90天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['9月余额'].iloc[0]
                data.loc[i, '91-120天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['8月余额'].iloc[0]
                data.loc[i, '121-150天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['7月余额'].iloc[0]
                data.loc[i, '151-180天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['6月余额'].iloc[0]
                data.loc[i, '181-210天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['5月余额'].iloc[0]
                data.loc[i, '211-240天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['4月余额'].iloc[0]
                data.loc[i, '241-270天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['3月余额'].iloc[0]
                data.loc[i, '271-365天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['2月余额'].iloc[0] + \
                                          bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['1月余额'].iloc[0] + \
                                          snyye[snyye['单位标识'] == data.loc[i, '单位标识']]['12月余额'].iloc[0]
            if str(jzy[-1])[-2:] == '12':
                data.loc[i, '0-30天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['12月余额'].iloc[0]
                data.loc[i, '31-60天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['11月余额'].iloc[0]
                data.loc[i, '61-90天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['10月余额'].iloc[0]
                data.loc[i, '91-120天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['9月余额'].iloc[0]
                data.loc[i, '121-150天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['8月余额'].iloc[0]
                data.loc[i, '151-180天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['7月余额'].iloc[0]
                data.loc[i, '181-210天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['6月余额'].iloc[0]
                data.loc[i, '211-240天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['5月余额'].iloc[0]
                data.loc[i, '241-270天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['4月余额'].iloc[0]
                data.loc[i, '271-365天'] = bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['3月余额'].iloc[0] + \
                                          bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['2月余额'].iloc[0] + \
                                          bnyye[bnyye['单位标识'] == data.loc[i, '单位标识']]['1月余额'].iloc[0]
            data['61-90天'] = data['0-30天'] + data['31-60天'] + data['61-90天']
            data['151-180天'] = data['91-120天'] + data['121-150天'] + data['151-180天']
            data['241-270天'] = data['181-210天'] + data['211-240天'] + data['241-270天']
            data['0-30天'] = 0
            data['31-60天'] = 0
            data['91-120天'] = 0
            data['121-150天'] = 0
            data['181-210天'] = 0
            data['211-240天'] = 0
    data['客户类型'] = data['客户类型'].replace({'个体诊所': '商业',
                                         '单体药店': '商业',
                                         '药店连锁': '商业',
                                         '商业批发': '商业',
                                         '体检机构': '商业',
                                         '疾控中心': '商业',
                                         '职工医院(医务室)': '商业',
                                         '乡镇卫生院': '商业',
                                         '卫生室': '商业',
                                         '各级社区医疗机构(中心、站、所)': '商业',
                                         '各级妇幼医疗机构(中心、站、所)': '商业',
                                         '各级计生医疗机构(中心、站、所)': '商业',
                                         '其他': '商业',
                                         '民营医院': '民办医院',
                                         '二级医院': '公立医院',
                                         '三级医院': '公立医院',
                                         '预算单位内部': '预算内部'
                                         })
    data['关联关系'] = data['客户类型'].replace({'商业': '第三方',
                                         '民办医院': '第三方',
                                         '公立医院': '第三方',
                                         '公立医院': '第三方',
                                         '预算内部': '关联方'
                                         })
    data['1-2年'] = 0
    data['2-3年'] = 0
    data['3年以上'] = 0
    sybb = sybb[['客户代码', '其中：坏账准备金余额']]
    data = pd.merge(data, sybb, on='客户代码', how='left')
    data['应收账款净额'] = data['期末余额'] - data['其中：坏账准备金余额']
    return data
