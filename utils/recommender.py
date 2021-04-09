from models.db import DB

class Recommender:

    @staticmethod
    def get_recommendations(uid, skip, limit):
        g = DB.get_neo4j_connection()
        result = g.run(f'''
            MATCH
            (u1:User{{id:$id}}) -[f1:FOLLOWS]-> (:Tag) <-[f2:FOLLOWS]- (u2:User)
            WITH SUM(f1.score * f2.score) / SQRT(SUM(f1.score * f1.score) * SUM(f2.score * f2.score)) AS sim, u1, u2
            WHERE sim > 0.5
            MATCH (u2) -[f:FOLLOWS]-> (t:Tag)
            WITH t, u1
            WHERE f.score <> 0
            MATCH (t) <-[:HAS_TAG]- (p:Product)
            WHERE NOT (u1)--(p)
            RETURN DISTINCT p AS rec
            UNION
            MATCH (u1:User{{id:$id}}) -[f:FOLLOWS]-> (:Tag) <-[:HAS_TAG]- (p:Product)
            WHERE f.score <> 0 AND NOT (u1)--(p)
            RETURN DISTINCT p AS rec
            SKIP $skip LIMIT $limit
        ''', {
            "id": uid,
            "skip": skip,
            "limit": limit
        })
        data = []
        for record in result:
            row = {}
            for name, value in record[0].items():
                row[name] = value
            data.append(row)
        return data

    @staticmethod
    def increase_user_score(uid, pid):
        g = DB.get_neo4j_connection()
        g.run(f'''
            MATCH (:Product{{id: $pid}}) -[:HAS_TAG]- (t:Tag)
            WITH t
            MATCH (:User{{id: $uid}}) -[f:FOLLOWS]- (t)
            SET f.score = f.score + 1
        ''', {
            "uid": uid,
            "pid": pid
        })

    @staticmethod
    def decrease_user_score(uid, pid):
        g = DB.get_neo4j_connection()
        g.run(f'''
            MATCH (:Product{{id: $pid}}) -[:HAS_TAG]- (t:Tag)
            WITH t
            MATCH (:User{{id: $uid}}) -[f:FOLLOWS]- (t)
            SET f.score = f.score - 1
        ''', {
            "uid": uid,
            "pid": pid
        })

