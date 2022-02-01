import hashlib,binascii
import base64


class Afflink_cookie:
    def __init__(self,pro_id=None,pro_name=None,aff_id=None,secretkey=None):
        self.pro_id=pro_id
        self.pro_name=pro_name
        self.secretkey=secretkey
        self.aff_id=aff_id
    def cookie_key(self):
        cryp=hashlib.pbkdf2_hmac("sha512", str(self.pro_id).encode()+str(self.pro_name).encode(), self.secretkey.encode(),2048,20)
        return binascii.hexlify(cryp).decode()
    def cookie_value_encode(self):
        a= base64.a85encode((str(self.aff_id)+","+str(self.pro_name)).encode())
        b=base64.standard_b64encode(a)
        c=base64.urlsafe_b64encode(b)
        val=base64.standard_b64encode(c+",".encode()+c)
        return val.decode()
    def cookie_value_decode(self,e_val):
        es_val=e_val.encode()
        val=base64.standard_b64decode(es_val).decode().split(",")[0].encode()
        c=base64.urlsafe_b64decode(val)
        b=base64.standard_b64decode(c)
        a=base64.a85decode(b)
        return a.decode()
class Aff_url_maker:
    def __init__(self,pro_id=None,pro_name=None,aff_id=None):
        self.aff_id=aff_id
        self.pro_name=pro_name
        self.pro_id=pro_id
    def encode_url(self):
        v=base64.urlsafe_b64encode(str(self.pro_id).encode()+"'~'".encode()+str(self.pro_name).encode()+"'~'".encode()+str(self.aff_id).encode())
        va=base64.a85encode(v)
        val=base64.urlsafe_b64encode(va)
        return val.decode()
    def decode_url(self,value):
        v=base64.urlsafe_b64decode(value.encode())
        va=base64.a85decode(v)
        val=base64.urlsafe_b64decode(va)
        return val.decode()


# "sha512", str(self.id).encode+str(self.name).encode, self.secretkey.encode,2048,10
# print(binascii.hexlify(stretched).decode())
if __name__ == '__main__':
    # a=Afflink_cookie(10000,"canvassddddddd","PASS").cookie_value_encode()
    # print(type(a))
    # print(a)
    # l="VFVkV2FVOXFaM2RUYVZKbFVXdFNURmhWWjNkU2FXaENXbTE0UWs0eFVUQllVVDA5LFRVZFdhVTlxWjNkVGFWSmxVV3RTVEZoVlozZFNhV2hDV20xNFFrNHhVVEJZVVQwOQ=="
    # c=Afflink_cookie().cookie_value_decode(l)
    # print(c)

    ab=Aff_url_maker(1,"Netflix",10).encode_url()
    print(ab)
    ac=Aff_url_maker().decode_url(ab)
    print(ac.split("'~'"))