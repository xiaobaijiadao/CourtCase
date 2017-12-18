from jieba import analyse, posseg

if __name__ == '__main__':
    tokenRes = list()
    flagRes = list()
    tfidfSrc = list()

    paragraph = "原告威海市商业银行股份有限公司文登支行诉称，2014年7月16日，原告与被告王进林签订借款合同，被告孙花作为配偶签订共同债务人承诺书，向原告借款2000000元，借款期限自2014年7月16" \
                "日至2015年7月16日，借款年利率8．4％，每月20日为结息日和还款日，逾期罚息利率在合同约定利率的基础上加收50％。同年7月14" \
                "日，原告与被告张世会、崔金秀、王基方、李令好、王相洋、文登市泽库镇金海冷藏厂签订最高额保证合同，上述被告为王进林在2014年7月14日至2015年7月14" \
                "日期间在原告处形成的债务本金余额最高2000000元内提供连带责任保证，保证范围包括主合同项下的债务本金、利息、逾期利息、复利、罚息、违约金、损害赔偿金等和为实现债权、担保权而发生的一切费用。2015" \
                "年6月15日，原告又与被告威海市海得冷藏厂签订保证合同，约定被告威海市海得冷藏厂为被告王进林在原告处的借款提供连带责任保证，保证范围包括主合同项下的本金、利息、违约金、赔偿金、实现债权的费用、因债务人违约而给债权人造成的损失和其他所有应付费用。现贷款已到期，被告仍未偿还借款本金及逾期利息。请求判令被告王进林与被告孙花共同偿还原告借款本金1483871．81元及2015年7月21日之后的逾期利息；判令被告张世会、崔金秀、王基方、李令好、王相洋、文登市泽库镇金海冷藏厂、威海市海得冷藏厂对上述债务承担连带保证责任。 "

    for word, flag in posseg.cut(paragraph):
        tokenRes.append(word)
        flagRes.append(flag)

    textrank = analyse.textrank
    analyse.set_stop_words("stopWords.txt")
    filterFlag = ('n', 'nz', 'nt', 'nl', 'ng', 'v', 'vd', 'vn', 'vi', 'vl', 'vg', 'v', 'vn', 'an', 'b', 'bl', 'd')
    keywordsRes = textrank(paragraph, topK=336, allowPOS=filterFlag)

    print(len(tokenRes))

    print(len(keywordsRes))
    print(keywordsRes)