import ctypes, os, sys
import ctypes.util

from ctypes import (
    byref, c_byte, c_int, c_uint, c_char_p, c_size_t, 
    c_void_p, create_string_buffer, CFUNCTYPE, POINTER
)

# Flags to pass to context_create.
CONTEXT_VERIFY = 0b0100000001
CONTEXT_SIGN =   0b1000000001
CONTEXT_NONE =   0b0000000001

# Flags to pass to ec_pubkey_serialize
EC_COMPRESSED =   0b0100000010
EC_UNCOMPRESSED = 0b0000000010

def _init(flags = (CONTEXT_SIGN | CONTEXT_VERIFY)):
    library_path = ctypes.util.find_library('libsecp256k1')
    if library_path is None:
        CURRENT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
        if sys.platform == 'darwin':
            library_path = os.path.abspath(os.path.join(CURRENT_DIR, "prebuilt/libsecp256k1.dylib"))
        else:
            library_path = os.path.abspath(os.path.join(CURRENT_DIR, "prebuilt/libsecp256k1.so"))

    secp256k1 = ctypes.cdll.LoadLibrary(library_path)

    secp256k1.secp256k1_context_create.argtypes = [c_uint]
    secp256k1.secp256k1_context_create.restype = c_void_p

    secp256k1.secp256k1_context_randomize.argtypes = [c_void_p, c_char_p]
    secp256k1.secp256k1_context_randomize.restype = c_int

    
    secp256k1.secp256k1_ec_privkey_negate.argtypes = [c_void_p, c_char_p]
    secp256k1.secp256k1_ec_privkey_negate.restype = c_int
    
    secp256k1.secp256k1_ec_privkey_tweak_add.argtypes = [c_void_p, c_char_p, c_char_p]
    secp256k1.secp256k1_ec_privkey_tweak_add.restype = c_int

    secp256k1.secp256k1_ec_privkey_tweak_mul.argtypes = [c_void_p, c_char_p, c_char_p]
    secp256k1.secp256k1_ec_privkey_tweak_mul.restype = c_int

    
    secp256k1.secp256k1_ec_pubkey_create.argtypes = [c_void_p, c_void_p, c_char_p]
    secp256k1.secp256k1_ec_pubkey_create.restype = c_int

    secp256k1.secp256k1_ec_pubkey_parse.argtypes = [c_void_p, c_char_p, c_char_p, c_int]
    secp256k1.secp256k1_ec_pubkey_parse.restype = c_int

    secp256k1.secp256k1_ec_pubkey_serialize.argtypes = [c_void_p, c_char_p, c_void_p, c_char_p, c_uint]
    secp256k1.secp256k1_ec_pubkey_serialize.restype = c_int

    secp256k1.secp256k1_ec_pubkey_tweak_add.argtypes = [c_void_p, c_char_p, c_char_p]
    secp256k1.secp256k1_ec_pubkey_tweak_add.restype = c_int

    secp256k1.secp256k1_ec_pubkey_tweak_mul.argtypes = [c_void_p, c_char_p, c_char_p]
    secp256k1.secp256k1_ec_pubkey_tweak_mul.restype = c_int

    
    secp256k1.secp256k1_ecdsa_signature_parse_compact.argtypes = [c_void_p, c_char_p, c_char_p]
    secp256k1.secp256k1_ecdsa_signature_parse_compact.restype = c_int

    secp256k1.secp256k1_ecdsa_signature_serialize_compact.argtypes = [c_void_p, c_char_p, c_char_p]
    secp256k1.secp256k1_ecdsa_signature_serialize_compact.restype = c_int

    secp256k1.secp256k1_ecdsa_signature_parse_der.argtypes = [c_void_p, c_char_p, c_char_p, c_uint]
    secp256k1.secp256k1_ecdsa_signature_parse_der.restype = c_int

    secp256k1.secp256k1_ecdsa_signature_serialize_der.argtypes = [c_void_p, c_char_p, c_void_p, c_char_p]
    secp256k1.secp256k1_ecdsa_signature_serialize_der.restype = c_int

    secp256k1.secp256k1_ecdsa_sign.argtypes = [c_void_p, c_char_p, c_char_p, c_char_p, c_void_p, c_void_p]
    secp256k1.secp256k1_ecdsa_sign.restype = c_int

    secp256k1.secp256k1_ecdsa_verify.argtypes = [c_void_p, c_char_p, c_char_p, c_char_p]
    secp256k1.secp256k1_ecdsa_verify.restype = c_int

    secp256k1.secp256k1_ec_pubkey_combine.argtypes = [c_void_p, c_char_p, c_void_p, c_size_t]
    secp256k1.secp256k1_ec_pubkey_combine.restype = c_int
    
    secp256k1.ctx = secp256k1.secp256k1_context_create(flags)
    
    r = secp256k1.secp256k1_context_randomize(secp256k1.ctx, os.urandom(32))
    
    """ Ugly check that schnorr is there """
    try:
        secp256k1.secp256k1_xonly_pubkey_serialize.argtypes = [c_void_p, c_char_p, c_char_p]
        secp256k1.secp256k1_xonly_pubkey_serialize.restype = c_int
        secret = b'\x55'*32
        pub = bytes(64)
        pubkey = secp256k1.secp256k1_ec_pubkey_create(secp256k1.ctx, pub, secret)
        x = bytes(32)
        secp256k1.secp256k1_xonly_pubkey_serialize(secp256k1.ctx, x, pub)
        secp256k1.schnorr_available = True

        secp256k1.secp256k1_xonly_pubkey_parse.argtypes = [c_void_p, c_char_p, c_char_p]
        secp256k1.secp256k1_xonly_pubkey_parse.restype = c_int

    except:
        secp256k1.schnorr_available = False

    return secp256k1

