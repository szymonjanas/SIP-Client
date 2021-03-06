import sip.header
import sip.authorization
import sip.Client

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
    if p_username_dest is None:
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

def REGISTER(p_client : sip.Client.Client,
             p_callDetails : sip.header.CallDetails = sip.header.CallDetails(),
             p_authorization : sip.authorization.Authorization = None):
    requestName = 'REGISTER'
    request = str()
    request += __buildBasicRequest__(p_requestName=requestName,
                                     p_username=p_client.config.username,
                                     p_domain=p_client.config.domain,
                                     p_clientIP=p_client.config.clientIP,
                                     p_clientPORT=p_client.config.clientPORT,
                                     p_branch=p_callDetails.branch,
                                     p_tag=p_callDetails.tag,
                                     p_callID=p_callDetails.callID,
                                     p_cseq=p_callDetails.cseq)
    request += 'Expires: {r_expires}\r\n'.format(r_expires=p_client.config.expires)
    request += 'User-Agent: {}\r\n'.format(p_client.config.userAgent)
    if not p_authorization is None and not p_client.config.password is None:
        request += p_authorization.getAuthorizationString(
            p_username=p_client.config.username, 
            p_password=p_client.config.password, 
            p_domain=p_client.config.domain)
    request += 'Content-Length: {}\r\n'.format(0)
    request += '\r\n'
    return request

def INVITE( p_client : sip.Client.Client, 
            p_username_dest : str,
            p_callDetails : sip.header.CallDetails = sip.header.CallDetails(),
            p_contentSDP : str = None):
    requestName = 'INVITE'
    request = str()
    request += __buildBasicRequest__(p_requestName=requestName,
                                        p_username=p_client.config.username,
                                        p_domain=p_client.config.domain,
                                        p_clientIP=p_client.config.clientIP,
                                        p_clientPORT=p_client.config.clientPORT,
                                        p_branch=p_callDetails.branch,
                                        p_tag=p_callDetails.tag,
                                        p_callID=p_callDetails.callID,
                                        p_cseq=p_callDetails.cseq,
                                        p_username_dest=p_username_dest)
    request += 'Supported: 100rel\r\n'
    request += 'User-Agent: {}\r\n'.format(p_client.config.userAgent)
    contentLength = 0
    if p_contentSDP is not None:
        contentLength = len(p_contentSDP)
    request += 'Content-Length: {}\r\n'.format(contentLength)
    if p_contentSDP is not None:
        request += 'Content-Type: {}\r\n'.format("application/sdp")
        request += '\r\n{}'.format(p_contentSDP)
    if p_contentSDP is None:
        request += '\r\n'
    return request

def ACK(p_client : sip.Client.Client, 
        p_username_dest : str,
        p_callDetails : sip.header.CallDetails = sip.header.CallDetails()):
    requestName = 'ACK'
    request = str()
    request += __buildBasicRequest__(   p_requestName=requestName,
                                        p_username=p_client.config.username,
                                        p_domain=p_client.config.domain,
                                        p_clientIP=p_client.config.clientIP,
                                        p_clientPORT=p_client.config.clientPORT,
                                        p_branch=p_callDetails.branch,
                                        p_tag=p_callDetails.tag,
                                        p_callID=p_callDetails.callID,
                                        p_cseq=p_callDetails.cseq,
                                        p_username_dest=p_username_dest)
    request += 'User-Agent: {}\r\n'.format(p_client.config.userAgent)
    contentLength = 0
    request += 'Content-Length: {}\r\n'.format(contentLength)
    request += '\r\n'
    return request

def CANCEL( p_client : sip.Client.Client, 
            p_username_dest : str,
            p_callDetails : sip.header.CallDetails = sip.header.CallDetails()):
    requestName = 'CANCEL'
    request = str()
    request += __buildBasicRequest__(   p_requestName=requestName,
                                        p_username=p_client.config.username,
                                        p_domain=p_client.config.domain,
                                        p_clientIP=p_client.config.clientIP,
                                        p_clientPORT=p_client.config.clientPORT,
                                        p_branch=p_callDetails.branch,
                                        p_tag=p_callDetails.tag,
                                        p_callID=p_callDetails.callID,
                                        p_cseq=p_callDetails.cseq,
                                        p_username_dest=p_username_dest)
    request += 'User-Agent: {}\r\n'.format(p_client.config.userAgent)
    contentLength = 0
    request += 'Content-Length: {}\r\n'.format(contentLength)
    request += '\r\n'
    return request

def BYE( p_client : sip.Client.Client, 
         p_username_dest : str,
         p_callDetails : sip.header.CallDetails = sip.header.CallDetails()):
    requestName = 'BYE'
    request = str()
    request += __buildBasicRequest__(   p_requestName=requestName,
                                        p_username=p_client.config.username,
                                        p_domain=p_client.config.domain,
                                        p_clientIP=p_client.config.clientIP,
                                        p_clientPORT=p_client.config.clientPORT,
                                        p_branch=p_callDetails.branch,
                                        p_tag=p_callDetails.tag,
                                        p_callID=p_callDetails.callID,
                                        p_cseq=p_callDetails.cseq,
                                        p_username_dest=p_username_dest)
    request += 'User-Agent: {}\r\n'.format(p_client.config.userAgent)
    contentLength = 0
    request += 'Content-Length: {}\r\n'.format(contentLength)
    request += '\r\n'
    return request
