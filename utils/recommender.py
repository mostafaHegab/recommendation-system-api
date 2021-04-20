from models.db import DB


class Recommender:

    g = DB.get_neo4j_connection()

    @staticmethod
    def process_result(result):
        data = []
        for record in result:
            row = {}
            for name, value in record[0].items():
                row[name] = value
            row['rating'] = row['pscore'] / (row['pscore']+row['nscore']+1) * 5
            data.append(row)
        data.sort(key=lambda i: i['pscore'] / (i['pscore']+i['nscore']+1),
                  reverse=True)
        return data

    @staticmethod
    def content_based(uid, skip, limit):
        result = Recommender.g.run(f'''
            MATCH (u:User{{id:$id}}) -[f:FOLLOWS]-> (:Tag) <-[:HAS_TAG]- (p:Product) WITH f,p ORDER BY f.score DESC RETURN DISTINCT p
            SKIP $skip LIMIT $limit
        ''', {
            "id": uid,
            "skip": skip,
            "limit": limit
        })
        return Recommender.process_result(result)

    @staticmethod
    def collaborative(uid, skip, limit):
        result = Recommender.g.run(f'''
            MATCH (u1:User{{id:$id}}) -[f1:FOLLOWS]-> (:Tag) <-[f2:FOLLOWS]- (u2:User)
            WITH SUM(f1.score * f2.score) / SQRT(SUM(f1.score * f1.score) * SUM(f2.score * f2.score)) AS sim, u1, u2
            WITH u1, COLLECT(u2)[0..10] AS kneighbours
            MATCH (p:Product) <-[r:REACT]- (u:User)
            WHERE u IN kneighbours 
            RETURN DISTINCT p AS rec
            SKIP $skip LIMIT $limit
        ''', {
            "id": uid,
            "skip": skip,
            "limit": limit
        })
        return Recommender.process_result(result)

    @staticmethod
    def hybrid(uid, skip, limit):
        r1 = Recommender.content_based(uid, skip, limit)
        r2 = Recommender.collaborative(uid, skip, limit)
        r = list({x['id']: x for x in r1 + r2}.values())
        return r
    
    @staticmethod
    def get_similar_product(pid, skip, limit):
        result = Recommender.g.run(f'''
            MATCH (:Product{{id: $id}}) -[:HAS_TAG]- (t:Tag)-[:HAS_TAG]-(p:Product) return p
            SKIP $skip LIMIT $limit
        ''', {
            "id": pid,
            "skip": skip,
            "limit": limit
        })
        return Recommender.process_result(result)

    @staticmethod
    def increase_score(uid, pid):
        g = DB.get_neo4j_connection()
        g.run(f'''
            MATCH (:Product{{id: $pid}}) -[:HAS_TAG]- (t:Tag)
            WITH t
            MATCH (:User{{id: $uid}}) -[f:FOLLOWS]- (t)
            SET f.score = f.score + 1
            UNION
            MATCH (p:Product{{id: $pid}})
            SET p.pscore = p.pscore + 1
            UNION
            MATCH (u:User{{id: $uid}}) -[r:REACT]- (p:Product{{id: $pid}})
            SET r.score = r.score + 1
        ''', {
            "uid": uid,
            "pid": pid
        })

    @staticmethod
    def decrease_score(uid, pid):
        g = DB.get_neo4j_connection()
        g.run(f'''
            MATCH (:Product{{id: $pid}}) -[:HAS_TAG]- (t:Tag)
            WITH t
            MATCH (:User{{id: $uid}}) -[f:FOLLOWS]- (t)
            SET f.score = f.score - 1
            UNION
            MATCH (p:Product{{id: $pid}})
            SET p.nscore = p.nscore + 1
            UNION
            MATCH (u:User{{id: $uid}}) -[r:REACT]- (p:Product{{id: $pid}})
            SET r.score = r.score - 1
        ''', {
            "uid": uid,
            "pid": pid
        })

    @staticmethod
    def create_relation(uid, pid):
        g = DB.get_neo4j_connection()
        g.run(f'''
            MATCH (p:Product{{id: $pid}}), (u:User{{id: $uid}})
            MERGE (u) -[r:REACT]- (p)
            ON CREATE SET r.score = 1
        ''', {
            "uid": uid,
            "pid": pid
        })


'''
MATCH
(u1:User{id:36771878181752}) -[f1:REACT]-> (:Product) <-[f2:REACT]- (u2:User)
WITH SUM(f1.score * f2.score) / SQRT(SUM(f1.score * f1.score) * SUM(f2.score * f2.score)) AS sim, u1, u2, f2
WHERE sim > 0.5
WITH sim, u1
MATCH (u2) -[f:REACT]-> (p:Product)
WHERE NOT (u1)--(p)
ORDER BY sim DESC, f.score DESC
RETURN DISTINCT p AS rec
SKIP 0 LIMIT 10
'''
