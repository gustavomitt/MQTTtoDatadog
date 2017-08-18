import unittest
import json
import time
import random

from mqtt import get_datalog_metric,setup_datalog,set_datalog_metric

def pp_json(json_thing, sort=True, indents=4):
    if type(json_thing) is str:
        print(json.dumps(json.loads(json_thing), sort_keys=sort, indent=indents))
    else:
        print(json.dumps(json_thing, sort_keys=sort, indent=indents))
    return None

class Tests(unittest.TestCase):
    def setUp(self):
        setup_datalog()



    def test_datalog_set_metric(self):
        now = int(time.time())
        value = random.uniform(10000.0, 20000.0 )
        status = set_datalog_metric('test_metric',now,value,'humidity_sensor')
        #print('test_datalog_set_metric:')
        #print("set metric: ")
        #pp_json(status)
        self.assertEqual(status['status'],'ok')
        time.sleep(30)
        query = 'test_metric{*}'
        now = int(time.time())
        response = get_datalog_metric(now - 600,now,query)
        #print("get metric: ")
        #pp_json(response)
        achou = False
        for resp in response['series'][0]['pointlist']:
            print "Response: ", resp[1] ," Value: ", value, " Abs: ", abs(resp[1] - value) < 0.1
            if abs(resp[1] - value) < 1.0:
                achou = True
        self.assertEqual(response['status'],'ok')
        self.assertEqual(response['res_type'],'time_series')
        self.assertNotEqual(response['series'],'[]')
        self.assertEqual(response['series'][0]['metric'],'test_metric')
        self.assertTrue(achou)


if __name__ == '__main__':
    unittest.main()
