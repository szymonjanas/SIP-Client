import sip.helpers
from random import randint

def branch():
    return "z9hG4bK" + sip.helpers.generate('0123456789abcdefghijklmnorstuvwxyz', 20)

def callID():
    return sip.helpers.generate('0123456789abcdefghijklmnorstuvwxyz', 41)

def cseq():
    cseq_max = 2**32
    cseq_out = str()
    while True:
        cseq_out = sip.helpers.generate('0123456789', 10)
        if not (int(cseq_out) >= cseq_max or cseq_out[0] == '0'):
            break
    return cseq_out

def maxForwards():
    return 70
