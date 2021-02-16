from flask import Flask
from flask_restful import Api , Resource , reqparse , abort ,marshal_with ,fields,request
from flask_sqlalchemy import SQLAlchemy
import json
from json import JSONEncoder

import datetime

app = Flask(__name__)
api  = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///audio.db'  #DB file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    
db = SQLAlchemy(app)


# Using SQL Alchemy as ORM to create DB tables and other operation on it

class Song(db.Model):
    ID = db.Column(db.Integer,primary_key = True)
    Song_Name = db.Column(db.String(100),nullable=False)
    Duration = db.Column(db.Integer, nullable=False)
    Uploaded_time = db.Column(db.DateTime, nullable = False, default = datetime.datetime.now())
    def __init__(self,ID,Song_Name,Duration,Uploaded_time):
        self.ID = ID
        self.Song_Name = Song_Name
        self.Duration = Duration
        self.Uploaded_time = Uploaded_time


song_pargs = reqparse.RequestParser()
song_pargs.add_argument("Song_Name",type=str,required=True)
song_pargs.add_argument("Duration",type=int,required=True)
song_pargs.add_argument("Uploaded_time",type=datetime.date,required=True)

SongFileds = {
 'ID' : fields.Integer,
 'Song_Name' : fields.String,
 'Duration' : fields.Integer,
 'Uploaded_time' : fields.DateTime

}

class Podcast(db.Model):
    ID = db.Column(db.Integer,primary_key = True)
    Name = db.Column(db.String(100),nullable=False)
    Duration = db.Column(db.Integer, nullable=False)
    Uploaded_time = db.Column(db.DateTime, nullable = False, default = datetime.datetime.now())
    Host = db.Column(db.String(100),nullable=False)
    Participants = db.Column(db.String(10000))
    
    def __init__(self,ID,Name,Duration,Uploaded_time,Host,Participants):
        self.ID = ID
        self.Name = Name
        self.Duration = Duration
        self.Uploaded_time = Uploaded_time
        self.Host = Host
        self.Participants = Participants
    



Podcast_pargs = reqparse.RequestParser()
Podcast_pargs.add_argument("Name",type=str,required=True)
Podcast_pargs.add_argument("Duration",type=int,required=True)
Podcast_pargs.add_argument("Uploaded_time",type=datetime.date,required=True)
Podcast_pargs.add_argument("Host",type=str,required=True)
Podcast_pargs.add_argument("Participants",type=str)


podcastFileds = {
 'ID' : fields.Integer,
 'Name' : fields.String,
 'Duration' : fields.Integer,
 'Uploaded_time' : fields.DateTime,
 'Host' : fields.String,
 'Participants' : fields.String

}

class Audiobook(db.Model):
    ID = db.Column(db.Integer,primary_key = True)
    Title = db.Column(db.String(100),nullable=False)
    Author = db.Column(db.String(100),nullable=False)
    Narrator = db.Column(db.String(100),nullable=False)
    Duration = db.Column(db.Integer, nullable=False)
    Uploaded_time = db.Column(db.DateTime, nullable = False, default = datetime.datetime.now())

    
    def __init__(self,ID,Title,Author,Narrator,Duration,Uploaded_time):
        self.ID = ID
        self.Title = Title
        self.Author = Author
        self.Narrator = Narrator
        self.Duration = Duration
        self.Uploaded_time = Uploaded_time
 
    


Audiobook_pargs = reqparse.RequestParser()
Audiobook_pargs.add_argument("Title",type=str,required=True)
Audiobook_pargs.add_argument("Author",type=str,required=True)
Audiobook_pargs.add_argument("Narrator",type=str,required=True)
Audiobook_pargs.add_argument("Duration",type=int,required=True)
Audiobook_pargs.add_argument("Uploaded_time",type=datetime.date,required=True)


AudiobookFileds = {
 'ID' : fields.Integer,
 'Title' : fields.String,
 'Narrator' : fields.String,
 'Author' : fields.String,
 'Duration' : fields.Integer,
 'Uploaded_time' : fields.DateTime
}


from sqlalchemy.ext.declarative import DeclarativeMeta

class AlchemyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata' and 'query' not  in x]:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)
                    fields[field] = data
                except TypeError:
                    if field == 'Uploaded_time':
                        fields[field] = data = json.dumps(str(obj.__getattribute__(field)))
                    else:    
                        fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)



