import unittest
import sys
import os
import re

sys.path.insert(0, os.path.dirname(os.path.abspath(os.getcwd())) + '/src')

from src.log import *
from src.cli import *
from src.certifier import *
from src.xpki_client import *
from src.main import *
'''
TODO
'''
def clear_log_file(file:str):
    with open(file, 'w') as f:
        f.close()

def get_last_log_line(file:str):
    with open(file, 'r') as f:
        lines = f.readlines()
    
    # Log function adds \n to log file
    return lines[-1].strip() if lines else ''

LOG_FILE = 'libcertifier.tests.log'

class Tests(unittest.TestCase):
    def test_expected_log_behavior(self):
        cli_setup()

        args = Namespace(config='./tests/cfgs/libcertifier.test.cfg', verbose=None, ca_path=None)

        log_setup(args)

        levels = [
            [1, "TRACE", "trace", r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} TRACE .+tests.py:\d+ test'],
            [2, "DEBUG", "debug", r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} DEBUG .+tests.py:\d+ test'],
            [3, "INFO", "info", r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} INFO .+tests.py:\d+ test'],
            [4, "WARN", "warn", r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} WARN .+tests.py:\d+ test'],
            [5, "ERROR", "error", r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} ERROR .+tests.py:\d+ test'],
            [6, "FATAL", "fatal", r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} FATAL .+tests.py:\d+ test']
        ]
        
        for level in levels:
            logger.setLevel(level[0])
            log("test", level[0])
            assert re.match(level[3], get_last_log_line(LOG_FILE)) is not None
            log("test", level[1])
            assert (re.match(level[3], get_last_log_line(LOG_FILE))) is not None
            log("test", level[2])
            assert (re.match(level[3], get_last_log_line(LOG_FILE))) is not None

        log_destroy()
        clear_log_file(LOG_FILE)

    def test_invalid_level(self):
        cli_setup()
        args = Namespace(config='./tests/cfgs/libcertifier.test.cfg', verbose=None, ca_path=None)
        log_setup(args)

        pattern = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} ERROR .+tests.py:\d+ Invalid level provided'

        log("test", 7)
        assert re.match(pattern, get_last_log_line(LOG_FILE)) is not None
        log("test", 999)
        assert re.match(pattern, get_last_log_line(LOG_FILE)) is not None
        log("test", -1)
        assert re.match(pattern, get_last_log_line(LOG_FILE)) is not None
        
        log_destroy()
        clear_log_file(LOG_FILE)

    def test_invalid_message(self):
        cli_setup()
        args = Namespace(config='./tests/cfgs/libcertifier.test.cfg', verbose=None, ca_path=None)
        log_setup(args)

        pattern = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} ERROR .+tests.py:\d+ Invalid message provided'

        log(None, 1)
        assert re.match(pattern, get_last_log_line(LOG_FILE)) is not None
        log(1, 1)
        assert re.match(pattern, get_last_log_line(LOG_FILE)) is not None

        log_destroy()
        clear_log_file(LOG_FILE)        

    def test_certifier_init(self):
        # Test what gets precedence: config file or direct arguments to CLI. Answer: CLI
        cli_setup()
        args = Namespace(command="get-cert-status", config='./tests/cfgs/libcertifier.test.cfg', input_p12_path= open("./tests/certs/output.p12", "r"), input_p12_password="changeit", verbose=False, ca_path=None, mtls_p12_path = None)
        log_setup(args)
        logger.setLevel(1)

        certifier = get_certifier_instance(args, 'xpki')
        assert(certifier.CertifierPropMap.p12_filename == "./resources/seed.p12")
        params = get_cert_status_param_t('xpki')
        process(certifier, args, params)
        xc_get_cert_status(certifier, params)

        with open("./tests/certs/output.p12", "r", encoding="UTF-8") as file:
            assert(str(certifier.CertifierPropMap.p12_filename) == str(file))

        log_destroy()
        clear_log_file(LOG_FILE)

    def test_missing_config_file(self):
        args = Namespace(config='./tests/cfgs/nonexistent.cfg', verbose=False, ca_path = None, command='get-cert-status', mtls_p12_path = None)
        certifier = get_certifier_instance(args, 'xpki')

        # Can verify in property_set_defaults() these are default values that contrast definition in libcertifier.tests.cfg
        assert certifier.CertifierPropMap.http_connect_timeout == 20 and certifier.CertifierPropMap.http_timeout == 20
        
    def test_invalid_pkcs12_file(self):
        # With argparse module, made it so p12_filename is expected to be readable file. This exits prematurely like C version so no logging
        args = Namespace(config='./tests/cfgs/libcertifier.test.cfg', verbose=True, ca_path=None, command='get-cert-status', mtls_p12_path = None)
        certifier = get_certifier_instance(args, 'xpki')
        params = get_cert_validity_param_t('xpki')
        params.p12_path = "invalid.p12"
        params.p12_password = "changeit"
        with self.assertRaises(FileNotFoundError):
            with open(params.p12_path, "rb") as p12_file:
                p12_file.read()    
        
        assert get_last_log_line(LOG_FILE) == ''
    
    def test_log_level(self):
        cli_setup()
        args = Namespace(config='./tests/cfgs/libcertifier.test.cfg', verbose=None, ca_path=None)
        log_setup(args)
        logger.setLevel(3)
        log("Shouldn't appear", "TRACE")
        assert get_last_log_line(LOG_FILE) == ''
        
        logger.setLevel(1)
        log("Should appear", "TRACE")
        pattern = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} TRACE .+tests.py:\d+ Should appear'
        assert re.match(pattern, get_last_log_line(LOG_FILE)) is not None

        log_destroy()
        clear_log_file(LOG_FILE)
       
    def test_get_cert_validity(self):
        cli_setup()
        args = Namespace(config='./tests/cfgs/libcertifier.test.cfg', verbose=False, ca_path=None, command='get-cert-validity')
        log_setup(args)
        logger.setLevel(1)
        error = XPKI_CLIENT_ERROR_CODE.XPKI_CLIENT_NOT_IMPLEMENTED
        status = XPKI_CLIENT_CERT_STATUS.XPKI_CLIENT_CERT_UNKNOWN
        params = get_cert_validity_param_t('xpki')

        ## Seed certificate
        certifier = get_certifier_instance(args, 'xpki')
        xc_get_default_cert_validity_param(certifier, params)
        params.input_p12_password = "changeit"
        with open("./src/resources/seed.p12", "r", encoding="utf-8") as p12_filename:
            params.input_p12_path = p12_filename
            status = xc_get_cert_validity(certifier, params)

        assert status == XPKI_CLIENT_CERT_STATUS.XPKI_CLIENT_CERT_VALID

        '''
        NOTE: Checking cert validity is based purely on valid to and valid from date. 
        In practice, implementation will only check/report validity if status is GOOD
        '''
        
        ## Self signed certificate about to expire
        # certifier = get_certifier_instance(args, 'xpki')
        # xc_get_default_cert_validity_param(certifier, params)
        # params.input_p12_password = "about_to_expire"
        # with open("./tests/certs/about_to_expire.p12", "r", encoding="utf-8") as p12_filename:
        #     params.input_p12_path = p12_filename
        #     error, status = xc_get_cert_validity(args, params)

        # assert error == XPKI_CLIENT_ERROR_CODE.XPKI_CLIENT_SUCCESS
        # assert status == XPKI_CLIENT_CERT_STATUS.XPKI_CLIENT_CERT_ABOUT_TO_EXPIRE

        # ## Self signed expired certificate
        # certifier = get_certifier_instance(args, 'xpki')
        # xc_get_default_cert_validity_param(certifier, params)
        # params.input_p12_password = "expired"
        # with open("./tests/certs/expired.p12", "r", encoding="utf-8") as p12_filename:
        #     params.input_p12_path = p12_filename
        #     error, status = xc_get_cert_validity(args, params)

        # assert error == XPKI_CLIENT_ERROR_CODE.XPKI_CLIENT_SUCCESS
        # assert status == XPKI_CLIENT_CERT_STATUS.XPKI_CLIENT_CERT_EXPIRED

        #  ## Self signed certificate not yet valid
        # certifier = get_certifier_instance(args, 'xpki')
        # xc_get_default_cert_validity_param(certifier, params)
        # params.input_p12_password = "not_yet_valid"
        # with open("./tests/certs/not_yet_valid.p12", "r", encoding="utf-8") as p12_filename:
        #     params.input_p12_path = p12_filename
        #     error, status = xc_get_cert_validity(args, params)

        # assert error == XPKI_CLIENT_ERROR_CODE.XPKI_CLIENT_SUCCESS
        # assert status == XPKI_CLIENT_CERT_STATUS.XPKI_CLIENT_CERT_NOT_YET_VALID

        # ## xPKI Revoked Seed Cert
        # certifier = get_certifier_instance(args, 'xpki')
        # xc_get_default_cert_validity_param(certifier, params)
        # params.input_p12_password = "12345"
        # with open("./tests/certs/seedrevoketest.p12", "r", encoding="utf-8") as p12_filename:
        #     params.input_p12_path = p12_filename
        #     error, status = xc_get_cert_validity(args, params)

        # assert error == XPKI_CLIENT_ERROR_CODE.XPKI_CLIENT_SUCCESS
        # assert status == XPKI_CLIENT_CERT_STATUS.XPKI_CLIENT_CERT_VALID

        # ## xPKI Revoked Operational (non-seed) Cert
        # certifier = get_certifier_instance(args, 'xpki')
        # xc_get_default_cert_validity_param(certifier, params)
        # params.input_p12_password = "12345"
        # with open("./tests/certs/oprevoketest.p12", "r", encoding="utf-8") as p12_filename:
        #     params.input_p12_path = p12_filename
        #     error, status = xc_get_cert_validity(args, params)

        # assert error == XPKI_CLIENT_ERROR_CODE.XPKI_CLIENT_SUCCESS
        # assert status == XPKI_CLIENT_CERT_STATUS.XPKI_CLIENT_CERT_VALID
        
        log_destroy()
        clear_log_file(LOG_FILE)
        
    def test_validity_output_status_dependent(self):
        # Testing validity only reported for certificates with GOOD status from API
        cli_setup()
        args = Namespace(config='./tests/cfgs/libcertifier.test.cfg', verbose=True, ca_path=None, command='get-cert-validity')
        log_setup(args)
        logger.setLevel(1)
        status = XPKI_CLIENT_CERT_STATUS.XPKI_CLIENT_CERT_UNKNOWN
        params = get_cert_status_param_t('xpki')

        ## Seed certificate
        certifier = get_certifier_instance(args, 'xpki')
        xc_get_default_cert_status_param(certifier, params)
        params.input_p12_password = "changeit"
        with open("./src/resources/seed.p12", "r", encoding="utf-8") as p12_filename:
            params.input_p12_path = p12_filename
            xc_get_cert_validity(certifier, params)

        pattern = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} INFO .+certifier.py:\d+ Certificate is valid and not close to expiring. Expires on: .+'
        assert re.match(pattern, get_last_log_line(LOG_FILE)) is not None
        
        clear_log_file(LOG_FILE)
        
        ## xPKI Revoked Seed Cert
        # certifier = get_certifier_instance(args, 'xpki')
        # xc_get_default_cert_validity_param(certifier, params)
        # params.p12_password = "12345"
        # with open("./tests/certs/seedrevoketest.p12", "r", encoding="utf-8") as p12_filename:
        #     params.p12_path = p12_filename
        #     xc_get_cert_status(certifier, params, status)
            
        # assert re.match(pattern, get_last_log_line(LOG_FILE)) is None

        log_destroy()
        clear_log_file(LOG_FILE)

    def test_get_cert_status(self):
        LOG_FILE = 'libcertifier.tests.log'

        cli_setup()
        args = Namespace(config='./tests/cfgs/libcertifier.test.cfg', verbose=False, ca_path=None, command='get-cert-status', mtls_p12_path=None)
        log_setup(args)
        logger.setLevel(1)
        status = XPKI_CLIENT_CERT_STATUS.XPKI_CLIENT_CERT_UNKNOWN
        params = get_cert_validity_param_t('xpki')
        certifier = get_certifier_instance(args, 'xpki')

        xc_get_default_cert_status_param(certifier, params)

        params.input_p12_password = "changeit"
        with open("./src/resources/seed.p12", "r", encoding="utf-8") as p12_filename:
            params.input_p12_path = p12_filename
            status = xc_get_cert_status(certifier, params)

        assert XPKI_CLIENT_CERT_STATUS.XPKI_CLIENT_CERT_VALID == status

        # params.input_p12_password = "about_to_expire"
        # with open("./tests/certs/about_to_expire.p12", "r", encoding="utf-8") as p12_filename:
        #     params.input_p12_path = p12_filename
        #     error, status = xc_get_cert_status(certifier, params, status)

        # assert XPKI_CLIENT_CERT_STATUS.XPKI_CLIENT_CERT_UNKNOWN == status

        ## xPKI Revoked Seed Cert
        # certifier = get_certifier_instance(args, 'xpki')
        # xc_get_default_cert_validity_param(certifier, params)
        # params.input_p12_password = "12345"
        # with open("./tests/certs/seedrevoketest.p12", "r", encoding="utf-8") as p12_filename:
        #     params.input_p12_path = p12_filename
        #     status = xc_get_cert_status(certifier, params, status)

        # assert status == XPKI_CLIENT_CERT_STATUS.XPKI_CLIENT_CERT_REVOKED

        ## xPKI Revoked Operational (non-seed) Cert
        # certifier = get_certifier_instance(args, 'xpki')
        # xc_get_default_cert_validity_param(certifier, params)
        # params.input_p12_password = "12345"
        # with open("./tests/certs/oprevoketest.p12", "r", encoding="utf-8") as p12_filename:
        #     params.p12_path = p12_filename
        #     error, status = xc_get_cert_status(certifier, params, status)

        # assert status == XPKI_CLIENT_CERT_STATUS.XPKI_CLIENT_CERT_REVOKED

        log_destroy()
        clear_log_file(LOG_FILE)
        
    def test_verbose(self):
        LOG_FILE = 'libcertifier.tests.log'

        cli_setup()
        args = Namespace(config='./tests/cfgs/libcertifier.test.cfg', verbose=False, ca_path=None, command='get-cert-status', mtls_p12_path=None)
        log_setup(args)
        status = XPKI_CLIENT_CERT_STATUS.XPKI_CLIENT_CERT_UNKNOWN
        params = get_cert_status_param_t('xpki')

        ## Seed certificate
        certifier = get_certifier_instance(args, 'xpki')
        xc_get_default_cert_status_param(certifier, params)
        params.input_p12_password = "changeit"
        count1 = 0
        print(os.getcwd())
        with open("./src/resources/seed.p12", "r", encoding="utf-8") as p12_filename:
            params.input_p12_path = p12_filename
            xc_get_cert_status(certifier, params)
            
        count1 = len(open(LOG_FILE, 'r').readlines())
            
        args = Namespace(config='./tests/cfgs/libcertifier.test.cfg', verbose=True, ca_path=None, command='get-cert-status', mtls_p12_path=None)

        status = XPKI_CLIENT_CERT_STATUS.XPKI_CLIENT_CERT_UNKNOWN
        params = get_cert_status_param_t('xpki')

        ## Seed certificate
        certifier = get_certifier_instance(args, 'xpki')
        xc_get_default_cert_status_param(certifier, params)
        params.input_p12_password = "changeit"

        with open("./src/resources/seed.p12", "r", encoding="utf-8") as p12_filename:
            params.input_p12_path = p12_filename
            xc_get_cert_status(certifier, params)
            
        count2 = len(open(LOG_FILE, 'r').readlines())
            
        assert count1 < count2

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(Tests('test_expected_log_behavior'))
    suite.addTest(Tests('test_invalid_level'))
    suite.addTest(Tests('test_invalid_message'))
    suite.addTest(Tests('test_log_level'))
    suite.addTest(Tests('test_verbose'))
    suite.addTest(Tests('test_certifier_init'))
    suite.addTest(Tests('test_missing_config_file'))
    suite.addTest(Tests('test_invalid_pkcs12_file'))
    suite.addTest(Tests('test_get_cert_validity'))
    suite.addTest(Tests('test_validity_output_status_dependent'))
    suite.addTest(Tests('test_get_cert_status'))

    runner = unittest.TextTestRunner()
    runner.run(suite)