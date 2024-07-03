from database.DB_connect import DBConnect
from model.genere import Genere
from model.track import Track


class DAO():

    @staticmethod
    def getGeneri():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select *
                from genre g
                order by Name"""
        cursor.execute(query, )
        for row in cursor:
            result.append(Genere(row['GenreId'],
                           row['Name']))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getNodes(genere):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select TrackId, Name, AlbumId, MediaTypeId, GenreId, Milliseconds, Bytes
                    from track t 
                    where GenreId = %s"""
        cursor.execute(query, (genere,))
        for row in cursor:
            result.append(Track(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getEdge(genere, idMap):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select t1.TrackId as tk1, t2.TrackId as tk2, t1.Milliseconds as d1, t2.Milliseconds as d2
                    from (select * 
                            from track t 
                            where GenreId = %s)t1,
                        (select * 
                            from track t 
                            where GenreId = %s) t2
                    where t1.MediaTypeId = t2.MediaTypeId and t1.TrackId <t2.TrackId"""
        cursor.execute(query, (genere, genere,))
        for row in cursor:
            result.append((idMap[row['tk1']],
                           idMap[row['tk2']],
                           row['d1'],
                           row['d2']))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getRimanenti(genere, tipo):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select TrackId, Name, AlbumId, MediaTypeId, GenreId, Milliseconds, Bytes
                    from track t 
                    where t.GenreId = %s and t.MediaTypeId = %s"""
        cursor.execute(query, (genere, tipo,))
        for row in cursor:
            result.append(Track(**row))

        cursor.close()
        conn.close()
        return result
