import pymongo

import tornado.escape

import WorkerAnt2

class DSNeighbor:
    def __init__(self, neighbor, weight=0.0, dotprod=0.0, cosine=0.0, rankby=0.0):
        self.neighbor = neighbor
        self.weight = weight
        self.dotprod = dotprod
        self.cosine = cosine
        self.rankby = rankby
        
    def __hash__(self):
        return self.neighbor.__hash__()
        
    def __eq__(self, other):
        return self.neighbor == other.neighbor
    
    def __ne__(self, other):
        return self.neighbor <> other.neighbor
    
    def __le__(self, other):
        return self.neighbor <= other.neighbor
    
    def __ge__(self, other):
        return self.neighbor >= other.neighbor
    
    def __lt__(self, other):
        return self.neighbor < other.neighbor
    
    def __gt__(self, other):
        return self.neighbor > other.neighbor
        
class WorkerBee():
    def __init__(self, term, space, domain):
        #logfile = open('C:/atlworkerbee.log', 'a')
        #print >> logfile, 'WorkerBee: term: %s | space: %s | domain: %s' % (term, space, domain)

        self.term = term
        self.space = space
        self.domain = domain

        self.connection = pymongo.connection.Connection()
        self.db = self.connection.dsspp

        # look for existing domain/space/term result in database
        row = self.db.lsaneighbors.find_one({'word': self.term, 'space': self.space, 'domain': self.domain})
        if row is None:
            #print >> logfile, 'WorkerBee: term: %s | space: %s | domain: %s does not exist' % (self.term, self.space, self.domain) 
            # look for word/space/'nodomain in the database'
            nd_row = self.db.lsaneighbors.find_one({'word': self.term, 'space': self.space, 'domain':'nodomain'})
            if nd_row is not None:
                self.f2(nd_row)
            else:
                worker = WorkerAnt2.WorkerAnt(self.term, self.space)
                worker.query()
        else:
            pass

    def f2(self, nd_row):
        if nd_row['pending'] == False:
            neighbors_in_domain = []
            if self.domain == 'nodomain':
                pass #do nothing
            else:
                lsaneighbor = {
                    'word': self.term,
                    'space': self.space,
                    'domain': self.domain.lower(),
                    'neighbors': tornado.escape.json_encode([]),
                    'pending': True,
                    'total_assn': 0.0,
                    'total_rankby': 0.0,
                    'total_weight': 0.0
                }

                self.db.lsaneighbors.insert(lsaneighbor)

                neighbors_in_nd_row = tornado.escape.json_decode(nd_row['neighbors'])

                nodomain = []

                for n in neighbors_in_nd_row:
                    nodomain.append(DSNeighbor(n['neighbor'], n['weight'], n['dotprod'], n['cosine'], n['rankby']))

                neighbors_in_nd_row_set = set(nodomain)
                domainterm = []

                domain_from_ds = self.db.domain.find({'domain': self.domain.lower()})
                for r in domain_from_ds:
                    domainterm.append(DSNeighbor(r['term']))

                domainterm_set = set(domainterm)

                intersect = neighbors_in_nd_row_set.intersection(domainterm_set)

                updated_row = self.db.lsaneighbors.find_one({
                    'word': self.term,
                    'space': self.space,
                    'domain': self.domain.lower()
                })

                word_weight = 0.0
                ds_neighbors = []
                for i in intersect:
                    ds_n = {
                        'cosine': i.cosine,
                        'rankby': i.rankby,
                        'neighbor': i.neighbor,
                        'dotprod': i.dotprod,
                        'weight': i.weight
                    }
                    ds_neighbors.append(ds_n)

                updated_row['neighbors'] = tornado.escape.json_encode(ds_neighbors)
                updated_row['pending'] = False

                for i in intersect:
                    updated_row['total_assn'] += i.cosine
                    updated_row['total_rankby'] += i.rankby
                    updated_row['total_weight'] += i.weight

                ndn = self.db.lsaneighbors.find_one({'word': updated_row['word'], 'space': updated_row['space'], 'domain':'nodomain'})
                for f in tornado.escape.json_decode(ndn['neighbors']):
                    if f['neighbor'] == updated_row['word']:
                        word_weight = f['weight']
                        break

                updated_row['word_weight'] = word_weight

                self.db.lsaneighbors.update({
                    'word': self.term,
                    'space': self.space,
                    'domain': self.domain.lower()
                }, updated_row)
        else:
            pass
