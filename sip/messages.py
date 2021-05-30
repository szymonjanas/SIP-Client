import sip.header
import sip.authorization

__allow__ = list()
def __sip_request__(method):
    __allow__.append(method.__name__)
    return method

def __getAllow__():
    allowStr = str()
    for req in __allow__:
        allowStr += req + ', '
    return allowStr[:len(allowStr)-2]

def __buildBasicRequest__(p_requestName : str,
                          p_username : str,
                          p_domain : str,
                          p_clientIP : str,
                          p_clientPORT : str,
                          p_tag : str,
                          p_branch : str, 
                          p_callID : str,
                          p_cseq : str,
                          p_username_dest : str = None):
    if p_username_dest == None:
        p_username_dest = p_username
    request = str()
    request += '{r_requestName} sip:{r_username}@{p_domain} SIP/2.0\r\n'.format(r_requestName=p_requestName,
                                                                            r_username=p_username_dest, 
                                                                            p_domain=p_domain)
    request += 'Via: SIP/2.0/UDP {r_clientIP}:{r_clientPORT};branch={r_branch};rport\r\n'.format(
        r_clientIP=p_clientIP,
        r_clientPORT=p_clientPORT,
        r_branch=p_branch)
    request += 'Contact: <sip:{r_username}@{r_clientIP}:{r_clientPORT}>\r\n'.format(
        r_username=p_username,
        r_clientIP=p_clientIP,
        r_clientPORT=p_clientPORT)
    request += 'From: <sip:{r_username}@{r_domain}>;tag={r_tag}\r\n'.format(
        r_username=p_username, 
        r_domain=p_domain,
        r_tag=p_tag)
    request += 'To: <sip:{r_username}@{r_domain}>\r\n'.format(
        r_username=p_username_dest,
        r_domain=p_domain)
    request += 'Call-ID: {r_callID}\r\n'.format(r_callID=p_callID)
    request += 'CSeq: {r_cseq} {r_requestName}\r\n'.format(r_requestName=p_requestName,
                                                         r_cseq=p_cseq)
    request += 'Max-Forwards: {}\r\n'.format(sip.header.maxForwards())
    request += 'Allow: ACK,BYE,CANCEL,INFO,INVITE,MESSAGE,NOTIFY,OPTIONS,PRACK,REFER,REGISTER,SUBSCRIBE\r\n'
    return request

@__sip_request__
def REGISTER(p_username : str, 
             p_domain : str,
             p_clientIP : str,
             p_clientPORT : str,
             p_tag : str,
             p_expires : int,
             p_branch : str = sip.header.branch(),
             p_callID : str = sip.header.callID(),
             p_cseq : str = sip.header.cseq(),
             p_password : str = None,
             p_authorization : sip.authorization.Authorization = None):
    requestName = 'REGISTER'
    request = str()
    request += __buildBasicRequest__(p_requestName=requestName,
                                     p_username=p_username,
                                     p_domain=p_domain,
                                     p_clientIP=p_clientIP,
                                     p_clientPORT=p_clientPORT,
                                     p_branch=p_branch,
                                     p_tag=p_tag,
                                     p_callID=p_callID,
                                     p_cseq=p_cseq)
    request += 'Expires: {r_expires}\r\n'.format(r_expires=p_expires)
    request += 'User-Agent: {}\r\n'.format('SIP-Client')
    if not p_authorization == None and not p_password == None:
        request += p_authorization.getAuthorizationString(p_username=p_username, p_password=p_password, p_domain=p_domain)
    request += 'Content-Length: {}'.format(0)
    return request

@__sip_request__
def INVITE( p_username : str, 
            p_username_dest : str,
            p_domain : str,
            p_clientIP : str,
            p_clientPORT : str,
            p_tag : str,
            p_branch : str = sip.header.branch(),
            p_callID : str = sip.header.callID(),
            p_cseq : str = sip.header.cseq(),
            p_contentSDP : str = None):
    requestName = 'INVITE'
    request = str()
    request += __buildBasicRequest__(p_requestName=requestName,
                                        p_username=p_username,
                                        p_domain=p_domain,
                                        p_clientIP=p_clientIP,
                                        p_clientPORT=p_clientPORT,
                                        p_branch=p_branch,
                                        p_tag=p_tag,
                                        p_callID=p_callID,
                                        p_cseq=p_cseq,
                                        p_username_dest=p_username_dest)
    request += 'Supported: 100rel\r\n'
    request += 'User-Agent: {}\r\n'.format('SIP-Client')
    request += 'Content-Length: {}'.format(0)
    return request
    # request += 'Content-Type: application/sdp'


