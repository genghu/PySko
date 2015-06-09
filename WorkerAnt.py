#worker ant looks for the 'nodomain'/term/space combo in the database and puts it there if it is not

import pymongo

import tornado.escape

class WorkerAnt():
    def __init__(self, term, space):
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
            row = self.db.lsaneighbors.find_one({
                'word': self.term, 
                'space': self.space, 
                'domain':'nodomain', 
                'pending': True
            })
            if row is None:
                lsaneighbor = {
                    'word': self.term,
                    'space': self.space,
                    'domain': 'nodomain',
                    'pending': True,
                    'neighbors': tornado.escape.json_encode([]),
                    'total_assn': 0.0,
                    'total_rankby': 0.0,
                    'total_weight': 0.0
                }

                self.db.lsaneighbors.insert(lsaneighbor)
            
            neighbors = []

            docs = self.db.space_fa.find({'term1': self.term})

            for doc in docs:
                neighbor = {
                    'cosine': doc['cosine'],
                    'weight': doc['weight'],
                    'rankby': doc['cosine'] * doc['weight'],
                    'neighbor': doc['term2'],
                    'dotprod': 0.0
                }
                neighbors.append(neighbor)

            _row = self.db.lsaneighbors.find_one({
                'word': self.term,
                'space': self.space,
                'domain': 'nodomain'
            })

            _row['pending'] = False
            _row['neighbors'] = tornado.escape.json_encode(neighbors)

            word_weight = 0.0

            for n in neighbors:
                _row['total_assn'] += n['cosine']
                _row['total_rankby'] += n['rankby']
                _row['total_weight'] += n['weight']
                if n['neighbor'] == self.term:
                    word_weight = n['weight']

            _row['word_weight'] = word_weight

            self.db.lsaneighbors.update({
                'word': self.term,
                'space': self.space,
                'domain': 'nodomain'
            }, _row)