class Audio(Resource):   
        
    
    def get(self,audioFileType,audioFileID): #For GetEndpoint
        if audioFileType == 'Song':
            result = Song.query.filter_by(ID=audioFileID).first()
            #res = MyEncoder().encode(result)
        elif audioFileType == 'Podcast':
            result = Podcast.query.filter_by(ID=audioFileID).first()
        elif audioFileType == 'Audiobook':
            result = Audiobook.query.filter_by(ID=audioFileID).first()
        else:
            pass
        if not result:
            return "Audio file not found",400
        else:
            return json.dumps(result, cls=AlchemyEncoder),200
            
    def post(self,audioFileType,audioFileID):    #For create end point
        
        
        if audioFileType == 'Song':
            result = Song.query.filter_by(ID=audioFileID).first()
            #res = MyEncoder().encode(result)
        elif audioFileType == 'Podcast':
            result = Podcast.query.filter_by(ID=audioFileID).first()
        elif audioFileType == 'Audiobook':
            result = Audiobook.query.filter_by(ID=audioFileID).first()
        else:
            pass
        if result:
            return "Audio ID already taken",400
        else:
            if audioFileType == 'Song':
                args = request.get_json()
                Uploaded_time = args['Uploaded_time']
                print(Uploaded_time)
                Uploaded_time1 = datetime.datetime.strptime(Uploaded_time, '%m/%d/%y %H:%M:%S')
                audio = Song(ID=audioFileID,Song_Name=args['Song_Name'],Duration=args['Duration'],Uploaded_time=Uploaded_time1)
            #res = MyEncoder().encode(result)
            elif audioFileType == 'Podcast':
                args = request.get_json()
                Uploaded_time = args['Uploaded_time']
                print(Uploaded_time)
                Uploaded_time1 = datetime.datetime.strptime(Uploaded_time, '%m/%d/%y %H:%M:%S')
                #args = Podcast_pargs.parse_args()
                audio = Podcast(ID=audioFileID,Name=args['Name'],Duration=args['Duration'],Uploaded_time=Uploaded_time1,Host= args['Host'],Participants=args['Participants'])
            elif audioFileType == 'Audiobook':
                args = request.get_json()
                Uploaded_time = args['Uploaded_time']
                print(Uploaded_time)
                Uploaded_time1 = datetime.datetime.strptime(Uploaded_time, '%m/%d/%y %H:%M:%S')
                #args = Audiobook_pargs.parse_args()
                audio = Audiobook(ID=audioFileID,Title=args['Title'],Author=args['Author'],Narrator=args['Narrator'],Duration=args['Duration'],Uploaded_time=Uploaded_time1)
            db.session.add(audio)
            db.session.commit()
            return "Added Successfully",200
    
    def delete(self,audioFileType,audioFileID): #For Delete Endpoint
        if audioFileType == 'Song':
            result = Song.query.filter_by(ID=audioFileID).first()
            #res = MyEncoder().encode(result)
        elif audioFileType == 'Podcast':
            result = Podcast.query.filter_by(ID=audioFileID).first()
        elif audioFileType == 'Audiobook':
            result = Audiobook.query.filter_by(ID=audioFileID).first()
        else:
            pass
        if not result:
            return "Audio file not found to delete",400
        else:
            if audioFileType == 'Song':
                Song.query.filter_by(ID=audioFileID).delete()
                #res = MyEncoder().encode(result)
            elif audioFileType == 'Podcast':
                Podcast.query.filter_by(ID=audioFileID).delete()
            elif audioFileType == 'Audiobook':
                Audiobook.query.filter_by(ID=audioFileID).delete()
            else:
                pass
            db.session.commit()
            return "Deleted Successfully",200  
    

    def put(self,audioFileType,audioFileID):    #For Update end point
        
        
        if audioFileType == 'Song':
            result = Song.query.filter_by(ID=audioFileID).first()
            #res = MyEncoder().encode(result)
        elif audioFileType == 'Podcast':
            result = Podcast.query.filter_by(ID=audioFileID).first()
        elif audioFileType == 'Audiobook':
            result = Audiobook.query.filter_by(ID=audioFileID).first()
        else:
            pass
        if not result:
            return "Audio ID Not found to update",400
        else:
            if audioFileType == 'Song':
                result = Song.query.filter_by(ID=audioFileID).first()
                args = request.get_json()
               
                try:
                    Uploaded_time = args['Uploaded_time']
                    Uploaded_time1 = datetime.datetime.strptime(Uploaded_time, '%m/%d/%y %H:%M:%S')
                    print(Uploaded_time1)
                except Exception as e:
                    print(e)
                    pass
                
                for k,v in args.items():
                    if k=='Song_Name':
                        result.Song_Name = v
                    elif k=='Duration':
                        result.Duration = v
                    elif k=='Uploaded_time':
                        result.Uploaded_time = Uploaded_time1
                    else:
                        pass
                        
            #res = MyEncoder().encode(result)
            elif audioFileType == 'Podcast':
                result = Podcast.query.filter_by(ID=audioFileID).first()
                args = request.get_json()
                try:
                    Uploaded_time = args['Uploaded_time']
                    Uploaded_time1 = datetime.datetime.strptime(Uploaded_time, '%m/%d/%y %H:%M:%S')
                    print(Uploaded_time1)
                except Exception as e:
                    print(e)
                    pass
                
                for k,v in args.items():
                    if k=='Name':
                        result.Name = v
                    elif k=='Duration':
                        result.Duration = v
                    elif k=='Uploaded_time':
                        result.Uploaded_time = Uploaded_time1
                    elif k=='Host':
                        result.Host = v
                    elif k=='Participants':
                        result.Participants = v
                    else:
                        pass
                      
            elif audioFileType == 'Audiobook':
                result = Audiobook.query.filter_by(ID=audioFileID).first()
                args = request.get_json()
                try:
                    Uploaded_time = args['Uploaded_time']
                    Uploaded_time1 = datetime.datetime.strptime(Uploaded_time, '%m/%d/%y %H:%M:%S')
                    print(Uploaded_time1)
                except Exception as e:
                    print(e)
                    pass
                
                for k,v in args.items():
                    if k=='Title':
                        result.Title = v
                    elif k=='Author':
                        result.Author = v
                        
                    elif k=='Narrator':
                        result.Narrator = v    
                    elif k=='Duration':
                        result.Duration = v
                    elif k=='Uploaded_time':
                        result.Uploaded_time = Uploaded_time1
                    else:
                        pass
               
            db.session.commit()
            return "Updated Successfully Successfully",200
            
                
            
        
    

api.add_resource(Audio,"/<audioFileType>/<audioFileID>")    


if __name__ == "__main__":
    app.run(debug=True)
