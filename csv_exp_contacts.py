import os
import csv
import sqlite3 as s

d=r"C:\Users\Koytcha\Downloads"

def HeadersCSV():

    headers=None
    with open(os.path.join(d,"google-contacts.csv")) as rf:
        #csvreader=csv.DictReader(rf)
        csvreader=csv.reader(rf)
        #headers=list(csvreader)[0]
        return list(csvreader)[0]





#ADD ERROR HANDLING FOR MISSING HEADERS
"""
for i in range (10):
    print(m[i])
"""    



class PersonBase:
    noms=("noms",None,"TEXT")
    prenoms=("prenoms",None,"TEXT")
    prefix=("prefix",None,"TEXT")
    suffix=("suffix",None,"TEXT")
    surnom=("surnom",None,"TEXT")

    def __repr__(self):
        return "PersonBase"

    def __str__(self):
        return "PersonBase"

    def __init__(self,**kwargs):
        self.noms[1]=kwargs.get('noms',None)
        self.prenoms[1]=kwargs.get('prenoms',None)
        self.prefix[1]=kwargs.get('prenoms',None)
        self.suffix[1]=kwargs.get('prenoms',None)
        self.surnom[1]=kwargs.get('prenoms',None)

class PhoneNumbers:
    type=("type",None,"TEXT")
    number=("number",None,"TEXT")
    person_id=("person_id",None,"INTERGER")
   
    def __repr__(self):
        return "PhoneNumbers"
    
    def __str__(self):
        return "PhoneNumbers"
    
    def __init__(self,**kwargs):
        self.type[1]=kwargs.get('type',None)
        self.number[1]=kwargs.get('number',None)
        self.person_id[1]=kwargs.get('person_id',None)

class Emails:
    type=("type",None,"TEXT")
    mail=("mail",None,"TEXT")
    person_id=("person_id",None,"INTERGER")
   
    def __repr__(self):
        return "Emails"

    def __str__(self):
        return "Emails"

    def __init__(self,**kwargs):
        self.type=kwargs.get('type',None)
        self.mail=kwargs.get('number',None)
        self.person_id=kwargs.get('person_id',None)

tables={1:PersonBase,
    2:PhoneNumbers,
    3:Emails}


class MyHand:
    file_name='mycontacts.db'
    def __init__(self,model):
        
        self.model=model
        #remove this part when done testing
        try :
            os.remove(os.path.join(self.file_name))
            print("removed")
        except:
            print('error')
        
        exist = os.path.exists(self.file_name)
        
        if not exist:
            new_table=self.creation
        else :
            new_table=self.nothing
        self.conn=s.connect(self.file_name)
        self.cursor=self.conn.cursor()
        new_table(self.model)
        

    def nothing(self,*args):
        pass
    
    def execute(self,query,*args):
        
##        if data:
##            self.cursor.execute(query,data)
##        else:
        self.cursor.execute(query)
        """the database commit, not the cursor"""
        self.conn.commit()
        print('query finished')

    def getheaders(self,table):
        headers=[]
        for attr in dir(table):
            if not attr.startswith("__"):
                headers.append(attr)
        return headers
                
    def creation (self, tables):
        for key in tables:
            self.create(tables[key])
        
    def create(self,table):
        y=[]
        print(self.getheaders(table))
        for column in self.getheaders(table):
            x=column+" "+eval(f"table.{column}[2]")
            y.append(x)
        phrase=', '.join(y)
        query=f"""CREATE TABLE {table.__name__} (
                {phrase}
                )"""
        print (query)
        return self.execute(query)
        

    def add(self,table,data):
        """Utilser les ? pour insert ne fonctionne qu'avec UN SEUL AJOUT.
        Pour plusieurs ajout, il faudra  soit:
        - lancer la requete plusieurs fois en utilisant les ?,
        - ou lancer la requete une seule fois en utilisant l'écriture classique
        "INSERT INTO table VALUES (x1,y1),(x2,y2),..."
        """
        
        query=f"""
            INSERT INTO {table} VALUES
            (
            ?,
            ?,
            ?,
            ?)
            """
        return self.execute(query,data)

    def getall(self):
        query="""SELECT * from person """
        self.execute(query)
        return self.cursor.fetchall()

    def getone(self,name):
        query="""SELECT * FROM person WHERE prenoms = ? """
        n=[name]
        #works with either list or tuple
        #n=(name,)
        self.execute(query,n)
        return self.cursor.fetchall()

    def getnum(self,num):
        query="""SELECT * FROM person WHERE ROWID=? """
        n=[num]
        #works with either list or tuple
        #n=(name,)
        self.execute(query,n)
        return self.cursor.fetchall()

def extraction(csv):
    pass

def extractdata(mydict):
    """to execute for each row of csv"""
    #for now, just testing for names
    mydata={}
    for key in mydict:
        #todo:to refactor
        if key=="Given Name":
            mydata["prenoms"]=mydict[key]
        elif key=="Family Name":
            mydata["noms"]=mydict[key]
        elif key=='Name Prefix':
            mydata["prefix"]=mydict[key]
        elif key=='Name Suffix':
            mydata["suffix"]=mydict[key]
        elif key=='Nickname':
            mydata["surnom"]=mydict[key]
    return mydata

#PersonBase(**mydata)


m=None
with open(os.path.join(d,"google-contacts.csv"),"r") as rf:
    csvreader=csv.DictReader(rf)
    m=list(csvreader)

listofcontacts=[]

for row in m:
    mydata=extractdata(row)
    person=PersonBase(**mydata)
    listofcontacts.append(person)
    

print(HeadersCSV())
#x=MyHand(tables)
#for i in listofcontacts:
#   x.add(i)
