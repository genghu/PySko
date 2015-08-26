#worker ant looks for the 'nodomain'/term/space combo in the database and puts it there if it is not

import pymongo

import tornado.escape

class WorkerAnt():
    def __init__(self, term, space):
        #self.logfile = open('C:/atlworkerant2.log', 'a')
        #print >> self.logfile, 'WorkerAnt: space: %s | term: %s' % (space, term)

        self.term = term
        self.space = space
        self.connection = pymongo.connection.Connection()
        self.db = self.connection.dsspp

    def query(self):
        row = self.db.lsaneighbors.find_one({
            'word': self.term, 
            'space': self.space, 
            'domain':'nodomain', 
            'pending': False
        })
        if row is None:
            #print >> self.logfile, 'WorkerAnt: term: %s | space: %s | domain: nodomain does not exist' % (self.term, self.space)
            lsaneighbor = {
                'word': self.term,
                'space': self.space,
                'domain': 'nodomain',
                'pending': False,
                'neighbors': tornado.escape.json_encode([]),
                'total_assn': 0.0,
                'total_rankby': 0.0,
                'total_weight': 0.0
            }

            
            neighbors = []

            docs = self.db.space_fa.find({'term1': self.term})

            #print >> self.logfile, 'WorkerAnt found %d neighbors for %s' % (docs.count(), self.term)

            for doc in docs:
                neighbor = {
                    'cosine': doc['cosine'],
                    'weight': doc['weight'],
                    'rankby': doc['cosine'] * doc['weight'],
                    'neighbor': doc['term2'],
                    'dotprod': 0.0
                }
                neighbors.append(neighbor)

            lsaneighbor['neighbors'] = tornado.escape.json_encode(neighbors)

            word_weight = 0.0

            for n in neighbors:
                lsaneighbor['total_assn'] += n['cosine']
                lsaneighbor['total_rankby'] += n['rankby']
                lsaneighbor['total_weight'] += n['weight']
                if n['neighbor'] == self.term:
                    word_weight = n['weight']

            lsaneighbor['word_weight'] = word_weight

            self.db.lsaneighbors.insert(lsaneighbor)

            return lsaneighbor
