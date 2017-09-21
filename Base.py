import tornado.escape

import re

import pymongo

from pymongo import MongoClient

import WorkerBee

class Base():
    def __init__(
        self,
        text = '',
        cosine = 0.0,
        weight = 0.0,
        etop = 500,
        ttop = 500,
        format = 'xml',
        domain = 'combineall',
        space = 'tasalsa',
        sort_method = 0,
        wc = 0.0,
        pretty=False,
        notes = '',
        rankby = 0.0):
        self.text = text
        self.cosine = cosine
        self.weight = weight
        self.etop = etop
        self.ttop = ttop
        self.format = format
        self.domain = domain.lower()
        self.space = space
        self.sort_method = [
            self.neighbor_compare_rankby,
            self.neighbor_compare_cosine,
            self.neighbor_compare_weight
        ][sort_method]
        self.wc = wc
        self.sort_methods = []
        self.quoted_pieces = [i for i in self.getText().lower().split(' ') if len(i) > 0]
        self.pretty = pretty
        self.notes = notes
        self.rankby = rankby

        #self.connection = pymongo.connection.Connection()
        #self.db = self.connection.dsspp

	self.client = MongoClient()
	self.db = client.dsspp

    def getText(self):
        remove_non_alphanum = re.compile('[^A-Za-z0-9\\s]+')
        remove_cr_lf = re.compile('[\t\r\n]')
        _text = self.text
        _text = remove_non_alphanum.subn('', _text)[0]
        _text = remove_cr_lf.subn(' ', _text)[0]
        
        return _text

    def neighbor_compare_rankby(self, a, b):
        f = float(a['rankby']) - float(b['rankby'])
        if f < 0: return -1
        if f > 0: return 1
        return 0

    def neighbor_compare_cosine(self, a, b):
        f = float(a['cosine']) - float(b['cosine'])
        if f < 0: return -1
        if f > 0: return 1
        return 0

    def neighbor_compare_weight(self, a, b):
        f = float(a['weight']) - float(b['weight'])
        if f < 0: return -1
        if f > 0: return 1
        return 0

    def export(self, query, message_id, pretty=False):
        if self.format == 'xml':
            xml = '<list>'
            if pretty == True:
                    xml += '\n'
            for row in query:
                xml += '<TERM WEIGHT="%s" AT="%s" RANK="%s" STR="%s">%s</TERM>' % (row['weight'], row['cosine'], row['rankby'], row['neighbor'], row['neighbor'])
                if pretty == True:
                    xml += '\n'
            if message_id is not None:
                xml += '<MESSAGE_ID MID="%s"/>' % message_id
            xml += '</list>'
            return xml
        if self.format == 'json':
            json = '{"list":['
            if len(query) > 0:
                for row in query:
                    json += '{"wt":"%s", "at":"%s", "rankby":"%s", "term":"%s"},' % (row['weight'], row['cosine'], row['rankby'], row['neighbor'])
                    if pretty == True:
                        json += '\n'
                json = json[:len(json)-1]
            json += ']'
            if message_id is not None:
                json += ', message_id:"%s"' % message_id
            json += '}'
            return json

    def get_all_neighbors(self, lsa_neighbors):
        rv = []
        for n in lsa_neighbors:
            neighbors = tornado.escape.json_decode(n['neighbors'])
            for j in neighbors:
                rv.append({
                    'weight': j['weight'],
                    'cosine': j['cosine'],
                    'rankby': j['rankby'],
                    'neighbor': j['neighbor']
                })
        return rv

    def update_word_weight(self, neighbor):
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
        return neighbor

    def query(self):
        rows_in_domain = []
        terms_in_datastore = []
        terms_not_in_datastore = []

        all_neighbors = []
        groups = {}

        for term in self.quoted_pieces:
            row = self.db.lsaneighbors.find_one({'domain': self.domain, 'word': term, 'space': self.space})
            if row is not None:
                updated_neighbor = self.update_word_weight(row)
                if updated_neighbor['word_weight'] >= self.wc:
                    if self.etop > 0 or self.ttop > 0:
                        local_neighbors = tornado.escape.json_decode(updated_neighbor['neighbors'])
                        local_neighbors_n = [n for n in local_neighbors if n['cosine'] > self.cosine and n['weight'] > self.weight and n['rankby'] > self.rankby]
                        local_neighbors_etop = sorted(local_neighbors_n, cmp=self.sort_method, reverse=True)[:self.etop]
                        all_neighbors.extend(local_neighbors_etop)
                    else:
                        all_neighbors.append(updated_neighbor)
            else:
                terms_not_in_datastore.append(term)

        if self.etop > 0 or self.ttop > 0:
            lsaquery_results = sorted(all_neighbors, cmp=self.sort_method, reverse=True)[:self.ttop]
        else:
            lsaquery_results = self.get_all_neighbors(all_neighbors)

        for term in terms_not_in_datastore:
            worker = WorkerBee.WorkerBee(term, self.space, self.domain)

        return self.export(lsaquery_results, None, self.pretty)

if __name__ == '__main__':
    import sys
    _text = sys.argv[1]
#    logfile = open('C:/atlbase.log', 'a')
#    print >> logfile, 'parsing: \n%s' % (_text)
    w = Base(text=_text, space='fa', domain='science_and_mathematics', pretty=True)
#    print >> logfile, 
    w.query()
#    logfile.close()