_secp = _init()
schnorr_available = _secp.schnorr_available

# bindings equal to ones in micropython
def context_randomize(seed, context=_secp.ctx):
    if len(seed)!=32:
        raise ValueError("Seed should be 32 bytes long")
    if _secp.secp256k1_context_randomize(context, seed) == 0:
        raise RuntimeError("Failed to randomize context")

def ec_pubkey_create(secret, context=_secp.ctx):
    if len(secret)!=32:
        raise ValueError("Private key should be 32 bytes long")
    pub = bytes(64)
    r = _secp.secp256k1_ec_pubkey_create(context, pub, secret)
    if r == 0:
        raise ValueError("Invalid private key")
    return pub

def ec_pubkey_parse(sec, context=_secp.ctx):
    if len(sec)!=33 and len(sec)!= 65:
        raise ValueError("Serialized pubkey should be 33 or 65 bytes long")
    if len(sec)==33:
        if sec[0] != 0x02 and sec[0] != 0x03:
            raise ValueError("Compressed pubkey should start with 0x02 or 0x03")
    else:
        if sec[0] != 0x04:
            raise ValueError("Uncompressed pubkey should start with 0x04")
    pub = bytes(64)
    r = _secp.secp256k1_ec_pubkey_parse(context, pub, sec, len(sec))
    if r == 0:
        raise ValueError("Failed parsing public key")
    return pub

def ec_pubkey_serialize(pubkey, flag=EC_COMPRESSED, context=_secp.ctx):
    if len(pubkey)!=64:
        raise ValueError("Pubkey should be 64 bytes long")
    if flag not in [EC_COMPRESSED, EC_UNCOMPRESSED]:
        raise ValueError("Invalid flag")
    sec = bytes(33) if (flag == EC_COMPRESSED) else bytes(65)
    sz = c_size_t(len(sec))
    r = _secp.secp256k1_ec_pubkey_serialize(context, sec, byref(sz), pubkey, flag)
    if r == 0:
        raise ValueError("Failed to serialize pubkey")
    return sec

def ecdsa_signature_parse_compact(compact_sig, context=_secp.ctx):
    if len(compact_sig)!=64:
        raise ValueError("Compact signature should be 64 bytes long")
    sig = bytes(64)
    r = _secp.secp256k1_ecdsa_signature_parse_compact(context, sig, compact_sig)
    if r == 0:
        raise ValueError("Failed parsing compact signature")
    return sig

def ecdsa_signature_parse_der(der, context=_secp.ctx):
    sig = bytes(64)
    r = _secp.secp256k1_ecdsa_signature_parse_der(context, sig, der, len(der))
    if r == 0:
        raise ValueError("Failed parsing der signature")
    return sig
    
def ecdsa_signature_serialize_der(sig, context=_secp.ctx):
    if len(sig)!=64:
        raise ValueError("Signature should be 64 bytes long")
    der = bytes(78) # max
    sz = c_size_t(len(der))
    r = _secp.secp256k1_ecdsa_signature_serialize_der(context, der, byref(sz), sig)
    if r == 0:
        raise ValueError("Failed serializing der signature")
    return der[:sz.value]

def ecdsa_signature_serialize_compact(sig, context=_secp.ctx):
    if len(sig)!=64:
        raise ValueError("Signature should be 64 bytes long")
    ser = bytes(64)
    r = _secp.secp256k1_ecdsa_signature_serialize_compact(context, ser, sig)
    if r == 0:
        raise ValueError("Failed serializing der signature")
    return ser
    
def ecdsa_signature_normalize(sig, context=_secp.ctx):
    if len(sig)!=64:
        raise ValueError("Signature should be 64 bytes long")
    sig2 = bytes(64)
    r = _secp.secp256k1_ecdsa_signature_normalize(context, sig2, sig)
    return sig2

