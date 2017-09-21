import tornado.escape 

import re

import pymongo

from pymongo import MongoClient

import WorkerBee

class SSA():
    def __init__(self, 
             _text = '', 
             _domains = [], 
             _space = '', 
             _columnType = 0, 
             _minAssoc = 0.0, 
             _minWeight = 0.0, 
             _minRankby = 0.0, 
             _wc = 0.0,
             _category = 'general'):
        #self.connection = pymongo.connection.Connection()
        #self.db = self.connection.dsspp
	self.client = MongoClient()
	self.db = client.dsspp

        self.text = _text
        self.domains = _domains
        self.space = _space
        self.columnType = _columnType
        self.minAssoc = _minAssoc
        self.minWeight = _minWeight
        self.minRankby = _minRankby
        self.wc = _wc
        self.category = _category
#        self.logfile = open('C:/atlssa.log', 'a')
#        print >> self.logfile, 'SSA'

    def getText(self):
        remove_non_alphanum = re.compile('[^A-Za-z0-9\\s]+')
        remove_cr_lf = re.compile('[\t\r\n]')
        text = self.text
        text = remove_non_alphanum.subn('', text)[0]
        text = remove_cr_lf.subn(' ', text)[0]
        
        return text

    def update_word_weight(self, neighbor):
#        print >> self.logfile, 'update_word_weight'
#        print >> self.logfile, neighbor
        if neighbor['word_weight'] >= 0:
            pass
        else:
            ndn = self.db.lsaneighbors.find_one({'word': neighbor['word'], 'space': neighbor['space'], 'domain':'nodomain'})
            for n in tornado.escape.json_decode(ndn['neighbors']):
                if n['neighbor'] == neighbor['word']:
                    neighbor['word_weight'] = n['weight']
                    self.db.lsaneighbor.update({
                        'domain': neighbor['domain'],
                        'word': neighbor['word'],
                        'space': neighbor['space']
                    }, neighbor)
                    break
        return neighbor

    def get_column_total(self, neighbor):
        local_neighbors = tornado.escape.json_decode(neighbor['neighbors'])
        local_column_total = 0
        for n in local_neighbors:
            if n['cosine'] >= self.minAssoc and n['rankby'] >= self.minRankby and n['weight'] >= self.minWeight:
                if self.columnType == 1:
                    local_column_total = local_column_total + n['cosine']
                elif self.columnType == 2:
                    local_column_total = local_column_total + n['rankby']
                else:
                    local_column_total = local_column_total + n['weight']
        return local_column_total

    def ssahistory(self, domain, score):
        row = {
            'category':self.category,
            'domain':domain,
            'ma':self.minAssoc,
            'mr':self.minRankby,
            'mw':self.minWeight,
            'space':self.space,
            'columnType':self.columnType,
            'wc':self.wc
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
    
    def query(self):
        totals = {}
        for domain in self.domains:
            totals[domain] = 0.0

            for word in self.getText().lower().split(' '):
                if len(word.strip()) > 0:
                    neighbor_in_datastore = self.db.lsaneighbors.find_one({
                        'word': word,
                        'domain': domain,
                        'space': self.space
                    })
                    if neighbor_in_datastore is not None:
                        neighbor = self.update_word_weight(neighbor_in_datastore)
                        if neighbor['word_weight'] > float(self.wc):
                            column_total = self.get_column_total(neighbor)
                            if column_total is None:
                                column_total = 0.0
#                            print >> self.logfile, totals
#                            print >> self.logfile, 'column_total: %.6f word: %s domain: %s' % (column_total, word, domain)
                            totals[domain] += column_total
                    else:
                        worker = WorkerBee.WorkerBee(word, self.space, domain)
        for key in totals.keys():
            totals[key] = float("%.6f" % (totals[key]))
            self.ssahistory(key, totals[key])

        return totals
