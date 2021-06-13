import re
import logging
__logger__ = logging.getLogger(__name__)

def decodeRequest(p_request):
    request = dict()
    p_request = p_request.split("\r\n")
    request['Message'] = p_request[0]

    t_addr = request['Message'].split()[1][4:]
    t_addr_idx = t_addr.find(':')
    request['contactPort'] = t_addr[t_addr_idx+1:]

    for idx in range(len(p_request)):

        if p_request[idx].find('WWW-Authenticate') != -1:
            t_req = p_request[idx].split()
            for t_idx in range(len(t_req)):

                if t_req[t_idx].find('nonce=') != -1:
                    request['nonce'] = t_req[t_idx][7:len(t_req[t_idx])-2]

                if t_req[t_idx].find('realm=') != -1:
                    request['realm'] = t_req[t_idx][7:len(t_req[t_idx])-2]

        if p_request[idx].find('Call-ID:') != -1:
            request['call-id'] = p_request[idx][8:].strip()

        if p_request[idx].find('CSeq:') != -1:
            request['cseq'] = p_request[idx][6:16]
            request['method'] = p_request[idx][17:]

        if p_request[idx].find('m=audio ') != -1:
            idx_t = len('nm=audio')
            request['audio-port'] = p_request[idx][idx_t:idx_t+5]

        if p_request[idx].find('Expires:') != -1:
            request['expires'] = p_request[idx][8:]

        if p_request[idx].find('From:') != -1:
            idx_t = p_request[idx].find('tag=')
            request['tag'] = p_request[idx][idx_t+4:idx_t+4+17]

    __logger__.info(request)
    return request
