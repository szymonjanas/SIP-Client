import sip.header

class RESPONSES:
    OK200 = '200 OK'

def __buildBasicResponse__( p_responseName : RESPONSES,
                            p_username : str,
                            p_domain : str,
                            p_clientIP : str,
                            p_clientPORT : str,
                            p_tag : str,
                            p_branch : str, 
                            p_callID : str,
                            p_cseq : str,
                            p_cseqResponseName,
                            p_tagFrom,
                            p_contactPort,
                            p_userAgent,
                            p_username_dest : str = None):
    if p_username_dest is None:
        p_username_dest = p_username
    response = str()
    response += 'SIP/2.0 {r_responseName}\r\n'.format(   r_responseName=p_responseName,
                                                        r_username=p_username_dest, 
                                                        p_domain=p_domain)
    response += 'Via: SIP/2.0/UDP {r_clientIP}:{r_clientPORT};branch={r_branch};received={p_ip};rport={p_clientPORT2}\r\n'.format(
        r_clientIP=p_clientIP,
        r_clientPORT=p_clientPORT,
        r_branch=p_branch,
        p_ip=p_clientIP,
        p_clientPORT2=p_clientPORT)
    response += 'From: <sip:{r_username}@{r_domain}>;tag={r_tag}\r\n'.format(
        r_username=p_username_dest, 
        r_domain=p_domain,
        r_tag=p_tagFrom)
    response += 'To: <sip:{r_username}@{r_domain}>;tag={r_tag}\r\n'.format(
        r_username=p_username,
        r_domain=p_domain,
        r_tag=p_tag)
    response += 'CSeq: {r_cseq} {r_cseqResponseName}\r\n'.format(r_cseqResponseName=p_cseqResponseName,
                                                         r_cseq=p_cseq)
    response += 'Call-ID: {r_callID}\r\n'.format(r_callID=p_callID)
    response += 'Allow: ACK,BYE,CANCEL,INFO,INVITE,MESSAGE,NOTIFY,OPTIONS,PRACK,REFER,REGISTER,SUBSCRIBE\r\n'
    response += 'User-Agent: {}\r\n'.format(p_userAgent)
    response += 'Contact: <sip:{r_username}@{r_clientIP}:{r_contactPort}>\r\n'.format(
        r_username=p_username,
        r_clientIP=p_clientIP,
        r_contactPort=p_contactPort)
    return response

def RESPONSE(   responseName : RESPONSES,
                p_username,
                p_username_dest,
                p_domain,
                p_clientIP,
                p_clientPORT,
                p_userAgent,
                p_requestResponse,
                p_tagFrom,
                p_contactPort,
                p_callDetails : sip.header.CallDetails = sip.header.CallDetails()):
    respName = str(responseName)
    resp = str()
    resp = __buildBasicResponse__(  p_responseName=respName,
                                    p_username=p_username,
                                    p_domain=p_domain,
                                    p_clientIP=p_clientIP,
                                    p_clientPORT=p_clientPORT,
                                    p_branch=p_callDetails.branch,
                                    p_tag=p_callDetails.tag,
                                    p_callID=p_callDetails.callID,
                                    p_cseq=p_callDetails.cseq,
                                    p_username_dest=p_username_dest,
                                    p_cseqResponseName=p_requestResponse,
                                    p_tagFrom=p_tagFrom,
                                    p_contactPort=p_contactPort,
                                    p_userAgent=p_userAgent)
    resp += 'Content-Length: 0\r\n'
    resp += '\r\n'
    return resp