def ecdsa_verify(sig, msg, pub, context=_secp.ctx):
    if len(sig)!=64:
        raise ValueError("Signature should be 64 bytes long")
    if len(msg)!=32:
        raise ValueError("Message should be 32 bytes long")
    if len(pub)!=64:
        raise ValueError("Public key should be 64 bytes long")
    r = _secp.secp256k1_ecdsa_verify(context, sig, msg, pub)
    return bool(r)

def ecdsa_sign(msg, secret, context=_secp.ctx):
    if len(msg)!=32:
        raise ValueError("Message should be 32 bytes long")
    if len(secret)!=32:
        raise ValueError("Secret key should be 32 bytes long")
    sig = bytes(64)
    r = _secp.secp256k1_ecdsa_sign(context, sig, msg, secret, None, None)
    if r == 0:
        raise ValueError("Failed to sign")
    return sig

def ec_seckey_verify(secret, context=_secp.ctx):
    if len(secret)!=32:
        raise ValueError("Secret should be 32 bytes long")
    return bool(_secp.secp256k1_ec_seckey_verify(context, secret))

def ec_privkey_negate(secret, context=_secp.ctx):
    if len(secret)!=32:
        raise ValueError("Secret should be 32 bytes long")
    _secp.secp256k1_ec_privkey_negate(context, secret);

def ec_pubkey_negate(pubkey, context=_secp.ctx):
    if len(pubkey)!=64:
        raise ValueError("Pubkey should be a 64-byte structure")
    r = _secp.secp256k1_ec_pubkey_negate(context, pubkey)
    if r == 0:
        raise ValueError("Failed to negate pubkey")

def ec_privkey_tweak_add(secret, tweak, context=_secp.ctx):
    if len(secret)!=32 or len(tweak)!=32:
        raise ValueError("Secret and tweak should both be 32 bytes long")
    if _secp.secp256k1_ec_privkey_tweak_add(context, secret, tweak) == 0:
        raise ValueError("Failed to tweak the secret")

def ec_pubkey_tweak_add(pub, tweak, context=_secp.ctx):
    if len(pub)!=64:
        raise ValueError("Public key should be 64 bytes long")
    if len(tweak)!=32:
        raise ValueError("Tweak should be 32 bytes long")
    if _secp.secp256k1_ec_pubkey_tweak_add(context, pub, tweak) == 0:
        raise ValueError("Failed to tweak the public key")

def ec_privkey_tweak_mul(secret, tweak, context=_secp.ctx):
    if len(secret)!=32 or len(tweak)!=32:
        raise ValueError("Secret and tweak should both be 32 bytes long")
    if _secp.secp256k1_ec_privkey_tweak_mul(context, secret, tweak) == 0:
        raise ValueError("Failed to tweak the secret")

def ec_pubkey_tweak_mul(pub, tweak, context=_secp.ctx):
    if len(pub)!=64:
        raise ValueError("Public key should be 64 bytes long")
    if len(tweak)!=32:
        raise ValueError("Tweak should be 32 bytes long")
    if _secp.secp256k1_ec_pubkey_tweak_mul(context, pub, tweak) == 0:
        raise ValueError("Failed to tweak the public key")

def ec_pubkey_combine(*args, context=_secp.ctx):
    pub = bytes(64)
    pubkeys = (c_char_p * len(args))(*args)
    r = _secp.secp256k1_ec_pubkey_combine(context, pub, pubkeys, len(args))
    if r == 0:
        raise ValueError("Failed to negate pubkey")
    return pub

if schnorr_available:
    def xonly_pubkey_parse(x, context=_secp.ctx):
        if len(x)!=32:
            raise ValueError("xonly-pubkey should be 32 bytes long")
        pub = bytes(64)
        r = _secp.secp256k1_xonly_pubkey_parse(context, pub, x)
        if r==0:
            raise ValueError("Failed to parse xonly-pubkey")
        return pub

    def xonly_pubkey_serialize(pub, context=_secp.ctx):
        if len(pub)!=64:
            raise ValueError("Public key should be 64 bytes long")
        x = bytes(32)
        _secp.secp256k1_xonly_pubkey_serialize(context, x, pub)
        return x

    # secp256k1_xonly_pubkey_create(ctx,pub,sec)
    # secp256k1_xonly_pubkey_from_pubkey(ctx,xonly,ref@is_negated?,pub)
    # secp256k1_xonly_seckey_tweak_add(ctx,sec,tweak)
    # secp256k1_xonly_pubkey_tweak_add(ctx,pub,ref@is_negated,tweak)
    # secp256k1_xonly_pubkey_tweak_test(ctx,pubout, isneg, pubint, tweak)
    # secp256k1_schnorrsig_serialize(ctx,out64,sig)
    # secp256k1_schnorrsig_parse(ctx,sig,in64)
    # secp256k1_schnorrsig_sign(ctx,sig,msg,sec,None,None)
    # secp256k1_schnorrsig_verify(ctx,sig,msg,pub)
    # secp256k1_schnorrsig_verify_batch(ctx,scratch,sigs[],msgs[],pubs[],n)
