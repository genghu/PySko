import tornado.escape

import pymongo

import SSA

import tornado.web

class SSAAll(tornado.web.RequestHandler):
    def initialize(self):
        self.connection = pymongo.connection.Connection()
        self.db = self.connection.dsspp

    def get(self):
        self.query()

    def post(self):
        self.query()

    def query(self):
        # this MUST be rewritten after the demo!
        json = tornado.escape.json_decode(self.get_argument('json'))

        domain = json['domain']

        try:
            text = json['text']
        except KeyError:
            text = ''

        if len(text) > 0:
            ssa = SSA.SSA(
                _text = json['text'],
                _domain = domain,
                _space = json['SS'],
                _columnType = json['type'],
                _minAssoc = json['minStrength'],
                _minWeight = json['minWeight'],
                _minRankby = json['minRankby'],
                _wc = json['wc'],
            )
            score = tornado.escape.json_decode(ssa.query())[domain]
            row = {
                'category':json['category'],
                'domain':domain,
                'ma':json['minStrength'],
                'mr':json['minRankby'],
                'mw':json['minWeight'],
                'space':json['SS'],
                'columnType':json['type'],
                'wc':json['wc']
            }

            cursor = self.db.ssahistory.find_one(row);

            if cursor is None:
                row['frequency'] = 1
                row['sum'] = score
                row['sumOfSquares'] = score ** 2

                cursor = row

                self.db.ssahistory.insert(row)
            else:
                freq = cursor['frequency']
                _sum = cursor['sum']
                _sumOfSquares = cursor['sumOfSquares']

                cursor['frequency'] = freq + 1
                cursor['sum'] = _sum + score
                cursor['sumOfSquares'] = _sumOfSquares + (score ** 2)

                self.db.ssahistory.update(row, cursor)
        else:
        
            row = {
                'category':json['category'],
                'domain':domain,
                'ma':json['minStrength'],
                'mr':json['minRankby'],
                'mw':json['minWeight'],
                'space':json['SS'],
                'columnType':json['type'],
                'wc':json['wc']
            }

            #print row

            cursor = self.db.ssahistory.find_one(row);

            if cursor is None:
                cursor = {
                    'sum':0,
                    'sumOfSquares':0,
                    'frequency':0,
                    'domain':domain,
                    'space':json['SS']
                }
        
        self.write(tornado.escape.json_encode({
            'sum':cursor['sum'],
            'sqr':cursor['sumOfSquares'],
            'n':cursor['frequency'],
            'domain':cursor['domain'],
            'space':cursor['space']
        }))


