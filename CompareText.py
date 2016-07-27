import tornado.web
import tornado.escape

import pymongo

import Base



import math

import datetime



class CompareText(tornado.web.RequestHandler):
    def initialize(self):
        self.connection = pymongo.connection.Connection()
        self.db = self.connection.dsspp

        self.jsonObject = None
    
    def getSortMethod(self):
        _sortMethod = 0
        try:
            _sortMethod = self.jsonObject['sort_method']
            logging.info("%s" % (str(_sortMethod)))
        except KeyError:
            pass
        
        return _sortMethod
    
    def getText1(self):
        _text = ''
        try:
            _text = self.jsonObject['text1']
        except KeyError:
            pass
        
        return _text
    
    def getText2(self):
        _text = ''
        try:
            _text = self.jsonObject['text2']
        except KeyError:
            pass
        
        return _text
    
    def getCosine(self):
        _cosine = 0.0
        try:
            _cosine = self.jsonObject['minStrength']
        except KeyError:
            pass
        
        return _cosine
    
    def getWeight(self):
        _weight = 0.0
        try:
            _weight = self.jsonObject['minWeight']
        except KeyError:
            pass
        
        return _weight
    
    def getEtop(self):
        _etop = 5
        try:
            _etop = self.jsonObject['etop']
        except KeyError:
            pass
        
        return _etop
    
    def getTtop(self):
        _ttop = 5
        try:
            _ttop = self.jsonObject['ttop']
        except KeyError:
            pass
        
        return _ttop
    
    def getFormat(self):
        _format = 'xml'
        try:
            _format = self.jsonObject['format']
        except KeyError:
            pass
        
        return _format
    
    def getDomain(self):
        _domain = 'combineall'
        try:
            _domain = self.jsonObject['domain'].lower()
        except KeyError:
            pass
        
        return _domain
    
    def getSpace(self):
        _space = 'tasalsa'
        try:
            _space = self.jsonObject['SS']
        except KeyError:
            pass
        
        return _space
    
    def getId1(self):
        _id1 = ''
        try:
            _id1 = self.jsonObject['id1']
        except KeyError:
            pass
        
        return _id1
    
    def getId2(self):
        _id2 = ''
        try:
            _id2 = self.jsonObject['id2']
        except KeyError:
            pass
        
        return _id2
    
    def getNotes(self):
        _notes = ''
        try:
            _notes = self.jsonObject['notes']
        except KeyError:
            pass
        
        return _notes
    
    def compute_aggregate(self, l):
        rankbys = {}
        for word in l:
            try:
                q = rankbys.keys().index(word['term'])
            except ValueError, e:
                rankbys[word['term']] = 0
            rankbys[word['term']] += float(word['rankby'])
        return rankbys
    
    def getWC(self):
        _wc = 0.0
        
        try:
            _wc = self.jsonObject['wc']
        except KeyError:
            pass
        
        return _wc
    
    def getRankby(self):
        _rankby = 0.0
        
        try:
            _rankby = self.jsonObject['minRankby']
        except KeyError:
            pass
        
        return _rankby
    
    def get(self):
        self.handle_request()
        
    def post(self):
        self.handle_request()
        
    def handle_request(self):
        json = self.get_argument('json', None)
        self.jsonObject = tornado.escape.json_decode(json)
        
        text1 = self.getText1()
        text2 = self.getText2()
        cosine = self.getCosine()
        weight = self.getWeight();
        etop = self.getEtop();
        ttop = self.getTtop();
        format = self.getFormat();
        domain = self.getDomain();
        space = self.getSpace();
        id1 = self.getId1();
        id2 = self.getId2();
        notes = self.getNotes()
        wc = self.getWC()
        sortMethod = int(self.getSortMethod())
        rankby = self.getRankby()
        
        string_query1 = Base.Base(
            text = text1, 
            cosine = cosine, 
            weight = weight, 
            rankby = rankby, 
            etop = etop, 
            ttop = ttop, 
            format = 'json', 
            domain = domain, 
            space = space, 
            sort_method = sortMethod, 
            wc = wc)
        string_query2 = Base.Base(
            text = text2, 
            cosine = cosine, 
            weight = weight, 
            rankby = rankby, 
            etop = etop, 
            ttop = ttop, 
            format = 'json', 
            domain = domain, 
            space = space, 
            sort_method = sortMethod, 
            wc = wc)
        
        json1 = string_query1.query()
        json2 = string_query2.query()
        
        n1 = tornado.escape.json_decode(json1)
        n2 = tornado.escape.json_decode(json2)
        
#        logfile = open('C:/atlcompare.log', 'a')
#        print >> logfile, n1
#        print >> logfile, n2
#        logfile.close()
        n1_aggregate = self.compute_aggregate(n1['list'])
        n2_aggregate = self.compute_aggregate(n2['list'])
        
        if len(n1_aggregate) > 0:       
        
            dotproduct = 0
            intersection = {}
            
            for w in n2_aggregate.keys():
                for n in n1_aggregate.keys():
                    if n == w:
                        intersection[n] = n1_aggregate[n]
                        dotproduct += n2_aggregate[w] * n1_aggregate[n]
                        break;
                    
            sum_input1 = sum([n1_aggregate[n]**2 for n in n1_aggregate.keys()])
            sum_input2 = sum([n2_aggregate[n]**2 for n in n2_aggregate.keys()])
            
            score = 0.0
            
            try:
                score = str(dotproduct/(math.sqrt(sum_input1) * math.sqrt(sum_input2)))
            except ZeroDivisionError:
                pass
        
            json_out = {'score':score, 'id1':id1, 'id2':id2, 'notes':notes}
            
        else:
            json_out = {'id1':id1, 'id2':id2}
        
        self.write(tornado.escape.json_encode(json_out))
        
        
