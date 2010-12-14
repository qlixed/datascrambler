'''
=== scrambler.py ===

@author: QliXed [aka QliX=D!, EHB]
@contact: qlixed_at_gmail_dot_com
'''
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from  base64 import b64encode, b64decode
from Queue import Queue

ADJUST_CHAR = '=' # B64 Adjust fill char.


class CryptoBlock(object):
    __encrypted = None
    __hash = None
    __block_id = None
    
    def __init__(self, block_id, encrypted_text, hash_digest):
        self.__encrypted = encrypted_text
        self.__block_id = block_id
        self.__hash = hash_digest

    def get_encrypted(self):
        return self.__encrypted

    def get_hash(self):
        return self.__hash

    def get_size(self):
        return len(self.__encrypted)

    def get_block_id(self):
        return self.__block_id

    def set_block_id(self, value):
        self.__block_id = value
    
    encrypted = property(get_encrypted, None, None, "Encrypted Data")
    hash = property(get_hash, None, None, "Hash of this encrypted data block")
    size = property(get_size, None, None, "The size of this block")
    block_id = property(get_block_id, set_block_id, None, "Number (order) Of Block")
    

class Crypter(object):
    __crypted_blocks = None
    __decrypted_blocks = None
    __key = None
    __cipher = None
    __blocksize = None
        
    def __init__(self, key, blocklimit=None):
        self.__key = SHA256.new(b64encode(key)).digest()
        self.__cipher = AES.new(self.__key)
        if blocklimit is None:
            self.__blocksize = 0
        else:
            self.__blocksize = blocklimit - (blocklimit % 16)
        self.__crypted_blocks = list()
        self.__decrypted_blocks = list()
    
    def encrypt_data(self, text):
        b64_text = b64encode(text)
        text_adjustement = 16 - (len(b64_text) % 16)
        if text_adjustement < 16:
            b64_text = b64_text + ADJUST_CHAR * text_adjustement
            #print "Adjusting by:", text_adjustement
        hash_text = ""
        block_count = 0
        if self.__blocksize != 0:
            txt_blocks = Queue()
            if len(b64_text) > self.__blocksize:
                i = 1
                block_offset = self.__blocksize * i
                while len(b64_text) > block_offset:
                    block_offset = self.__blocksize * i 
                    txt_blocks.put(b64_text[self.__blocksize * (i - 1):block_offset])
                    i += 1
            else:
                txt_blocks.put(b64_text)
            b64_text_block = ""
            while not txt_blocks.empty():
                block_count += 1
                b64_text_block = txt_blocks.get()
                hash_text = SHA256.new(b64_text_block).hexdigest()
                self.__crypted_blocks.append(CryptoBlock(block_count, self.__cipher.encrypt(b64_text_block), hash_text))
        else:
            #print "b64_text size:", len(b64_text)
            hash_text = SHA256.new(b64_text).hexdigest()
            block_count += 1
            #print "dataenc size:", len(dataenc)
            self.__crypted_blocks.append(CryptoBlock(block_count, self.__cipher.encrypt(b64_text), hash_text))
    
    def decrypt_cryptoblocks(self, crypto_blocks):
        block_list = None
        if isinstance(crypto_blocks, list):
            block_list = crypto_blocks
            if not isinstance(crypto_blocks[0], CryptoBlock):
                raise TypeError("crypto_blocks needs to be a CryptoBlock or a list of it!")
        elif isinstance(crypto_blocks, CryptoBlock):
            block_list = list(crypto_blocks)
        else:
            raise TypeError("crypto_blocks needs to be a CryptoBlock or a list of it!")
        for block in block_list:
            #print "blocksize:", block.size, " - ", (block.size%16)
            b64_text = self.__cipher.decrypt(block.encrypted)
            hash_text = SHA256.new(b64_text).hexdigest()
            if block.hash != hash_text:
                raise ValueError("Hash Test Failed!")
            self.__decrypted_blocks.append(b64decode(b64_text))
        
    def get_encrypted_blocks(self):
        return self.__crypted_blocks
    
    def get_decrypted_blocks(self):
        return self.__decrypted_blocks
