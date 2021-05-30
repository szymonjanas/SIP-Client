import hashlib

class Authorization:
    def __init__(self,
                 p_nonce : str,
                 p_realm : str,
                 p_method : str):
        self.nonce = p_nonce
        self.realm = p_realm
        self.method = p_method

    def __H__(self, data):
        return hashlib.md5(data.encode('utf-8')).hexdigest()

    def __KD__(self, secret, data):
        return self.__H__(secret + ":" + data)

    def getAuthorizationString(self, p_username : str, p_password : str, p_domain : str):
        A1 = p_username + ':' + self.realm + ':' + p_password
        uri = 'sip:{r_username}@{r_domain}'.format(r_username=p_username, r_domain=p_domain)
        A2 = self.method + ':' + uri
        response = self.__KD__( self.__H__(A1), self.nonce + ":" + self.__H__(A2))
        return 'Authorization: Digest username="' + p_username + '",realm="' + self.realm + '",nonce="' + self.nonce + '",uri="' + uri + '",response="' + response + '",algorithm=MD5' + "\r\n"
